"""Combined PR23/PR25 behavior with real catalogs/helper and isolated CLI fixtures."""

import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'plugins/dev-environment-standard/skills/dev-environment-standard/scripts/environment.py'
SPEC = importlib.util.spec_from_file_location('environment_devops_integration', SCRIPT)
environment = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(environment)


class EnvironmentDevOpsIntegration(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'harness'
        self.workspace = self.base / 'project'
        self.workspace.mkdir()
        shutil.copytree(ROOT / 'plugins', self.root / 'plugins',
                        ignore=shutil.ignore_patterns('runtime-state', '__pycache__'))
        for relative in ('README.md', '.gitignore', 'docs/workflow-pipeline.md', '.agents/plugins/marketplace.json',
                         '.claude-plugin/marketplace.json'):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        self.bin = self.base / 'bin'
        self.bin.mkdir()
        for command in ('git', 'python3'):
            self.fixture(command)
        # No real infrastructure executable or inherited external state is reachable.
        scoped_env = {key: value for key, value in os.environ.items()
                      if key not in ('TOOL_REGISTRY_PATH', 'TOOL_STATE_PATH')}
        scoped_env.update(PATH=str(self.bin), PYTHONDONTWRITEBYTECODE='1')
        self.environ = patch.dict(os.environ, scoped_env, clear=True)
        self.environ.start()
        self.addCleanup(self.environ.stop)
        self.env = environment.Environment(self.root, self.workspace,
            self.workspace / 'runtime-state', 'claude', self.workspace / '.mcp.json')
        self.tools = self.env.tools()
        self.install = patch.object(self.tools, 'install',
                                   side_effect=AssertionError('unexpected installation'))
        self.install.start()
        self.addCleanup(self.install.stop)

    def fixture(self, command, directory=None):
        target = (directory or self.bin) / command
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('#!/bin/sh\necho 1.2.3\n')
        target.chmod(0o755)
        return target

    def snapshot(self):
        return {str(path.relative_to(self.base)): path.read_bytes()
                for path in self.base.rglob('*') if path.is_file()}

    def test_real_twenty_tool_registry_is_discovered_read_only(self):
        before = self.snapshot()
        report = self.env.doctor()
        devops = report['skills']['devops-standard']
        self.assertEqual(report['blockers'], [])
        self.assertEqual(devops['status'], 'INSPECTED')
        self.assertEqual(len(devops['tools']), 20)
        self.assertEqual(devops['tools']['git']['status'], 'INSTALLED')
        self.assertEqual(len(devops['missing_tools']), 19)
        self.assertEqual(before, self.snapshot())
        self.assertFalse(any(m['connected'] or m['authenticated'] for m in report['mcps'].values()))
        self.assertNotEqual(report['plugin_health'], 'HEALTHY')

    def test_all_selected_missing_devops_tools_remain_owner_gated_even_with_approval(self):
        report = self.env.doctor()
        selected = ['tool:devops-standard:' + name
                    for name in report['skills']['devops-standard']['missing_tools']]
        plan = self.env.prepare(selected=selected, dry_run=True)['plan']
        approvals = [{key: action[key] for key in ('component', 'command', 'scope')}
                     for action in plan if action['component'] in selected]
        report = self.env.prepare(selected=selected, approvals=approvals)
        receipts = [r for r in report['receipts'] if r['component'] in selected]
        self.assertEqual(len(receipts), 19)
        self.assertTrue(all(r['result'] == 'OWNER_APPROVAL_REQUIRED' for r in receipts))
        self.assertTrue(all(not r['executed'] and r['command'] == [] for r in receipts))
        self.assertFalse(self.env.config.exists())
        self.assertFalse(any(m['authenticated'] for m in report['mcps'].values()))

    def test_required_devops_capability_uses_project_local_tool_then_reports_removal(self):
        self.fixture('actionlint')
        local = self.fixture('actionlint', self.workspace / 'node_modules/.bin')
        report = self.env.doctor(required=['github-actions-validation'])
        tool = report['skills']['devops-standard']['tools']['actionlint']
        self.assertEqual(tool['executable'], str(local))
        self.assertNotIn('required-capability:github-actions-validation', report['blockers'])
        local.unlink()
        (self.bin / 'actionlint').unlink()
        missing = self.env.doctor(required=['github-actions-validation'])
        self.assertIn('required-capability:github-actions-validation', missing['blockers'])
        self.assertEqual(missing['skills']['devops-standard']['tools']['actionlint']['status'], 'MISSING')

    def test_registry_source_drift_rejects_cache_without_mutating_read_only_state(self):
        self.fixture('actionlint')
        self.assertIsNotNone(self.tools.detect('devops-standard', 'actionlint', self.workspace))
        registry, state = self.tools.paths('devops-standard')
        before = state.read_bytes()
        catalog = json.loads(registry.read_text())
        next(t for t in catalog['tools'] if t['id'] == 'actionlint')['repository'] = 'https://example.org/changed'
        registry.write_text(json.dumps(catalog))
        self.assertIsNone(self.tools.cached('devops-standard', 'actionlint', self.workspace, read_only=True))
        self.assertEqual(state.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
