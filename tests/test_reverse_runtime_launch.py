import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

RUNTIME = Path(__file__).resolve().parents[1] / 'plugins/reverse-engineering-standard/runtime'

class ReverseRuntimeLaunchTests(unittest.TestCase):
    def setUp(self):
        self.node = shutil.which('node')
        if not self.node:
            self.skipTest('Node runtime not installed')
        self.temp = tempfile.TemporaryDirectory(prefix='rea space & ')
        self.addCleanup(self.temp.cleanup)
        self.runtime = Path(self.temp.name)
        for name in ('process-launch.mjs', 'reverse-context-gateway.mjs', 'rea-capability-catalog.json'):
            shutil.copyfile(RUNTIME / name, self.runtime / name)
        self.entry = self.runtime / 'node_modules/rea-agents/scripts/rea.mjs'
        self.entry.parent.mkdir(parents=True)

    def call(self, *args):
        return subprocess.run([self.node, str(self.runtime / 'reverse-context-gateway.mjs'), *args], capture_output=True, text=True)

    def test_shell_metacharacters_are_literal_arguments(self):
        self.entry.write_text('console.log(JSON.stringify(process.argv.slice(2)))', encoding='utf-8')
        target = str(self.runtime / 'owned & quoted $ artifact')
        result = self.call('analyze-javascript', target)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), ['analyze-javascript-application', target, '--json'])

    def test_missing_runtime_explains_failure(self):
        result = self.call('probe')
        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertFalse(report['healthy'])
        self.assertIn('Cannot find module', report['stderr'])

    def test_invalid_doctor_output_is_structured_failure(self):
        self.entry.write_text('console.log("not json")', encoding='utf-8')
        result = self.call('probe')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('invalid JSON', json.loads(result.stdout)['stderr'])

    def test_direct_javascript_package_manager(self):
        manager = self.runtime / 'pnpm.cjs'
        manager.write_text('', encoding='utf-8')
        script = 'import {packageManagerInvocation} from "./process-launch.mjs"; console.log(JSON.stringify(packageManagerInvocation()))'
        env = dict(os.environ, DEV_WORKFLOW_PACKAGE_MANAGER_JS=str(manager))
        result = subprocess.run([self.node, '--input-type=module', '-e', script], cwd=self.runtime, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['kind'], 'pnpm')
        self.assertEqual(Path(report['args'][0]), manager)
        self.assertEqual(Path(report['executable']), Path(self.node))

    def test_optional_provider_failure_does_not_hide_available_runtime(self):
        self.entry.write_text('console.log(JSON.stringify({healthy:false,scope_checks:[{name:"ghidra",ok:false}]})); process.exitCode=1', encoding='utf-8')
        result = self.call('probe')
        report = json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(report['runtime_available'])
        self.assertFalse(report['healthy'])

    def test_local_provider_paths_are_reused_and_environment_wins(self):
        config = self.runtime / 'runtime-state/providers.json'
        config.parent.mkdir()
        config.write_text(json.dumps({'schema_version':1,'paths':{'JAVA_HOME':str(self.runtime)}}), encoding='utf-8')
        self.entry.write_text('console.log(JSON.stringify({java:process.env.JAVA_HOME}))', encoding='utf-8')
        env = dict(os.environ)
        env.pop('JAVA_HOME', None)
        result = subprocess.run([self.node, str(self.runtime / 'reverse-context-gateway.mjs'), 'cli', 'test'], env=env, capture_output=True, text=True)
        self.assertEqual(json.loads(result.stdout)['java'], str(self.runtime))
        env['JAVA_HOME'] = 'explicit override'
        result = subprocess.run([self.node, str(self.runtime / 'reverse-context-gateway.mjs'), 'cli', 'test'], env=env, capture_output=True, text=True)
        self.assertEqual(json.loads(result.stdout)['java'], 'explicit override')

    def test_local_provider_config_rejects_extra_environment_injection(self):
        config = self.runtime / 'runtime-state/providers.json'
        config.parent.mkdir()
        config.write_text(json.dumps({'schema_version':1,'paths':{'NODE_OPTIONS':str(self.runtime)}}), encoding='utf-8')
        self.entry.write_text('console.log("unexpected execution")', encoding='utf-8')
        result = self.call('cli', 'test')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('unexpected execution', result.stdout)
        self.assertIn('Invalid local provider path', result.stderr)

    def test_existing_absolute_target_uses_native_path(self):
        target = self.runtime / 'owned fixture.bin'
        target.write_bytes(b'fixture')
        self.entry.write_text('console.log(JSON.stringify(process.argv.slice(2)))', encoding='utf-8')
        result = self.call('cli', 'analyze', target.as_posix())
        expected = str(target.resolve()) if os.name == 'nt' else target.as_posix()
        self.assertEqual(json.loads(result.stdout), ['analyze', expected])


class ReverseRuntimeBootstrapTests(unittest.TestCase):
    def setUp(self):
        self.node = shutil.which('node')
        if not self.node:
            self.skipTest('Node runtime not installed')
        self.temp = tempfile.TemporaryDirectory(prefix='rea bootstrap & ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.runtime = self.root / 'runtime'
        self.runtime.mkdir()
        for name in ('process-launch.mjs', 'install-local-runtime.mjs'):
            shutil.copyfile(RUNTIME / name, self.runtime / name)
        vendor = self.root / 'vendor/rea-runtime'
        vendor.mkdir(parents=True)
        for name in ('rea-agents-4.1.0.tgz', 'rea-agents-4.1.0.tgz.sha256'):
            shutil.copyfile(RUNTIME.parent / 'vendor/rea-runtime' / name, vendor / name)
        self.env = dict(os.environ)
        self.env.pop('DEV_WORKFLOW_PACKAGE_MANAGER_JS', None)

    def manager(self, kind, status=0):
        entry = self.root / ('pnpm.cjs' if kind == 'pnpm' else 'npm-cli.js')
        entry.write_text(
            'const fs = require("node:fs");'
            'fs.writeFileSync("invoked.json", JSON.stringify(process.argv.slice(2)));'
            f'if ({status}) process.exit({status});'
            'fs.mkdirSync("node_modules/rea-agents/scripts", {recursive:true});'
            'fs.writeFileSync("node_modules/rea-agents/scripts/rea.mjs", "");',
            encoding='utf-8')
        return entry

    def bootstrap(self):
        return subprocess.run([self.node, str(self.runtime / 'install-local-runtime.mjs')],
                              cwd=self.runtime, env=self.env, capture_output=True, text=True)

    def lock(self, kind):
        name = 'pnpm-lock.yaml' if kind == 'pnpm' else 'package-lock.json'
        (self.runtime / name).write_text('fixture', encoding='utf-8')

    def test_npm_bootstrap_environment_uses_pnpm_lock_and_discovery(self):
        self.lock('pnpm')
        manager = self.manager('pnpm')
        self.env['PATH'] = str(manager.parent)
        self.env['npm_execpath'] = str(self.manager('npm'))
        result = self.bootstrap()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads((self.runtime / 'invoked.json').read_text()),
                         ['install', '--ignore-scripts', '--frozen-lockfile'])
        self.assertFalse((self.runtime / 'package-lock.json').exists())

    def test_explicit_pnpm_uses_frozen_install(self):
        self.lock('pnpm')
        self.env['DEV_WORKFLOW_PACKAGE_MANAGER_JS'] = str(self.manager('pnpm'))
        result = self.bootstrap()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--frozen-lockfile', json.loads((self.runtime / 'invoked.json').read_text()))

    def test_npm_requires_its_lock_and_uses_ci(self):
        self.lock('npm')
        self.env['DEV_WORKFLOW_PACKAGE_MANAGER_JS'] = str(self.manager('npm'))
        result = self.bootstrap()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads((self.runtime / 'invoked.json').read_text()),
                         ['ci', '--ignore-scripts', '--no-audit', '--no-fund'])

    def test_missing_lock_fails_before_manager_execution(self):
        self.env['DEV_WORKFLOW_PACKAGE_MANAGER_JS'] = str(self.manager('npm'))
        result = self.bootstrap()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('lock.json is required', result.stderr)
        self.assertFalse((self.runtime / 'invoked.json').exists())

    def test_explicit_manager_mismatch_fails_before_install(self):
        for lock_kind, manager_kind in [('pnpm', 'npm'), ('npm', 'pnpm')]:
            with self.subTest(lock=lock_kind):
                for name in ('pnpm-lock.yaml', 'package-lock.json'):
                    (self.runtime / name).unlink(missing_ok=True)
                self.lock(lock_kind)
                self.env['DEV_WORKFLOW_PACKAGE_MANAGER_JS'] = str(self.manager(manager_kind))
                result = self.bootstrap()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Committed lockfile requires', result.stderr)
                self.assertFalse((self.runtime / 'invoked.json').exists())

    def test_pnpm_lock_takes_precedence_when_both_exist(self):
        self.lock('pnpm')
        self.lock('npm')
        self.env['DEV_WORKFLOW_PACKAGE_MANAGER_JS'] = str(self.manager('pnpm'))
        result = self.bootstrap()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--frozen-lockfile', json.loads((self.runtime / 'invoked.json').read_text()))

    def test_install_failure_is_propagated(self):
        self.lock('pnpm')
        self.env['DEV_WORKFLOW_PACKAGE_MANAGER_JS'] = str(self.manager('pnpm', status=17))
        self.assertEqual(self.bootstrap().returncode, 17)
