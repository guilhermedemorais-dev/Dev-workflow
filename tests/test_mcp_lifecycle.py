import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'plugins/dev-environment-standard/skills/dev-environment-standard/scripts/mcp_lifecycle.py'
spec = importlib.util.spec_from_file_location('lifecycle_test', SOURCE)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

FIXTURE = '''import json,os,sys,time,subprocess
child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(300)'])
tool={'name':'inspect','inputSchema':{'type':'object','properties':{},'additionalProperties':False},'annotations':{'readOnlyHint':True,'destructiveHint':False}}
for line in sys.stdin:
 m=json.loads(line); method=m['method']
 if 'id' not in m: continue
 if method=='initialize': result={'protocolVersion':'2024-11-05','capabilities':{'tools':{}}}
 elif method=='tools/list': result={'tools':[tool]}
 elif method=='tools/call':
  if m['params']['arguments'].get('counter'):
   from pathlib import Path
   p=Path(m['params']['arguments']['counter']); p.write_text(str(int(p.read_text())+1) if p.exists() else '1')
   if m['params']['arguments'].get('disconnect'): os._exit(1)
  time.sleep(m['params']['arguments'].get('delay',0))
  result={'content':[{'type':'text','text':json.dumps({'pid':os.getpid(),'child':child.pid,'args':m['params']['arguments']})}]}
 print(json.dumps({'jsonrpc':'2.0','id':m['id'],'result':result}),flush=True)
'''


def alive(pid):
    if os.name == 'nt':
        import ctypes
        kernel = ctypes.WinDLL('kernel32'); kernel.OpenProcess.restype = ctypes.c_void_p
        handle = kernel.OpenProcess(0x1000, False, pid)
        if not handle: return False
        code = ctypes.c_ulong(); kernel.GetExitCodeProcess(ctypes.c_void_p(handle), ctypes.byref(code)); kernel.CloseHandle(ctypes.c_void_p(handle))
        return code.value == 259
    try:
        os.kill(pid, 0)
        stat = Path('/proc') / str(pid) / 'stat'
        return not stat.exists() or stat.read_text().split()[2] != 'Z'
    except ProcessLookupError: return False


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'upstream.py'; self.path.write_text(FIXTURE)
        self.definition = {'command': sys.executable, 'args': [str(self.path)]}
        child = module.OwnedChild(self.definition)
        try: tools = child.metadata()
        finally: child.close()
        self.manifest = {'version': 1, 'definition': self.definition, 'binding': module.binding(self.definition), 'tools': tools}
        self.lifecycle = module.Lifecycle(self.manifest, 1)
        self.addCleanup(self.lifecycle.stop)
    def data(self, result): return json.loads(result['content'][0]['text'])
    def wait_dead(self, pid):
        until = time.monotonic() + 5
        while alive(pid) and time.monotonic() < until: time.sleep(.03)
        self.assertFalse(alive(pid))
    def test_metadata_does_not_start_child_and_preserves_schema_annotations(self):
        tools = self.lifecycle.metadata()
        self.assertEqual(tools[0], self.manifest['tools'][0])
        self.assertIsNone(self.lifecycle.child)
        self.assertEqual(self.data(self.lifecycle.call('_harness_status', {}))['state'], 'STOPPED')
    def test_stdio_newer_protocol_negotiates_supported_snapshot_without_child(self):
        path = Path(self.temp.name) / 'stdio_fixture.json'; path.write_text(json.dumps(self.manifest))
        script = "import importlib.util,json,sys; from pathlib import Path; s=importlib.util.spec_from_file_location('stdio_fixture',sys.argv[1]); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); m.serve(json.loads(Path(sys.argv[2]).read_text()))"
        child = module.OwnedChild({'command': sys.executable, 'args': ['-c', script, str(SOURCE), str(path)]})
        try:
            result = child.request('initialize', {'protocolVersion': '2025-11-25', 'capabilities': {}})
            self.assertEqual(result['protocolVersion'], '2024-11-05')
            child.send({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
            tools = child.request('tools/list')['tools']; self.assertEqual(tools[0], self.manifest['tools'][0])
            status = self.data(child.request('tools/call', {'name': '_harness_status', 'arguments': {}}))
            self.assertEqual(status['state'], 'STOPPED'); self.assertIsNone(status['owned_pid'])
        finally: child.close()
    def test_lazy_workflow_reuses_pid_arguments_unchanged_finish_kills_owned_tree(self):
        first = self.data(self.lifecycle.call('inspect', {'value': 'preserved'}))
        second = self.data(self.lifecycle.call('inspect', {}))
        self.assertEqual(first['pid'], second['pid']); self.assertEqual(first['args'], {'value': 'preserved'})
        self.lifecycle.call('_harness_finish_session', {})
        self.wait_dead(first['pid']); self.wait_dead(first['child'])
        third = self.data(self.lifecycle.call('inspect', {})); self.assertNotEqual(third['pid'], first['pid'])
    def test_shared_leases_only_last_release_stops(self):
        a = self.data(self.lifecycle.call('_harness_begin_session', {}))['session']
        b = self.data(self.lifecycle.call('_harness_begin_session', {}))['session']
        result = self.data(self.lifecycle.call('inspect', {}, {'harness_session': a}))
        self.lifecycle.call('_harness_finish_session', {'session': a}); self.assertTrue(alive(result['pid']))
        self.lifecycle.call('_harness_finish_session', {'session': b}); self.wait_dead(result['pid'])
    def test_release_during_call_drains(self):
        token = self.data(self.lifecycle.call('_harness_begin_session', {}))['session']
        outcomes = []
        worker = threading.Thread(target=lambda: outcomes.append(self.data(self.lifecycle.call('inspect', {'delay': .4}, {'harness_session': token}))))
        worker.start()
        until = time.monotonic() + 5
        while not self.lifecycle.child and time.monotonic() < until: time.sleep(.01)
        self.lifecycle.call('_harness_finish_session', {'session': token})
        self.assertEqual(self.lifecycle.active, 1)
        worker.join(5); self.assertEqual(len(outcomes), 1); self.wait_dead(outcomes[0]['pid'])
    def test_idle_expires_abandoned_lease_and_kills_children(self):
        token = self.data(self.lifecycle.call('_harness_begin_session', {}))['session']
        result = self.data(self.lifecycle.call('inspect', {}, {'harness_session': token}))
        time.sleep(1.1); self.lifecycle.reap(); self.wait_dead(result['pid']); self.wait_dead(result['child'])
        with self.assertRaises(ValueError): self.lifecycle.call('inspect', {}, {'harness_session': token})
    def test_runtime_drift_blocks_cached_metadata_and_launch(self):
        self.path.write_text(self.path.read_text() + '\n# drift')
        with self.assertRaises(ValueError): self.lifecycle.metadata()
        with self.assertRaises(ValueError): self.lifecycle.call('inspect', {})
        self.assertIsNone(self.lifecycle.child)
    def test_env_drift_blocks_launch(self):
        from unittest.mock import patch
        self.definition['inherited_env'] = ['N8N_API_KEY']
        self.manifest['binding'] = module.binding(self.definition)
        with patch.dict(os.environ, {'N8N_API_KEY': 'secret'}):
            with self.assertRaises(ValueError): self.lifecycle.call('inspect', {})
    def test_provider_credential_isolation_and_explicit_overrides(self):
        from unittest.mock import patch
        secrets = {'N8N_API_KEY': 'n8n-test', 'N8N_API_URL': 'https://n8n.invalid', 'ANTHROPIC_API_KEY': 'claude-test', 'CLAUDE_CODE_OAUTH_TOKEN': 'oauth-test', 'USER_SELECTED_CREDENTIAL': 'explicit-test'}
        with patch.dict(os.environ, secrets):
            for provider, keys in module.PROVIDER_ENV.items():
                env = module.effective_env({'inherited_env': list(keys)})
                for key in secrets:
                    self.assertEqual(key in env, key in keys, (provider, key))
            env = module.effective_env({'inherited_env': [], 'env_vars': ['USER_SELECTED_CREDENTIAL'], 'env': {'N8N_API_KEY': 'approved-override'}})
            self.assertEqual(env['USER_SELECTED_CREDENTIAL'], 'explicit-test')
            self.assertEqual(env['N8N_API_KEY'], 'approved-override')
            self.assertNotIn('ANTHROPIC_API_KEY', env)
    def test_unrelated_provider_credential_drift_does_not_invalidate(self):
        from unittest.mock import patch
        self.definition['inherited_env'] = []
        self.manifest['binding'] = module.binding(self.definition)
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'other-provider'}):
            self.assertEqual(self.lifecycle.metadata()[0], self.manifest['tools'][0])
    def test_unrelated_client_env_does_not_invalidate(self):
        from unittest.mock import patch
        with patch.dict(os.environ, {'CODEX_EPHEMERAL_ID': 'changed'}):
            self.assertEqual(self.lifecycle.metadata()[0], self.manifest['tools'][0])
    def test_unknown_tool_and_session_do_not_start(self):
        with self.assertRaises(ValueError): self.lifecycle.call('unknown', {})
        with self.assertRaises(ValueError): self.lifecycle.call('inspect', {}, {'harness_session': 'unowned'})
        self.assertIsNone(self.lifecycle.child)
    def test_failed_call_does_not_replay(self):
        self.lifecycle.call('inspect', {})
        self.lifecycle.child.process.kill()
        with self.assertRaises(ValueError): self.lifecycle.call('inspect', {})
        self.assertIsNone(self.lifecycle.child)
    def test_partial_mutation_disconnect_is_not_replayed(self):
        counter = Path(self.temp.name) / 'counter'
        with self.assertRaises(ValueError):
            self.lifecycle.call('inspect', {'counter': str(counter), 'disconnect': True})
        self.assertEqual(counter.read_text(), '1')
        self.lifecycle.call('inspect', {'counter': str(counter)})
        self.assertEqual(counter.read_text(), '2')
    def test_failed_concurrent_call_does_not_kill_or_replay_queued_call(self):
        counter = Path(self.temp.name) / 'concurrent_counter'; errors = []; outputs = []
        def failure():
            try: self.lifecycle.call('inspect', {'counter': str(counter), 'disconnect': True})
            except ValueError: errors.append(True)
        first = threading.Thread(target=failure)
        second = threading.Thread(target=lambda: outputs.append(self.data(self.lifecycle.call('inspect', {'counter': str(counter)}))))
        first.start()
        until = time.monotonic() + 5
        while self.lifecycle.active == 0 and time.monotonic() < until: time.sleep(.001)
        second.start(); first.join(5); second.join(5)
        self.assertEqual(errors, [True]); self.assertEqual(len(outputs), 1)
        self.assertEqual(counter.read_text(), '2'); self.assertTrue(alive(outputs[0]['pid']))
    def test_unsupported_server_approval_request_fails_and_closes_owned_tree(self):
        source = FIXTURE.replace("time.sleep(m['params']['arguments'].get('delay',0))", "print(json.dumps({'jsonrpc':'2.0','id':'server-approval','method':'sampling/createMessage','params':{}}),flush=True); time.sleep(30)")
        self.path.write_text(source); self.manifest['binding'] = module.binding(self.definition)
        with self.assertRaises(ValueError): self.lifecycle.call('inspect', {})
        self.assertIsNone(self.lifecycle.child)
    def test_changed_tool_metadata_fails_before_tool_execution(self):
        source = FIXTURE.replace("'readOnlyHint':True", "'readOnlyHint':False")
        self.path.write_text(source); self.manifest['binding'] = module.binding(self.definition)
        with self.assertRaises(ValueError): self.lifecycle.call('inspect', {})
        self.assertIsNone(self.lifecycle.child)
    def test_list_changed_capability_allowed_actual_notification_invalidates(self):
        source = FIXTURE.replace("'capabilities':{'tools':{}}", "'capabilities':{'tools':{'listChanged':True}}")
        source = source.replace("time.sleep(m['params']['arguments'].get('delay',0))", "tool['annotations']['readOnlyHint']=False; print(json.dumps({'jsonrpc':'2.0','method':'notifications/tools/list_changed'}),flush=True)")
        self.path.write_text(source); self.manifest['binding'] = module.binding(self.definition)
        child = module.OwnedChild(self.definition)
        try: self.assertEqual(child.metadata(), self.manifest['tools'])
        finally: child.close()
        with self.assertRaises(ValueError): self.lifecycle.call('inspect', {})
        self.assertTrue(self.lifecycle.invalidated)
        with self.assertRaises(ValueError): self.lifecycle.call('inspect', {})
        self.assertIsNone(self.lifecycle.child)
    def test_harmless_list_changed_rechecks_equal_inventory_without_replay(self):
        source = FIXTURE.replace("time.sleep(m['params']['arguments'].get('delay',0))", "print(json.dumps({'jsonrpc':'2.0','method':'notifications/tools/list_changed'}),flush=True)")
        self.path.write_text(source); self.manifest['binding'] = module.binding(self.definition)
        counter = Path(self.temp.name) / 'harmless_counter'
        first = self.data(self.lifecycle.call('inspect', {'counter': str(counter)}))
        second = self.data(self.lifecycle.call('inspect', {'counter': str(counter)}))
        self.assertEqual(counter.read_text(), '2'); self.assertEqual(first['pid'], second['pid'])
        self.assertFalse(self.lifecycle.invalidated)
    def test_closed_client_blocks_queued_mutation(self):
        counter = Path(self.temp.name) / 'closed_counter'; errors = []
        def queued():
            try: self.lifecycle.call('inspect', {'counter': str(counter)})
            except ValueError: errors.append(True)
        self.lifecycle.calls.acquire()
        worker = threading.Thread(target=queued); worker.start()
        until = time.monotonic() + 5
        while not self.lifecycle.active and time.monotonic() < until: time.sleep(.001)
        with self.lifecycle.lock: self.lifecycle.closed = True
        self.lifecycle.calls.release(); worker.join(5)
        self.assertEqual(errors, [True]); self.assertFalse(counter.exists()); self.assertIsNone(self.lifecycle.child)
    def test_invalidated_inventory_blocks_previously_queued_mutation(self):
        counter = Path(self.temp.name) / 'invalidated_counter'; errors = []
        def queued():
            try: self.lifecycle.call('inspect', {'counter': str(counter)})
            except ValueError: errors.append(True)
        self.lifecycle.calls.acquire()
        worker = threading.Thread(target=queued); worker.start()
        until = time.monotonic() + 5
        while not self.lifecycle.active and time.monotonic() < until: time.sleep(.001)
        with self.lifecycle.lock: self.lifecycle.invalidated = True
        self.lifecycle.calls.release(); worker.join(5)
        self.assertEqual(errors, [True]); self.assertFalse(counter.exists()); self.assertIsNone(self.lifecycle.child)
    def test_private_manifest_digest_and_permissions(self):
        import hashlib
        path = Path(self.temp.name) / 'manifest.json'
        spec = importlib.util.spec_from_file_location('environment_cache_test', SOURCE.with_name('environment.py'))
        environment = importlib.util.module_from_spec(spec); spec.loader.exec_module(environment)
        environment.atomic(path, json.dumps(self.manifest))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(module.read_manifest(path, digest)['tools'], self.manifest['tools'])
        environment.atomic(path, json.dumps(dict(self.manifest, tools=[])))
        with self.assertRaises(ValueError): module.read_manifest(path, digest)
    def test_aliased_generated_proxy_reconciles_global_and_plugin_duplicates(self):
        spec = importlib.util.spec_from_file_location('lifecycle_identity_test', SOURCE.with_name('native_mcp.py'))
        native = importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
        proxy = {'command': sys.executable, 'args': [str(SOURCE), '--manifest', str(Path(self.temp.name) / 'claude-code.json'), '--manifest-sha256', 'a' * 64, '--idle-seconds', '60']}
        self.assertEqual(native.identity('arbitrary-alias', proxy), 'claude-code')
        config = Path(self.temp.name) / 'proxy-config.toml'
        config.write_text('[mcp_servers.claude]\ncommand="claude.exe"\nargs=["mcp","serve"]\n[mcp_servers.other]\ncommand=' + json.dumps(proxy['command']) + '\nargs=' + json.dumps(proxy['args']))
        adapter = native.NativeMCP(config, Path(self.temp.name) / 'prefix', None, discovered={'runtime': 'WINDOWS_NATIVE', 'claude': 'C:/Tools/claude.exe'})
        with self.assertRaises(ValueError): adapter.prepare(['claude-code'])
        config.write_text('')
        plugin = Path(self.temp.name) / 'plugin.json'; plugin.write_text(json.dumps({'mcpServers': {'another-alias': proxy}}))
        adapter.plugin_configs = (plugin,)
        with self.assertRaises(ValueError): adapter.prepare(['claude-code'])
        self.assertIsNone(self.lifecycle.child)
    def test_unrecognized_or_malformed_owned_proxy_fails_closed(self):
        spec = importlib.util.spec_from_file_location('lifecycle_ambiguous_test', SOURCE.with_name('native_mcp.py'))
        native = importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
        with self.assertRaises(ValueError): native.identity('other', {'command': sys.executable, 'args': [str(SOURCE), '--manifest', 'unknown.json']})
    def test_idle_does_not_expire_or_kill_active_call(self):
        token = self.data(self.lifecycle.call('_harness_begin_session', {}))['session']
        outcomes = []
        worker = threading.Thread(target=lambda: outcomes.append(self.data(self.lifecycle.call('inspect', {'delay': 1.4}, {'harness_session': token}))))
        worker.start(); time.sleep(1.15); self.lifecycle.reap()
        self.assertEqual(self.lifecycle.active, 1); self.assertIn(token, self.lifecycle.leases)
        worker.join(5); self.assertEqual(len(outcomes), 1)
        self.assertTrue(alive(outcomes[0]['pid']))
    def test_unrelated_process_survives_cleanup(self):
        other = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'])
        try:
            self.lifecycle.call('inspect', {}); self.lifecycle.call('_harness_finish_session', {})
            self.assertIsNone(other.poll())
        finally: other.kill(); other.wait()


if __name__ == '__main__': unittest.main()
