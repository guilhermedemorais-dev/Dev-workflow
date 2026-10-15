"""Native MCP configuration owner. Plans are sanitized; configuration stays private."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import subprocess
import tomllib

PROVIDERS = {
    'playwright': {'package': '@playwright/mcp', 'bin_key': 'playwright-mcp', 'version': '0.0.83', 'bin': 'cli.js', 'node': (18, 0, 0), 'source': 'https://github.com/microsoft/playwright-mcp', 'windows10': 'CONDITIONAL_NOT_OFFICIALLY_SUPPORTED'},
    'chrome-devtools': {'package': 'chrome-devtools-mcp', 'bin_key': 'chrome-devtools-mcp', 'version': '1.10.1', 'bin': 'build/src/bin/chrome-devtools-mcp.js', 'node': (20, 19, 0), 'source': 'https://github.com/ChromeDevTools/chrome-devtools-mcp', 'windows10': 'CANDIDATE_REQUIRES_RUNTIME_PROOF'},
    'n8n': {'package': 'n8n-mcp', 'bin_key': 'n8n-mcp', 'version': '2.93.0', 'bin': 'dist/mcp/stdio-wrapper.js', 'node': (20, 0, 0), 'source': 'https://github.com/czlonkowski/n8n-mcp', 'windows10': 'THIRD_PARTY_REQUIRES_RUNTIME_PROOF'},
    'claude-code': {'package': '@anthropic-ai/claude-code', 'version': '2.1.300', 'source': 'https://code.claude.com/docs/en/setup', 'windows10': 'SUPPORTED_1809_OR_NEWER'},
}
ALIASES = {'n8n-mcp': 'n8n', 'claude': 'claude-code', 'claude_code': 'claude-code', 'chrome_devtools': 'chrome-devtools'}


def file_hash(path):
    if not path.exists(): return 'missing'
    with path.open('rb') as stream: return hashlib.file_digest(stream, 'sha256').hexdigest()


def runtime():
    if os.name == 'nt':
        return 'WINDOWS_NATIVE'
    return 'WSL' if 'microsoft' in platform.release().lower() or os.environ.get('WSL_DISTRO_NAME') else 'LINUX' if platform.system() == 'Linux' else platform.system().upper()


def stable(path):
    if not path:
        return None
    path = Path(path).resolve()
    parts = {part.lower() for part in path.parts}
    if not path.is_file() or parts & {'tmp', 'temp', 'codex-runtimes', 'node_modules', '.cache'} or '/home/' in str(path).replace('\\', '/'):
        return None
    return str(path)


def discover(node_override=None, claude_override=None, browser_override=None):
    if node_override and (not stable(node_override) or Path(node_override).name.lower() != 'node.exe'):
        raise ValueError('invalid explicit Node override; fallback forbidden')
    candidates = [node_override] if node_override else [shutil.which('node')]
    for directory in os.environ.get('PATH', '').split(os.pathsep):
        candidates.append(Path(directory) / ('node.exe' if os.name == 'nt' else 'node'))
    candidates.extend(Path(os.environ.get(base, '/nonexistent')) / 'nodejs/node.exe' for base in ('PROGRAMFILES', 'LOCALAPPDATA'))
    node = next((candidate for value in candidates if (candidate := stable(value))), None)
    if node_override and (not node or Path(node).name.lower() != 'node.exe'):
        raise ValueError('native Node override must be a stable external node.exe')
    npm = stable(str(Path(node).with_name('node_modules') / 'npm' / 'bin' / 'npm-cli.js')) if node else None
    # npm is expected inside Node's own installation, unlike transient MCP copies.
    if node:
        candidate = Path(node).parent / 'node_modules/npm/bin/npm-cli.js'
        npm = str(candidate) if candidate.is_file() else None
    version = None
    if node:
        try:
            output = subprocess.run([node, '--version'], capture_output=True, text=True, timeout=10, check=True).stdout.strip()
            version = output if re.fullmatch(r'v\d+\.\d+\.\d+', output) else None
        except (OSError, subprocess.SubprocessError):
            pass
    browsers = {}
    for name, suffix in [('chrome', 'Google/Chrome/Application/chrome.exe'), ('edge', 'Microsoft/Edge/Application/msedge.exe')]:
        for base in ('PROGRAMFILES', 'PROGRAMFILES(X86)', 'LOCALAPPDATA'):
            candidate = stable(Path(os.environ.get(base, '/nonexistent')) / suffix)
            if candidate:
                browsers[name] = candidate
                break
    if browser_override:
        browser = stable(browser_override)
        if not browser or Path(browser).name.lower() not in ('chrome.exe', 'msedge.exe'):
            raise ValueError('native browser override requires an installed Chrome or Edge executable')
        browsers['selected'] = browser
    claude = stable(claude_override) if claude_override else stable(shutil.which('claude.exe')) if os.name == 'nt' else stable(shutil.which('claude'))
    if claude_override and (not claude or Path(claude).name.lower() != 'claude.exe'):
        raise ValueError('native Claude override requires stable official claude.exe')
    return {'runtime': runtime(), 'node': node, 'npm_cli': npm, 'node_version': version, 'claude': claude, 'browsers': browsers}


def identity(name, definition):
    args = definition.get('args', [])
    if not isinstance(args, list) or not all(isinstance(x, str) for x in args):
        return None
    if args and Path(args[0]).resolve() == Path(__file__).with_name('mcp_lifecycle.py').resolve():
        # Recognize generated transports by their owner and manifest, not alias.
        # Never open a credential-bearing manifest merely to classify identity.
        command = str(definition.get('command', '')).replace('\\', '/').rsplit('/', 1)[-1].lower()
        if command not in ('python.exe', 'python3', 'python') or len(args) != 7 or args[1] != '--manifest' or args[3] != '--manifest-sha256' or not re.fullmatch(r'[0-9a-f]{64}', args[4]) or args[5] != '--idle-seconds' or not args[6].isdigit() or not 1 <= int(args[6]) <= 3600:
            raise ValueError('ambiguous lifecycle transport requires explicit reconciliation')
        provider = args[2].replace('\\', '/').rsplit('/', 1)[-1].removesuffix('.json')
        if provider not in PROVIDERS or not args[2].replace('\\', '/').endswith(provider + '.json'):
            raise ValueError('unrecognized lifecycle manifest requires explicit reconciliation')
        return provider
    text = ' '.join(arg for arg in args if '=' not in arg and not arg.startswith(('http:', 'https:')))
    for key, metadata in PROVIDERS.items():
        if metadata['package'] in text:
            return key
    for position, arg in enumerate(args):
        if '=' in arg:
            continue
        executable = arg.replace('\\', '/').rsplit('/', 1)[-1].lower()
        known = {'playwright-mcp': 'playwright', 'chrome-devtools-mcp': 'chrome-devtools', 'n8n-mcp': 'n8n'}
        if executable in known:
            return known[executable]
        if executable in ('claude', 'claude.exe') and args[position + 1:position + 3] == ['mcp', 'serve']:
            return 'claude-code'
    command = str(definition.get('command', '')).replace('\\', '/').rsplit('/', 1)[-1].lower()
    if command in ('claude', 'claude.exe') and args[:2] == ['mcp', 'serve']:
        return 'claude-code'
    return ALIASES.get(name, name if name in PROVIDERS else None)


def diagnose(table):
    result = []
    for name, definition in table.items():
        if not isinstance(definition, dict):
            continue
        command = str(definition.get('command', '')).replace('\\', '/').rsplit('/', 1)[-1].lower()
        result.append({'name': name, 'identity': identity(name, definition), 'enabled': definition.get('enabled', True) is not False, 'transport': 'WSL' if command in ('wsl', 'wsl.exe') else 'HTTP' if 'url' in definition else 'STDIO', 'credentials_present': bool(definition.get('env') or definition.get('http_headers') or definition.get('bearer_token_env_var'))})
    return result


class NativeMCP:
    def __init__(self, config, prefix, atomic, plugin_configs=(), discovered=None):
        self.config, self.prefix = Path(config).resolve(), Path(prefix).resolve()
        self.atomic = atomic
        self.plugin_configs = tuple(Path(p) for p in plugin_configs)
        self.host = discovered or discover()

    def read(self):
        raw = self.config.read_bytes().decode('utf-8') if self.config.exists() else ''
        return raw, tomllib.loads(raw).get('mcp_servers', {})

    def lifecycle_module(self):
        spec = importlib.util.spec_from_file_location('environment_mcp_lifecycle', Path(__file__).with_name('mcp_lifecycle.py'))
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        return module

    def lifecycle_prime(self, selected, cache_dir, expected, conditional=False):
        plan = self.prepare(selected, conditional)
        if plan['fingerprint'] != expected:
            raise ValueError('reviewed native fingerprint required before metadata priming')
        module = self.lifecycle_module(); results = []
        for key in selected:
            name = next(item['name'] for item in plan['changes'] if identity(item['name'], tomllib.loads(plan['content'])['mcp_servers'][item['name']]) == key)
            configured = tomllib.loads(plan['content'])['mcp_servers'][name]
            definition = {field: configured[field] for field in ('command', 'args', 'env', 'env_vars') if field in configured}
            definition['inherited_env'] = list(module.PROVIDER_ENV[key])
            base = self.definition(key, conditional)
            extras = definition['args'][len(base['args']):]
            if definition['command'] != base['command'] or definition['args'][:len(base['args'])] != base['args'] or any(flag not in ('--headless', '--isolated', '--no-usage-statistics', '--no-performance-crux') for flag in extras):
                raise ValueError('lifecycle requires reviewed native arguments')
            owner = {'provider': key, 'name': name, 'config': str(self.config), 'prefix': str(self.prefix),
                'plugin_configs': [str(p) for p in self.plugin_configs], 'host': self.host, 'conditional': conditional,
                'source': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
            owner['extra_args'] = extras
            _, original_table = self.read()
            owner['operational'] = [module.operational(original_table.get(name, {})), module.operational(configured)]
            owner['prior_transport'] = {field: original_table.get(name, {}).get(field) for field in ('command', 'args') if field in original_table.get(name, {})}
            target = Path(cache_dir).resolve() / (key + '.json')
            results.append({'component': key, 'manifest': str(target), **module.prime(definition, target, self.atomic, owner)})
        return {'operation': 'native-lifecycle-prime', 'receipts': results}

    def lifecycle_prepare(self, selected, cache_dir, python, conditional=False, idle=60):
        python = stable(python)
        if not python or Path(python).name.lower() not in ('python.exe', 'python3', 'python'):
            raise ValueError('stable external Python3.11+ interpreter required')
        try:
            version = subprocess.run([python, '-c', 'import sys; print(sys.version_info >= (3,11))'], capture_output=True, timeout=10, check=True)
            if version.stdout.strip() != b'True': raise ValueError('Python3.11+ required')
        except subprocess.SubprocessError:
            raise ValueError('Python runtime verification failed') from None
        plan = self.prepare(selected, conditional); module = self.lifecycle_module(); cache_hashes = []
        for key in selected:
            manifest_path = Path(cache_dir).resolve() / (key + '.json')
            manifest = module.read_manifest(manifest_path)
            cache_hashes.append(hashlib.sha256(manifest_path.read_bytes()).hexdigest())
            lifecycle = module.Lifecycle(manifest, idle)
            name = manifest['owner']['name']
            if manifest['owner']['provider'] != key or manifest['owner']['config'] != str(self.config):
                raise ValueError('unrelated lifecycle cache')
            transport = {'command': python, 'args': [str(Path(module.__file__).resolve()), '--manifest', str(manifest_path), '--manifest-sha256', manifest['_cache_digest'], '--idle-seconds', str(idle)]}
            # Read-only preview cannot mutate manifests. Apply binds this exact transport.
            plan['content'] = self.patch(plan['content'], name, transport)
        plan['operation'] = 'native-lifecycle-plan'
        plan['fingerprint'] = hashlib.sha256((plan['fingerprint'] + plan['content'] + json.dumps(cache_hashes) + module.binding({'command': python, 'args': []})).encode()).hexdigest()
        return plan

    def fingerprint(self):
        paths = [self.config, Path(__file__), *self.plugin_configs]
        paths.extend(Path(value) for key in ('node', 'npm_cli', 'claude') if (value := self.host.get(key)))
        paths.extend(Path(value) for value in self.host.get('browsers', {}).values())
        for metadata in PROVIDERS.values():
            package = self.prefix / 'node_modules' / metadata['package']
            paths.extend([package / 'package.json', package / metadata.get('bin', 'missing')])
        return hashlib.sha256(json.dumps([(str(p), file_hash(p)) for p in paths]).encode()).hexdigest()

    def plugin_tables(self):
        result = []
        for path in self.plugin_configs:
            data = json.loads(path.read_text(encoding='utf-8'))
            table = data.get('mcpServers', data.get('mcp_servers', {}))
            if not isinstance(table, dict):
                raise ValueError('invalid plugin definitions')
            result.extend(diagnose(table))
        return result

    def definition(self, key, conditional=False):
        if self.host['runtime'] != 'WINDOWS_NATIVE':
            raise ValueError('native migration requires Windows execution; use existing Linux/WSL preparation')
        metadata = PROVIDERS[key]
        if key == 'playwright' and not conditional:
            raise ValueError('Playwright Windows10 needs explicit conditional support consent')
        if key == 'claude-code':
            if not self.host.get('claude') or not self.host['claude'].lower().endswith('.exe'):
                raise ValueError('official native Claude executable required')
            return {'command': self.host['claude'], 'args': ['mcp', 'serve']}
        version = tuple(int(x) for x in (self.host.get('node_version') or 'v0.0.0')[1:].split('.'))
        if not self.host.get('node') or version < metadata['node'] or (key == 'chrome-devtools' and not (version[0] == 20 and version >= (20, 19, 0) or version[0] == 22 and version >= (22, 12, 0) or version[0] >= 23)):
            raise ValueError('compatible stable external Node required')
        package = self.prefix / 'node_modules' / metadata['package'] / 'package.json'
        data = json.loads(package.read_text())
        if data.get('version') != metadata['version'] or data.get('name') != metadata['package']:
            raise ValueError('installed package identity/version differs from reviewed source')
        binary = data.get('bin')
        target = binary if isinstance(binary, str) else binary.get(metadata['bin_key']) if isinstance(binary, dict) else None
        if not isinstance(target, str) or PurePosixPath(target).is_absolute() or '..' in PurePosixPath(target).parts or '\\' in target:
            raise ValueError('unsafe package entrypoint')
        target = str(PurePosixPath(target))
        if target != metadata['bin']:
            raise ValueError('package entrypoint differs from reviewed provider')
        script = (package.parent / target).resolve()
        if not script.is_relative_to(package.parent.resolve()) or not script.is_file() or script.suffix != '.js':
            raise ValueError('invalid package executable')
        definition = {'command': self.host['node'], 'args': [str(script)]}
        if key == 'playwright':
            browser = self.host.get('browsers', {}).get('selected') or self.host.get('browsers', {}).get('edge') or self.host.get('browsers', {}).get('chrome')
            if not browser:
                raise ValueError('compatible installed browser required')
            definition['args'] += ['--executable-path', browser]
        if key == 'chrome-devtools':
            browser = self.host.get('browsers', {}).get('selected') or self.host.get('browsers', {}).get('chrome')
            if browser and Path(browser).name.lower() == 'msedge.exe' and not conditional:
                raise ValueError('Chrome DevTools Edge candidate requires explicit conditional consent')
            if not browser:
                raise ValueError('Chrome required; Edge support not presumed')
            definition['args'] += ['--executablePath', browser, '--no-usage-statistics', '--no-performance-crux']
        return definition

    def install_plan(self, selected):
        self.validate_selection(selected)
        if self.host['runtime'] != 'WINDOWS_NATIVE':
            raise ValueError('native install requires Windows')
        plans = []
        for key in selected:
            metadata = PROVIDERS[key]
            if key == 'claude-code':
                plans.append({'component': key, 'action': 'MANUAL_OFFICIAL_INSTALLER', 'source': metadata['source'], 'version': metadata['version'], 'command': []})
            else:
                if not self.host.get('node') or not self.host.get('npm_cli'):
                    raise ValueError('matching stable Node/npm required')
                plans.append({'component': key, 'action': 'INSTALL', 'source': metadata['source'], 'version': metadata['version'], 'command': [self.host['node'], self.host['npm_cli'], 'install', '--prefix', str(self.prefix), '--no-audit', '--no-fund', metadata['package'] + '@' + metadata['version']]})
        return {'operation': 'native-install-plan', 'fingerprint': hashlib.sha256((self.fingerprint() + json.dumps(plans, sort_keys=True) + json.dumps(self.host, sort_keys=True)).encode()).hexdigest(), 'actions': plans, 'installation_performed': False}

    def install(self, selected, expected):
        plan = self.install_plan(selected)
        if plan['fingerprint'] != expected:
            raise ValueError('installation plan changed since approval')
        if any(item['action'] != 'INSTALL' for item in plan['actions']):
            raise ValueError('manual official installer must be completed separately')
        receipts = []
        for item in plan['actions']:
            try:
                result = subprocess.run(item['command'], capture_output=True, timeout=300, check=False)
                receipts.append({'component': item['component'], 'result': 'INSTALLED_NOT_VALIDATED' if result.returncode == 0 else 'FAILED', 'exit_code': result.returncode})
            except (OSError, subprocess.SubprocessError):
                receipts.append({'component': item['component'], 'result': 'FAILED'})
            if receipts[-1]['result'] == 'FAILED':
                break
        return {'operation': 'native-install', 'receipts': receipts}

    @staticmethod
    def validate_selection(selected):
        if not selected or len(set(selected)) != len(selected) or any(key not in PROVIDERS for key in selected):
            raise ValueError('explicit unique known provider selection required')

    def prepare(self, selected, conditional=False):
        self.validate_selection(selected)
        raw, table = self.read()
        global_defs, plugin_defs = diagnose(table), self.plugin_tables()
        changes = []
        for key in selected:
            matching = [item for item in global_defs if item['identity'] == key]
            if len(matching) > 1 or any(item['identity'] == key and item['enabled'] for item in plugin_defs):
                raise ValueError('redundant global/plugin integration requires explicit reconciliation')
            name = matching[0]['name'] if matching else key
            definition = self.definition(key, conditional)
            old = table.get(name, {})
            old_args = old.get('args', [])
            old_command = str(old.get('command', '')).lower()
            if old_command.endswith(('wsl.exe', '/wsl')) or old_command == 'wsl':
                # Inline shell/env is deliberately not rewritten: silent loss could alter authentication.
                if any(x in ('-c', '-lc', 'bash', 'sh') for x in old_args):
                    raise ValueError('WSL shell/env wrapper requires reviewed manual normalization')
            elif old and old_args != definition['args'] and identity(name, old) == key:
                raise ValueError('existing native options require reviewed manual reconciliation')
            if old_command.endswith('wsl.exe') or old_command == 'wsl':
                position = 0
                if old_args[:1] in (['-d'], ['--distribution']):
                    if len(old_args) < 3:
                        raise ValueError('invalid WSL distribution argument')
                    position = 2
                if old_args[position:position + 1] in (['--exec'], ['-e'], ['--']):
                    position += 1
                if old_args[position:position + 1] == ['env']:
                    position += 1
                    while position < len(old_args) and '=' in old_args[position]:
                        position += 1
                if position >= len(old_args):
                    raise ValueError('missing reviewed WSL executable')
                executable = old_args[position].replace('\\', '/').rsplit('/', 1)[-1]
                if executable not in ('npx', 'node', 'claude', 'n8n-mcp', 'playwright-mcp', 'chrome-devtools-mcp'):
                    raise ValueError('unreviewed WSL executable')
                tail = old_args[position + 1:]
                if executable == 'npx':
                    if tail[:1] == ['-y']:
                        tail = tail[1:]
                    if not tail or not re.fullmatch(re.escape(PROVIDERS[key]['package']) + r'(?:@(?:\d+\.\d+\.\d+|latest))?', tail[0]):
                        raise ValueError('unreviewed package or wrapper provider mismatch')
                    tail = tail[1:]
                elif executable == 'node':
                    if not tail or PROVIDERS[key]['package'] not in tail[0]:
                        raise ValueError('unreviewed Node wrapper')
                    tail = tail[1:]
                elif executable == 'claude':
                    if tail[:2] != ['mcp', 'serve']:
                        raise ValueError('unreviewed Claude wrapper')
                    tail = tail[2:]
                position = 0
                while position < len(tail):
                    flag = tail[position]
                    if flag in ('--headless', '--isolated', '--no-usage-statistics', '--no-performance-crux'):
                        if flag not in definition['args']:
                            definition['args'].append(flag)
                        position += 1
                    elif flag in ('--executable-path', '--executablePath') and key in ('playwright', 'chrome-devtools') and position + 1 < len(tail):
                        position += 2  # Native browser was explicitly selected by discovery.
                    else:
                        raise ValueError('unreviewed WSL argument requires manual reconciliation')
            inline_env = {}
            if 'env' in old_args:
                position = old_args.index('env') + 1
                while position < len(old_args) and '=' in old_args[position]:
                    env_key, value = old_args[position].split('=', 1)
                    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', env_key) or any(c in value for c in ('\n', '\r', '\x00')):
                        raise ValueError('unsupported inline environment')
                    inline_env[env_key] = value
                    position += 1
                if not inline_env or position >= len(old_args):
                    raise ValueError('ambiguous environment wrapper')
            elif any('=' in arg for arg in old_args):
                raise ValueError('ambiguous inline environment')
            definition['_inline_env'] = inline_env
            changes.append((name, definition, old))
        content = raw
        for name, definition, old in changes:
            inline_env = definition.pop('_inline_env')
            content = self.patch(content, name, definition)
            if inline_env:
                content = self.patch_env(content, name, inline_env)
            if identity(name, definition) == 'n8n':
                # Defaults do not overwrite the existing secret-bearing env table.
                parsed = tomllib.loads(content)['mcp_servers'][name]
                defaults = {'MCP_MODE': 'stdio', 'LOG_LEVEL': 'error', 'DISABLE_CONSOLE_OUTPUT': 'true'}
                missing = {k: v for k, v in defaults.items() if k not in parsed.get('env', {})}
                if missing:
                    if 'env' in parsed and not re.search(r'^\[mcp_servers\.' + re.escape(name) + r'\.env\]\s*$', content, re.M):
                        raise ValueError('inline env requires manual normalization')
                    extra = ''.join(k + ' = ' + json.dumps(v) + '\n' for k, v in missing.items())
                    if not re.search(r'^\[mcp_servers\.' + re.escape(name) + r'\.env\]\s*$', content, re.M):
                        content += '\n[mcp_servers.' + name + '.env]\n' + extra
                    else:
                        env_header = re.search(r'^\[mcp_servers\.' + re.escape(name) + r'\.env\]\s*$', content, re.M)
                        content = content[:env_header.end()] + '\n' + extra + content[env_header.end():]
        tomllib.loads(content)
        return {'operation': 'native-plan', 'fingerprint': hashlib.sha256((self.fingerprint() + content + json.dumps(self.host, sort_keys=True) + json.dumps(list(selected)) + str(conditional)).encode()).hexdigest(), 'selected': list(selected), 'definitions': global_defs, 'plugin_definitions': plugin_defs, 'changes': [{'name': name, 'action': 'MIGRATE' if old else 'ADD', 'credentials_preserved': True, 'runtime_validation': 'NOT_VALIDATED'} for name, _, old in changes], 'conditional_support': conditional, 'content': content}

    @staticmethod
    def patch_env(content, name, values):
        parsed = tomllib.loads(content)['mcp_servers'][name]
        header = re.search(r'^\[mcp_servers\.' + re.escape(name) + r'\.env\]\s*$', content, re.M)
        if not header:
            if 'env' in parsed:
                raise ValueError('inline environment table requires manual normalization')
            return content + '\n[mcp_servers.' + name + '.env]\n' + ''.join(k + ' = ' + json.dumps(v) + '\n' for k, v in values.items())
        next_header = re.search(r'^\[', content[header.end():], re.M)
        end = header.end() + next_header.start() if next_header else len(content)
        block = content[header.end():end]
        for key, value in values.items():
            assignment = re.compile(r'^' + re.escape(key) + r'\s*=.*$', re.M)
            if key in parsed.get('env', {}) and not assignment.search(block):
                raise ValueError('complex environment assignment requires manual normalization')
            line = key + ' = ' + json.dumps(value)
            if assignment.search(block):
                block = assignment.sub(lambda _: line, block, count=1)
            else:
                block += '\n' + line + '\n'
        return content[:header.end()] + block + content[end:]

    @staticmethod
    def patch(content, name, definition):
        if not re.fullmatch(r'[A-Za-z0-9_-]+', name):
            raise ValueError('complex TOML server names require manual normalization')
        header = re.compile(r'^\[mcp_servers\.' + re.escape(name) + r'\]\s*(?:#.*)?$', re.M)
        match = header.search(content)
        current = tomllib.loads(content).get('mcp_servers', {}).get(name, {})
        values = dict(definition, enabled=current.get('enabled', True))
        if not match:
            if name in tomllib.loads(content).get('mcp_servers', {}):
                raise ValueError('complex TOML layout requires manual normalization')
            return content + '\n[mcp_servers.' + name + ']\n' + ''.join(k + ' = ' + json.dumps(v) .lower() + '\n' if isinstance(v, bool) else k + ' = ' + json.dumps(v) + '\n' for k, v in values.items())
        end_match = re.search(r'^\[', content[match.end():], re.M)
        end = match.end() + end_match.start() if end_match else len(content)
        block = content[match.end():end]
        for key, value in values.items():
            assignment = re.compile(r'^' + key + r'\s*=.*$', re.M)
            line = key + ' = ' + (str(value).lower() if isinstance(value, bool) else json.dumps(value))
            if assignment.search(block):
                # Multiline values cannot be safely edited by a line replacement.
                original = assignment.search(block).group()
                if key == 'args' and not original.split('=', 1)[1].strip().endswith(']'):
                    raise ValueError('multiline arguments require manual normalization')
                block = assignment.sub(lambda _: line, block, count=1)
            else:
                block += '\n' + line + '\n'
        return content[:match.end()] + block + content[end:]

    def apply(self, selected, expected, backup_dir, conditional=False, lifecycle=None):
        plan = self.lifecycle_prepare(selected, **lifecycle, conditional=conditional) if lifecycle else self.prepare(selected, conditional)
        if plan['fingerprint'] != expected:
            raise ValueError('configuration or selected plan changed since approval')
        source_fingerprint = self.fingerprint()
        backup_dir = Path(backup_dir).resolve()
        if backup_dir == self.config.parent or self.config.is_relative_to(backup_dir):
            raise ValueError('separate private backup directory required')
        original = self.config.read_bytes().decode('utf-8') if self.config.exists() else ''
        backup = backup_dir / (expected + '.toml')
        receipt = backup_dir / (expected + '.json')
        if backup.exists() or receipt.exists():
            raise ValueError('backup already exists; no duplicate migration')
        self.atomic(backup, original.encode('utf-8'))
        record = {'config': str(self.config), 'backup': str(backup), 'before': hashlib.sha256(original.encode()).hexdigest(), 'after': hashlib.sha256(plan['content'].encode()).hexdigest(), 'existed': self.config.exists()}
        self.atomic(receipt, json.dumps(record))
        if self.fingerprint() != source_fingerprint:
            raise ValueError('configuration changed before commit')
        self.atomic(self.config, plan['content'])
        return {'operation': 'native-apply', 'result': 'CONFIGURED_NOT_VALIDATED', 'receipt': str(receipt), 'selected': list(selected)}

    def rollback(self, receipt):
        record = json.loads(Path(receipt).read_text())
        if record.get('config') != str(self.config) or hashlib.sha256(self.config.read_bytes()).hexdigest() != record.get('after'):
            raise ValueError('rollback refuses changed or unrelated configuration')
        backup = Path(record['backup']).read_bytes()
        if hashlib.sha256(backup).hexdigest() != record['before']:
            raise ValueError('backup integrity mismatch')
        if hashlib.sha256(self.config.read_bytes()).hexdigest() != record['after']:
            raise ValueError('configuration changed during backup verification')
        if not record['existed']:
            self.config.unlink()
        else:
            self.atomic(self.config, backup)
        return {'operation': 'native-rollback', 'result': 'RESTORED'}
