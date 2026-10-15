"""Internal, opt-in stdio front-end. Metadata is cached; only calls launch children."""
import argparse
import ctypes
from ctypes import wintypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import queue
import signal
import subprocess
import sys
import threading
import time
import uuid

PROTOCOL = '2024-11-05'
CONTROL = '_harness_'
LEASE = '_harness_session'
MAX_LINE = 8_000_000
ENVIRONMENT = {'PATH', 'SYSTEMROOT', 'WINDIR', 'COMSPEC', 'PATHEXT', 'USERPROFILE', 'HOME', 'HOMEDRIVE', 'HOMEPATH',
    'APPDATA', 'LOCALAPPDATA', 'TEMP', 'TMP', 'PROGRAMFILES', 'PROGRAMFILES(X86)', 'PROGRAMDATA', 'LANG', 'LC_ALL',
    'NODE_EXTRA_CA_CERTS', 'HTTPS_PROXY', 'HTTP_PROXY', 'ALL_PROXY', 'NO_PROXY'}
PROVIDER_ENV = {'playwright': (), 'chrome-devtools': (),
    'n8n': ('N8N_API_URL', 'N8N_API_KEY'),
    'claude-code': ('ANTHROPIC_API_KEY', 'CLAUDE_CODE_OAUTH_TOKEN')}


class MetadataDrift(ValueError):
    pass


def effective_env(definition):
    names = definition.get('env_vars', [])
    inherited = definition.get('inherited_env', [])
    if not isinstance(names, list) or not all(isinstance(name, str) for name in names) or not isinstance(inherited, list) or not all(name in {item for values in PROVIDER_ENV.values() for item in values} for name in inherited):
        raise ValueError('invalid explicit environment contract')
    return dict({key: value for key, value in os.environ.items() if key.upper() in ENVIRONMENT or key in names or key in inherited}, **definition.get('env', {}))


def read_manifest(path, expected=None):
    path = Path(path)
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents) or path.stat().st_size > MAX_LINE:
        raise ValueError('unsafe lifecycle cache')
    helper = Path(__file__).resolve().parents[5] / 'plugins/dev-workflow-standard/scripts/tool-state.py'
    spec = importlib.util.spec_from_file_location('lifecycle_private_state', helper)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    if not module.private_state_permissions(path):
        raise ValueError('lifecycle cache requires private owner permissions')
    raw = path.read_bytes(); digest = hashlib.sha256(raw).hexdigest()
    if expected is not None and digest != expected:
        raise ValueError('lifecycle metadata cache differs from approved transport')
    data = json.loads(raw)
    data['_cache_path'] = str(path.resolve()); data['_cache_digest'] = digest
    return data


def operational(definition):
    return hashlib.sha256(json.dumps({key: value for key, value in definition.items() if key not in ('command', 'args')}, sort_keys=True).encode()).hexdigest()


def binding(definition):
    """Bind executable, arguments, their files, environment and this implementation."""
    paths = [Path(__file__), Path(definition['command'])]
    paths += [Path(arg) for arg in definition['args'] if Path(arg).is_file()]
    files = []
    for path in paths:
        with path.open('rb') as stream:
            files.append((str(path.resolve()), hashlib.file_digest(stream, 'sha256').hexdigest()))
    return hashlib.sha256(json.dumps([definition, files, effective_env(definition)], sort_keys=True).encode()).hexdigest()


class OwnedChild:
    """No caller-supplied PID. Kill only the process group/job created here."""
    def __init__(self, definition):
        self.job = None
        self.process = None
        self.messages = queue.Queue()
        self.serial = 0
        self.changed = False
        if os.name == 'nt':
            self._job()
        try:
            self.process = subprocess.Popen([definition['command'], *definition['args']],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                env=effective_env(definition),
                creationflags=(0x4 | 0x08000000) if os.name == 'nt' else 0, start_new_session=os.name != 'nt')
            if os.name == 'nt':
                if not self.kernel.AssignProcessToJobObject(self.job, int(self.process._handle)):
                    raise ValueError('owned process containment failed')
                # Popen closes the initial thread handle; resume via NtResumeProcess.
                resume = ctypes.WinDLL('ntdll').NtResumeProcess
                resume.argtypes = [wintypes.HANDLE]; resume.restype = ctypes.c_long
                if resume(int(self.process._handle)) != 0:
                    raise ValueError('owned process resume failed')
            threading.Thread(target=self._read, daemon=True).start()
        except BaseException:
            self.close()
            raise

    def _job(self):
        class Basic(ctypes.Structure):
            _fields_ = [('PerProcessUserTimeLimit', ctypes.c_int64), ('PerJobUserTimeLimit', ctypes.c_int64),
                ('LimitFlags', wintypes.DWORD), ('MinimumWorkingSetSize', ctypes.c_size_t),
                ('MaximumWorkingSetSize', ctypes.c_size_t), ('ActiveProcessLimit', wintypes.DWORD),
                ('Affinity', ctypes.c_size_t), ('PriorityClass', wintypes.DWORD), ('SchedulingClass', wintypes.DWORD)]
        class IO(ctypes.Structure):
            _fields_ = [(name, ctypes.c_uint64) for name in ('ReadOperationCount', 'WriteOperationCount', 'OtherOperationCount', 'ReadTransferCount', 'WriteTransferCount', 'OtherTransferCount')]
        class Extended(ctypes.Structure):
            _fields_ = [('BasicLimitInformation', Basic), ('IoInfo', IO), ('ProcessMemoryLimit', ctypes.c_size_t),
                ('JobMemoryLimit', ctypes.c_size_t), ('PeakProcessMemoryUsed', ctypes.c_size_t), ('PeakJobMemoryUsed', ctypes.c_size_t)]
        self.kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        self.kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        self.kernel.CreateJobObjectW.restype = wintypes.HANDLE
        self.kernel.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        self.kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        self.kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        self.job = self.kernel.CreateJobObjectW(None, None)
        limits = Extended(); limits.BasicLimitInformation.LimitFlags = 0x2000
        if not self.job or not self.kernel.SetInformationJobObject(self.job, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            self.close()
            raise ValueError('owned job setup failed')

    def _read(self):
        try:
            for line in iter(lambda: self.process.stdout.readline(MAX_LINE + 1), b''):
                if len(line) > MAX_LINE:
                    raise ValueError('oversized upstream message')
                self.messages.put(json.loads(line))
        except (ValueError, OSError):
            pass
        finally:
            self.messages.put(None)

    def send(self, message):
        self.process.stdin.write((json.dumps(message) + '\n').encode()); self.process.stdin.flush()

    def notification(self, item):
        if 'id' in item or item.get('method') not in ('notifications/tools/list_changed', 'notifications/message', 'notifications/progress'):
            raise ValueError('unsupported upstream protocol request/notification')
        if item['method'] == 'notifications/tools/list_changed': self.changed = True

    def pending(self):
        for _ in range(1000):
            try: item = self.messages.get_nowait()
            except queue.Empty: return
            if item is None or 'method' not in item:
                raise ValueError('upstream disconnected or unexpected response')
            self.notification(item)
        raise ValueError('upstream notification flood')

    def request(self, method, params=None, timeout=60):
        self.serial += 1
        self.send({'jsonrpc': '2.0', 'id': self.serial, 'method': method, 'params': params or {}})
        until = time.monotonic() + timeout
        while True:
            try: item = self.messages.get(timeout=min(.2, max(0.001, until - time.monotonic())))
            except queue.Empty:
                if self.process.poll() is not None or time.monotonic() >= until:
                    raise ValueError('upstream disconnected or timed out') from None
                continue
            if item is None:
                raise ValueError('upstream disconnected')
            if 'method' in item:
                # Never consume server-origin approval/sampling as a successful call.
                self.notification(item)
                continue
            if item.get('id') != self.serial or 'error' in item or 'result' not in item:
                raise ValueError('upstream request failed')
            return item['result']

    def metadata(self):
        result = self.request('initialize', {'protocolVersion': PROTOCOL, 'capabilities': {}, 'clientInfo': {'name': 'harness-lifecycle', 'version': '1'}})
        if result.get('protocolVersion') != PROTOCOL or set(result.get('capabilities', {})) - {'tools', 'logging', 'resources', 'prompts'}:
            raise ValueError('unsupported upstream capabilities')
        # A declared listChanged capability is compatible with a bound snapshot.
        # Notifications trigger exact inventory recheck; actual drift needs re-prime.
        self.send({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
        return self.inventory()

    def inventory(self):
        self.changed = False
        tools = []; cursor = None
        while True:
            result = self.request('tools/list', {'cursor': cursor} if cursor else {})
            tools.extend(result['tools']); cursor = result.get('nextCursor')
            if not cursor:
                break
            if len(tools) > 1000:
                raise ValueError('tool inventory limit exceeded')
        for tool in tools:
            if tool['name'].startswith(CONTROL) or LEASE in tool['inputSchema'].get('properties', {}) or tool['inputSchema'].get('type') != 'object':
                raise ValueError('tool schema collision')
        if len({t['name'] for t in tools}) != len(tools):
            raise ValueError('duplicate tool identity')
        if self.changed:
            raise MetadataDrift('inventory changed while being checked; explicit re-prime required')
        return tools

    def close(self):
        if self.process and self.process.stdin and not self.process.stdin.closed:
            try: self.process.stdin.close()
            except OSError: pass
            try: self.process.wait(timeout=.3)
            except subprocess.TimeoutExpired: pass
        if self.job:
            self.kernel.CloseHandle(self.job); self.job = None
        if self.process:
            if os.name != 'nt':
                try: os.killpg(self.process.pid, signal.SIGKILL)
                except ProcessLookupError: pass
            elif self.process.poll() is None:
                self.process.kill()
            try: self.process.wait(timeout=5)
            except subprocess.TimeoutExpired: pass
            for stream in (self.process.stdin, self.process.stdout):
                if stream: stream.close()


def prime(definition, target, atomic, owner):
    before = binding(definition)
    child = OwnedChild(definition)
    try: tools = child.metadata()
    finally: child.close()
    if before != binding(definition):
        raise ValueError('runtime changed during metadata prime')
    manifest = {'version': 1, 'definition': definition, 'binding': before, 'tools': tools, 'owner': owner}
    atomic(target, json.dumps(manifest))
    return {'result': 'PRIMED_STOPPED', 'tools': len(tools)}


class Lifecycle:
    def __init__(self, manifest, idle=60):
        if not 1 <= idle <= 3600:
            raise ValueError('idle timeout outside approved bounds')
        self.manifest = manifest
        self.child = None; self.leases = {}; self.active = 0
        self.closed = False
        self.invalidated = False
        self.idle = idle; self.last = time.monotonic()
        self.lock = threading.RLock(); self.calls = threading.Lock()
        self.validate()

    def validate(self):
        if self.invalidated:
            raise ValueError('upstream metadata invalidated; explicit re-prime required')
        if self.manifest.get('version') != 1 or self.manifest['binding'] != binding(self.manifest['definition']):
            raise ValueError('metadata/runtime/environment drift; re-prime required')
        owner = self.manifest.get('owner')
        if owner:
            spec = importlib.util.spec_from_file_location('lifecycle_native_owner', Path(__file__).with_name('native_mcp.py'))
            module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
            manager = module.NativeMCP(owner['config'], owner['prefix'], None, owner['plugin_configs'], owner['host'])
            selected = manager.definition(owner['provider'], owner['conditional'])
            selected['inherited_env'] = list(PROVIDER_ENV[owner['provider']])
            extras = owner.get('extra_args', [])
            if any(flag not in ('--headless', '--isolated', '--no-usage-statistics', '--no-performance-crux') for flag in extras):
                raise ValueError('unreviewed native options')
            selected['args'] += extras
            selected.update({'env': self.manifest['definition']['env']} if 'env' in self.manifest['definition'] else {})
            selected.update({'env_vars': self.manifest['definition']['env_vars']} if 'env_vars' in self.manifest['definition'] else {})
            if selected != self.manifest['definition'] or owner['source'] != hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest():
                raise ValueError('approved native owner changed')
            _, table = manager.read()
            current = table.get(owner['name'], {})
            if operational(current) not in owner['operational']:
                raise ValueError('operational config drift requires explicit re-prime')
            if any(item['identity'] == owner['provider'] and item['enabled'] for item in manager.plugin_tables()):
                raise ValueError('redundant plugin transport detected')
            duplicates = [name for name, value in table.items() if name != owner['name'] and isinstance(value, dict) and module.identity(name, value) == owner['provider'] and value.get('enabled', True)]
            if duplicates:
                raise ValueError('redundant global transport detected')
            if current:
                transport = {key: current[key] for key in ('command', 'args') if key in current}
                approved = {key: selected[key] for key in ('command', 'args')}
                front_end = {'command': str(Path(sys.executable).resolve()), 'args': [str(Path(__file__).resolve()), '--manifest', self.manifest.get('_cache_path'), '--manifest-sha256', self.manifest.get('_cache_digest'), '--idle-seconds', str(self.idle)]}
                if transport not in (approved, owner.get('prior_transport'), front_end):
                    raise ValueError('unapproved transport change')

    def metadata(self):
        self.validate()
        tools = json.loads(json.dumps(self.manifest['tools']))
        for name in ('begin_session', 'finish_session', 'status'):
            tools.append({'name': CONTROL + name, 'description': {'begin_session': 'Begin a shared workflow; does not start the upstream. Expired leases require a fresh workflow.', 'finish_session': 'Release your lease after the workflow. Last release stops owned processes after active calls finish.', 'status': 'Inspect lifecycle state without starting upstream.'}[name],
                'inputSchema': {'type': 'object', 'properties': {'session': {'type': 'string', 'description': 'Explicit lease; omit for the default workflow.'}} if name == 'finish_session' else {}, 'additionalProperties': False},
                'annotations': {'readOnlyHint': name == 'status', 'destructiveHint': name == 'finish_session', 'idempotentHint': name != 'begin_session', 'openWorldHint': False}})
        return tools

    def status(self):
        return {'state': 'RUNNING' if self.child else 'STOPPED', 'owned_pid': self.child.process.pid if self.child else None,
            'active_calls': self.active, 'sessions': len(self.leases), 'idle_seconds': self.idle}

    def stop(self):
        if self.child:
            self.child.close(); self.child = None

    def reap(self):
        with self.lock:
            if self.active:
                return
            now = time.monotonic()
            self.leases = {key: stamp for key, stamp in self.leases.items() if now - stamp < self.idle}
            if not self.leases and now - self.last >= self.idle:
                self.stop()

    def call(self, name, arguments, meta=None):
        arguments = dict(arguments)
        with self.lock:
            if self.closed: raise ValueError('client lifecycle closed')
            self.validate(); self.reap()
            if name == CONTROL + 'begin_session':
                token = uuid.uuid4().hex; self.leases[token] = time.monotonic()
                return self.text({'session': token, **self.status()})
            if name == CONTROL + 'finish_session':
                token = arguments.get('session', 'default')
                if token not in self.leases:
                    raise ValueError('unknown or expired workflow')
                del self.leases[token]
                if not self.leases and not self.active: self.stop()
                return self.text(self.status())
            if name == CONTROL + 'status': return self.text(self.status())
            if name not in {tool['name'] for tool in self.manifest['tools']}:
                raise ValueError('unknown upstream tool')
            token = (meta or {}).get('harness_session', 'default')
            if token != 'default' and token not in self.leases:
                raise ValueError('unknown or expired workflow')
            self.leases[token] = time.monotonic()
            self.active += 1
        try:
            with self.calls:
                with self.lock:
                    if self.closed: raise ValueError('client lifecycle closed; queued call not executed')
                    self.validate()
                    if not self.child:
                        child = OwnedChild(self.manifest['definition'])
                        try:
                            if child.metadata() != self.manifest['tools']:
                                self.invalidated = True
                                raise MetadataDrift('upstream tool metadata changed; re-prime required')
                        except BaseException:
                            child.close(); raise
                        self.child = child
                    child = self.child
                try:
                    child.pending()
                    if child.changed and child.inventory() != self.manifest['tools']:
                        raise MetadataDrift('upstream inventory changed; explicit re-prime required')
                    result = child.request('tools/call', {'name': name, 'arguments': arguments})
                    if child.changed and child.inventory() != self.manifest['tools']:
                        raise MetadataDrift('upstream inventory changed; explicit re-prime required')
                    return result
                except (ValueError, OSError, queue.Empty):
                    with self.lock:
                        if sys.exc_info()[0] is MetadataDrift: self.invalidated = True
                        self.stop()
                    raise
        except (ValueError, OSError, queue.Empty):
            if sys.exc_info()[0] is MetadataDrift:
                with self.lock: self.invalidated = True
            raise ValueError('upstream call failed; no automatic replay') from None
        finally:
            with self.lock:
                self.active -= 1; self.last = time.monotonic()
                if token in self.leases: self.leases[token] = self.last
                if not self.active and (self.closed or token and not self.leases): self.stop()

    @staticmethod
    def text(value):
        return {'content': [{'type': 'text', 'text': json.dumps(value)}]}


def serve(manifest, idle=60):
    lifecycle = Lifecycle(manifest, idle)
    output_lock = threading.Lock()
    stopped = threading.Event()
    def emit(value):
        with output_lock:
            sys.stdout.write(json.dumps(value) + '\n'); sys.stdout.flush()
    def dispatch(message):
        if 'id' not in message:
            if message.get('method') != 'notifications/initialized':
                stopped.set()
                with lifecycle.lock:
                    lifecycle.closed = True
                    if not lifecycle.active: lifecycle.stop()
            return
        try:
            method = message['method']
            if method == 'initialize':
                lifecycle.validate()
                if not isinstance(message.get('params', {}).get('protocolVersion'), str):
                    raise ValueError('unsupported protocol')
                result = {'protocolVersion': PROTOCOL, 'capabilities': {'tools': {}}, 'serverInfo': {'name': 'harness-lifecycle', 'version': '1'}}
            elif method == 'tools/list': result = {'tools': lifecycle.metadata()}
            elif method == 'tools/call':
                params = message['params']; result = lifecycle.call(params['name'], params.get('arguments', {}), params.get('_meta'))
            elif method == 'ping': result = {}
            else: raise ValueError('unsupported method')
            emit({'jsonrpc': '2.0', 'id': message['id'], 'result': result})
        except (ValueError, OSError, KeyError, TypeError, queue.Empty):
            emit({'jsonrpc': '2.0', 'id': message['id'], 'error': {'code': -32000, 'message': 'Lifecycle request failed; inspect sanitized state and re-prime if required. No call replayed.'}})
    def timer():
        while not stopped.wait(0.25): lifecycle.reap()
    threading.Thread(target=timer, daemon=True).start()
    workers = []; admission = threading.BoundedSemaphore(16)
    try:
        for line in sys.stdin.buffer:
            if stopped.is_set() or len(line) > MAX_LINE: break
            message = json.loads(line)
            if message.get('method') == 'tools/call':
                workers = [worker for worker in workers if worker.is_alive()]
                if not admission.acquire(blocking=False):
                    emit({'jsonrpc': '2.0', 'id': message.get('id'), 'error': {'code': -32000, 'message': 'Lifecycle busy; request not executed.'}})
                    continue
                def execute(message=message):
                    try: dispatch(message)
                    finally: admission.release()
                worker = threading.Thread(target=execute, daemon=True); worker.start(); workers.append(worker)
            else: dispatch(message)
    finally:
        stopped.set()
        with lifecycle.lock: lifecycle.closed = True
        until = time.monotonic() + 65
        for worker in workers: worker.join(timeout=max(0, until - time.monotonic()))
        with lifecycle.lock: lifecycle.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True); parser.add_argument('--manifest-sha256', required=True); parser.add_argument('--idle-seconds', type=int, default=60)
    args = parser.parse_args()
    try:
        manifest = read_manifest(args.manifest, args.manifest_sha256)
        if not manifest.get('owner'): raise ValueError('approved native owner required')
        serve(manifest, args.idle_seconds)
    except (ValueError, OSError, KeyError, TypeError): raise SystemExit(2)
