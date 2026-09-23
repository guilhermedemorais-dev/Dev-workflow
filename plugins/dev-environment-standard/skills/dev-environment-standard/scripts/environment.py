#!/usr/bin/env python3
"""Capability-driven bootstrap. Configuration is not evidence of availability."""

import argparse
import ast
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import tomllib
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[5]
TIERS = {'CORE', 'RECOMMENDED', 'OPTIONAL', 'PROJECT_SPECIFIC', 'COMMUNITY', 'RUNTIME_PROVIDED'}
ORIGINS = {'OFFICIAL', 'VERIFIED_THIRD_PARTY', 'COMMUNITY', 'UNKNOWN'}
POLICIES = {'AUTO_SAFE', 'PROJECT_SCOPED', 'USER_SCOPED', 'AUTH_REQUIRED', 'PRIVILEGED', 'MANUAL_ONLY', 'RUNTIME_PROVIDED'}
ID = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}$')
SECRET = re.compile(r'(?i)(?:(?:bearer|basic)\s+|gh[pousr]_[A-Za-z0-9]|github_pat_|sk-[A-Za-z0-9]|--[\w-]*(?:token|password|secret|cookie|api[_-]?key)(?:[=\s]|$)|(?:password|api[_-]?key|access[_-]?token|secret|cookie|authorization)\s*[:=])')


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def digest(path):
    try:
        path = Path(path)
        if path.is_dir():
            content = '\n'.join(sorted(p.name for p in path.iterdir() if p.name not in ('runtime-state', '__pycache__', '.git'))).encode()
        else:
            content = path.read_bytes()
        return hashlib.sha256(content).hexdigest()
    except OSError:
        return 'missing'


def safe(value):
    """Reject credential-bearing values, rather than trying to redact after use."""
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() in {'token', 'password', 'secret', 'api_key', 'apikey', 'cookie', 'authorization', 'env', 'headers'}:
                raise ValueError('credential-bearing fields are not accepted')
            safe(item)
    elif isinstance(value, list):
        for item in value:
            safe(item)
    elif isinstance(value, str):
        if SECRET.search(value):
            raise ValueError('credential-bearing values are not accepted')
        for url in re.findall(r'https?://[^\s\"<>]+', value):
            parsed = urlsplit(url)
            if parsed.username or parsed.password or parsed.query or '=' in parsed.fragment:
                raise ValueError('URLs must not contain credentials or query')
    return value


def read_json(path):
    path = Path(path)
    if path.stat().st_size > 2_000_000:
        raise ValueError('input exceeds size limit')
    return json.loads(path.read_text(encoding='utf-8'))


def atomic(path, text):
    path = Path(path)
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise ValueError('symlink write target rejected')
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(prefix='.environment-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def fresh(value, seconds=300):
    try:
        stamp = dt.datetime.fromisoformat(value)
        age = (dt.datetime.now(dt.timezone.utc) - stamp).total_seconds()
        return 0 <= age <= seconds
    except (ValueError, TypeError):
        return False


def library(path):
    data = safe(read_json(path))
    if data.get('schema_version') != 1 or not isinstance(data.get('mcps'), list):
        raise ValueError('invalid MCP library')
    result = {}
    for entry in data['mcps']:
        if not isinstance(entry, dict) or not ID.fullmatch(entry.get('id', '')):
            raise ValueError('invalid MCP identifier')
        if entry['id'] in result or entry.get('tier') not in TIERS or entry.get('origin') not in ORIGINS:
            raise ValueError('invalid MCP classification')
        required = ('provider', 'capabilities', 'provenance') if entry['tier'] == 'RUNTIME_PROVIDED' else ('provider', 'repository', 'documentation', 'capabilities', 'provenance')
        if not all(entry.get(k) for k in required):
            raise ValueError('MCP provenance and capabilities are required')
        if not isinstance(entry['capabilities'], list) or not all(isinstance(c, str) and c for c in entry['capabilities']):
            raise ValueError('invalid capabilities')
        if entry.get('preparation', {}).get('policy') not in POLICIES:
            raise ValueError('invalid preparation policy')
        if entry.get('configuration'):
            validate_configuration(entry['configuration'])
        result[entry['id']] = entry
    return result


def validate_configuration(config):
    safe(config)
    if config.get('transport') == 'http':
        if set(config) != {'transport', 'url'} or urlsplit(config['url']).scheme != 'https' or not urlsplit(config['url']).hostname or urlsplit(config['url']).fragment:
            raise ValueError('HTTP MCP requires a credential-free HTTPS URL')
    elif config.get('transport') == 'stdio':
        if set(config) != {'transport', 'command', 'args'} or not isinstance(config['args'], list):
            raise ValueError('invalid stdio MCP configuration')
        if config['command'] != 'npx' or len(config['args']) < 2 or config['args'][0] != '-y' or not re.fullmatch(r'(?:@[a-z0-9-]+/)?[a-z0-9-]+@\d+\.\d+\.\d+', config['args'][1]) or any(arg not in ('--no-usage-statistics', '--no-performance-crux') for arg in config['args'][2:]):
            raise ValueError('only pinned catalog npx packages are supported')
    else:
        raise ValueError('unsupported MCP transport')


def custom_entries(path, public):
    return validate_custom(safe(read_json(path)).get('custom_mcps', []), public)


def validate_custom(entries, public):
    safe(entries)
    result = []
    allowed = {'id', 'name', 'provider', 'repository', 'documentation', 'capabilities', 'maintainer', 'installation', 'transport', 'permissions', 'authentication', 'risks', 'origin'}
    if not isinstance(entries, list):
        raise ValueError('custom MCP list required')
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('custom MCP object required')
        if set(entry) != allowed or not ID.fullmatch(entry.get('id', '')) or entry['id'] in public:
            raise ValueError('invalid custom MCP fields or identifier')
        if not all(entry.values()) or entry['origin'] not in ORIGINS or not isinstance(entry['capabilities'], list) or entry['authentication'] not in ('none', 'host-managed', 'oauth', 'api-key'):
            raise ValueError('custom MCP requires complete provenance and capability metadata')
        for key in ('repository', 'documentation'):
            if urlsplit(entry[key]).scheme != 'https':
                raise ValueError('custom MCP requires HTTPS provenance')
        result.append(entry)
    if len({e['id'] for e in result}) != len(result):
        raise ValueError('duplicate custom MCP')
    return result


class Environment:
    def __init__(self, repo_root=ROOT, workspace='.', state_dir=None, host='unknown', host_config=None, runtime_evidence=None, validation_evidence=None):
        self.root = Path(repo_root).resolve()
        self.workspace = Path(workspace).resolve()
        self.skill = self.root / 'plugins/dev-environment-standard/skills/dev-environment-standard'
        self.state_path = Path(state_dir or self.skill / 'runtime-state') / 'environment-state.json'
        self.library_path = self.skill / 'references/mcp-library.json'
        self.host = host
        self.explicit_config = host_config is not None
        defaults = {'codex': Path(os.environ.get('CODEX_HOME', Path.home() / '.codex')) / 'config.toml', 'claude': self.workspace / '.mcp.json'}
        self.config = Path(host_config) if host_config else defaults.get(host)
        self.runtime_evidence = Path(runtime_evidence) if runtime_evidence else None
        self.validation_evidence = Path(validation_evidence) if validation_evidence else None
        self.helper = None

    def tools(self):
        if self.helper is None:
            path = self.root / 'plugins/dev-workflow-standard/scripts/tool-state.py'
            spec = importlib.util.spec_from_file_location('environment_tool_state', path)
            self.helper = importlib.util.module_from_spec(spec)
            old = sys.dont_write_bytecode
            try:
                sys.dont_write_bytecode = True
                spec.loader.exec_module(self.helper)
            finally:
                sys.dont_write_bytecode = old
            self.helper.ROOT = self.root
        return self.helper

    def catalog(self, custom=None):
        entries = library(self.library_path)
        local = self.state().get('custom_mcps', []) if custom is None else custom
        for entry in validate_custom(local, entries):
            entries[entry['id']] = dict(entry, tier='PROJECT_SPECIFIC', preparation={'policy': 'MANUAL_ONLY', 'method': 'host_handoff', 'scope': 'host'}, auth={'required': entry['authentication'] != 'none'}, provenance={'source': entry['repository'], 'verification': 'local metadata; host runtime evidence required'})
        return entries

    def source_paths(self):
        result = [self.root / name for name in ('README.md', 'AGENTS.md', '.gitignore')]
        for directory in ('plugins', 'tests', '.agents', '.claude-plugin', 'docs'):
            start = self.root / directory
            if not start.exists():
                continue
            for current, directories, files in os.walk(start):
                directories[:] = [d for d in directories if d not in ('runtime-state', '__pycache__', '.git') and not (Path(current) / d).is_symlink()]
                result.append(Path(current))
                result.extend(Path(current) / f for f in files if not f.endswith('.pyc'))
        return result

    def fingerprint(self, watched=None):
        parts = [platform.node(), sys.platform, sys.prefix, os.environ.get('VIRTUAL_ENV', ''), os.environ.get('PATH', ''), os.environ.get('TOOL_RUNTIME_ID', 'host'), self.host, str(self.root), str(self.workspace), str(self.config), digest(self.config) if self.config else 'none', digest(self.library_path)]
        parts.append(sorted(str(p.relative_to(self.root)) for p in self.root.glob('plugins/*/skills/*')))
        for name in ('package.json', 'package-lock.json', 'pnpm-lock.yaml', 'yarn.lock', 'uv.lock', 'pyproject.toml'):
            parts.append(digest(self.workspace / name))
        paths = [self.root / p for p in watched] if watched is not None else self.source_paths()
        parts.extend((str(p.relative_to(self.root)), digest(p)) for p in sorted(paths))
        return hashlib.sha256(json.dumps(parts).encode()).hexdigest()

    def state(self):
        try:
            data = safe(read_json(self.state_path))
            if data.get('schema_version') != 1 or not isinstance(data.get('snapshot'), dict) or not isinstance(data.get('mcp_preferences'), dict) or not isinstance(data.get('custom_mcps'), list):
                raise ValueError('invalid state schema')
            snapshot = data['snapshot']
            if not all(isinstance(snapshot.get(k), dict) for k in ('runtimes', 'mcps', 'skills', 'watched')) or not isinstance(snapshot.get('blockers'), list):
                raise ValueError('invalid snapshot')
            if any(not (self.root / p).resolve().is_relative_to(self.root) for p in snapshot['watched']):
                raise ValueError('snapshot path escapes root')
            return data
        except (OSError, ValueError, TypeError):
            return {}

    def registered(self):
        if not self.config or not self.config.exists():
            return {}, None
        try:
            raw = self.config.read_bytes()
            data = tomllib.loads(raw.decode()) if self.host == 'codex' else json.loads(raw)
            table = data.get('mcp_servers' if self.host == 'codex' else 'mcpServers', {})
            if not isinstance(table, dict):
                raise ValueError('invalid config')
            # Retain names and enabled flags only; never propagate commands/env/tokens.
            return {key: value.get('enabled', True) is not False for key, value in table.items() if ID.fullmatch(key) and isinstance(value, dict)}, None
        except (OSError, ValueError, TypeError):
            return {}, 'host configuration unreadable or invalid'

    def evidence(self):
        if not self.runtime_evidence:
            return {}
        try:
            data = safe(read_json(self.runtime_evidence))
            if data.get('schema_version') != 1 or data.get('host') != self.host or data.get('workspace') != str(self.workspace) or not fresh(data.get('observed_at')) or data.get('config_digest') != (digest(self.config) if self.config else 'none'):
                return {}
            result = {}
            for key, item in data.get('mcps', {}).items():
                if not ID.fullmatch(key) or not isinstance(item, dict):
                    continue
                if set(item) - {'installed', 'connected', 'authenticated', 'auth_required', 'broken', 'available'}:
                    continue
                if not all(type(v) is bool for v in item.values()):
                    continue
                result[key] = item
            return result
        except (OSError, ValueError, TypeError):
            return {}

    def mcp_status(self, entries):
        registered, error = self.registered()
        evidence = self.evidence()
        result = {}
        for key, entry in entries.items():
            facts = evidence.get(key, {})
            status = 'MISSING'
            if entry.get('kind') == 'catalog':
                facts = {}
                status = 'UNSUPPORTED'
            elif entry['tier'] == 'RUNTIME_PROVIDED':
                status = 'AVAILABLE' if facts.get('available') else 'UNSUPPORTED'
            elif facts.get('broken'):
                status = 'BROKEN'
            elif facts.get('auth_required'):
                status = 'AUTH_REQUIRED'
            elif facts.get('connected'):
                status = 'CONNECTED'
            elif facts.get('installed'):
                status = 'INSTALLED'
            result[key] = {'status': status, 'registered': registered.get(key, False), 'installed': facts.get('installed', False), 'connected': facts.get('connected', False), 'authenticated': facts.get('authenticated', False), 'authentication': 'AUTH_REQUIRED' if facts.get('auth_required') else 'AUTHENTICATED' if facts.get('authenticated') else 'NOT_OBSERVED', 'tier': entry['tier'], 'origin': entry['origin']}
        return result, error

    def discover(self):
        return sorted(self.root.glob('plugins/*/skills/*/SKILL.md'))

    def health(self, skills):
        checks, blockers, watched = [], [], []

        def check(name, okay):
            checks.append({'check': name, 'result': 'PASS' if okay else 'FAIL'})
            if not okay:
                blockers.append(name)

        plugins = sorted(p for p in (self.root / 'plugins').iterdir() if p.is_dir())
        for plugin in plugins:
            for relative in ('plugin.json', '.codex-plugin/plugin.json', '.claude-plugin/plugin.json'):
                path = plugin / relative
                watched.append(path)
                try:
                    manifest = read_json(path)
                    valid = manifest.get('name') == plugin.name
                    if 'skills' in manifest:
                        declared = (plugin / manifest['skills']).resolve()
                        valid &= declared.is_relative_to(plugin.resolve()) and declared.is_dir()
                    check(f'manifest:{plugin.name}:{relative}', valid)
                except (OSError, ValueError, AttributeError):
                    check(f'manifest:{plugin.name}:{relative}', False)
            check(f'canonical-skill:{plugin.name}', (plugin / 'skills' / plugin.name / 'SKILL.md').is_file())
        for path in skills:
            watched.append(path)
            text = path.read_text(encoding='utf-8')
            check(f'skill:{path.parent.name}', bool(re.match(r'---\s*\nname:\s*[\w-]+\n', text) and re.search(r'^description:', text, re.M)))
            agent = path.parent / 'agents/openai.yaml'
            watched.append(agent)
            check(f'agent:{path.parent.name}', agent.is_file())
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
                target = target.split('#')[0]
                if not target or '://' in target or target.startswith('mailto:'):
                    continue
                referenced = path.parent / target
                watched.append(referenced)
                check(f'reference:{path.parent.name}:{target}', referenced.exists())
            for script in (path.parent / 'scripts').glob('*.py'):
                watched.append(script)
                try:
                    ast.parse(script.read_text())
                    check(f'syntax:{script.name}', True)
                except (SyntaxError, OSError):
                    check(f'syntax:{script.name}', False)
        for path in (self.root / '.agents/plugins/marketplace.json', self.root / '.claude-plugin/marketplace.json'):
            watched.append(path)
            try:
                entries = read_json(path)['plugins']
                names = []
                for entry in entries:
                    source = entry['source']
                    source = source['path'] if isinstance(source, dict) else source
                    resolved = (self.root / source).resolve()
                    names.append(entry['name'])
                    check(f'marketplace:{path.parent.name}:{entry["name"]}', resolved.parent == self.root / 'plugins' and resolved.name == entry['name'] and resolved.is_dir())
                check(f'marketplace-complete:{path.parent.name}', len(names) == len(set(names)) and set(names) == {p.name for p in plugins})
            except (OSError, ValueError, KeyError, TypeError):
                check(f'marketplace:{path.parent.name}', False)
        ignore = self.root / '.gitignore'
        watched.append(ignore)
        check('runtime-state-ignored', ignore.exists() and 'runtime-state' in ignore.read_text())
        parent = self.state_path.parent
        while not parent.exists():
            parent = parent.parent
        check('runtime-state-writable', bool(parent.stat().st_mode & 0o222) and os.access(parent, os.W_OK))
        readme = self.root / 'README.md'
        watched.append(readme)
        check('readme-architecture', readme.exists() and all(word in readme.read_text() for word in ('Environment & Capability Bootstrap', 'dev-environment-standard', 'README', 'NOT READY TO COMMIT')))
        return checks, blockers, watched

    def runtimes(self, required):
        commands = {'git': 'git', 'python': 'python3', 'node': 'node'}
        for name in ('docker', 'java', 'go', 'php'):
            if name in required:
                commands[name] = name
        result = {}
        for name, command in commands.items():
            executable = shutil.which(command)
            version = None
            if executable:
                try:
                    output = subprocess.run([executable, '-version' if name == 'java' else '--version'], capture_output=True, text=True, timeout=10, cwd=self.workspace)
                    match = re.search(r'\d+\.\d+(?:\.\d+)*', output.stdout + output.stderr)
                    version = match.group() if match and output.returncode == 0 else None
                except (OSError, subprocess.TimeoutExpired):
                    pass
            result[name] = {'status': 'AVAILABLE' if version else 'MISSING', 'executable': executable, 'version': version}
        return result

    def project_environment(self):
        managers = set()
        for filename, manager in (('package-lock.json', 'npm'), ('pnpm-lock.yaml', 'pnpm'), ('yarn.lock', 'yarn'), ('uv.lock', 'uv'), ('requirements.txt', 'pip')):
            if (self.workspace / filename).exists():
                managers.add(manager)
        browsers = {}
        cache = Path(os.environ.get('PLAYWRIGHT_BROWSERS_PATH', Path.home() / '.cache/ms-playwright'))
        for name, commands in {'chromium': ('chromium', 'chromium-browser'), 'chrome': ('google-chrome', 'google-chrome-stable'), 'firefox': ('firefox',), 'webkit': ()}.items():
            found = next((shutil.which(c) for c in commands if shutil.which(c)), None)
            browsers[name] = {'status': 'AVAILABLE' if found else 'CACHED_NOT_VALIDATED' if list(cache.glob(name + '-*')) else 'MISSING'}
        return {'package_managers': {m: {'status': 'AVAILABLE' if self.tools().resolve_executable(m, self.workspace) else 'MISSING', 'selected_by_lockfile': m in managers} for m in ('pip', 'pipx', 'uv', 'npm', 'npx', 'pnpm', 'yarn')}, 'browsers': browsers, 'project_dependencies': {'status': 'NOT VALIDATED', 'lockfiles': [p.name for p in self.workspace.iterdir() if p.name in ('package-lock.json', 'pnpm-lock.yaml', 'yarn.lock', 'uv.lock')]}}

    def doctor(self, required=(), custom=None):
        entries = self.catalog(custom)
        skills = self.discover()
        checks, blockers, watched = self.health(skills)
        found = {}
        for path in skills:
            registry = path.parent / 'references/tool-registry.json'
            if not registry.exists():
                found[path.parent.name] = {'status': 'NO_REGISTRY', 'tools': {}, 'missing_tools': []}
                continue
            watched.append(registry)
            try:
                data = read_json(registry)
                if data.get('schema_version') != 1 or data.get('owner') != path.parent.name or not isinstance(data.get('tools'), list):
                    raise ValueError('invalid registry')
                observed = {}
                for tool in data['tools']:
                    if not ID.fullmatch(tool.get('id', '')) or not all(tool.get(k) for k in ('capabilities', 'repository', 'command', 'install_policy')) or not (tool.get('verify_args') or tool.get('verify_distribution')):
                        raise ValueError('invalid registry tool')
                    entry = self.tools().probe(path.parent.name, tool['id'], self.workspace)
                    observed[tool['id']] = {'status': 'INSTALLED' if entry else 'MISSING', 'executable': entry.get('executable') if entry else None, 'capabilities': tool['capabilities'], 'repository': tool['repository'], 'install_policy': tool['install_policy']}
                found[path.parent.name] = {'status': 'INSPECTED', 'tools': observed, 'missing_tools': [k for k, v in observed.items() if v['status'] == 'MISSING']}
                checks.append({'check': f'registry:{path.parent.name}', 'result': 'PASS'})
            except (OSError, ValueError, KeyError, TypeError, StopIteration):
                blockers.append(f'registry:{path.parent.name}')
                checks.append({'check': f'registry:{path.parent.name}', 'result': 'FAIL'})
        mcps, config_error = self.mcp_status(entries)
        if config_error:
            blockers.append(config_error)
        evidence = 'NOT VALIDATED'
        validation_observed_at = None
        verified_components = []
        if self.validation_evidence:
            try:
                data = safe(read_json(self.validation_evidence))
                if data.get('schema_version') == 1 and data.get('fingerprint') == self.fingerprint() and fresh(data.get('observed_at'), 86400) and data.get('checks') and all(c.get('exit_code') == 0 and c.get('command') and c.get('result') == 'PASS' for c in data['checks']):
                    evidence = 'PASS'
                    validation_observed_at = data['observed_at']
                    verified_components = [c['component'] for c in data['checks'] if isinstance(c.get('component'), str)]
            except (OSError, ValueError, TypeError):
                pass
        checks.append({'check': 'tests-and-validators', 'result': evidence})
        for capability in required:
            available = any(capability in e['capabilities'] and mcps[k]['status'] in {'AVAILABLE', 'CONNECTED'} and (not e.get('auth', {}).get('required') or mcps[k]['authenticated']) for k, e in entries.items())
            available |= any(capability in t['capabilities'] and t['status'] == 'INSTALLED' for s in found.values() for t in s['tools'].values())
            if not available and capability not in ('git', 'python', 'node', 'docker', 'java', 'go', 'php'):
                blockers.append('required-capability:' + capability)
        runtimes = self.runtimes(required)
        blockers.extend('runtime:' + k for k, v in runtimes.items() if v['status'] == 'MISSING' and (k in required or k in ('git', 'python')))
        watched = self.source_paths()
        core_missing = any(mcps[k]['status'] not in ('CONNECTED', 'AVAILABLE') or (e.get('auth', {}).get('required') and not mcps[k]['authenticated']) for k, e in entries.items() if e['tier'] == 'CORE')
        report = {'schema_version': 1, 'operation': 'doctor', 'observed_at': now(), 'fingerprint': self.fingerprint(), 'plugin_health': 'BLOCKED' if blockers else 'DEGRADED' if evidence != 'PASS' or core_missing else 'HEALTHY', 'checks': checks, 'runtimes': runtimes, 'mcps': mcps, 'skills': found, 'blockers': blockers, 'watched': {str(p.relative_to(self.root)): digest(p) for p in watched if p.is_relative_to(self.root)}, 'required': list(required)}
        report.update(self.project_environment())
        report['validation_observed_at'] = validation_observed_at
        report['verified_components'] = verified_components
        return report

    def status(self, required=()):
        state = self.state()
        report = state.get('snapshot', {})
        if not report or not fresh(report.get('observed_at'), 86400) or not report.get('watched') or state.get('fingerprint') != self.fingerprint(report['watched']) or any(digest(self.root / p) != d for p, d in report.get('watched', {}).items()):
            return {'schema_version': 1, 'operation': 'status', 'plugin_health': 'DEGRADED', 'ready': False, 'refresh_required': True, 'reason': 'missing, invalid or incompatible snapshot; run doctor/prepare'}
        report = json.loads(json.dumps(report))
        report.update(operation='status', checked_at=now(), refresh_required=False)
        if any(c.get('check') == 'tests-and-validators' and c.get('result') == 'PASS' for c in report.get('checks', [])) and not fresh(report.get('validation_observed_at'), 86400):
            report['refresh_required'] = True
            for check in report['checks']:
                if check.get('check') == 'tests-and-validators':
                    check['result'] = 'NOT VALIDATED'
        report['mcps'], error = self.mcp_status(self.catalog())
        for runtime in report['runtimes'].values():
            path = runtime.get('executable')
            if runtime['status'] == 'AVAILABLE' and (not path or not os.access(path, os.X_OK)):
                runtime['status'] = 'MISSING'
                report['refresh_required'] = True
        for owner, skill in report['skills'].items():
            for key, tool in skill['tools'].items():
                if tool['status'] == 'INSTALLED' and not self.tools().cached(owner, key, self.workspace, read_only=True):
                    tool['status'] = 'MISSING'
                    report['refresh_required'] = True
        entries = self.catalog()
        required = set(required) | set(report.get('required', []))
        available = {c for owner in report['skills'].values() for t in owner['tools'].values() if t['status'] == 'INSTALLED' for c in t['capabilities']}
        available |= {c for k, e in entries.items() if report['mcps'][k]['status'] in ('CONNECTED', 'AVAILABLE') and (not e.get('auth', {}).get('required') or report['mcps'][k]['authenticated']) for c in e['capabilities']}
        available |= {k for k, v in report['runtimes'].items() if v['status'] == 'AVAILABLE'}
        report['capabilities_ready'] = not error and not report['blockers'] and required <= available and not report['refresh_required']
        tests_valid = any(c.get('check') == 'tests-and-validators' and c.get('result') == 'PASS' for c in report.get('checks', []))
        core_ready = all(report['mcps'][k]['status'] in ('CONNECTED', 'AVAILABLE') and (not e.get('auth', {}).get('required') or report['mcps'][k]['authenticated']) for k, e in entries.items() if e['tier'] == 'CORE')
        pending_validation = any(r.get('result') in ('EXECUTED', 'VERIFICATION_REQUIRED') for r in report.get('receipts', []))
        report['ready'] = report['capabilities_ready'] and tests_valid and core_ready and not pending_validation
        if not report['ready'] or any(report['mcps'][k]['status'] not in ('CONNECTED', 'AVAILABLE') for k, e in entries.items() if e['tier'] == 'CORE'):
            report['plugin_health'] = 'DEGRADED' if not report['blockers'] else 'BLOCKED'
        return report

    def dependency_plan(self):
        js = [name for name in ('package-lock.json', 'pnpm-lock.yaml', 'yarn.lock') if (self.workspace / name).exists()]
        if len(js) > 1:
            raise ValueError('conflicting JavaScript lockfiles require an explicit project decision')
        commands = {'package-lock.json': ['npm', 'ci'], 'pnpm-lock.yaml': ['pnpm', 'install', '--frozen-lockfile']}
        if js and js[0] == 'yarn.lock':
            package = read_json(self.workspace / 'package.json')
            manager = package.get('packageManager', '')
            match = re.fullmatch(r'yarn@(\d+)\.[\w.+-]+', manager)
            if not match:
                raise ValueError('Yarn lock requires pinned packageManager version')
            command = ['yarn', 'install', '--frozen-lockfile' if match[1] == '1' else '--immutable']
        elif js:
            command = commands[js[0]]
        elif (self.workspace / 'uv.lock').exists():
            command = ['uv', 'sync', '--locked']
        else:
            raise ValueError('no supported project lockfile')
        if js and (self.workspace / 'uv.lock').exists():
            raise ValueError('multiple ecosystems: select and prepare dependencies separately')
        return {'component': 'project:dependencies', 'command': command, 'scope': str(self.workspace), 'policy': 'PROJECT_SCOPED', 'method': 'locked-dependencies', 'source': 'project-lockfile'}

    def declared_tool(self, identifier):
        """Only restore dependencies the project actually declares, never add a package."""
        if (self.workspace / 'uv.lock').exists() and (self.workspace / 'pyproject.toml').exists():
            data = tomllib.loads((self.workspace / 'pyproject.toml').read_text())
            project = data.get('project', {})
            dependencies = list(project.get('dependencies', []))
            dependencies.extend(item for group in project.get('optional-dependencies', {}).values() for item in group)
            dependencies.extend(item for group in data.get('dependency-groups', {}).values() for item in group if isinstance(item, str))
            return any(re.split(r'[\s<>=!~;\[]', item, maxsplit=1)[0].lower().replace('_', '-') == identifier.lower().replace('_', '-') for item in dependencies)
        if (self.workspace / 'package.json').exists():
            data = read_json(self.workspace / 'package.json')
            names = set(data.get('dependencies', {})) | set(data.get('devDependencies', {}))
            return identifier in names or (identifier == 'playwright' and bool(names & {'@playwright/test', 'playwright'}))
        return False

    def plan(self, report, selected=(), required=(), preferences=None, custom=None):
        entries = self.catalog(custom)
        preferences = preferences or {}
        plan = []
        selected = set(selected)
        for key, entry in entries.items():
            if not (entry['tier'] == 'CORE' or key in selected or preferences.get(key) == 'enabled' or set(required) & set(entry['capabilities'])):
                continue
            observed = report['mcps'][key]
            if observed['status'] in ('CONNECTED', 'AVAILABLE') and (not entry.get('auth', {}).get('required') or observed['authenticated']):
                continue
            prep = entry['preparation']
            command = ['host-config:add', self.host, key, json.dumps(entry.get('configuration'), sort_keys=True)]
            action = 'CONFIGURE'
            if entry['origin'] == 'UNKNOWN' or prep['policy'] in ('MANUAL_ONLY', 'PRIVILEGED') or entry['tier'] == 'RUNTIME_PROVIDED' or prep['method'] != 'host_config' or not self.explicit_config or self.host not in ('codex', 'claude') or observed['registered']:
                action = 'USER_ACTION_REQUIRED'
            if observed['connected'] and entry.get('auth', {}).get('required') and not observed['authenticated']:
                action = 'USER_ACTION_REQUIRED'
            if entry.get('configuration', {}).get('transport') == 'stdio':
                node = report['runtimes'].get('node', {})
                version = tuple(int(p) for p in (node.get('version') or '0.0.0').split('.')[:3])
                required_node = entry.get('requirements', {}).get('node')
                compatible = version >= (18, 0, 0) if required_node == '>=18' else (version >= (23, 0, 0) or (version[0] == 22 and version >= (22, 12, 0)) or (version[0] == 20 and version >= (20, 19, 0))) if required_node else True
                if not compatible or not shutil.which('npx'):
                    action = 'USER_ACTION_REQUIRED'
            plan.append({'component': key, 'command': command, 'scope': str(self.config.resolve()) if self.config else 'host', 'policy': prep['policy'], 'method': prep['method'], 'source': entry['repository'], 'origin': entry['origin'], 'tier': entry['tier'], 'action': action})
        for owner, skill in report['skills'].items():
            for key, tool in skill['tools'].items():
                component = f'tool:{owner}:{key}'
                if tool['status'] == 'INSTALLED' or not (component in selected or set(required) & set(tool['capabilities'])):
                    continue
                # Owner-approved dependency declarations are the install source. Never map arbitrary tool IDs to packages.
                action = {'component': component, 'command': [], 'scope': str(self.workspace), 'policy': 'PROJECT_SCOPED' if tool['install_policy'] == 'project-approved-dependency' else 'MANUAL_ONLY', 'owner_install_policy': tool['install_policy'], 'method': 'owner-tool', 'source': tool['repository'], 'action': 'OWNER_APPROVAL_REQUIRED'}
                try:
                    if tool['install_policy'] == 'project-approved-dependency' and self.declared_tool(key):
                        dependency = self.dependency_plan()
                        action.update(command=dependency['command'], action='INSTALL')
                except (OSError, ValueError):
                    pass
                plan.append(action)
        if 'project:dependencies' in selected:
            plan.append(self.dependency_plan())
        for browser in ('chromium', 'chrome', 'firefox', 'webkit'):
            if 'browser:' + browser in selected:
                executable = self.workspace / 'node_modules/.bin/playwright'
                plan.append({'component': 'browser:' + browser, 'command': [str(executable), 'install', browser], 'scope': str(self.workspace), 'policy': 'PRIVILEGED' if browser == 'chrome' else 'PROJECT_SCOPED', 'method': 'browser', 'browser_cache': str(self.workspace / '.cache/ms-playwright'), 'source': 'https://github.com/microsoft/playwright', 'action': 'INSTALL' if executable.is_file() and browser != 'chrome' else 'USER_ACTION_REQUIRED'})
        known = set(entries) | {'project:dependencies'} | {'browser:' + x for x in ('chromium', 'chrome', 'firefox', 'webkit')} | {f'tool:{o}:{k}' for o, s in report['skills'].items() for k in s['tools']}
        if selected - known:
            raise ValueError('unknown selected component')
        return plan

    def configure(self, entry):
        config = entry['configuration']
        validate_configuration(config)
        registered, error = self.registered()
        if error or entry['id'] in registered:
            raise ValueError('existing or invalid MCP configuration requires manual reconciliation')
        old_digest = digest(self.config)
        if self.host == 'claude':
            data = read_json(self.config) if self.config.exists() else {}
            servers = data.setdefault('mcpServers', {})
            servers[entry['id']] = ({'type': 'http', 'url': config['url']} if config['transport'] == 'http' else {'command': config['command'], 'args': config['args']})
            content = json.dumps(data, indent=2) + '\n'
        else:
            content = self.config.read_text() if self.config.exists() else ''
            content += '\n[mcp_servers.' + entry['id'] + ']\n'
            if config['transport'] == 'http':
                content += 'url = ' + json.dumps(config['url']) + '\n'
            else:
                content += 'command = ' + json.dumps(config['command']) + '\nargs = ' + json.dumps(config['args']) + '\n'
            tomllib.loads(content)
        if digest(self.config) != old_digest:
            raise ValueError('host configuration changed during preparation')
        atomic(self.config, content)

    def prepare(self, selected=(), required=(), preferences=None, approvals=(), custom=None, dry_run=False, component=None):
        safe(preferences or {})
        safe(approvals)
        safe(custom or [])
        report = self.doctor(required, custom)
        previous = self.state()
        prefs = dict(previous.get('mcp_preferences', {}))
        entries = self.catalog(custom)
        for key, value in (preferences or {}).items():
            if key not in entries or value not in ('enabled', 'disabled', 'not_requested'):
                raise ValueError('invalid MCP preference')
            prefs[key] = value
        for key in selected:
            if key in entries:
                prefs[key] = 'enabled'
        plan = self.plan(report, selected, required, prefs, custom)
        structural_failure = any(not b.startswith(('required-capability:', 'runtime:')) for b in report['blockers'])
        if component:
            prior = previous.get('snapshot', {})
            prior_mcp = prior.get('mcps', {}).get(component, {})
            failed = report['mcps'].get(component, {}).get('status') in ('BROKEN', 'MISSING')
            prior_available = prior_mcp.get('status') in ('CONNECTED', 'AVAILABLE', 'INSTALLED')
            if component.startswith('tool:'):
                _, owner, key = component.split(':')
                prior_available = prior.get('skills', {}).get(owner, {}).get('tools', {}).get(key, {}).get('status') == 'INSTALLED'
                failed = report['skills'].get(owner, {}).get('tools', {}).get(key, {}).get('status') == 'MISSING'
            if not prior_available or not failed:
                raise ValueError('repair requires a previously available component and current failure')
            plan = [p for p in self.plan(report, [component], (), prefs, custom) if p['component'] == component]
        receipts = []
        for action in plan:
            receipt = dict(action, executed=False, result='PLANNED')
            approval = next((a for a in approvals if a.get('component') == action['component'] and a.get('command') == action['command'] and a.get('scope') == action['scope']), None)
            prior_receipt = next((r for r in previous.get('snapshot', {}).get('receipts', []) if r.get('component') == action['component'] and r.get('command') == action['command'] and r.get('scope') == action['scope'] and r.get('result') in ('FAILED', 'RETRY_DEFERRED')), None)
            prior_execution = next((r for r in previous.get('snapshot', {}).get('receipts', []) if r.get('component') == action['component'] and r.get('command') == action['command'] and r.get('scope') == action['scope'] and r.get('result') in ('EXECUTED', 'VERIFICATION_REQUIRED')), None)
            if prior_receipt or prior_execution:
                receipt['executed_at'] = (prior_receipt or prior_execution).get('executed_at')
            if structural_failure:
                receipt['result'] = 'BLOCKED_INVALID_ENVIRONMENT'
            elif prior_receipt and not component:
                receipt['result'] = 'RETRY_DEFERRED'
            elif prior_execution and not component:
                receipt['result'] = 'VERIFICATION_REQUIRED'
            elif action.get('action') in ('USER_ACTION_REQUIRED', 'OWNER_APPROVAL_REQUIRED'):
                receipt['result'] = action['action']
            elif (action.get('origin') == 'COMMUNITY' or action.get('tier') == 'COMMUNITY') and (not approval or approval.get('community_confirmed') is not True):
                receipt['result'] = 'COMMUNITY_CONFIRMATION_REQUIRED'
            elif not approval:
                receipt['result'] = 'APPROVAL_REQUIRED'
            elif dry_run:
                receipt['result'] = 'APPROVED_DRY_RUN'
            elif action['method'] == 'host_config':
                self.configure(entries[action['component']])
                receipt.update(executed=True, result='REGISTERED', exit_code=0)
            elif action['method'] == 'owner-tool':
                _, owner, key = action['component'].split(':')
                result = self.tools().install(owner, key, self.workspace, action['command'], 'project-locked-dependencies', force_retry=bool(component))
                receipt.update(executed=True, result='VERIFIED' if result['status'] == 'installed' else 'FAILED', exit_code=result.get('exit_code', 0 if result['status'] == 'installed' else 2))
            else:
                try:
                    options = {'cwd': self.workspace, 'capture_output': True, 'timeout': 300, 'check': False}
                    if action['method'] == 'browser':
                        options['env'] = dict(os.environ, PLAYWRIGHT_BROWSERS_PATH=action['browser_cache'])
                    result = subprocess.run(action['command'], **options)
                    receipt.update(executed=True, exit_code=result.returncode, result='EXECUTED' if result.returncode == 0 else 'FAILED')
                    receipt['verification'] = 'NOT VALIDATED'
                except (OSError, subprocess.TimeoutExpired):
                    receipt.update(executed=True, result='FAILED', exit_code=2)
            receipts.append(receipt)
            if receipt['executed']:
                receipt['executed_at'] = now()
        pending = [k for k, e in entries.items() if e['tier'] in ('RECOMMENDED', 'OPTIONAL', 'PROJECT_SPECIFIC') and k not in prefs and (e['tier'] != 'PROJECT_SPECIFIC' or set(required) & set(e['capabilities']))]
        if not dry_run and any(r['executed'] for r in receipts):
            report = self.doctor(required, custom)
        pending_results = {'FAILED', 'RETRY_DEFERRED', 'EXECUTED', 'VERIFICATION_REQUIRED'}
        current = {r['component'] for r in receipts}
        receipts.extend(dict(r, executed=False, carried_forward=True) for r in previous.get('snapshot', {}).get('receipts', []) if r.get('result') in pending_results and r.get('component') not in current)
        for receipt in receipts:
            if receipt['result'] in pending_results and receipt['component'] in report.get('verified_components', []) and receipt.get('executed_at') and report.get('validation_observed_at') and dt.datetime.fromisoformat(report['validation_observed_at']) >= dt.datetime.fromisoformat(receipt['executed_at']):
                receipt.update(result='VERIFIED_EXTERNALLY', verification='PASS')
        if any(r['result'] in ('FAILED', 'RETRY_DEFERRED') for r in receipts):
            report['plugin_health'] = 'BLOCKED'
            report['blockers'].extend('preparation-failed:' + r['component'] for r in receipts if r['result'] in ('FAILED', 'RETRY_DEFERRED'))
        report.update(operation='repair' if component else 'prepare', plan=plan, receipts=receipts, optional_choices=pending, custom_mcp_question=not previous.get('custom_prompt_shown', False), custom_mcps={e['id']: {'status': 'USER_ACTION_REQUIRED', 'origin': e['origin']} for e in (custom if custom is not None else previous.get('custom_mcps', []))}, mcp_preferences=prefs, dry_run=dry_run)
        if not dry_run:
            for key in pending:
                prefs.setdefault(key, 'not_requested')
            # Persist observations through the existing owner helper, not a second cache.
            for owner, skill in report['skills'].items():
                for key, tool in skill['tools'].items():
                    if tool['status'] == 'INSTALLED':
                        self.tools().detect(owner, key, self.workspace)
            report['mcps'], _ = self.mcp_status(entries)
            report['fingerprint'] = self.fingerprint()
            state = {'schema_version': 1, 'fingerprint': report['fingerprint'], 'snapshot': report, 'mcp_preferences': prefs, 'custom_mcps': custom if custom is not None else previous.get('custom_mcps', []), 'custom_prompt_answered': custom is not None or previous.get('custom_prompt_answered', False), 'custom_prompt_shown': True, 'last_prepare': now()}
            safe(state)
            atomic(self.state_path, json.dumps(state, indent=2) + '\n')
        return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('doctor', 'prepare', 'repair', 'status'))
    parser.add_argument('--repo-root', '--harness-root', default=str(ROOT))
    parser.add_argument('--workspace', default='.')
    parser.add_argument('--state-dir')
    parser.add_argument('--host', choices=('codex', 'claude', 'unknown'), default='unknown')
    for name in ('host-config', 'runtime-evidence', 'validation-evidence', 'preferences', 'custom-mcps', 'approvals', 'component'):
        parser.add_argument('--' + name)
    parser.add_argument('--select', action='append', default=[])
    parser.add_argument('--require', action='append', default=[])
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    try:
        env = Environment(args.repo_root, args.workspace, args.state_dir, args.host, args.host_config, args.runtime_evidence, args.validation_evidence)
        if args.operation == 'doctor':
            report = env.doctor(args.require)
        elif args.operation == 'status':
            report = env.status(args.require)
        else:
            prefs = safe(read_json(args.preferences)).get('mcp_preferences', {}) if args.preferences else None
            approvals = safe(read_json(args.approvals)).get('approvals', []) if args.approvals else []
            custom = custom_entries(args.custom_mcps, library(env.library_path)) if args.custom_mcps else None
            if args.operation == 'repair' and not args.component:
                raise ValueError('repair requires --component')
            report = env.prepare(args.select, args.require, prefs, approvals, custom, args.dry_run, args.component if args.operation == 'repair' else None)
        if args.json:
            print(json.dumps(report, sort_keys=True))
        else:
            print('PLUGIN HEALTH: ' + report['plugin_health'])
            for key, value in report.get('mcps', {}).items():
                print(f'MCP {key}: {value["status"]}; authentication={value["authentication"]}')
            for receipt in report.get('receipts', []):
                print(receipt['component'] + ': ' + receipt['result'])
            if report.get('optional_choices'):
                print('Choose optional MCPs with --preferences: ' + ', '.join(report['optional_choices']))
            if report.get('custom_mcp_question'):
                print('Do you use a custom MCP? Supply --custom-mcps, including an empty list to decline.')
        failed = any(r.get('result') == 'FAILED' for r in report.get('receipts', []))
        return 2 if report['plugin_health'] == 'BLOCKED' or failed else 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        # Do not echo hostile input, config, subprocess stdout or secrets.
        print(json.dumps({'error': 'invalid or inaccessible environment input', 'plugin_health': 'BLOCKED'}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
