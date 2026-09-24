#!/usr/bin/env python3
"""Conservative GitHub governance reconciliation using existing gh credentials.

Only apply with a reviewed, freshly matching proposal permits writes. This is
not a credential manager, CI runner, policy engine or merge/deployment tool.
"""
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import quote

STAGES = ['Backlog', 'Discovery / SDD', 'Ready for Dev', 'In Progress',
          'Validation', 'In Review', 'Awaiting Final Approval', 'Done']
VERSION = 1
REQUIRED_GOVERNANCE_FILES = ('.github/CODEOWNERS', '.github/PULL_REQUEST_TEMPLATE.md',
                             'CONTRIBUTING.md', '.github/ISSUE_TEMPLATE/config.yml',
                             '.github/ISSUE_TEMPLATE/bug.yml', '.github/ISSUE_TEMPLATE/feature.yml',
                             '.github/ISSUE_TEMPLATE/task.yml')
STACK_INPUTS = ('package.json', 'package-lock.json', 'npm-shrinkwrap.json',
                'pnpm-lock.yaml', 'yarn.lock', 'composer.json', 'composer.lock',
                'pyproject.toml', 'requirements.txt', 'requirements-dev.txt',
                'uv.lock', 'poetry.lock', 'go.mod', 'go.sum', 'pytest.ini', 'setup.cfg')
STACK_INPUTS += ('.nvmrc', '.node-version', '.python-version', '.php-version')
# Verified against upstream git refs on 2026-09-24; updates require a new review.
ACTION_PINS = {'checkout': 'actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683',
               'node': 'actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020',
               'go': 'actions/setup-go@d35c59abb061a4a6fb18e82ac0862c26744d6ab5',
               'uv': 'astral-sh/setup-uv@6b9c6063abd6010835644d4c2e1bef4cf5cd0fca',
               'php': 'shivammathur/setup-php@20529878ed81ef8e78ddf08b480401e6101a850f'}


class GovernanceError(Exception):
    def __init__(self, code, message='Operation could not be validated safely.'):
        self.code = code
        super().__init__(message)


def fail(code='VALIDATION_FAILED', message='Invalid governance input.'):
    raise GovernanceError(code, message)


def canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def output_guard(value):
    """Reject, never echo, recognizable credentials in review diffs/API strings."""
    encoded = canonical(value)
    if re.search(r'github_pat_|gh[pousr]_|-----BEGIN [A-Z ]*PRIVATE KEY|(?i:bearer)\s|(?i:(?:password|secret|token|api[_-]?key)\s*[:=])', encoded):
        fail('VALIDATION_FAILED', 'Potential credential in reviewed material. Remove it locally before generating a proposal; content suppressed.')
    for key in ('GH_TOKEN', 'GITHUB_TOKEN', 'GH_ENTERPRISE_TOKEN', 'GITHUB_ENTERPRISE_TOKEN'):
        secret = os.environ.get(key)
        if secret and len(secret) >= 8 and secret in encoded:
            fail('VALIDATION_FAILED', 'Sensitive material cannot be included in output.')
    return value


def norm(value):
    return ' '.join(value.split()).casefold()


def text_value(value, max_length=120):
    if (not isinstance(value, str) or not value.strip() or len(value) > max_length
            or re.search(r'[\x00-\x1f\x7f`$<>;\\]', value)
            or re.search(r'(github_pat_|gh[pousr]_|Bearer\s)', value, re.I)):
        fail()
    return value


def shape(value, required, optional=()):
    if not isinstance(value, dict) or set(value) - set(required) - set(optional) or set(required) - set(value):
        fail()


def validate_config(d):
    shape(d, ['schema_version', 'repository', 'project', 'labels', 'human_gates',
              'automation', 'local', 'ci', 'rules', 'exceptions'])
    if type(d['schema_version']) is not int or d['schema_version'] != VERSION:
        fail()
    r = d['repository']
    shape(r, ['host', 'owner', 'name', 'default_branch', 'agent_branch_prefix',
              'squash_only', 'delete_branch_on_merge'])
    # Public GitHub schema was researched; do not claim GHES API compatibility.
    if r['host'] != 'github.com':
        fail(message='Only github.com is supported by this version.')
    for key in ('owner', 'name'):
        if not isinstance(r[key], str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,99}', r[key]) or '..' in r[key]:
            fail()
    for key in ('default_branch', 'agent_branch_prefix'):
        value = text_value(r[key])
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_./-]*', value) or '..' in value or '//' in value or value.endswith('.lock'):
            fail()
    if r['default_branch'].endswith('/'):
        fail()
    for key in ('squash_only', 'delete_branch_on_merge'):
        if type(r[key]) is not bool:
            fail()
    p = d['project']
    shape(p, ['enabled', 'title', 'statuses', 'view_name'], ['reason'])
    text_value(p['title']); text_value(p['view_name'])
    if p['statuses'] != STAGES:
        fail(message='The eight approved lifecycle stages are required.')
    shape(d['ci'], ['enabled', 'required_checks'], ['reason'])
    shape(d['rules'], ['enabled', 'required_approvals'], ['reason'])
    for part in (p, d['ci'], d['rules']):
        if type(part.get('enabled')) is not bool:
            fail()
        if not part['enabled']:
            text_value(part.get('reason'), 500)
    shape(d['ci'], ['enabled', 'required_checks'], ['reason'])
    shape(d['rules'], ['enabled', 'required_approvals'], ['reason'])
    if type(d['rules']['required_approvals']) is not int or not 0 <= d['rules']['required_approvals'] <= 6:
        fail()
    for items in (d['labels'], d['ci']['required_checks']):
        if not isinstance(items, list) or len(items) > 100:
            fail()
        for value in items:
            text_value(value)
        if len({norm(x) for x in items}) != len(items):
            fail()
    shape(d['human_gates'], ['task', 'pr', 'merge', 'deploy'])
    if any(value is not True for value in d['human_gates'].values()):
        fail()
    shape(d['automation'], ['auto_merge', 'auto_deploy', 'max_rework_cycles'])
    a = d['automation']
    if a['auto_merge'] is not False or a['auto_deploy'] is not False or type(a['max_rework_cycles']) is not int or not 1 <= a['max_rework_cycles'] <= 3:
        fail()
    shape(d['local'], ['generate', 'codeowners'])
    if type(d['local']['generate']) is not bool or not isinstance(d['local']['codeowners'], list) or not d['local']['codeowners']:
        fail()
    for owner in d['local']['codeowners']:
        if not isinstance(owner, str) or not re.fullmatch(r'@[A-Za-z0-9][A-Za-z0-9_-]*(/[A-Za-z0-9_-]+)?', owner):
            fail()
    if not isinstance(d['exceptions'], list):
        fail()
    for exception in d['exceptions']:
        shape(exception, ['capability', 'reason'])
        if exception['capability'] not in ('rules', 'project_grouping', 'project_automation'):
            fail()
        text_value(exception['reason'], 500)
    return d


def safe_path(root, relative):
    relative = Path(relative)
    if relative.is_absolute() or '..' in relative.parts or not relative.parts:
        fail('LOCAL_CONFLICT', 'Local path must stay inside the workspace.')
    path = root
    for part in relative.parts:
        path = path / part
        if path.is_symlink():
            fail('LOCAL_CONFLICT', 'Symlinks are not allowed for governed files.')
    if not path.resolve().is_relative_to(root.resolve()):
        fail('LOCAL_CONFLICT')
    return path


def read_json(path):
    try:
        if path.stat().st_size > 2_000_000:
            fail()
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError, UnicodeError):
        fail(message='Cannot read valid JSON input; no raw content is logged.')


def api_error(raw, code):
    low = raw.casefold()
    if 'upgrade to github' in low or 'not available on your plan' in low:
        return GovernanceError('PLAN_LIMITATION', 'API explicitly reports a plan restriction.')
    if '401' in low or 'authentication' in low or 'not logged' in low:
        return GovernanceError('AUTH_REQUIRED', 'USER_ACTION_REQUIRED: run gh auth login --hostname github.com, then diagnose.')
    if '403' in low or '404' in low or 'scope' in low or 'permission' in low:
        return GovernanceError('INSUFFICIENT_PERMISSION', 'Access is denied or resource is inaccessible; inspect account and minimum permissions.')
    if 'undefinedfield' in low or 'doesn\'t exist on type' in low or 'unknown argument' in low:
        return GovernanceError('GRAPHQL_UNSUPPORTED', 'Requested schema operation is not supported.')
    return GovernanceError('API_UNAVAILABLE', 'GitHub operation failed; raw response suppressed.')


class GH:
    def __init__(self, host, writable=False):
        self.host, self.writable = host, writable

    def run(self, args, payload=None):
        try:
            result = subprocess.run(['gh', *args], input=canonical(payload) if payload is not None else None,
                                    capture_output=True, text=True, timeout=60, check=False)
        except FileNotFoundError:
            fail('GH_MISSING', 'USER_ACTION_REQUIRED: ask Environment to prepare gh, then diagnose.')
        except (OSError, subprocess.TimeoutExpired):
            fail('API_UNAVAILABLE', 'GitHub CLI could not complete the operation.')
        if result.returncode:
            raise api_error(result.stderr, result.returncode)
        return result.stdout

    def preflight(self):
        if not shutil.which('gh'):
            fail('GH_MISSING', 'USER_ACTION_REQUIRED: ask Environment to prepare gh, then diagnose.')
        version = self.run(['--version'])
        match = re.search(r'gh version ([0-9]+\.[0-9]+\.[0-9]+)', version)
        if not match:
            fail('GH_BROKEN', 'Cannot identify a valid GitHub CLI version.')
        self.version = match.group(1)
        try:
            self.run(['auth', 'status', '--hostname', self.host])
        except GovernanceError:
            fail('AUTH_REQUIRED', 'USER_ACTION_REQUIRED: run gh auth login --hostname github.com, then diagnose.')
        return self.rest('GET', 'user')

    def rest(self, method, endpoint, payload=None):
        if method != 'GET' and not self.writable:
            fail(message='Read-only mode rejected a mutation.')
        args = ['api', '--hostname', self.host, '--method', method, endpoint,
                '-H', 'Accept: application/vnd.github+json', '-H', 'X-GitHub-Api-Version: 2026-03-10']
        if payload is not None:
            args += ['--input', '-']
        try:
            return json.loads(self.run(args, payload))
        except ValueError:
            fail('API_UNAVAILABLE', 'Malformed API JSON response.')

    def pages(self, endpoint, key=None):
        result, seen = [], set()
        for number in range(1, 10001):
            sep = '&' if '?' in endpoint else '?'
            page = self.rest('GET', f'{endpoint}{sep}per_page=100&page={number}')
            rows = page[key] if key else page
            if not isinstance(rows, list):
                fail('API_UNAVAILABLE')
            fresh = 0
            for row in rows:
                if not isinstance(row, dict):
                    fail('API_UNAVAILABLE', 'Malformed API collection member.')
                identity = row.get('id', canonical(row))
                if identity not in seen:
                    seen.add(identity); result.append(row); fresh += 1
            if len(rows) < 100:
                return result
            if not fresh:
                fail('API_UNAVAILABLE', 'Pagination did not advance.')
        fail('API_UNAVAILABLE', 'Pagination safety limit exceeded; evidence is incomplete.')

    def graphql(self, query, variables=None):
        if not self.writable and not query.lstrip().startswith('query'):
            fail(message='Read-only mode rejected a GraphQL mutation.')
        raw = self.run(['api', '--hostname', self.host, 'graphql', '--input', '-'],
                       {'query': query, 'variables': variables or {}})
        try:
            data = json.loads(raw)
        except ValueError:
            fail('API_UNAVAILABLE')
        if not isinstance(data, dict):
            fail('API_UNAVAILABLE')
        if data.get('errors'):
            raise api_error(canonical(data['errors']), 1)
        if not isinstance(data.get('data'), dict):
            fail('API_UNAVAILABLE')
        return data['data']

    def connection(self, query, variables, path):
        rows, cursors, seen = [], set(), set()
        variables = dict(variables)
        for _ in range(10000):
            data = self.graphql(query, variables)
            for part in path:
                data = data[part]
            for row in data['nodes']:
                if row is None:
                    continue
                if not isinstance(row, dict) or not isinstance(row.get('id'), str):
                    fail('API_UNAVAILABLE')
                if row['id'] in seen:
                    continue
                seen.add(row['id']); rows.append(row)
            info = data['pageInfo']
            if not info['hasNextPage']:
                return rows
            cursor = info['endCursor']
            if not cursor or cursor in cursors:
                fail('API_UNAVAILABLE', 'GraphQL pagination did not advance.')
            cursors.add(cursor); variables['cursor'] = cursor
        fail('API_UNAVAILABLE')


def status_options(existing, names):
    keys = [norm(item['name']) for item in existing]
    if len(set(keys)) != len(keys):
        fail('REMOTE_CONFLICT', 'Ambiguous equivalent Status options require manual reconciliation.')
    options = [{key: item[key] for key in ('id', 'name', 'color', 'description')} for item in existing]
    for name in names:
        if norm(name) not in keys:
            options.append({'name': name, 'color': 'GRAY', 'description': ''})
    return options


def limitation(capability, reason, code='NOT_VALIDATED'):
    return {'capability': capability, 'status': code, 'reason': reason}


def local_artifacts(root, d):
    files, limits = {}, []
    if d['local']['generate']:
        files = {
            '.github/CODEOWNERS': '# File presence does not prove review enforcement.\n* ' + ' '.join(d['local']['codeowners']) + '\n',
            '.github/ISSUE_TEMPLATE/config.yml': 'blank_issues_enabled: false\n',
            '.github/PULL_REQUEST_TEMPLATE.md': '## Task / Issue / Spec\n\n## Change and evidence\n\n- [ ] Tests and required sector receipts linked\n- [ ] Security disposition recorded\n- [ ] Human review required, no automatic merge or deployment\n',
            'CONTRIBUTING.md': '# Contributing\n\nUse ' + d['repository']['agent_branch_prefix'] + ' branches for agent work.\nApprove Task and SDD before implementation. Supply tests and sector receipts.\nOpen a PR for human review. Done requires observed human merge.\nDeployment requires separate human approval. Stop after ' + str(d['automation']['max_rework_cycles']) + ' rework cycles.\n',
        }
        for kind in ('bug', 'feature', 'task'):
            files[f'.github/ISSUE_TEMPLATE/{kind}.yml'] = ('name: ' + kind.title() + '\ndescription: Governed ' + kind + '\nbody:\n  - type: textarea\n    id: context\n    attributes:\n      label: Context, scope and acceptance criteria\n    validations:\n      required: true\n')
        for directory in ('specs', 'tasks', 'execution'):
            files[f'docs/{directory}/.gitkeep'] = ''
    else:
        if any(not safe_path(root, name).is_file() for name in REQUIRED_GOVERNANCE_FILES) or any(not safe_path(root, 'docs/' + part).is_dir() for part in ('specs', 'tasks', 'execution')):
            limits.append(limitation('local_governance', 'Generation is disabled but required governance files/directories are missing.'))
    if not d['ci']['enabled']:
        return files, limits
    if workflow_paths(root):
        # Reuse native pipelines. Actual remote checks, not YAML parsing, prove CI.
        return files, limits
    detected = [name for name in ('package.json', 'composer.json', 'pyproject.toml', 'go.mod') if safe_path(root, name).is_file()]
    commands, setup = [], ''
    if detected == ['package.json']:
        package = read_json(safe_path(root, 'package.json'))
        scripts = package.get('scripts', {})
        if not isinstance(scripts, dict):
            fail()
        version_files = [name for name in ('.nvmrc', '.node-version') if safe_path(root, name).is_file()]
        runtime = safe_path(root, version_files[0]).read_text().strip() if version_files else ''
        if (safe_path(root, 'package-lock.json').is_file() or safe_path(root, 'npm-shrinkwrap.json').is_file()) and re.fullmatch(r'v?[0-9]+(?:\.[0-9]+){0,2}', runtime):
            commands = ['npm ci'] + ['npm run ' + name for name in ('lint', 'typecheck', 'test', 'build') if isinstance(scripts.get(name), str)]
            setup = '      - uses: ' + ACTION_PINS['node'] + '\n        with:\n          node-version-file: ' + version_files[0] + '\n          cache: npm\n'
    elif detected == ['composer.json'] and safe_path(root, 'composer.lock').is_file():
        package = read_json(safe_path(root, 'composer.json'))
        scripts = package.get('scripts', {})
        runtime = package.get('config', {}).get('platform', {}).get('php', '')
        if re.fullmatch(r'[0-9]+\.[0-9]+(?:\.[0-9]+)?', str(runtime)):
            commands = ['composer install --no-interaction --prefer-dist'] + ['composer run-script ' + key for key in ('lint', 'test', 'analyse') if key in scripts]
            setup = '      - uses: ' + ACTION_PINS['php'] + '\n        with:\n          php-version: ' + json.dumps(runtime) + '\n          tools: composer\n'
    elif detected == ['go.mod']:
        commands = ['go mod download', 'go test ./...', 'go vet ./...', 'go build ./...']
        setup = '      - uses: ' + ACTION_PINS['go'] + '\n        with:\n          go-version-file: go.mod\n'
    elif detected == ['pyproject.toml']:
        import tomllib
        try:
            project = tomllib.loads(safe_path(root, 'pyproject.toml').read_text())
        except (ValueError, OSError):
            fail()
        if safe_path(root, 'uv.lock').is_file() and 'pytest' in canonical(project):
            commands = ['uv sync --frozen', 'uv run --no-sync pytest']
            setup = '      - uses: ' + ACTION_PINS['uv'] + '\n'
    if len(commands) < 2:
        limits.append(limitation('ci_stack', 'MANUAL_ACTION_REQUIRED: choose reviewed stack-native locked install and existing validation commands.'))
    else:
        branch = json.dumps(d['repository']['default_branch'])
        files['.github/workflows/quality.yml'] = ('name: Quality\non:\n  pull_request:\n  push:\n    branches: [' + branch + ']\npermissions:\n  contents: read\njobs:\n  quality:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: ' + ACTION_PINS['checkout'] + '\n' + setup + ''.join('      - run: ' + cmd + '\n' for cmd in commands))
    return files, limits


def workflow_paths(root):
    folder = safe_path(root, '.github/workflows')
    if not folder.is_dir():
        return []
    paths = []
    for path in sorted(folder.iterdir()):
        if path.suffix in ('.yml', '.yaml'):
            safe_path(root, str(path.relative_to(root)))
            if path.is_file():
                paths.append(str(path.relative_to(root)))
    return paths


def observe(client, root, d):
    """Fresh, read-only observations. Optional capabilities fail closed independently."""
    user = client.preflight()
    r = d['repository']
    base = f"repos/{r['owner']}/{r['name']}"
    repo = client.rest('GET', base)
    if norm(repo.get('full_name', '')) != norm(r['owner'] + '/' + r['name']):
        fail('REMOTE_CONFLICT', 'Repository identity changed or redirected.')
    fields = ('id', 'node_id', 'full_name', 'default_branch', 'allow_squash_merge',
              'allow_merge_commit', 'allow_rebase_merge', 'allow_auto_merge',
              'delete_branch_on_merge', 'permissions', 'owner', 'visibility')
    repository = {key: repo.get(key) for key in fields}
    repository['owner'] = {key: repo['owner'][key] for key in ('login', 'type')}
    branch = client.rest('GET', base + '/branches/' + quote(r['default_branch'], safe=''))
    sha = branch['commit']['sha']
    snapshot = {'repository': repository, 'revision': sha,
                'labels': client.pages(base + '/labels'), 'project': None, 'owner_id': None,
                'rulesets': [], 'effective_rules': [], 'checks': [], 'statuses': [],
                'local': {}, 'stack': {}, 'limits': [], 'publication': 'NOT_VALIDATED',
                'identity': {'gh_version': getattr(client, 'version', 'NOT_VALIDATED'),
                             'login': text_value(user['login']), 'repository_access': 'SUPPORTED',
                             'owner_type': repository['owner']['type']}}
    def optional(capability, action):
        try:
            return action()
        except GovernanceError as error:
            status = {'PLAN_LIMITATION': 'UNSUPPORTED_BY_PLAN', 'INSUFFICIENT_PERMISSION': 'NOT_AUTHORIZED'}.get(error.code, 'NOT_VALIDATED')
            snapshot['limits'].append(limitation(capability, str(error), status))
            return None
    if d['rules']['enabled']:
        rulesets = optional('rules', lambda: client.pages(base + '/rulesets')) or []
        for ruleset in rulesets:
            detail = optional('rules', lambda row=ruleset: client.rest('GET', base + '/rulesets/' + str(row['id'])))
            if detail:
                snapshot['rulesets'].append(detail)
        snapshot['effective_rules'] = optional('rules', lambda: client.pages(base + '/rules/branches/' + quote(r['default_branch'], safe=''))) or []
    if d['ci']['enabled']:
        checks = optional('ci', lambda: client.pages(base + '/commits/' + sha + '/check-runs', 'check_runs'))
        snapshot['checks'] = [{key: row.get(key) for key in ('id', 'name', 'head_sha', 'status', 'conclusion', 'app')} for row in checks or []]
        for row in snapshot['checks']:
            row['app'] = {'id': (row.get('app') or {}).get('id')}
        statuses = optional('ci', lambda: client.pages(base + '/commits/' + sha + '/statuses'))
        snapshot['statuses'] = [{key: row.get(key) for key in ('id', 'context', 'state')} for row in statuses or []]
    if d['project']['enabled']:
        def project_observation():
            kind = 'organization' if repo['owner']['type'] == 'Organization' else 'user'
            owner = client.graphql('query($login:String!){' + kind + '(login:$login){id}}', {'login': r['owner']})[kind]
            snapshot['owner_id'] = owner['id']
            projects = client.connection('query($login:String!,$cursor:String){' + kind + '(login:$login){projectsV2(first:100,after:$cursor){nodes{id number title closed url viewerCanUpdate} pageInfo{hasNextPage endCursor}}}}', {'login': r['owner']}, [kind, 'projectsV2'])
            matches = [p for p in projects if norm(p['title']) == norm(d['project']['title'])]
            if len(matches) > 1 or (matches and matches[0]['closed']):
                fail('REMOTE_CONFLICT', 'Project title is ambiguous or matches a closed Project.')
            if not matches:
                return None
            project = matches[0]
            if project.get('viewerCanUpdate') is not True:
                snapshot['limits'].append(limitation('project_write', 'Project read access does not grant update permission.', 'NOT_AUTHORIZED'))
            selections = {
                'fields': '... on ProjectV2Field{id name dataType} ... on ProjectV2SingleSelectField{id name dataType options{id name color description}} ... on ProjectV2IterationField{id name dataType}',
                'repositories': 'id nameWithOwner',
                'views': 'id name layout groupByFields(first:100){nodes{... on ProjectV2Field{id name} ... on ProjectV2SingleSelectField{id name}} pageInfo{hasNextPage endCursor}}',
                'workflows': 'id name enabled',
            }
            for name, selection in selections.items():
                project[name] = client.connection('query($id:ID!,$cursor:String){node(id:$id){... on ProjectV2{' + name + '(first:100,after:$cursor){nodes{' + selection + '} pageInfo{hasNextPage endCursor}}}}}', {'id': project['id']}, ['node', name])
            return project
        try:
            snapshot['project'] = project_observation()
        except GovernanceError as error:
            if error.code == 'REMOTE_CONFLICT':
                raise
            snapshot['limits'].append(limitation('project', str(error), 'NOT_AUTHORIZED' if error.code == 'INSUFFICIENT_PERMISSION' else 'NOT_VALIDATED'))
    artifacts, _ = local_artifacts(root, d)
    # Hash both inputs AND governed outputs. A lockfile/script edit invalidates approval.
    for name in sorted(set(REQUIRED_GOVERNANCE_FILES) | set(artifacts) | set(workflow_paths(root)) | {'.github/workflows/quality.yml'}):
        path = safe_path(root, name)
        snapshot['local'][name] = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    for name in STACK_INPUTS:
        path = safe_path(root, name)
        snapshot['stack'][name] = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    try:
        head = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], capture_output=True, text=True, timeout=10)
        dirty = subprocess.run(['git', '-C', str(root), 'status', '--porcelain', '--untracked-files=all'], capture_output=True, text=True, timeout=10)
        if head.returncode == dirty.returncode == 0 and head.stdout.strip() == sha and not dirty.stdout.strip():
            # Ignored generated/stack files are not protected by git status.
            matched = True
            for name in set(snapshot['local']) | set(snapshot['stack']):
                path = safe_path(root, name)
                if path.is_file():
                    blob = subprocess.run(['git', '-C', str(root), 'show', sha + ':' + name], capture_output=True, timeout=10)
                    if blob.returncode or blob.stdout != path.read_bytes():
                        matched = False
                        break
            if matched:
                snapshot['publication'] = 'MATCHED'
    except (OSError, subprocess.SubprocessError):
        pass
    # Stable collection ordering avoids false drift from API order alone.
    for key in ('labels', 'rulesets', 'effective_rules', 'checks', 'statuses'):
        snapshot[key].sort(key=canonical)
    return snapshot


def manual_evidence(evidence, capability, d, snapshot):
    """A manual observation is never inferred from acceptance of a limitation."""
    from datetime import date
    if not evidence:
        return False
    shape(evidence, ['schema_version', 'repository', 'revision', 'observations'])
    if evidence['schema_version'] != 1 or evidence['repository'] != d['repository']['owner'] + '/' + d['repository']['name'] or evidence['revision'] != snapshot['revision']:
        fail(message='Manual evidence must match the target and current branch revision.')
    if not isinstance(evidence['observations'], list):
        fail()
    found = False
    for entry in evidence['observations']:
        shape(entry, ['capability', 'result', 'observed_at', 'reference', 'action'])
        if entry['capability'] not in ('project_grouping', 'project_automation', 'rules') or entry['result'] != 'PASS':
            fail()
        text_value(entry['action'], 1000)
        if not isinstance(entry['reference'], str) or not re.fullmatch(r'https://github\.com/[A-Za-z0-9_./?#=&%-]+', entry['reference']):
            fail()
        try:
            age = (date.today() - date.fromisoformat(entry['observed_at'])).days
        except (ValueError, TypeError):
            fail()
        if not 0 <= age <= 7:
            fail(message='Manual evidence must be from the last seven days, not a future date.')
        if entry['capability'] == capability:
            found = True
    return found


def make_proposal(root, d, snapshot, evidence):
    validate_config(d)
    actions, limits = [], list(snapshot['limits'])
    r, repo = d['repository'], snapshot['repository']
    wanted = {'default_branch': r['default_branch'], 'allow_auto_merge': False,
              'delete_branch_on_merge': r['delete_branch_on_merge']}
    if r['squash_only']:
        wanted.update(allow_squash_merge=True, allow_merge_commit=False, allow_rebase_merge=False)
    changes = {key: value for key, value in wanted.items() if repo.get(key) != value}
    if changes:
        if not (repo.get('permissions') or {}).get('admin'):
            limits.append(limitation('repository_admin', 'Administrative settings require repository admin permission.', 'NOT_AUTHORIZED'))
        else:
            actions.append({'kind': 'settings', 'changes': changes})
    labels = [norm(row['name']) for row in snapshot['labels']]
    if len(set(labels)) != len(labels):
        fail('REMOTE_CONFLICT', 'Equivalent duplicate labels require manual reconciliation.')
    for name in d['labels']:
        if norm(name) not in labels:
            actions.append({'kind': 'label', 'name': name})
    artifacts, local_limits = local_artifacts(root, d)
    limits.extend(local_limits)
    for name, content in sorted(artifacts.items()):
        path = safe_path(root, name)
        old = path.read_text(encoding='utf-8') if path.is_file() else ''
        if not path.exists() or old != content:
            # Gitkeep is unnecessary if the existing directory already has contents.
            if name.endswith('/.gitkeep') and path.parent.is_dir() and any(path.parent.iterdir()):
                continue
            output_guard(old)
            hidden_old = ['[existing line omitted; inspect the local file before approval]\n'] * len(old.splitlines())
            actions.append({'kind': 'local_file', 'path': name, 'content': content,
                            'operation': 'UPDATE' if path.exists() else 'CREATE',
                            'before_sha256': hashlib.sha256(old.encode()).hexdigest() if path.is_file() else None,
                            'diff': ''.join(difflib.unified_diff(hidden_old, content.splitlines(True), fromfile=name, tofile=name))})
    project = snapshot['project']
    if d['project']['enabled'] and not any(x['capability'] == 'project' for x in limits):
        if project is None:
            actions.append({'kind': 'project_create', 'owner_id': snapshot['owner_id'], 'title': d['project']['title']})
            actions.append({'kind': 'project_link', 'project_id': '$created_project', 'repository_id': repo['node_id']})
            actions.append({'kind': 'status_bootstrap', 'project_id': '$created_project', 'names': STAGES})
            actions.append({'kind': 'view_create', 'project_id': '$created_project', 'name': d['project']['view_name']})
            limits.append(limitation('project_grouping', 'MANUAL_ACTION_REQUIRED: verify board grouping is Status after Project creation.'))
        else:
            fields = [f for f in project['fields'] if norm(f['name']) == 'status']
            if len(fields) != 1 or 'options' not in fields[0]:
                fail('REMOTE_CONFLICT', 'A unique single-select Status field is required.')
            field = fields[0]
            options = status_options(field['options'], STAGES)
            if options != field['options']:
                actions.append({'kind': 'status_options', 'field_id': field['id'], 'options': options})
            if not any(item['id'] == repo['node_id'] for item in project['repositories']):
                actions.append({'kind': 'project_link', 'project_id': project['id'], 'repository_id': repo['node_id']})
            views = [v for v in project['views'] if norm(v['name']) == norm(d['project']['view_name'])]
            if len(views) > 1:
                fail('REMOTE_CONFLICT', 'Ambiguous board views require manual reconciliation.')
            if not views:
                actions.append({'kind': 'view_create', 'project_id': project['id'], 'name': d['project']['view_name']})
            elif views[0]['layout'] != 'BOARD_LAYOUT':
                actions.append({'kind': 'view_update', 'view_id': views[0]['id']})
            grouping = views[0].get('groupByFields', {}) if views else {}
            grouped = any(item['id'] == field['id'] for item in grouping.get('nodes', [])) and not grouping.get('pageInfo', {}).get('hasNextPage', False)
            if not grouped:
                limits.append(limitation('project_grouping', 'MANUAL_ACTION_REQUIRED: set and verify board grouping to Status in Project settings.'))
        if not manual_evidence(evidence, 'project_automation', d, snapshot):
            limits.append(limitation('project_automation', 'MANUAL_ACTION_REQUIRED: configure Auto-add repo-specific is:issue is:open with Backlog; review/disable closed-item to Done automation; Done only after human merge. API does not expose enough configuration to certify this.'))
    check_names = {x['name'] for x in snapshot['checks']}
    check_names.update(x['context'] for x in snapshot['statuses'])
    if d['ci']['enabled']:
        if not d['ci']['required_checks']:
            limits.append(limitation('ci', 'MANUAL_ACTION_REQUIRED: observe CI then explicitly select actual required check names.'))
        elif set(d['ci']['required_checks']) - check_names:
            limits.append(limitation('ci', 'Required checks have not been observed at the current default-branch revision.'))
    if d['rules']['enabled'] and not any(x['capability'] == 'rules' for x in limits):
        required = {'deletion', 'non_fast_forward', 'pull_request'}
        actual = {x['type'] for x in snapshot['effective_rules']}
        sufficient = required <= actual
        prs = [x for x in snapshot['effective_rules'] if x['type'] == 'pull_request']
        sufficient = sufficient and any(x.get('parameters', {}).get('required_approving_review_count', -1) >= d['rules']['required_approvals'] and x.get('parameters', {}).get('dismiss_stale_reviews_on_push') is True and x.get('parameters', {}).get('required_review_thread_resolution') is True for x in prs)
        status_rules = [x for x in snapshot['effective_rules'] if x['type'] == 'required_status_checks']
        needed = set(d['ci']['required_checks'])
        observed = set().union(*[{c['context'] for c in x.get('parameters', {}).get('required_status_checks', [])} for x in status_rules]) if status_rules else set()
        sufficient = sufficient and needed <= observed and (not needed or any(x.get('parameters', {}).get('strict_required_status_checks_policy') for x in status_rules))
        # Binding a check to an integration prevents an unrelated app satisfying it.
        for name in needed:
            ids = {x['app']['id'] for x in snapshot['checks'] if x['name'] == name}
            if len(ids) > 1:
                fail('REMOTE_CONFLICT', 'Check name is emitted by multiple integrations.')
            if ids and None not in ids:
                sufficient = sufficient and any(c.get('integration_id') in ids and c['context'] == name for rule in status_rules for c in rule.get('parameters', {}).get('required_status_checks', []))
        relevant_ids = {rule.get('ruleset_id') for rule in snapshot['effective_rules'] if rule.get('ruleset_id') is not None}
        if any(row.get('bypass_actors') for row in snapshot['rulesets'] if row['id'] in relevant_ids):
            limits.append(limitation('rules_bypass', 'Applicable ruleset has bypass actors; enforcement is not universal. Review bypass policy manually before readiness.'))
        if not sufficient:
            if not (repo.get('permissions') or {}).get('admin'):
                limits.append(limitation('rules', 'Repository administration permission required.', 'NOT_AUTHORIZED'))
            elif d['ci']['enabled'] and (not needed or needed - check_names):
                limits.append(limitation('rules', 'Observe and approve actual CI check contexts before proposing rules.'))
            elif any(x.get('name') == 'Governed delivery' for x in snapshot['rulesets']):
                limits.append(limitation('rules', 'Existing managed ruleset differs; review exact remote configuration manually, never weaken it automatically.'))
            else:
                rules = [{'type': 'deletion'}, {'type': 'non_fast_forward'}, {'type': 'pull_request', 'parameters': {'dismiss_stale_reviews_on_push': True, 'require_code_owner_review': False, 'require_last_push_approval': False, 'required_approving_review_count': d['rules']['required_approvals'], 'required_review_thread_resolution': True}}]
                if needed:
                    checks = []
                    for name in sorted(needed):
                        ids = {x['app']['id'] for x in snapshot['checks'] if x['name'] == name}
                        if len(ids) > 1:
                            fail('REMOTE_CONFLICT', 'Check name is emitted by multiple integrations.')
                        item = {'context': name}
                        if ids and None not in ids:
                            item['integration_id'] = ids.pop()
                        checks.append(item)
                    rules.append({'type': 'required_status_checks', 'parameters': {'strict_required_status_checks_policy': True, 'required_status_checks': checks}})
                actions.append({'kind': 'ruleset_create', 'payload': {'name': 'Governed delivery', 'target': 'branch', 'enforcement': 'active', 'bypass_actors': [], 'conditions': {'ref_name': {'include': ['refs/heads/' + r['default_branch']], 'exclude': []}}, 'rules': rules}})
    return output_guard({'schema_version': VERSION, 'target': {'host': r['host'], 'repository': r['owner'] + '/' + r['name'], 'workspace': str(root.resolve())},
            'desired_hash': digest(d), 'snapshot_hash': digest(snapshot), 'evidence_hash': digest(evidence),
            'actions': actions, 'limits': limits, 'summary': 'CHANGES PROPOSED' if actions else 'NO CHANGE REQUIRED'})


def execute_action(client, root, d, action, created):
    r = d['repository']; base = f"repos/{r['owner']}/{r['name']}"
    kind = action['kind']
    if kind == 'local_file':
        safe_path(root, action['path'])
        parts = Path(action['path']).parts
        parent_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            for part in parts[:-1]:
                try:
                    os.mkdir(part, dir_fd=parent_fd)
                except FileExistsError:
                    pass
                child_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent_fd)
                os.close(parent_fd); parent_fd = child_fd
            flags = os.O_RDWR | os.O_NOFOLLOW
            if action['before_sha256'] is None:
                flags |= os.O_CREAT | os.O_EXCL
            fd = os.open(parts[-1], flags, 0o644, dir_fd=parent_fd)
            with os.fdopen(fd, 'r+b') as stream:
                if os.fstat(stream.fileno()).st_nlink > 1:
                    fail('LOCAL_CONFLICT', 'Hard-linked governed files require manual reconciliation.')
                before = hashlib.sha256(stream.read()).hexdigest()
                if action['before_sha256'] is not None and before != action['before_sha256']:
                    fail('LOCAL_CONFLICT', 'Local file changed after approval; no overwrite performed.')
                stream.seek(0); stream.write(action['content'].encode()); stream.truncate()
        finally:
            os.close(parent_fd)
        return
    if kind == 'settings':
        client.rest('PATCH', base, action['changes']); return
    if kind == 'label':
        client.rest('POST', base + '/labels', {'name': action['name'], 'color': 'ededed'}); return
    if kind == 'ruleset_create':
        client.rest('POST', base + '/rulesets', action['payload']); return
    if kind == 'project_create':
        result = client.graphql('mutation($input:CreateProjectV2Input!){createProjectV2(input:$input){projectV2{id}}}', {'input': {'ownerId': action['owner_id'], 'title': action['title']}})
        created['project_id'] = result['createProjectV2']['projectV2']['id']; return
    pid = created.get('project_id') if action.get('project_id') == '$created_project' else action.get('project_id')
    if kind == 'project_link':
        client.graphql('mutation($input:LinkProjectV2ToRepositoryInput!){linkProjectV2ToRepository(input:$input){repository{id}}}', {'input': {'projectId': pid, 'repositoryId': action['repository_id']}}); return
    if kind == 'status_bootstrap':
        fields = client.connection('query($id:ID!,$cursor:String){node(id:$id){... on ProjectV2{fields(first:100,after:$cursor){nodes{... on ProjectV2SingleSelectField{id name options{id name color description}} ... on ProjectV2Field{id name}} pageInfo{hasNextPage endCursor}}}}}', {'id': pid}, ['node', 'fields'])
        matches = [f for f in fields if norm(f['name']) == 'status' and 'options' in f]
        if len(matches) != 1:
            fail('REMOTE_CONFLICT', 'New Project does not expose an unambiguous Status field.')
        action = {'field_id': matches[0]['id'], 'options': status_options(matches[0]['options'], action['names'])}
        kind = 'status_options'
    if kind == 'status_options':
        client.graphql('mutation($input:UpdateProjectV2FieldInput!){updateProjectV2Field(input:$input){projectV2Field{... on ProjectV2SingleSelectField{id}}}}', {'input': {'fieldId': action['field_id'], 'singleSelectOptions': action['options']}}); return
    if kind == 'view_create':
        client.graphql('mutation($input:CreateProjectV2ViewInput!){createProjectV2View(input:$input){projectV2View{id}}}', {'input': {'projectId': pid, 'name': action['name'], 'layout': 'BOARD_LAYOUT'}}); return
    if kind == 'view_update':
        client.graphql('mutation($input:UpdateProjectV2ViewInput!){updateProjectV2View(input:$input){projectV2View{id}}}', {'input': {'viewId': action['view_id'], 'layout': 'BOARD_LAYOUT'}}); return
    fail(message='Unsupported action, no arbitrary commands can be executed.')


def apply_proposal(client, root, d, proposal, evidence, confirm):
    if not confirm:
        fail(message='USER_ACTION_REQUIRED: review proposal and pass --confirm explicitly.')
    snapshot = observe(client, root, d)
    expected = make_proposal(root, d, snapshot, evidence)
    if proposal != expected:
        fail('REMOTE_CONFLICT', 'Proposal, target or relevant state changed; generate and approve a new proposal.')
    blocking = [x for x in expected['limits'] if x['status'] == 'NOT_AUTHORIZED']
    if blocking:
        fail('INSUFFICIENT_PERMISSION', 'Resolve missing capabilities before applying this proposal.')
    if any(action['kind'] == 'local_file' for action in expected['actions']):
        if (not all(hasattr(os, flag) for flag in ('O_DIRECTORY', 'O_NOFOLLOW'))
                or os.open not in os.supports_dir_fd or os.mkdir not in os.supports_dir_fd):
            fail('LOCAL_CONFLICT', 'Secure local writes require POSIX directory-descriptor/no-follow primitives; no mutations were attempted. Windows is not validated.')
    completed, created = [], {}
    client.writable = True
    try:
        for index, action in enumerate(expected['actions']):
            execute_action(client, root, d, action, created)
            completed.append({'index': index, 'kind': action['kind']})
    except (GovernanceError, OSError, ValueError, KeyError, TypeError, AttributeError, IndexError) as error:
        return {'operation': 'apply', 'readiness': 'BLOCKED', 'status': 'PARTIAL' if completed else 'FAILED',
                'error': error.code if isinstance(error, GovernanceError) else 'VALIDATION_FAILED',
                'completed': completed, 'created_resources': created, 'next_step': 'Inspect partial state and generate a new proposal. No automatic rollback or retry.'}
    finally:
        client.writable = False
    return {'operation': 'apply', 'readiness': 'NOT_VALIDATED', 'status': 'APPLIED' if completed else 'NO CHANGE REQUIRED',
            'completed': completed, 'created_resources': created, 'identity': snapshot.get('identity', {}), 'next_step': 'Run verify for fresh evidence; apply never certifies readiness.'}


def verify(client, root, d, evidence):
    snapshot = observe(client, root, d)
    proposal = make_proposal(root, d, snapshot, evidence)
    limits = list(proposal['limits'])
    if snapshot.get('publication') != 'MATCHED':
        limits.append(limitation('publication', 'Local repository and governed/stack files are not proven identical to the remotely checked revision. Commit/publication requires separate human authorization.'))
    if d['ci']['enabled']:
        for name in d['ci']['required_checks']:
            checks = [x for x in snapshot['checks'] if x['name'] == name]
            statuses = [x for x in snapshot['statuses'] if x['context'] == name]
            passed = bool(checks) and all(x['head_sha'] == snapshot['revision'] and x['status'] == 'completed' and x['conclusion'] == 'success' for x in checks)
            if not checks and statuses:
                passed = max(statuses, key=lambda x: x['id'])['state'] == 'success'
            if not passed:
                limits.append(limitation('ci', 'Required CI context has no successful completed result at the current revision.'))
    accepted = {x['capability'] for x in d['exceptions']}
    unaccepted = [x for x in limits if not (x['capability'] == 'rules' and x['capability'] in accepted and x['status'] == 'UNSUPPORTED_BY_PLAN' and manual_evidence(evidence, 'rules', d, snapshot))]
    readiness = 'BLOCKED' if proposal['actions'] or unaccepted else ('READY_WITH_LIMITATIONS' if limits else 'READY')
    return {'operation': 'verify', 'readiness': readiness, 'verification': 'OBSERVED',
            'revision': snapshot['revision'], 'target': proposal['target'], 'identity': snapshot.get('identity', {}), 'pending_actions': len(proposal['actions']),
            'limits': limits, 'ci': 'NOT_APPLICABLE' if not d['ci']['enabled'] else 'OBSERVED',
            'codeowners': 'CODEOWNERS_FILE_PRESENT' if safe_path(root, '.github/CODEOWNERS').is_file() else 'MISSING',
            'production_authorized': False, 'manual_evidence_supplied': bool(evidence)}


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        print(json.dumps({'readiness': 'BLOCKED', 'error': 'VALIDATION_FAILED',
                          'message': 'Invalid CLI arguments. Run --help; input values are not echoed.'}))
        raise SystemExit(2)


def main(argv=None):
    parser = SafeParser(description=__doc__)
    parser.add_argument('operation', choices=('diagnose', 'propose', 'apply', 'verify'))
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--config', default='.github/governance.json')
    parser.add_argument('--proposal')
    parser.add_argument('--evidence')
    parser.add_argument('--confirm', action='store_true')
    args = parser.parse_args(argv)
    try:
        root = Path(args.workspace).absolute()
        if root.is_symlink() or root == Path(root.anchor) or root == Path.home() or not root.is_dir():
            fail('LOCAL_CONFLICT', 'Use an existing, dedicated repository workspace.')
        if root.resolve() != root:
            fail('LOCAL_CONFLICT', 'Workspace ancestors must not be symlinks.')
        result = subprocess.run(['git', '-C', str(root), 'rev-parse', '--show-toplevel'], capture_output=True, text=True, timeout=10)
        if result.returncode or Path(result.stdout.strip()).resolve() != root:
            fail('LOCAL_CONFLICT', 'Workspace must be the Git repository root.')
        d = validate_config(read_json(safe_path(root, args.config)))
        evidence = read_json(Path(args.evidence)) if args.evidence else {}
        client = GH(d['repository']['host'])
        if args.operation == 'apply':
            if not args.confirm or not args.proposal:
                fail(message='Apply requires --proposal and --confirm after human review.')
            output = apply_proposal(client, root, d, read_json(Path(args.proposal)), evidence, True)
        elif args.operation == 'verify':
            output = verify(client, root, d, evidence)
        else:
            snapshot = observe(client, root, d)
            proposal = make_proposal(root, d, snapshot, evidence)
            output = proposal if args.operation == 'propose' else {'operation': 'diagnose', 'readiness': 'NOT_VALIDATED',
                'target': proposal['target'], 'admin': bool((snapshot['repository'].get('permissions') or {}).get('admin')),
                'revision': snapshot['revision'], 'identity': snapshot.get('identity', {}), 'limits': proposal['limits'], 'pending_actions': len(proposal['actions'])}
        output_guard(output)
        print(json.dumps(output, indent=2, ensure_ascii=True))
        print(output.get('readiness', output.get('summary', 'COMPLETE')), file=sys.stderr)
        return 1 if output.get('readiness') in ('BLOCKED', 'AUTH_REQUIRED') else 0
    except GovernanceError as error:
        print(json.dumps({'operation': args.operation, 'readiness': 'AUTH_REQUIRED' if error.code == 'AUTH_REQUIRED' else 'BLOCKED', 'error': error.code, 'message': str(error)}))
        print(error.code, file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError, subprocess.SubprocessError):
        print(json.dumps({'operation': args.operation, 'readiness': 'BLOCKED', 'error': 'VALIDATION_FAILED', 'message': 'Input or observation could not be safely validated; raw details suppressed.'}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
