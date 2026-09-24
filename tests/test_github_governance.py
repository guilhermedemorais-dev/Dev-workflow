"""Offline behavioral tests. No GitHub authentication/network is used."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import os
import subprocess
import sys
from unittest.mock import patch
from copy import deepcopy

STAGES = ['Backlog', 'Discovery / SDD', 'Ready for Dev', 'In Progress',
          'Validation', 'In Review', 'Awaiting Final Approval', 'Done']


def module():
    if not HELPER.exists():
        raise AssertionError('governance helper missing')
    spec = importlib.util.spec_from_file_location('github_governance', HELPER)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def config():
    return {'schema_version': 1,
            'repository': {'host': 'github.com', 'owner': 'example', 'name': 'app',
                           'default_branch': 'main', 'agent_branch_prefix': 'agent/',
                           'squash_only': True, 'delete_branch_on_merge': True},
            'project': {'enabled': True, 'title': 'App Delivery', 'statuses': STAGES,
                        'view_name': 'Delivery'},
            'labels': ['bug', 'feature', 'blocked'],
            'human_gates': {'task': True, 'pr': True, 'merge': True, 'deploy': True},
            'automation': {'auto_merge': False, 'auto_deploy': False, 'max_rework_cycles': 3},
            'local': {'generate': True, 'codeowners': ['@example']},
            'ci': {'enabled': True, 'required_checks': []},
            'rules': {'enabled': True, 'required_approvals': 0}, 'exceptions': []}


class GovernanceBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.g = module()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_03_validate_schema_and_forbid_auto_merge(self):
        desired = config()
        self.g.validate_config(desired)
        desired['automation']['auto_merge'] = True
        with self.assertRaises(self.g.GovernanceError):
            self.g.validate_config(desired)

    def test_04_runtime_ids_and_unknown_keys_rejected(self):
        desired = config()
        desired['project']['id'] = 'PVT_not_configuration'
        with self.assertRaises(self.g.GovernanceError):
            self.g.validate_config(desired)

    def test_05_status_preserves_ids_and_custom_options(self):
        old = [{'id': 'observed-9', 'name': ' backlog ', 'color': 'RED', 'description': 'old'},
               {'id': 'custom', 'name': 'Parked', 'color': 'GRAY', 'description': ''}]
        got = self.g.status_options(old, STAGES)
        self.assertEqual(got[:2], old)
        self.assertEqual(len(got), 9)
        self.assertEqual(got[2]['name'], 'Discovery / SDD')
        self.assertNotIn('id', got[2])

    def test_06_duplicate_status_is_conflict(self):
        with self.assertRaises(self.g.GovernanceError):
            self.g.status_options([{'name': 'Backlog'}, {'name': ' backlog '}], STAGES)

    def test_07_safe_path_rejects_traversal(self):
        with self.assertRaises(self.g.GovernanceError):
            self.g.safe_path(self.root, '../outside')

    def test_08_safe_path_rejects_symlinks(self):
        (self.root / '.github').symlink_to(self.root.parent, target_is_directory=True)
        with self.assertRaises(self.g.GovernanceError):
            self.g.safe_path(self.root, '.github/CODEOWNERS')

    def test_09_ci_only_uses_existing_node_scripts(self):
        (self.root / 'package.json').write_text(json.dumps({'scripts': {'test': 'node test.js'}}))
        (self.root / 'package-lock.json').write_text('{}')
        (self.root / '.nvmrc').write_text('22.14.0')
        artifacts, limitations = self.g.local_artifacts(self.root, config())
        workflow = artifacts['.github/workflows/quality.yml']
        self.assertIn('npm ci', workflow)
        self.assertIn('npm run test', workflow)
        self.assertNotIn('npm run lint', workflow)

    def test_10_unknown_stack_no_invented_workflow(self):
        artifacts, limitations = self.g.local_artifacts(self.root, config())
        self.assertNotIn('.github/workflows/quality.yml', artifacts)
        self.assertIn('ci_stack', [item['capability'] for item in limitations])

    def test_11_gh_absent_is_classified(self):
        with patch('shutil.which', return_value=None):
            with self.assertRaises(self.g.GovernanceError) as caught:
                self.g.GH('github.com').preflight()
        self.assertEqual(caught.exception.code, 'GH_MISSING')

    def test_12_readonly_guard_rejects_mutations(self):
        client = self.g.GH('github.com')
        with self.assertRaises(self.g.GovernanceError):
            client.rest('PATCH', 'repos/example/app', {})
        with self.assertRaises(self.g.GovernanceError):
            client.graphql('mutation { createProjectV2(input:{}) { clientMutationId } }')

    def test_13_unknown_403_not_plan_limitation(self):
        err = self.g.api_error('gh: Forbidden (HTTP 403) secret-ghp_xyz', 1)
        self.assertEqual(err.code, 'INSUFFICIENT_PERMISSION')
        self.assertNotIn('secret', str(err))
        self.assertNotIn('ghp_', str(err))

    def test_14_explicit_plan_failure_classified(self):
        err = self.g.api_error('Upgrade to GitHub Pro or make this repository public to enable this feature (HTTP 403)', 1)
        self.assertEqual(err.code, 'PLAN_LIMITATION')

    def test_15_rest_pagination_exceeds_first_page(self):
        class Fake(self.g.GH):
            def rest(self, method, endpoint, payload=None):
                if '&page=1' in endpoint:
                    return [{'id': i} for i in range(100)]
                return [{'id': 100}]
        self.assertEqual(len(Fake('github.com').pages('repos/a/b/labels')), 101)

    def test_16_apply_requires_confirmation_before_any_observation(self):
        with self.assertRaises(self.g.GovernanceError):
            self.g.apply_proposal(None, self.root, config(), {}, {}, False)

    def test_17_disabled_project_requires_reason(self):
        desired = config()
        desired['project']['enabled'] = False
        with self.assertRaises(self.g.GovernanceError):
            self.g.validate_config(desired)

    def test_18_branch_injection_rejected(self):
        desired = config()
        desired['repository']['default_branch'] = 'main; touch /tmp/pwn'
        with self.assertRaises(self.g.GovernanceError):
            self.g.validate_config(desired)

    def snapshot(self):
        return {'repository': {'id': 11, 'node_id': 'R_observed', 'full_name': 'example/app',
                               'default_branch': 'main', 'allow_squash_merge': True,
                               'allow_merge_commit': False, 'allow_rebase_merge': False,
                               'allow_auto_merge': False, 'delete_branch_on_merge': True,
                               'permissions': {'admin': True}, 'owner': {'login': 'example', 'type': 'User'}},
                'revision': 'a' * 40, 'labels': [{'id': 1, 'name': 'BUG'}],
                'project': None, 'owner_id': 'U_observed', 'rulesets': [],
                'effective_rules': [], 'checks': [], 'statuses': [],
                'local': {}, 'stack': {}, 'limits': []}

    def test_19_proposal_missing_labels_only_and_no_writes(self):
        snapshot = self.snapshot()
        proposal = self.g.make_proposal(self.root, config(), snapshot, {})
        creates = [a['name'] for a in proposal['actions'] if a['kind'] == 'label']
        self.assertEqual(creates, ['feature', 'blocked'])
        self.assertEqual(list(self.root.iterdir()), [])

    def test_20_proposal_target_binding(self):
        proposal = self.g.make_proposal(self.root, config(), self.snapshot(), {})
        self.assertEqual(proposal['target']['repository'], 'example/app')
        self.assertEqual(proposal['target']['workspace'], str(self.root))
        self.assertEqual(len(proposal['snapshot_hash']), 64)

    def test_21_tampered_actions_never_execute(self):
        snapshot = self.snapshot()
        proposal = self.g.make_proposal(self.root, config(), snapshot, {})
        proposal['actions'].append({'kind': 'run', 'command': 'touch stolen'})
        with patch.object(self.g, 'observe', return_value=snapshot):
            with self.assertRaises(self.g.GovernanceError):
                self.g.apply_proposal(None, self.root, config(), proposal, {}, True)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_22_remote_drift_never_executes(self):
        snapshot = self.snapshot()
        proposal = self.g.make_proposal(self.root, config(), snapshot, {})
        changed = deepcopy(snapshot)
        changed['labels'].append({'id': 2, 'name': 'feature'})
        with patch.object(self.g, 'observe', return_value=changed):
            with self.assertRaises(self.g.GovernanceError) as caught:
                self.g.apply_proposal(None, self.root, config(), proposal, {}, True)
        self.assertEqual(caught.exception.code, 'REMOTE_CONFLICT')

    def test_23_stack_input_changes_invalidate_proposal(self):
        snapshot = self.snapshot()
        snapshot['stack']['package.json'] = 'oldhash'
        proposal = self.g.make_proposal(self.root, config(), snapshot, {})
        changed = deepcopy(snapshot)
        changed['stack']['package.json'] = 'newhash'
        with patch.object(self.g, 'observe', return_value=changed):
            with self.assertRaises(self.g.GovernanceError):
                self.g.apply_proposal(None, self.root, config(), proposal, {}, True)

    def test_24_no_admin_blocks_settings(self):
        snapshot = self.snapshot()
        snapshot['repository']['permissions']['admin'] = False
        snapshot['repository']['allow_merge_commit'] = True
        proposal = self.g.make_proposal(self.root, config(), snapshot, {})
        self.assertNotIn('settings', [x['kind'] for x in proposal['actions']])
        self.assertIn('repository_admin', [x['capability'] for x in proposal['limits']])

    def test_25_existing_project_uses_dynamic_id_and_preserves_status(self):
        snapshot = self.snapshot()
        snapshot['project'] = {'id': 'PVT_dynamic', 'number': 72, 'title': 'App Delivery',
            'fields': [{'id': 'FIELD_dynamic', 'name': 'Status', 'options': [
                {'id': 'OPT_dynamic', 'name': 'Backlog', 'color': 'GREEN', 'description': 'existing'}]}],
            'repositories': [], 'views': [], 'workflows': []}
        proposal = self.g.make_proposal(self.root, config(), snapshot, {})
        self.assertNotIn('project_create', [a['kind'] for a in proposal['actions']])
        update = next(a for a in proposal['actions'] if a['kind'] == 'status_options')
        self.assertEqual(update['field_id'], 'FIELD_dynamic')
        self.assertEqual(update['options'][0]['id'], 'OPT_dynamic')

    def test_26_verify_missing_checks_never_ready(self):
        snapshot = self.snapshot()
        with patch.object(self.g, 'observe', return_value=snapshot):
            result = self.g.verify(None, self.root, config(), {})
        self.assertNotEqual(result['readiness'], 'READY')

    def test_27_graphql_cursor_pagination_dedupes(self):
        class Fake(self.g.GH):
            def graphql(self, query, variables=None):
                second = variables.get('cursor') == 'next'
                return {'node': {'items': {'nodes': [{'id': 'one'}, {'id': 'two'}] if second else [{'id': 'one'}],
                    'pageInfo': {'hasNextPage': not second, 'endCursor': None if second else 'next'}}}}
        self.assertEqual(len(Fake('github.com').connection('query {}', {}, ['node', 'items'])), 2)

    def test_28_node_missing_runtime_version_requires_manual_decision(self):
        (self.root / 'package.json').write_text(json.dumps({'scripts': {'test': 'node test.js'}}))
        (self.root / 'package-lock.json').write_text('{}')
        artifacts, limits = self.g.local_artifacts(self.root, config())
        self.assertNotIn('.github/workflows/quality.yml', artifacts)
        self.assertTrue(limits)

    def test_29_generated_actions_are_full_sha_pinned(self):
        (self.root / 'go.mod').write_text('module example.com/example\n\ngo 1.24.0\n')
        artifacts, _ = self.g.local_artifacts(self.root, config())
        import re
        uses = re.findall(r'uses: (\S+)', artifacts['.github/workflows/quality.yml'])
        self.assertTrue(uses)
        self.assertTrue(all(re.fullmatch(r'[\w-]+/[\w-]+@[a-f0-9]{40}', x) for x in uses))

    def test_30_auth_error_does_not_echo_raw_credentials(self):
        class Fake(self.g.GH):
            def run(self, args, payload=None):
                if args == ['--version']:
                    return 'gh version 2.80.0 (date)'
                raise self_outer.g.GovernanceError('API_UNAVAILABLE', 'ghp_SYNTHETIC_SECRET')
        self_outer = self
        with patch('shutil.which', return_value='/fake/gh'):
            with self.assertRaises(self.g.GovernanceError) as caught:
                Fake('github.com').preflight()
        self.assertEqual(caught.exception.code, 'AUTH_REQUIRED')
        self.assertNotIn('SYNTHETIC', str(caught.exception))

    def ready_case(self):
        desired = config()
        desired['project'].update(enabled=False, reason='Approved no-board fixture')
        desired['rules'].update(enabled=False, reason='Approved isolated fixture')
        desired['ci'].update(enabled=False, reason='Approved documentation-only fixture')
        snapshot = self.snapshot()
        snapshot['labels'] = [{'id': i, 'name': name} for i, name in enumerate(desired['labels'])]
        snapshot['publication'] = 'MATCHED'
        artifacts, _ = self.g.local_artifacts(self.root, desired)
        for name, content in artifacts.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        return desired, snapshot

    def test_31_ready_only_fresh_complete_observations(self):
        desired, snapshot = self.ready_case()
        with patch.object(self.g, 'observe', return_value=snapshot):
            self.assertEqual(self.g.verify(None, self.root, desired, {})['readiness'], 'READY')

    def test_32_unpublished_local_changes_deny_ready(self):
        desired, snapshot = self.ready_case()
        snapshot['publication'] = 'NOT_VALIDATED'
        with patch.object(self.g, 'observe', return_value=snapshot):
            self.assertEqual(self.g.verify(None, self.root, desired, {})['readiness'], 'BLOCKED')

    def test_33_unknown_rules_cannot_be_waived(self):
        desired, snapshot = self.ready_case()
        desired['rules']['enabled'] = True
        desired['exceptions'] = [{'capability': 'rules', 'reason': 'approved manual fallback'}]
        snapshot['limits'] = [self.g.limitation('rules', 'API unavailable')]
        with patch.object(self.g, 'observe', return_value=snapshot):
            self.assertEqual(self.g.verify(None, self.root, desired, {})['readiness'], 'BLOCKED')

    def test_34_diff_never_emits_secret_from_existing_files(self):
        (self.root / 'CONTRIBUTING.md').write_text('credential: ghp_SYNTHETIC_SECRET_DO_NOT_PRINT\n')
        with self.assertRaises(self.g.GovernanceError) as caught:
            self.g.make_proposal(self.root, config(), self.snapshot(), {})
        self.assertNotIn('SYNTHETIC', str(caught.exception))

    def test_35_existing_workflow_preserved_and_no_unknown_stack_blocker(self):
        folder = self.root / '.github/workflows'
        folder.mkdir(parents=True)
        (folder / 'custom.yaml').write_text('name: Custom\njobs: {}\n')
        artifacts, limits = self.g.local_artifacts(self.root, config())
        self.assertNotIn('.github/workflows/quality.yml', artifacts)
        self.assertNotIn('ci_stack', [x['capability'] for x in limits])

    def test_36_apply_failure_stops_and_reports_completed_actions(self):
        desired, snapshot = self.ready_case()
        snapshot['labels'] = []
        proposal = self.g.make_proposal(self.root, desired, snapshot, {})
        class Client:
            writable = False
            calls = 0
            def rest(inner, method, endpoint, payload):
                inner.calls += 1
                if inner.calls == 2:
                    raise self.g.GovernanceError('API_UNAVAILABLE')
        client = Client()
        with patch.object(self.g, 'observe', return_value=snapshot):
            result = self.g.apply_proposal(client, self.root, desired, proposal, {}, True)
        self.assertEqual(result['status'], 'PARTIAL')
        self.assertEqual(len(result['completed']), 1)
        self.assertEqual(client.calls, 2)
        self.assertFalse(client.writable)

    def test_37_noop_apply_is_idempotent_and_not_ready(self):
        desired, snapshot = self.ready_case()
        proposal = self.g.make_proposal(self.root, desired, snapshot, {})
        self.assertEqual(proposal['actions'], [])
        class Client:
            writable = False
        with patch.object(self.g, 'observe', return_value=snapshot):
            result = self.g.apply_proposal(Client(), self.root, desired, proposal, {}, True)
        self.assertEqual(result['status'], 'NO CHANGE REQUIRED')
        self.assertEqual(result['readiness'], 'NOT_VALIDATED')

    def test_38_malformed_api_row_fails_safely(self):
        class Client(self.g.GH):
            def rest(self, *args, **kwargs):
                return ['malformed-row']
        with self.assertRaises(self.g.GovernanceError):
            Client('github.com').pages('repos/a/b/labels')

    def test_39_wrong_config_type_is_governance_error(self):
        desired = config()
        desired['ci'] = []
        with self.assertRaises(self.g.GovernanceError):
            self.g.validate_config(desired)

    def test_40_removed_file_lines_not_reflected_even_unknown_secret_format(self):
        (self.root / 'CONTRIBUTING.md').write_text('confidential arbitrary CANARY-no-standard-prefix\n')
        plan = self.g.make_proposal(self.root, config(), self.snapshot(), {})
        self.assertNotIn('CANARY', json.dumps(plan))
        change = next(x for x in plan['actions'] if x.get('path') == 'CONTRIBUTING.md')
        self.assertIn('before_sha256', change)

    def test_41_weak_rules_not_mistaken_for_enforcement(self):
        desired, snapshot = self.ready_case()
        desired['rules']['enabled'] = True
        snapshot['effective_rules'] = [{'type': 'deletion'}, {'type': 'non_fast_forward'},
            {'type': 'pull_request', 'parameters': {'required_approving_review_count': 0,
            'dismiss_stale_reviews_on_push': False, 'required_review_thread_resolution': False}}]
        plan = self.g.make_proposal(self.root, desired, snapshot, {})
        self.assertIn('ruleset_create', [x['kind'] for x in plan['actions']])

    def test_42_write_time_precondition_preserves_concurrent_local_edit(self):
        path = self.root / 'CONTRIBUTING.md'
        path.write_text('approved original')
        action = {'kind': 'local_file', 'path': 'CONTRIBUTING.md', 'content': 'replacement',
                  'before_sha256': self.g.hashlib.sha256(path.read_bytes()).hexdigest()}
        path.write_text('concurrent user edit')
        with self.assertRaises(self.g.GovernanceError):
            self.g.execute_action(None, self.root, config(), action, {})
        self.assertEqual(path.read_text(), 'concurrent user edit')

    def test_43_real_cli_fake_gh_readonly_apply_and_idempotency(self):
        workspace = self.root / 'repo'
        workspace.mkdir()
        fakebin = self.root / 'bin'
        fakebin.mkdir()
        statefile, logfile = self.root / 'state.json', self.root / 'calls.jsonl'
        statefile.write_text(json.dumps({'labels': [], 'malformed': False}))
        fake = fakebin / 'gh'
        fake.write_text('''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
a=sys.argv[1:]
statepath=Path(os.environ['FAKE_STATE'])
state=json.loads(statepath.read_text())
with open(os.environ['FAKE_LOG'], 'a') as log: log.write(json.dumps(a)+'\\n')
if a==['--version']: print('gh version 2.80.0 (fixture)'); sys.exit()
if a[:2]==['auth','status']: sys.exit()
if a[0]!='api': sys.exit(3)
method=a[a.index('--method')+1]
endpoint=a[a.index('--method')+2]
payload=json.loads(sys.stdin.read()) if '--input' in a else None
base='repos/example/app'
if endpoint=='user': out={'login':'fixture-user'}
elif endpoint==base:
 out={'id':11,'node_id':'R_fixture','full_name':'example/app','default_branch':'main',
 'allow_squash_merge':True,'allow_merge_commit':False,'allow_rebase_merge':False,
 'allow_auto_merge':False,'delete_branch_on_merge':True,'permissions':{'admin':True},
 'owner':{'login':'example','type':'User'},'visibility':'private'}
elif '/branches/' in endpoint: out={'commit':{'sha':os.environ['FAKE_SHA']}}
elif '/labels' in endpoint:
 if method=='POST':
  out={'id':len(state['labels'])+1,'name':payload['name']}
  state['labels'].append(out); statepath.write_text(json.dumps(state))
 else: out=['malformed-row'] if state['malformed'] else state['labels']
else: sys.stderr.write('unexpected call'); sys.exit(3)
print(json.dumps(out))
''')
        fake.chmod(0o755)
        desired = config()
        for key in ('project', 'rules', 'ci'):
            desired[key].update(enabled=False, reason='Approved isolated fixture')
        (workspace / '.github').mkdir()
        (workspace / '.github/governance.json').write_text(json.dumps(desired))
        for command in (['git', 'init', '-b', 'main', str(workspace)],
                        ['git', '-C', str(workspace), 'add', '.'],
                        ['git', '-C', str(workspace), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.test', 'commit', '-m', 'fixture']):
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        sha = subprocess.check_output(['git', '-C', str(workspace), 'rev-parse', 'HEAD'], text=True).strip()
        env = dict(os.environ, PATH=str(fakebin) + os.pathsep + os.environ['PATH'], FAKE_STATE=str(statefile), FAKE_LOG=str(logfile), FAKE_SHA=sha)
        def call(operation, *options):
            result = subprocess.run([sys.executable, str(HELPER), operation, '--workspace', str(workspace), *options], capture_output=True, text=True, env=env)
            self.assertNotIn('Traceback', result.stderr)
            return result, json.loads(result.stdout)
        for operation in ('diagnose', 'propose', 'verify'):
            before = {str(p.relative_to(workspace)): p.read_bytes() for p in workspace.rglob('*') if p.is_file()}
            result, output = call(operation)
            after = {str(p.relative_to(workspace)): p.read_bytes() for p in workspace.rglob('*') if p.is_file()}
            self.assertEqual(before, after)
            if operation == 'propose':
                plan = output
        calls = [json.loads(x) for x in logfile.read_text().splitlines()]
        self.assertTrue(all('--method' not in x or x[x.index('--method')+1]=='GET' for x in calls))
        proposal = self.root / 'proposal.json'
        proposal.write_text(json.dumps(plan))
        result, output = call('apply', '--proposal', str(proposal))
        self.assertEqual(result.returncode, 1)
        result, output = call('apply', '--proposal', str(proposal), '--confirm')
        self.assertEqual(result.returncode, 0, output)
        self.assertEqual(output['status'], 'APPLIED')
        self.assertEqual(output['readiness'], 'NOT_VALIDATED')
        self.assertEqual(len(json.loads(statefile.read_text())['labels']), 3)
        result, plan = call('propose')
        self.assertEqual(plan['actions'], [])
        proposal.write_text(json.dumps(plan))
        result, output = call('apply', '--proposal', str(proposal), '--confirm')
        self.assertEqual(output['status'], 'NO CHANGE REQUIRED')
        state = json.loads(statefile.read_text()); state['malformed'] = True
        statefile.write_text(json.dumps(state))
        result, output = call('diagnose')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(output['error'], 'API_UNAVAILABLE')

    def test_44_invalid_cli_never_echoes_input(self):
        result = subprocess.run([sys.executable, str(HELPER), 'ghp_SYNTHETIC_CLI_SECRET'], capture_output=True, text=True)
        self.assertNotIn('SYNTHETIC', result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['error'], 'VALIDATION_FAILED')

    def test_45_disabling_generation_does_not_waive_required_files(self):
        desired = config()
        desired['local']['generate'] = False
        desired['ci'].update(enabled=False, reason='No CI fixture')
        artifacts, limits = self.g.local_artifacts(self.root, desired)
        self.assertEqual(artifacts, {})
        self.assertIn('local_governance', [x['capability'] for x in limits])

    def test_46_disabled_generation_still_hashes_and_checks_ignored_governance(self):
        desired = config()
        desired['labels'] = []
        for key in ('project', 'rules', 'ci'):
            desired[key].update(enabled=False, reason='Isolated approved fixture')
        artifacts, _ = self.g.local_artifacts(self.root, desired)
        for name, content in artifacts.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        desired['local']['generate'] = False
        (self.root / '.github/governance.json').write_text(json.dumps(desired))
        (self.root / '.gitignore').write_text('CONTRIBUTING.md\n')
        for command in (['git', 'init', '-b', 'main', str(self.root)],
                        ['git', '-C', str(self.root), 'add', '.'],
                        ['git', '-C', str(self.root), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.test', 'commit', '-m', 'fixture']):
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        sha = subprocess.check_output(['git', '-C', str(self.root), 'rev-parse', 'HEAD'], text=True).strip()
        (self.root / 'CONTRIBUTING.md').write_text('Ignored content absent from the checked revision')
        repo = self.snapshot()['repository']
        class Fake:
            version = '2.80.0'
            def preflight(inner):
                return {'login': 'fixture'}
            def rest(inner, method, endpoint):
                return {'commit': {'sha': sha}} if '/branches/' in endpoint else repo
            def pages(inner, endpoint):
                return []
        observed = self.g.observe(Fake(), self.root, desired)
        self.assertIn('CONTRIBUTING.md', observed['local'])
        self.assertEqual(observed['publication'], 'NOT_VALIDATED')
        result = self.g.verify(Fake(), self.root, desired, {})
        self.assertEqual(result['readiness'], 'BLOCKED')
        self.assertIn('publication', [x['capability'] for x in result['limits']])

    def test_47_unsupported_local_write_platform_blocks_before_remote_mutations(self):
        desired, snapshot = self.ready_case()
        (self.root / 'CONTRIBUTING.md').unlink()
        snapshot['labels'] = []
        proposal = self.g.make_proposal(self.root, desired, snapshot, {})
        class Fake:
            writable = False
            calls = 0
            def rest(inner, *args):
                inner.calls += 1
                return {}
        client = Fake()
        with patch.object(self.g, 'observe', return_value=snapshot), patch.object(self.g.os, 'supports_dir_fd', set()):
            with self.assertRaises(self.g.GovernanceError):
                self.g.apply_proposal(client, self.root, desired, proposal, {}, True)
        self.assertEqual(client.calls, 0)
        self.assertFalse(client.writable)

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / 'plugins/devops-standard/skills/devops-standard/scripts/github_governance.py'


class GovernanceBootstrapTests(unittest.TestCase):
    def test_01_helper_exists(self):
        self.assertTrue(HELPER.is_file(), 'approved governance executor is missing')

    def test_02_template_has_no_runtime_identifiers(self):
        path = HELPER.parent.parent / 'templates/github-governance.json'
        self.assertTrue(path.is_file(), 'desired-state template is missing')
        desired = json.loads(path.read_text())
        self.assertEqual(desired['schema_version'], 1)
        self.assertEqual(len(desired['project']['statuses']), 8)
        self.assertFalse(desired['automation']['auto_merge'])
        self.assertFalse(desired['automation']['auto_deploy'])


if __name__ == '__main__':
    unittest.main()
