import importlib.util
import json
from pathlib import Path
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'plugins/dev-environment-standard/skills/dev-environment-standard/scripts'
spec = importlib.util.spec_from_file_location('native_test', SCRIPTS / 'native_mcp.py')
native = importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
spec = importlib.util.spec_from_file_location('environment_test_native', SCRIPTS / 'environment.py')
environment = importlib.util.module_from_spec(spec); spec.loader.exec_module(environment)

class NativeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = self.root / 'config.toml'
        self.host = {'runtime': 'WINDOWS_NATIVE', 'node': 'C:/Program Files/nodejs/node.exe', 'node_version': 'v24.22.0', 'npm_cli': 'C:/Program Files/nodejs/node_modules/npm/bin/npm-cli.js', 'claude': 'C:/Users/u/.local/bin/claude.exe', 'browsers': {'edge': 'C:/Edge/msedge.exe', 'chrome': 'C:/Chrome/chrome.exe'}}
        self.adapter = native.NativeMCP(self.config, self.root / 'persistent', environment.atomic, discovered=self.host)
        for key in ('playwright', 'chrome-devtools', 'n8n'):
            metadata = native.PROVIDERS[key]
            package = self.adapter.prefix / 'node_modules' / metadata['package']
            package.mkdir(parents=True)
            (package / 'package.json').write_text(json.dumps({'name': metadata['package'], 'version': metadata['version'], 'bin': metadata['bin']}))
            script = package / metadata['bin']; script.parent.mkdir(parents=True, exist_ok=True); script.write_text('/* fixture */')
    def test_runtime_distinguishes_wsl_linux(self):
        with patch.object(native.os, 'name', 'posix'), patch.object(native.platform, 'system', return_value='Linux'), patch.object(native.platform, 'release', return_value='Microsoft-standard'), patch.dict(native.os.environ, {}, clear=True):
            self.assertEqual(native.runtime(), 'WSL')
        with patch.object(native.os, 'name', 'posix'), patch.object(native.platform, 'system', return_value='Linux'), patch.object(native.platform, 'release', return_value='6.0'), patch.dict(native.os.environ, {}, clear=True):
            self.assertEqual(native.runtime(), 'LINUX')
    def test_native_launch_and_conditional_playwright(self):
        with self.assertRaises(ValueError): self.adapter.prepare(['playwright'])
        content = self.adapter.prepare(['playwright'], True)['content']
        data = tomllib.loads(content)['mcp_servers']['playwright']
        self.assertNotIn('wsl', data['command'])
        self.assertIn(self.host['browsers']['edge'], data['args'])
    def test_secret_preferences_comments_and_byte_exact_rollback(self):
        original = b'# comment\r\nmodel="owned"\r\n[mcp_servers.n8n]\r\ncommand="wsl.exe"\r\nargs=["-d","kali-linux","--exec","n8n-mcp"]\r\nenabled=false\r\nstartup_timeout_sec=40\r\n[mcp_servers.n8n.env]\r\nN8N_API_KEY="SECRET_SENTINEL"\r\nLOG_LEVEL="warn"\r\n[unrelated]\r\nkeep=true\r\n'
        self.config.write_bytes(original)
        plan = self.adapter.prepare(['n8n'])
        public = {k:v for k,v in plan.items() if k != 'content'}
        self.assertNotIn('SECRET_SENTINEL', json.dumps(public))
        data = tomllib.loads(plan['content']); self.assertFalse(data['mcp_servers']['n8n']['enabled'])
        self.assertEqual(data['mcp_servers']['n8n']['env']['LOG_LEVEL'], 'warn')
        self.assertEqual(data['mcp_servers']['n8n']['env']['MCP_MODE'], 'stdio')
        self.assertEqual(data['unrelated'], {'keep': True})
        result = self.adapter.apply(['n8n'], plan['fingerprint'], self.root / 'backup')
        self.adapter.rollback(result['receipt']); self.assertEqual(self.config.read_bytes(), original)
    def test_stale_selection_and_config_refused(self):
        plan = self.adapter.prepare(['claude-code'])
        with self.assertRaises(ValueError): self.adapter.apply(['n8n'], plan['fingerprint'], self.root / 'backup')
        self.config.write_text('changed=true')
        with self.assertRaises(ValueError): self.adapter.apply(['claude-code'], plan['fingerprint'], self.root / 'backup')
    def test_rollback_refuses_later_edits(self):
        plan = self.adapter.prepare(['claude-code']); result = self.adapter.apply(['claude-code'], plan['fingerprint'], self.root / 'backup')
        self.config.write_text(self.config.read_text() + '\nchanged=true\n')
        with self.assertRaises(ValueError): self.adapter.rollback(result['receipt'])
    def test_plugin_alias_collision(self):
        plugin = self.root / 'plugin.json'; plugin.write_text(json.dumps({'mcpServers': {'alias': {'command':'npx','args':['-y','n8n-mcp@2.93.0']}}}))
        self.adapter.plugin_configs = (plugin,)
        with self.assertRaises(ValueError): self.adapter.prepare(['n8n'])
    def test_global_alias_collision(self):
        self.config.write_text('[mcp_servers.n8n]\ncommand="npx"\nargs=["n8n-mcp"]\n[mcp_servers.other]\ncommand="npx"\nargs=["n8n-mcp"]')
        with self.assertRaises(ValueError): self.adapter.prepare(['n8n'])
    def test_shell_wrappers_not_executed(self):
        self.config.write_text('[mcp_servers.n8n]\ncommand="wsl.exe"\nargs=["bash","-lc","API_KEY=SECRET npx n8n-mcp"]')
        with self.assertRaises(ValueError): self.adapter.prepare(['n8n'])
    def test_chrome_requires_chrome_and_engine(self):
        self.host['browsers'].pop('chrome')
        with self.assertRaises(ValueError): self.adapter.prepare(['chrome-devtools'])
        self.host['browsers']['chrome'] = 'C:/Chrome/chrome.exe'
        for version in ('v21.0.0', 'v22.11.0', 'v20.18.0'):
            self.host['node_version'] = version
            with self.assertRaises(ValueError): self.adapter.prepare(['chrome-devtools'])
    def test_package_identity_and_version(self):
        path = self.adapter.prefix / 'node_modules/n8n-mcp/package.json'; data = json.loads(path.read_text());data['version']='0.0.1';path.write_text(json.dumps(data))
        with self.assertRaises(ValueError): self.adapter.prepare(['n8n'])
    def test_install_exact_selection_and_stdout_private(self):
        plan = self.adapter.install_plan(['n8n'])
        with patch.object(native.subprocess, 'run') as run:
            run.return_value.returncode = 0
            result = self.adapter.install(['n8n'], plan['fingerprint'])
            self.assertEqual(run.call_args.args[0][-1], 'n8n-mcp@2.93.0')
            self.assertEqual(result['receipts'][0]['result'], 'INSTALLED_NOT_VALIDATED')
    def test_linux_no_native_rewrite(self):
        self.host['runtime'] = 'WSL'
        with self.assertRaises(ValueError): self.adapter.prepare(['claude-code'])
    def test_symlink_backup_rejected(self):
        plan = self.adapter.prepare(['claude-code'])
        with patch.object(Path, 'is_symlink', return_value=True):
            with self.assertRaises(ValueError): self.adapter.apply(['claude-code'], plan['fingerprint'], self.root / 'backup')
    def test_structured_inline_env_retains_precedence_privately(self):
        self.config.write_text('[mcp_servers.n8n]\ncommand="wsl.exe"\nargs=["-d","kali-linux","--exec","env","N8N_API_KEY=SECRET_INLINE","npx","-y","n8n-mcp@2.93.0"]\n[mcp_servers.n8n.env]\nN8N_API_KEY="SECRET_OLD"\n')
        plan = self.adapter.prepare(['n8n'])
        self.assertEqual(tomllib.loads(plan['content'])['mcp_servers']['n8n']['env']['N8N_API_KEY'], 'SECRET_INLINE')
        self.assertNotIn('SECRET_INLINE', json.dumps({k:v for k,v in plan.items() if k != 'content'}))
    def test_browser_wrapper_preserves_flags_replaces_linux_path(self):
        self.config.write_text('[mcp_servers.playwright]\ncommand="wsl.exe"\nargs=["-d","kali-linux","--exec","npx","-y","@playwright/mcp@0.0.82","--headless","--executable-path","/home/u/chrome"]\n')
        plan = self.adapter.prepare(['playwright'], True)
        args = tomllib.loads(plan['content'])['mcp_servers']['playwright']['args']
        self.assertIn('--headless', args);self.assertNotIn('/home/u/chrome', args)
    def test_unknown_wrapper_positional_option_refused(self):
        for extra in ('"arbitrary"', '"-x"', '"--dangerous"'):
            self.config.write_text('[mcp_servers.n8n]\ncommand="wsl.exe"\nargs=["--exec","n8n-mcp",' + extra + ']\n')
            with self.assertRaises(ValueError): self.adapter.prepare(['n8n'])

    def test_actual_wsl_delimiter_and_empty_env_table(self):
        self.config.write_text('[mcp_servers.n8n]\ncommand="wsl.exe"\nargs=["-d","kali-linux","--","/home/u/bin/n8n-mcp"]\n[mcp_servers.n8n.env]\n')
        plan = self.adapter.prepare(['n8n'])
        self.assertEqual(plan['content'].count('[mcp_servers.n8n.env]'), 1)
        self.assertEqual(tomllib.loads(plan['content'])['mcp_servers']['n8n']['env']['MCP_MODE'], 'stdio')
    def test_runtime_and_entrypoint_byte_drift(self):
        binary = self.root / 'node.exe'; binary.write_bytes(b'original fixture');self.host['node'] = str(binary)
        plan = self.adapter.prepare(['n8n']);binary.write_bytes(b'changed fixture')
        with self.assertRaises(ValueError): self.adapter.apply(['n8n'], plan['fingerprint'], self.root / 'backup')
        plan = self.adapter.prepare(['n8n'])
        script = self.adapter.prefix / 'node_modules/n8n-mcp' / native.PROVIDERS['n8n']['bin'];script.write_text('changed')
        with self.assertRaises(ValueError): self.adapter.apply(['n8n'], plan['fingerprint'], self.root / 'backup')
    def test_entrypoint_metadata_cannot_select_unreviewed_script(self):
        path = self.adapter.prefix / 'node_modules/n8n-mcp/package.json';data=json.loads(path.read_text());data['bin']='unreviewed.js';path.write_text(json.dumps(data))
        with self.assertRaises(ValueError): self.adapter.prepare(['n8n'])
    def test_edge_chrome_candidate_requires_explicit_consent(self):
        self.host['browsers']['selected']='C:/Edge/msedge.exe'
        with self.assertRaises(ValueError): self.adapter.prepare(['chrome-devtools'])
        self.assertIn('C:/Edge/msedge.exe', self.adapter.prepare(['chrome-devtools'], True)['content'])
    def test_explicit_node_override_wins_over_internal_path(self):
        node = self.root / 'node.exe';node.write_text('fixture')
        with patch.object(native, 'stable', side_effect=lambda value: str(value) if value and str(value).endswith('node.exe') and 'codex-runtimes' not in str(value) else None), patch.object(native.subprocess, 'run') as run:
            run.return_value.stdout='v24.22.0'
            with patch.dict(native.os.environ, {'PATH':'C:/codex-runtimes/bin'}):
                self.assertEqual(native.discover(node_override=str(node))['node'], str(node))

    def test_unknown_alias_strict_known_wrapper_identity(self):
        for key, executable, tail in (('playwright','playwright-mcp',[]),('claude-code','claude',['mcp','serve'])):
            self.config.write_text('[mcp_servers.browser_automation]\ncommand="wsl.exe"\nargs=' + json.dumps(['-d','kali-linux','--','/home/bin/' + executable] + tail) + '\n')
            plan=self.adapter.prepare([key],True)
            self.assertEqual(plan['changes'][0]['name'],'browser_automation')
            self.assertNotIn('[mcp_servers.'+key+']',plan['content'])
    def test_claude_binary_replacement_invalidates_plan(self):
        executable=self.root/'claude.exe';executable.write_bytes(b'original');self.host['claude']=str(executable)
        plan=self.adapter.prepare(['claude-code']);executable.write_bytes(b'changed')
        with self.assertRaises(ValueError):self.adapter.apply(['claude-code'],plan['fingerprint'],self.root/'backup')
    def test_rollback_rechecks_config_after_backup_read(self):
        plan=self.adapter.prepare(['claude-code']);result=self.adapter.apply(['claude-code'],plan['fingerprint'],self.root/'backup')
        original_read=Path.read_bytes
        def altered_read(path):
            content=original_read(path)
            if path.name.endswith('.toml') and path.parent==self.root/'backup':
                self.config.write_bytes(b'newer=true')
            return content
        with patch.object(Path,'read_bytes',altered_read):
            with self.assertRaises(ValueError):self.adapter.rollback(result['receipt'])
        self.assertEqual(self.config.read_bytes(),b'newer=true')

    def test_invalid_explicit_node_never_falls_back(self):
        with patch.object(native, 'stable', side_effect=lambda value: None if value=='C:/missing/node.exe' else 'C:/Program Files/nodejs/node.exe'), patch.object(native.shutil,'which',return_value='C:/Program Files/nodejs/node.exe'):
            with self.assertRaises(ValueError): native.discover(node_override='C:/missing/node.exe')

    def test_actual_chrome_two_bin_metadata(self):
        path=self.adapter.prefix/'node_modules/chrome-devtools-mcp/package.json';data=json.loads(path.read_text());data['bin']={'chrome-devtools-mcp':'./build/src/bin/chrome-devtools-mcp.js','chrome-devtools':'./build/src/bin/chrome-devtools.js'};path.write_text(json.dumps(data))
        self.assertIn('build',self.adapter.prepare(['chrome-devtools'])['content'])
    def test_actual_n8n_dot_prefix_metadata(self):
        path=self.adapter.prefix/'node_modules/n8n-mcp/package.json';data=json.loads(path.read_text());data['bin']={'n8n-mcp':'./dist/mcp/stdio-wrapper.js'};path.write_text(json.dumps(data))
        self.assertIn('stdio-wrapper.js',self.adapter.prepare(['n8n'])['content'])

    def test_explicit_selection(self):
        for values in ([], ['n8n','n8n'], ['unknown']):
            with self.assertRaises(ValueError): self.adapter.install_plan(values)

if __name__ == '__main__': unittest.main()
