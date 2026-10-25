"""Portable routing tests do not certify a mocked operating system."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('platform_environment', ROOT / 'plugins/dev-environment-standard/skills/dev-environment-standard/scripts/environment.py')
envmod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(envmod)


class PlatformRouting(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'harness'
        shutil.copytree(ROOT / 'plugins/dev-environment-standard', self.root / 'plugins/dev-environment-standard', ignore=shutil.ignore_patterns('__pycache__', 'runtime-state'))
        for catalog in (self.root / 'plugins/dev-environment-standard').glob('Tools */catalog.json'):
            for tool in json.loads(catalog.read_text(encoding='utf-8'))['tools']:
                target = self.root / tool['path']
                if not target.exists():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text('# fixture\n', encoding='utf-8')
        self.env = envmod.Environment(self.root, self.root, self.root / 'runtime-state')

    def catalog(self, system='Linux'):
        return self.root / 'plugins/dev-environment-standard' / f'Tools ({system})' / 'catalog.json'

    def mutate(self, change):
        path = self.catalog()
        data = json.loads(path.read_text(encoding='utf-8'))
        change(data)
        path.write_text(json.dumps(data), encoding='utf-8')

    def test_each_platform_selects_its_folder_and_windows_mac_fail_closed(self):
        for platform, folder in [('linux', 'Linux'), ('win32', 'Windows'), ('darwin', 'macOS')]:
            with self.subTest(platform=platform), patch.object(sys, 'platform', platform), patch.object(envmod.shutil, 'which', return_value=None):
                route = self.env.platform_tools()
                self.assertTrue(route['selected_folder'].endswith(f'Tools ({folder})'))
                self.assertEqual(len(route['tools']), 14)  # original 11 plus three opt-in cinematic helpers
                if platform != 'linux':
                    self.assertFalse(any(t['eligible'] for t in route['tools'] if t['validation'] != 'WINDOWS_SUITE'))
        with patch.object(sys, 'platform', 'freebsd'):
            self.assertEqual(self.env.platform_tools()['tools'], [])

    def test_binding_reused_but_runtime_catalog_and_source_drift_invalidate(self):
        with patch.object(sys, 'platform', 'linux'):
            first = self.env.platform_tools()
            self.assertTrue(self.env.platform_tools(first)['reused'])
            with patch.dict('os.environ', {'TOOL_RUNTIME_ID': 'container-new'}):
                self.assertFalse(self.env.platform_tools(first)['reused'])
            with patch.object(envmod.platform, 'release', return_value='changed'):
                self.assertFalse(self.env.platform_tools(first)['reused'])
            with patch.object(sys, 'executable', 'new-python'):
                self.assertFalse(self.env.platform_tools(first)['reused'])
            self.mutate(lambda d: d.update(evidence_revision='changed'))
            self.assertFalse(self.env.platform_tools(first)['reused'])
            current = self.env.platform_tools()
            (self.root / current['tools'][0]['path']).write_text('# changed\n', encoding='utf-8')
            self.assertFalse(self.env.platform_tools(current)['reused'])

    def test_insufficient_python_blocks_only_affected_tools(self):
        with patch.object(sys, 'platform', 'linux'), patch.object(sys, 'version_info', (3, 10)):
            route = self.env.platform_tools()
            self.assertFalse(any(t['eligible'] for t in route['tools'] if t['runtime'] == 'Python'))
            self.assertTrue(any(t['reason'] == 'Python runtime below required minimum' for t in route['tools']))

    def test_malformed_traversal_duplicate_and_false_platform_never_eligible(self):
        changes = [lambda d: d['tools'][0].update(path='../outside.py'),
                   lambda d: d['tools'][0].update(path='plugins/dev-workflow-standard/../outside.py'),
                   lambda d: d['tools'][0].update(path='C:\\outside.py'),
                   lambda d: d['tools'].append(copy.deepcopy(d['tools'][0])),
                   lambda d: d.update(system='Windows'),
                   lambda d: d['tools'][0].update(validation='PASS'),
                   lambda d: d.update(validation='PASS'),
                   lambda d: d['tools'][0].update(runtime='ArbitraryShell')]
        original = self.catalog().read_text(encoding='utf-8')
        with patch.object(sys, 'platform', 'linux'):
            for change in changes:
                self.catalog().write_text(original, encoding='utf-8')
                self.mutate(change)
                self.assertEqual(self.env.platform_tools()['tools'], [])

    def test_owner_symlink_escape_is_rejected(self):
        outside = Path(self.tmp.name) / 'outside'
        outside.mkdir()
        (outside / 'tool.py').write_text('# outside', encoding='utf-8')
        owner = self.root / 'plugins/escaped-owner'
        try:
            owner.symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest('OS disallows unprivileged symlink creation')
        self.mutate(lambda d: d['tools'][0].update(owner='escaped-owner', path='plugins/escaped-owner/tool.py'))
        with patch.object(sys, 'platform', 'linux'):
            self.assertEqual(self.env.platform_tools()['tools'], [])

    def test_interpreter_stat_drift_invalidates_without_subprocess_probe(self):
        executable = self.root / 'node-fixture'
        executable.write_bytes(b'old')
        with patch.object(sys, 'platform', 'linux'), patch.object(envmod.shutil, 'which', return_value=str(executable)), patch.object(envmod.subprocess, 'run', side_effect=AssertionError('probe called')):
            first = self.env.platform_tools()
            executable.write_bytes(b'new executable')
            self.assertFalse(self.env.platform_tools(first)['reused'])

    def test_generated_dependencies_do_not_change_normative_fingerprint(self):
        before = self.env.fingerprint()
        dependency = self.root / 'plugins/dev-workflow-standard/node_modules/fixture/generated.js'
        dependency.parent.mkdir(parents=True)
        dependency.write_text('generated dependency', encoding='utf-8')
        self.assertEqual(self.env.fingerprint(), before)
        dependency.write_text('updated generated dependency', encoding='utf-8')
        self.assertEqual(self.env.fingerprint(), before)
        script = self.root / 'plugins/dev-workflow-standard/scripts/tool-state.py'
        script.write_text('# source changed', encoding='utf-8')
        self.assertNotEqual(self.env.fingerprint(), before)

    def test_verified_windows_route_requires_matching_platform_evidence(self):
        path = self.catalog('Windows')
        data = json.loads(path.read_text(encoding='utf-8'))
        data['validation'] = 'WINDOWS_SUITE'
        data['tools'][0]['validation'] = 'WINDOWS_SUITE'
        data['tools'][1]['validation'] = 'LINUX_SUITE'
        path.write_text(json.dumps(data), encoding='utf-8')
        with patch.object(sys, 'platform', 'win32'), patch.object(envmod.shutil, 'which', return_value=None):
            route = self.env.platform_tools()
            self.assertTrue(route['tools'][0]['eligible'])
            self.assertFalse(route['tools'][1]['eligible'])

    def test_prepare_persists_selection_once_and_status_reuses_it(self):
        with patch.object(sys, 'platform', 'linux'):
            route = self.env.platform_tools()
            report = {'schema_version': 1, 'operation': 'doctor', 'observed_at': envmod.now(),
                      'runtimes': {}, 'mcps': {}, 'skills': {}, 'blockers': [], 'checks': [],
                      'watched': {str(p.relative_to(self.root)): envmod.digest(p) for p in self.env.source_paths()},
                      'platform_tools': route, 'plugin_health': 'DEGRADED'}
            with patch.object(self.env, 'doctor', return_value=report), patch.object(self.env, 'catalog', return_value={}), patch.object(self.env, 'plan', return_value=[]), patch.object(self.env, 'mcp_status', return_value=({}, None)):
                self.env.prepare(dry_run=True)
                self.assertFalse(self.env.state_path.exists())
                self.env.prepare()
                stored = self.env.state_path.read_bytes()
                result = self.env.status()
                self.assertTrue(result['platform_tools']['reused'])
                self.assertEqual(self.env.state_path.read_bytes(), stored)
                self.assertFalse(any(b.startswith('platform') for b in result['blockers']))

    def test_absent_catalog_does_not_invalidate_external_health_but_loss_does(self):
        with patch.object(sys, 'platform', 'linux'):
            valid = self.env.platform_tools()
            self.catalog().unlink()
            missing = self.env.platform_tools()
            report = {'schema_version': 1, 'observed_at': envmod.now(), 'runtimes': {},
                      'mcps': {}, 'skills': {}, 'blockers': [], 'checks': [],
                      'watched': {str(p.relative_to(self.root)): envmod.digest(p) for p in self.env.source_paths()},
                      'plugin_health': 'DEGRADED'}
            report['fingerprint'] = self.env.fingerprint()
            state = {'snapshot': report, 'fingerprint': report['fingerprint'], 'platform_tools': missing}
            with patch.object(self.env, 'state', return_value=state), patch.object(self.env, 'catalog', return_value={}), patch.object(self.env, 'mcp_status', return_value=({}, None)):
                self.assertFalse(self.env.status()['refresh_required'])
                self.assertTrue(self.env.status()['capabilities_ready'])
                state['platform_tools'] = valid
                self.assertTrue(self.env.status()['refresh_required'])

    def test_status_returns_persisted_selection_without_doctor_or_writes(self):
        with patch.object(sys, 'platform', 'linux'):
            route = self.env.platform_tools()
            with patch.object(self.env, 'state', return_value={'platform_tools': route}), patch.object(self.env, 'doctor', side_effect=AssertionError('doctor called')):
                report = self.env.status()
                self.assertTrue(report['platform_tools']['reused'])
                self.assertFalse(self.env.state_path.exists())

    def test_catalog_inventory_covers_only_authored_entrypoints(self):
        expected = {p.relative_to(ROOT).as_posix() for p in envmod.Environment(ROOT).source_paths() if p.is_file() and p.is_relative_to(ROOT / 'plugins') and p.suffix in ('.py', '.mjs', '.sh') and 'vendor' not in p.parts and p.read_bytes().startswith(b'#!')}
        for system in ('Linux', 'Windows', 'macOS'):
            data = json.loads((ROOT / 'plugins/dev-environment-standard' / f'Tools ({system})' / 'catalog.json').read_text(encoding='utf-8'))
            self.assertEqual({t['path'] for t in data['tools']}, expected)


if __name__ == '__main__':
    unittest.main()
