"""Behavioral acceptance for TASK-005. All mutating scenarios use temporary fixtures."""
import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'plugins/dev-environment-standard/skills/dev-environment-standard/scripts/environment.py'
SPEC = importlib.util.spec_from_file_location('environment_bootstrap', SCRIPT)
envmod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(envmod)


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value) if not isinstance(value, str) else value)


def mcp(identifier='core', tier='CORE', origin='OFFICIAL'):
    return {'id': identifier, 'name': identifier, 'provider': 'fixture', 'repository': 'https://example.org/provider', 'documentation': 'https://example.org/docs', 'tier': tier, 'origin': origin, 'capabilities': [identifier + '-capability'], 'preparation': {'policy': 'PROJECT_SCOPED', 'method': 'host_config', 'scope': 'host'}, 'configuration': {'transport': 'http', 'url': 'https://example.org/mcp'}, 'auth': {'required': True}, 'provenance': {'verified_at': '2026-09-23', 'source': 'https://example.org/provider'}}


class EnvironmentBootstrap(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'harness'
        self.workspace = Path(self.temp.name) / 'project'
        self.workspace.mkdir()
        self.config = self.workspace / '.mcp.json'
        self.env = envmod.Environment(self.root, self.workspace, self.workspace / 'runtime-state', 'claude', self.config)
        self.add_skill('dev-environment-standard')
        self.add_skill('future-specialist')
        self.entries = [mcp(), mcp('optional', 'OPTIONAL'), mcp('recommended', 'RECOMMENDED'), mcp('project', 'PROJECT_SPECIFIC'), mcp('community', 'COMMUNITY', 'COMMUNITY'), mcp('unknown', 'COMMUNITY', 'UNKNOWN'), mcp('node_repl', 'RUNTIME_PROVIDED', 'UNKNOWN')]
        self.entries[-1]['preparation'] = {'policy': 'RUNTIME_PROVIDED', 'method': 'runtime', 'scope': 'runtime'}
        self.save_library()
        write(self.root / '.gitignore', '**/runtime-state/\n')
        write(self.root / 'README.md', 'Environment & Capability Bootstrap\ndev-environment-standard\nREADME stale = NOT READY TO COMMIT\n')
        self.marketplaces()
        self.env.helper = Mock()
        self.env.helper.probe.return_value = None
        self.env.helper.cached.return_value = None
        self.env.helper.resolve_executable.side_effect = lambda cmd, workspace: shutil.which(cmd)
        self.env.helper.install.return_value = {'status': 'installed', 'installation_performed': True}
        self.env.runtimes = Mock(return_value={k: {'status': 'AVAILABLE', 'executable': sys.executable, 'version': '24.0.0'} for k in ('git', 'python', 'node')})

    def add_skill(self, name):
        plugin = self.root / 'plugins' / name
        skill = plugin / 'skills' / name
        write(skill / 'SKILL.md', f'---\nname: {name}\ndescription: fixture\n---\n# Fixture\n')
        write(skill / 'agents/openai.yaml', 'interface:\n  display_name: fixture\n')
        for rel in ('plugin.json', '.codex-plugin/plugin.json', '.claude-plugin/plugin.json'):
            write(plugin / rel, {'name': name})
        return skill

    def marketplaces(self):
        plugins = [{'name': p.name, 'source': './plugins/' + p.name} for p in (self.root / 'plugins').iterdir()]
        for rel in ('.agents/plugins/marketplace.json', '.claude-plugin/marketplace.json'):
            write(self.root / rel, {'plugins': plugins})

    def save_library(self):
        write(self.env.library_path, {'schema_version': 1, 'mcps': self.entries})

    def registry(self, name='future-specialist'):
        path = self.root / 'plugins' / name / 'skills' / name / 'references/tool-registry.json'
        write(path, {'schema_version': 1, 'owner': name, 'tools': [{'id': 'lint', 'command': 'lint', 'capabilities': ['lint-capability'], 'repository': 'https://example.org/lint', 'verify_args': ['--version'], 'install_policy': 'project-approved-dependency'}]})
        return path

    def evidence(self, entries, age=None):
        path = self.workspace / 'runtime-evidence.json'
        self.env.runtime_evidence = path
        write(path, {'schema_version': 1, 'host': 'claude', 'workspace': str(self.workspace), 'config_digest': envmod.digest(self.config), 'observed_at': age or envmod.now(), 'mcps': entries})

    def approval(self, component, **extra):
        action = next(p for p in self.env.prepare(selected=[component], dry_run=True)['plan'] if p['component'] == component)
        return dict({k: action[k] for k in ('component', 'command', 'scope')}, **extra)

    def snapshot(self):
        return {str(p.relative_to(self.temp.name)): p.read_bytes() for p in Path(self.temp.name).rglob('*') if p.is_file()}

    def test_01_new_skill_has_valid_structure(self):
        report = self.env.doctor()
        self.assertFalse(report['blockers'])
        self.assertIn('dev-environment-standard', report['skills'])

    def test_02_manifest_names_are_checked(self):
        report = self.env.doctor()
        self.assertTrue(all(c['result'] == 'PASS' for c in report['checks'] if c['check'].startswith('manifest:')))

    def test_03_marketplace_paths_and_completeness(self):
        write(self.root / '.agents/plugins/marketplace.json', {'plugins': [{'name': 'bad', 'source': '../other'}]})
        self.assertEqual(self.env.doctor()['plugin_health'], 'BLOCKED')

    def test_04_doctor_and_dry_run_never_write(self):
        self.registry()
        before = self.snapshot()
        self.env.doctor()
        self.env.prepare(selected=['optional'], dry_run=True)
        self.assertEqual(before, self.snapshot())
        self.env.helper.detect.assert_not_called()
        self.env.helper.install.assert_not_called()

    def test_05_prepare_configures_only_selected_and_approved(self):
        approval = self.approval('optional')
        report = self.env.prepare(selected=['optional'], approvals=[approval])
        self.assertEqual(set(json.loads(self.config.read_text())['mcpServers']), {'optional'})
        self.assertEqual([r['component'] for r in report['receipts'] if r['executed']], ['optional'])
        self.assertEqual(stat.S_IMODE(self.env.state_path.stat().st_mode), 0o600)

    def test_06_repair_limits_to_observed_broken_component(self):
        self.evidence({'optional': {'installed': True, 'connected': True}, 'recommended': {'connected': True}})
        self.env.prepare(selected=['optional', 'recommended'])
        self.evidence({'optional': {'broken': True}, 'recommended': {'connected': True}})
        report = self.env.prepare(component='optional', dry_run=True)
        self.assertEqual([p['component'] for p in report['plan']], ['optional'])
        with self.assertRaises(ValueError):
            self.env.prepare(component='recommended')

    def test_07_status_does_not_discover_or_install(self):
        self.env.prepare()
        self.env.discover = Mock(side_effect=AssertionError('full discovery forbidden'))
        self.env.runtimes = Mock(side_effect=AssertionError('runtime probes forbidden'))
        self.env.helper.probe.reset_mock()
        report = self.env.status()
        self.assertFalse(report['refresh_required'])
        self.env.helper.probe.assert_not_called()
        self.env.helper.install.assert_not_called()

    def test_08_new_skill_discovered_without_hardcoding(self):
        self.add_skill('brand-new-owner')
        self.marketplaces()
        self.assertIn('brand-new-owner', self.env.doctor()['skills'])

    def test_09_new_registry_discovered(self):
        self.registry()
        self.assertIn('lint', self.env.doctor()['skills']['future-specialist']['tools'])

    def test_10_environment_has_no_copy_of_owner_registry(self):
        self.registry()
        self.env.doctor()
        self.assertFalse((self.env.skill / 'references/tool-registry.json').exists())
        self.assertEqual(self.env.helper.probe.call_args.args[:2], ('future-specialist', 'lint'))

    def test_11_install_reuses_helper_and_lock_command(self):
        self.registry()
        write(self.workspace / 'uv.lock', 'version = 1')
        write(self.workspace / 'pyproject.toml', '[project]\ndependencies = ["lint>=1"]\n')
        component = 'tool:future-specialist:lint'
        approval = self.approval(component)
        report = self.env.prepare(selected=[component], approvals=[approval])
        self.env.helper.install.assert_called_once_with('future-specialist', 'lint', self.workspace, ['uv', 'sync', '--locked'], 'project-locked-dependencies', force_retry=False)
        self.assertTrue(any(r['result'] == 'VERIFIED' for r in report['receipts']))

    def test_12_library_schema_and_provenance_required(self):
        self.assertEqual(len(envmod.library(self.env.library_path)), 7)
        del self.entries[0]['provenance']
        self.save_library()
        with self.assertRaises(ValueError):
            envmod.library(self.env.library_path)

    def test_13_tiers_and_required_capabilities_route(self):
        report = self.env.prepare(required=['project-capability'], dry_run=True)
        self.assertEqual({p['component'] for p in report['plan']}, {'core', 'project'})
        self.assertIn('project', report['optional_choices'])

    def test_14_optional_never_implicitly_configured(self):
        report = self.env.prepare()
        self.assertEqual([p['component'] for p in report['plan']], ['core'])
        self.assertFalse(self.config.exists())

    def test_15_declined_optional_not_prompted_again(self):
        self.env.prepare(preferences={'optional': 'disabled', 'recommended': 'not_requested'})
        report = self.env.prepare()
        self.assertNotIn('optional', report['optional_choices'])
        self.assertNotIn('recommended', report['optional_choices'])

    def test_16_preferences_persist_across_instances(self):
        self.env.prepare(preferences={'optional': 'enabled'})
        new = envmod.Environment(self.root, self.workspace, self.env.state_path.parent, 'claude', self.config)
        self.assertEqual(new.state()['mcp_preferences']['optional'], 'enabled')

    def test_17_custom_stays_private(self):
        entry = {'id': 'company', 'name': 'Company', 'provider': 'Company', 'repository': 'https://example.org/company', 'documentation': 'https://example.org/docs', 'capabilities': ['internal-search'], 'maintainer': 'team', 'installation': 'manual', 'transport': 'http', 'permissions': ['read'], 'authentication': 'host-managed', 'risks': ['internal-data'], 'origin': 'UNKNOWN'}
        path = self.workspace / 'custom.json'
        write(path, {'custom_mcps': [entry]})
        before = self.env.library_path.read_bytes()
        parsed = envmod.custom_entries(path, envmod.library(self.env.library_path))
        self.env.prepare(custom=parsed)
        self.assertEqual(self.env.state()['custom_mcps'], [entry])
        self.assertFalse(self.env.prepare()['custom_mcp_question'])
        self.assertEqual(before, self.env.library_path.read_bytes())
        self.evidence({'company': {'connected': True, 'authenticated': True}})
        report = self.env.doctor(['internal-search'])
        self.assertEqual(report['mcps']['company']['status'], 'CONNECTED')
        self.assertNotIn('required-capability:internal-search', report['blockers'])

    def test_18_unknown_never_configures_even_approved(self):
        report = self.env.prepare(selected=['unknown'], approvals=[self.approval('unknown')])
        receipt = next(r for r in report['receipts'] if r['component'] == 'unknown')
        self.assertEqual(receipt['result'], 'USER_ACTION_REQUIRED')
        self.assertFalse(self.config.exists())

    def test_19_community_needs_specific_confirmation(self):
        approval = self.approval('community')
        self.env.prepare(selected=['community'], approvals=[approval])
        self.assertFalse(self.config.exists())
        approval['community_confirmed'] = True
        self.env.prepare(selected=['community'], approvals=[approval])
        self.assertIn('community', json.loads(self.config.read_text())['mcpServers'])

    def test_20_installed_does_not_imply_connected(self):
        self.evidence({'core': {'installed': True}})
        item = self.env.doctor()['mcps']['core']
        self.assertEqual(item['status'], 'INSTALLED')
        self.assertFalse(item['connected'])

    def test_21_connected_does_not_imply_authenticated(self):
        self.evidence({'core': {'connected': True}})
        report = self.env.doctor(['core-capability'])
        self.assertEqual(report['mcps']['core']['status'], 'CONNECTED')
        self.assertFalse(report['mcps']['core']['authenticated'])
        self.assertIn('required-capability:core-capability', report['blockers'])

    def test_22_auth_handoff_is_observed_not_invented(self):
        self.assertEqual(self.env.doctor()['mcps']['core']['authentication'], 'NOT_OBSERVED')
        self.evidence({'core': {'connected': True, 'auth_required': True}})
        item = self.env.doctor()['mcps']['core']
        self.assertEqual(item['status'], 'AUTH_REQUIRED')

    def test_23_runtime_only_never_installs(self):
        report = self.env.prepare(selected=['node_repl'], approvals=[self.approval('node_repl')])
        self.assertFalse(any(r['executed'] for r in report['receipts']))
        self.evidence({'node_repl': {'available': True}})
        self.assertEqual(self.env.doctor()['mcps']['node_repl']['status'], 'AVAILABLE')

    def test_24_secrets_rejected_and_no_config_disclosure(self):
        for secret in ({'token': 'private'}, {'url': 'https://user:pass@example.org'}, {'url': 'https://example.org?token=private'}, {'args': ['Authorization: Bearer private']}):
            with self.subTest(secret=next(iter(secret))):
                with self.assertRaises(ValueError):
                    envmod.safe(secret)
        write(self.config, {'mcpServers': {'core': {'env': {'PRIVATE_TOKEN': 'SYNTHETIC_DO_NOT_COPY'}}}})
        self.assertNotIn('SYNTHETIC_DO_NOT_COPY', json.dumps(self.env.doctor()))

    def test_25_state_ignored_by_real_repository(self):
        result = subprocess.run(['git', 'check-ignore', '--no-index', 'plugins/dev-environment-standard/skills/dev-environment-standard/runtime-state/environment-state.json'], cwd=ROOT, capture_output=True)
        self.assertEqual(result.returncode, 0)

    def test_26_fingerprint_invalidates_changed_host_config(self):
        self.env.prepare()
        write(self.config, {'mcpServers': {}})
        self.assertTrue(self.env.status()['refresh_required'])

    def test_27_broken_manifest_blocks_health(self):
        write(self.root / 'plugins/future-specialist/plugin.json', '{bad')
        self.assertEqual(self.env.doctor()['plugin_health'], 'BLOCKED')

    def test_28_invalid_registry_blocks_health(self):
        path = self.registry()
        write(path, {'schema_version': 1, 'owner': 'other', 'tools': []})
        self.assertIn('registry:future-specialist', self.env.doctor()['blockers'])

    def test_29_missing_reference_blocks_health(self):
        path = self.root / 'plugins/future-specialist/skills/future-specialist/SKILL.md'
        path.write_text(path.read_text() + '\n[missing](references/missing.md)\n')
        self.assertTrue(any(b.startswith('reference:') for b in self.env.doctor()['blockers']))

    def test_30_readme_gate_remains_enforced(self):
        write(self.root / 'README.md', 'stale README')
        self.assertIn('readme-architecture', self.env.doctor()['blockers'])
        self.assertIn('NOT READY TO COMMIT', (ROOT / 'README.md').read_text())

    def test_stale_runtime_evidence_is_not_reused(self):
        self.evidence({'core': {'connected': True, 'authenticated': True}}, '2000-01-01T00:00:00+00:00')
        self.assertEqual(self.env.doctor()['mcps']['core']['status'], 'MISSING')

    def test_registered_is_not_installed(self):
        write(self.config, {'mcpServers': {'core': {'url': 'https://example.org'}}})
        item = self.env.doctor()['mcps']['core']
        self.assertTrue(item['registered'])
        self.assertFalse(item['installed'])
        self.assertEqual(item['status'], 'MISSING')

    def test_invalid_state_recovers_conservatively(self):
        write(self.env.state_path, '{broken')
        before = self.env.state_path.read_bytes()
        self.assertTrue(self.env.status()['refresh_required'])
        self.assertEqual(before, self.env.state_path.read_bytes())

    def test_status_current_auth_failure_blocks_required_capability(self):
        self.evidence({'core': {'connected': True, 'authenticated': True}})
        validation = self.workspace / 'validation.json'
        write(validation, {'schema_version': 1, 'fingerprint': self.env.fingerprint(), 'observed_at': envmod.now(), 'checks': [{'command': 'fixture-tests', 'exit_code': 0, 'result': 'PASS'}]})
        self.env.validation_evidence = validation
        self.env.prepare(required=['core-capability'])
        self.assertTrue(self.env.status(['core-capability'])['ready'])
        self.evidence({'core': {'auth_required': True}})
        self.assertFalse(self.env.status(['core-capability'])['ready'])

    def test_lockfile_commands_and_conflicts(self):
        for filename, command in [('package-lock.json', ['npm', 'ci']), ('pnpm-lock.yaml', ['pnpm', 'install', '--frozen-lockfile']), ('uv.lock', ['uv', 'sync', '--locked'])]:
            with self.subTest(lockfile=filename):
                path = self.workspace / filename
                write(path, '{}')
                self.assertEqual(self.env.dependency_plan()['command'], command)
                path.unlink()
        write(self.workspace / 'package-lock.json', '{}')
        write(self.workspace / 'pnpm-lock.yaml', '{}')
        with self.assertRaises(ValueError):
            self.env.dependency_plan()

    def test_dependency_install_is_real_scoped_and_exit_retained(self):
        write(self.workspace / 'package-lock.json', '{}')
        approval = self.approval('project:dependencies')
        with patch.object(envmod.subprocess, 'run', return_value=subprocess.CompletedProcess([], 7)) as execute:
            report = self.env.prepare(selected=['project:dependencies'], approvals=[approval])
        execute.assert_called_once_with(['npm', 'ci'], cwd=self.workspace, capture_output=True, timeout=300, check=False)
        self.assertEqual(next(r for r in report['receipts'] if r['component'] == 'project:dependencies')['exit_code'], 7)

    def test_approval_scope_and_command_are_exact(self):
        approval = self.approval('optional')
        approval['scope'] = '/different-project'
        self.env.prepare(selected=['optional'], approvals=[approval])
        self.assertFalse(self.config.exists())
        approval = self.approval('optional')
        approval['command'].append('arbitrary')
        self.env.prepare(selected=['optional'], approvals=[approval])
        self.assertFalse(self.config.exists())

    def test_codex_append_preserves_existing_configuration(self):
        self.env.host = 'codex'
        self.env.config = self.workspace / 'config.toml'
        write(self.env.config, 'model = "example"\n[mcp_servers.existing]\nurl = "https://example.org"\n')
        before = self.env.config.read_text()
        self.env.prepare(selected=['optional'], approvals=[self.approval('optional')])
        self.assertTrue(self.env.config.read_text().startswith(before))
        self.assertIn('[mcp_servers.optional]', self.env.config.read_text())

    def test_absent_test_evidence_never_healthy(self):
        self.assertEqual(self.env.doctor()['plugin_health'], 'DEGRADED')
        self.assertIn({'check': 'tests-and-validators', 'result': 'NOT VALIDATED'}, self.env.doctor()['checks'])

    def test_browser_preparation_selects_exactly_one(self):
        executable = self.workspace / 'node_modules/.bin/playwright'
        write(executable, '# fixture')
        approval = self.approval('browser:firefox')
        with patch.object(envmod.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0)) as execute:
            self.env.prepare(selected=['browser:firefox'], approvals=[approval])
        self.assertEqual(execute.call_args.args[0], [str(executable), 'install', 'firefox'])

    def test_symlink_state_cannot_overwrite_external_file(self):
        target = self.workspace / 'protected'
        write(target, 'preserve')
        self.env.state_path.parent.mkdir()
        self.env.state_path.symlink_to(target)
        with self.assertRaises(ValueError):
            self.env.prepare()
        self.assertEqual(target.read_text(), 'preserve')

    def test_cli_error_does_not_echo_secret(self):
        path = self.workspace / 'preferences.json'
        write(path, {'token': 'SYNTHETIC_DO_NOT_ECHO'})
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = envmod.main(['prepare', '--repo-root', str(self.root), '--workspace', str(self.workspace), '--preferences', str(path), '--json'])
        self.assertEqual(code, 2)
        self.assertNotIn('SYNTHETIC_DO_NOT_ECHO', output.getvalue())

    def test_expired_snapshot_cannot_be_ready_or_rejuvenated(self):
        self.env.prepare()
        state = json.loads(self.env.state_path.read_text())
        state['snapshot']['observed_at'] = '2000-01-01T00:00:00+00:00'
        write(self.env.state_path, state)
        report = self.env.status()
        self.assertFalse(report['ready'])
        self.assertTrue(report['refresh_required'])

    def test_source_changes_invalidate_validation_evidence(self):
        fingerprint = self.env.fingerprint()
        write(self.root / 'tests/example.py', 'assert True\n')
        self.assertNotEqual(self.env.fingerprint(), fingerprint)
        fingerprint = self.env.fingerprint()
        write(self.root / 'tests/example.py', 'assert False\n')
        self.assertNotEqual(self.env.fingerprint(), fingerprint)

    def test_cli_credentials_and_basic_auth_are_rejected(self):
        for value in ('npx example --token abcdef0123456789', 'Basic dXNlcjpwYXNz', 'https://example.org#token=secret', 'tool --api-key abcdef'):
            with self.subTest(value=value[:10]):
                with self.assertRaises(ValueError):
                    envmod.safe(value)

    def test_owner_policy_cannot_be_replaced_by_project_policy(self):
        path = self.registry()
        data = json.loads(path.read_text())
        data['tools'][0]['install_policy'] = 'PRIVILEGED'
        write(path, data)
        write(self.workspace / 'package-lock.json', '{}')
        write(self.workspace / 'package.json', {'devDependencies': {'lint': '1.0.0'}})
        component = 'tool:future-specialist:lint'
        report = self.env.prepare(selected=[component], approvals=[self.approval(component)])
        item = next(p for p in report['plan'] if p['component'] == component)
        self.assertEqual(item['owner_install_policy'], 'PRIVILEGED')
        self.assertEqual(item['action'], 'OWNER_APPROVAL_REQUIRED')
        self.env.helper.install.assert_not_called()

    def test_tool_must_be_declared_before_locked_dependency_restore(self):
        self.registry()
        write(self.workspace / 'package-lock.json', '{}')
        write(self.workspace / 'package.json', {'devDependencies': {'other': '1.0.0'}})
        component = 'tool:future-specialist:lint'
        report = self.env.prepare(selected=[component], approvals=[self.approval(component)])
        self.assertEqual(next(r for r in report['receipts'] if r['component'] == component)['result'], 'OWNER_APPROVAL_REQUIRED')

    def test_community_tier_requires_confirmation_independent_of_origin(self):
        next(e for e in self.entries if e['id'] == 'community')['origin'] = 'VERIFIED_THIRD_PARTY'
        self.save_library()
        report = self.env.prepare(selected=['community'], approvals=[self.approval('community')])
        self.assertEqual(next(r for r in report['receipts'] if r['component'] == 'community')['result'], 'COMMUNITY_CONFIRMATION_REQUIRED')
        self.assertFalse(self.config.exists())

    def test_chrome_system_install_requires_human_action(self):
        write(self.workspace / 'node_modules/.bin/playwright', 'fixture')
        report = self.env.prepare(selected=['browser:chrome'], approvals=[self.approval('browser:chrome')])
        receipt = next(r for r in report['receipts'] if r['component'] == 'browser:chrome')
        self.assertEqual(receipt['policy'], 'PRIVILEGED')
        self.assertEqual(receipt['result'], 'USER_ACTION_REQUIRED')

    def test_structurally_broken_plugin_blocks_installation(self):
        approval = self.approval('optional')
        write(self.root / 'plugins/future-specialist/plugin.json', '{bad')
        report = self.env.prepare(selected=['optional'], approvals=[approval])
        self.assertEqual(next(r for r in report['receipts'] if r['component'] == 'optional')['result'], 'BLOCKED_INVALID_ENVIRONMENT')
        self.assertFalse(self.config.exists())

    def test_ignored_optional_offer_is_not_repeated(self):
        self.assertIn('optional', self.env.prepare()['optional_choices'])
        self.assertNotIn('optional', self.env.prepare()['optional_choices'])
        self.assertEqual(self.env.state()['mcp_preferences']['optional'], 'not_requested')

    def test_failed_generic_install_is_blocked_and_not_retried(self):
        write(self.workspace / 'package-lock.json', '{}')
        approval = self.approval('project:dependencies')
        with patch.object(envmod.subprocess, 'run', return_value=subprocess.CompletedProcess([], 9)) as execute:
            report = self.env.prepare(selected=['project:dependencies'], approvals=[approval])
            again = self.env.prepare(selected=['project:dependencies'], approvals=[approval])
        self.assertEqual(execute.call_count, 1)
        self.assertEqual(report['plugin_health'], 'BLOCKED')
        self.assertFalse(self.env.status()['ready'])
        self.assertEqual(next(r for r in again['receipts'] if r['component'] == 'project:dependencies')['result'], 'RETRY_DEFERRED')

    def test_healthy_core_does_not_require_every_optional_mcp(self):
        self.evidence({'core': {'connected': True, 'authenticated': True}})
        path = self.workspace / 'validation.json'
        write(path, {'schema_version': 1, 'fingerprint': self.env.fingerprint(), 'observed_at': envmod.now(), 'checks': [{'command': 'fixture-tests', 'exit_code': 0, 'result': 'PASS'}]})
        self.env.validation_evidence = path
        self.assertEqual(self.env.doctor()['plugin_health'], 'HEALTHY')

    def test_catalog_is_not_a_connected_server(self):
        self.entries[1]['kind'] = 'catalog'
        self.save_library()
        self.evidence({'optional': {'connected': True, 'authenticated': True}})
        observed = self.env.doctor()['mcps']['optional']
        self.assertEqual(observed['status'], 'UNSUPPORTED')
        self.assertFalse(observed['connected'])

    def test_missing_optional_runtime_does_not_force_rediscovery(self):
        self.env.runtimes.return_value['docker'] = {'status': 'MISSING', 'executable': None, 'version': None}
        self.env.prepare()
        self.assertFalse(self.env.status()['refresh_required'])

    def test_not_validated_environment_is_never_ready(self):
        self.env.prepare()
        report = self.env.status()
        self.assertFalse(report['ready'])
        self.assertTrue(report['capabilities_ready'])

    def test_expired_validation_evidence_invalidates_status(self):
        self.env.prepare()
        state = json.loads(self.env.state_path.read_text())
        state['snapshot']['validation_observed_at'] = '2000-01-01T00:00:00+00:00'
        next(c for c in state['snapshot']['checks'] if c['check'] == 'tests-and-validators')['result'] = 'PASS'
        write(self.env.state_path, state)
        report = self.env.status()
        self.assertTrue(report['refresh_required'])
        self.assertFalse(report['ready'])

    def test_successful_generic_install_is_not_repeated_before_verification(self):
        write(self.workspace / 'package-lock.json', '{}')
        approval = self.approval('project:dependencies')
        with patch.object(envmod.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0)) as execute:
            self.env.prepare(selected=['project:dependencies'], approvals=[approval])
            again = self.env.prepare(selected=['project:dependencies'], approvals=[approval])
        self.assertEqual(execute.call_count, 1)
        self.assertEqual(next(r for r in again['receipts'] if r['component'] == 'project:dependencies')['result'], 'VERIFICATION_REQUIRED')
        self.assertFalse(self.env.status()['ready'])
        self.env.prepare()
        self.assertIn('VERIFICATION_REQUIRED', [r['result'] for r in self.env.state()['snapshot']['receipts']])
        self.assertFalse(self.env.status()['ready'])

    def test_community_consent_requires_boolean_true(self):
        for value in ('false', 'true', 1):
            approval = self.approval('community', community_confirmed=value)
            report = self.env.prepare(selected=['community'], approvals=[approval])
            self.assertEqual(next(r for r in report['receipts'] if r['component'] == 'community')['result'], 'COMMUNITY_CONFIRMATION_REQUIRED')
        self.assertFalse(self.config.exists())

    def test_connected_without_authentication_has_handoff(self):
        self.evidence({'core': {'connected': True}})
        report = self.env.prepare(required=['core-capability'], dry_run=True)
        self.assertEqual(next(r for r in report['receipts'] if r['component'] == 'core')['result'], 'USER_ACTION_REQUIRED')

    def test_manager_detection_does_not_select_every_manager(self):
        report = self.env.doctor()
        self.assertEqual(set(report['package_managers']), {'pip', 'pipx', 'uv', 'npm', 'npx', 'pnpm', 'yarn'})
        self.assertFalse(any(m['selected_by_lockfile'] for m in report['package_managers'].values()))

    def test_manual_component_recovery_requires_new_explicit_validation(self):
        write(self.workspace / 'package-lock.json', '{}')
        self.evidence({'core': {'connected': True, 'authenticated': True}})
        approval = self.approval('project:dependencies')
        with patch.object(envmod.subprocess, 'run', return_value=subprocess.CompletedProcess([], 9)):
            self.env.prepare(selected=['project:dependencies'], approvals=[approval])
        self.env.prepare()
        self.assertFalse(self.env.status()['ready'])
        validation = self.workspace / 'validation.json'
        write(validation, {'schema_version': 1, 'fingerprint': self.env.fingerprint(), 'observed_at': envmod.now(), 'checks': [{'command': 'fixture verifies repaired dependency tree', 'component': 'project:dependencies', 'exit_code': 0, 'result': 'PASS'}]})
        self.env.validation_evidence = validation
        with patch.object(envmod.subprocess, 'run', side_effect=AssertionError('must not reinstall')):
            report = self.env.prepare()
        receipt = next(r for r in report['receipts'] if r['component'] == 'project:dependencies')
        self.assertEqual(receipt['result'], 'VERIFIED_EXTERNALLY')
        self.assertTrue(self.env.status()['ready'])


if __name__ == '__main__':
    unittest.main()
