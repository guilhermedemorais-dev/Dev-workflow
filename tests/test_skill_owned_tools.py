"""Behavioral tests for per-skill registries and runtime tool state."""

import importlib.util
import json
from pathlib import Path
import tempfile
import os
import subprocess
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/dev-workflow-standard/scripts/tool-state.py"
spec = importlib.util.spec_from_file_location("tool_state", SCRIPT)
tool_state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool_state)


class ToolStateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.registry = self.base / "registry.json"
        self.state = self.base / "state.json"
        self.executable = self.base / "fake-tool"
        self.executable.write_text("#!/bin/sh\necho 1.0\n", encoding="utf-8")
        self.executable.chmod(0o755)
        environment = patch.dict(os.environ, {"PATH": str(self.base) + os.pathsep + os.environ.get("PATH", "")})
        environment.start()
        self.addCleanup(environment.stop)
        self.registry.write_text(json.dumps({"tools": [{"id": "fake", "command": "fake-tool",
            "repository": "https://github.com/example/fake", "verify_args": ["--version"]}]}), encoding="utf-8")
        self.path_patch = patch.object(tool_state, "paths", return_value=(self.registry, self.state))
        self.path_patch.start()
        self.addCleanup(self.path_patch.stop)

    def test_first_detection_records_version_path_and_source(self):
        with patch.object(tool_state.shutil, "which", return_value=str(self.executable)):
            entry = tool_state.detect("security-standard", "fake", self.base)
        self.assertEqual(entry["version"], "1.0")
        self.assertEqual(entry["executable"], str(self.executable))
        self.assertEqual(entry["install_method"], "preexisting")
        self.assertEqual(json.loads(self.state.read_text())["tools"]["fake"], entry)

    def test_post_install_detection_records_actual_method(self):
        with patch.object(tool_state.shutil, "which", return_value=str(self.executable)):
            entry = tool_state.detect("security-standard", "fake", self.base, "official-release")
        self.assertEqual(entry["install_method"], "official-release")

    def test_python_plugin_verification_uses_environment_interpreter(self):
        self.registry.write_text(json.dumps({"tools": [{"id": "fake", "command": "fake-tool",
            "repository": "https://github.com/example/fake", "verify_distribution": "fake-plugin"}]}), encoding="utf-8")
        interpreter = self.base / "python"
        interpreter.write_text("#!/bin/sh\necho 2.1\n", encoding="utf-8")
        interpreter.chmod(0o755)
        with patch.object(tool_state.shutil, "which", return_value=str(self.executable)):
            entry = tool_state.detect("security-standard", "fake", self.base)
        self.assertEqual(entry["version"], "2.1")

    def test_fast_path_skips_discovery_and_uses_cached_executable(self):
        with patch.object(tool_state.shutil, "which", return_value=str(self.executable)):
            tool_state.detect("security-standard", "fake", self.base)
        with patch.object(tool_state, "detect", side_effect=AssertionError("unexpected discovery")):
            result = tool_state.run("security-standard", "fake", self.base, ["--version"])
        self.assertEqual(result["tool_state_source"], "cached-installed")
        self.assertEqual(result["exit_code"], 0)

    def test_environment_change_does_not_reuse_host_state(self):
        with patch.object(tool_state.shutil, "which", return_value=str(self.executable)):
            tool_state.detect("security-standard", "fake", self.base)
        with patch.dict(tool_state.os.environ, {"TOOL_RUNTIME_ID": "container-a"}):
            self.assertIsNone(tool_state.cached("security-standard", "fake", self.base))

    def test_missing_executable_and_required_version_invalidate(self):
        with patch.object(tool_state.shutil, "which", return_value=str(self.executable)):
            tool_state.detect("security-standard", "fake", self.base)
        self.assertIsNone(tool_state.cached("security-standard", "fake", self.base, "2.0"))
        self.assertEqual(tool_state.read_state("security-standard", self.base)["tools"]["fake"]["status"], "stale")
        with patch.object(tool_state.shutil, "which", return_value=str(self.executable)):
            tool_state.detect("security-standard", "fake", self.base)
        self.executable.unlink()
        self.assertIsNone(tool_state.cached("security-standard", "fake", self.base))

    def test_execution_disappearance_invalidates_cache(self):
        with patch.object(tool_state.shutil, "which", return_value=str(self.executable)):
            tool_state.detect("security-standard", "fake", self.base)
        with patch.object(tool_state.subprocess, "run", side_effect=FileNotFoundError):
            result = tool_state.run("security-standard", "fake", self.base, [])
        self.assertEqual(result["status"], "stale")

    def test_required_version_cannot_execute_incompatible_detected_tool(self):
        with patch.object(tool_state.shutil, "which", return_value=str(self.executable)):
            result = tool_state.run("security-standard", "fake", self.base, [], "2.0")
        self.assertEqual(result["status"], "incompatible")
        self.assertEqual(tool_state.read_state("security-standard", self.base)["tools"]["fake"]["status"], "stale")

    def test_failure_never_claims_installed_and_can_retry_later(self):
        tool_state.record_failure("security-standard", "fake", self.base, "network unavailable")
        self.assertIsNone(tool_state.cached("security-standard", "fake", self.base))
        self.assertEqual(tool_state.read_state("security-standard", self.base)["tools"]["fake"]["status"], "install_failed")
        with patch.object(tool_state.shutil, "which", return_value=str(self.executable)):
            entry = tool_state.detect("security-standard", "fake", self.base)
        self.assertEqual(entry["status"], "installed")

    def test_install_verifies_and_persists_or_records_failure_without_loop(self):
        with patch.object(tool_state.shutil, "which", return_value=str(self.executable)):
            result = tool_state.install("security-standard", "fake", self.base,
                                        ["/bin/true"], "official-release")
        self.assertEqual(result["status"], "installed")
        self.assertEqual(tool_state.cached("security-standard", "fake", self.base)["install_method"], "official-release")
        failure = tool_state.install("security-standard", "fake", self.base,
                                     ["/bin/false"], "official-release")
        self.assertEqual(failure["status"], "install_failed")
        with patch.object(tool_state.subprocess, "run", side_effect=AssertionError("repeat install")):
            deferred = tool_state.install("security-standard", "fake", self.base,
                                          ["/bin/true"], "official-release")
        self.assertEqual(deferred["status"], "retry_deferred")

    def test_registries_are_owned_and_contain_only_official_source_knowledge(self):
        owners = {"security-standard": 6, "dev-implementation-standard": 6, "ui-ux-standard": 1}
        for owner, count in owners.items():
            with self.subTest(owner=owner):
                path = ROOT / "plugins" / owner / "skills" / owner / "references/tool-registry.json"
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(data["owner"], owner)
                self.assertEqual(len(data["tools"]), count)
                for item in data["tools"]:
                    self.assertTrue(item["repository"].startswith("https://github.com/"))
                    self.assertNotIn("installed", item)
                    self.assertNotIn("executable", item)

    def test_contract_and_task_do_not_include_local_state(self):
        contract = (ROOT / "plugins/sdd-spec-factory/templates/execution-contract-template.json").read_text()
        task = (ROOT / "plugins/sdd-spec-factory/templates/task-template.md").read_text()
        self.assertIn("required_validations", contract)
        self.assertNotIn("tool-state", contract)
        self.assertIn("Validação e tools previstas", task)
        self.assertNotIn("tool-state.json", task)
        self.assertIn("plugins/*/skills/*/runtime-state/", (ROOT / ".gitignore").read_text())

    def test_separately_installed_skill_can_use_writable_state_override(self):
        self.path_patch.stop()
        with patch.dict(tool_state.os.environ, {
            "TOOL_REGISTRY_PATH": str(self.registry), "TOOL_STATE_PATH": str(self.state)
        }):
            self.assertEqual(tool_state.paths("security-standard"), (self.registry, self.state))

    def test_probe_and_stale_cache_read_only_do_not_write(self):
        with patch.object(tool_state.shutil, "which", return_value=str(self.executable)):
            self.assertEqual(tool_state.probe("security-standard", "fake", self.base)["version"], "1.0")
            self.assertFalse(self.state.exists())
            tool_state.detect("security-standard", "fake", self.base)
        before = self.state.read_bytes()
        self.executable.unlink()
        self.assertIsNone(tool_state.cached("security-standard", "fake", self.base, read_only=True))
        self.assertEqual(before, self.state.read_bytes())

    def test_local_executable_and_project_cwd(self):
        local = self.base / ".venv/bin/fake-tool"
        local.parent.mkdir(parents=True)
        local.write_text("#!/bin/sh\ntest -f workspace-marker || exit 8\necho 3.1\n")
        local.chmod(0o755)
        (self.base / "workspace-marker").touch()
        entry = tool_state.probe("security-standard", "fake", self.base)
        self.assertEqual(entry["executable"], str(local))
        self.assertEqual(tool_state.run("security-standard", "fake", self.base, [])["exit_code"], 0)

    def test_install_uses_workspace_cwd(self):
        (self.base / "workspace-marker").touch()
        with patch.object(tool_state.shutil, "which", return_value=str(self.executable)):
            result = tool_state.install("security-standard", "fake", self.base,
                [sys.executable, "-c", "from pathlib import Path; assert Path('workspace-marker').is_file()"], "project")
        self.assertEqual(result["status"], "installed")

    def test_dynamic_owner_and_traversal(self):
        self.path_patch.stop()
        registry = self.base / "plugins/bundle/skills/new-specialist/references/tool-registry.json"
        registry.parent.mkdir(parents=True)
        registry.write_text(json.dumps({"owner": "new-specialist", "tools": []}))
        with patch.object(tool_state, "ROOT", self.base), patch.dict(os.environ, {}, clear=True):
            self.assertEqual(tool_state.paths("new-specialist")[0], registry)
            for owner in ("../new-specialist", "/tmp/owner", "x/y", ".."):
                with self.assertRaises(ValueError):
                    tool_state.paths(owner)

    def test_malformed_state_is_conservative_and_state_private(self):
        for value in ([], {"environment_id": tool_state.fingerprint(self.base), "tools": []}):
            self.state.write_text(json.dumps(value))
            self.assertIsNone(tool_state.cached("security-standard", "fake", self.base, read_only=True))
        with patch.object(tool_state.shutil, "which", return_value=str(self.executable)):
            tool_state.detect("security-standard", "fake", self.base)
        self.assertEqual(self.state.stat().st_mode & 0o777, 0o600)

    def test_cli_streams_findings_unless_quiet_and_preserves_failure_exit(self):
        self.executable.write_text('#!/bin/sh\nif [ "$1" = "--version" ]; then echo 1.0; else echo synthetic-finding; echo synthetic-diagnostic >&2; exit 7; fi\n')
        for quiet in (False, True):
            with self.subTest(quiet=quiet):
                result = subprocess.run([sys.executable, str(SCRIPT), "security-standard", "fake", "run",
                    "--workspace", str(self.base), *(["--quiet"] if quiet else []), "--", "validate"],
                    capture_output=True, text=True,
                    env={**os.environ, "TOOL_REGISTRY_PATH": str(self.registry), "TOOL_STATE_PATH": str(self.state),
                         "PATH": str(self.base) + os.pathsep + os.environ.get("PATH", "")})
                self.assertEqual(result.returncode, 7)
                self.assertEqual("synthetic-finding" in result.stdout, not quiet)
                self.assertEqual("synthetic-diagnostic" in result.stderr, not quiet)
                self.assertEqual(json.loads(result.stdout.splitlines()[-1])["exit_code"], 7)
                self.assertNotIn("synthetic-finding", self.state.read_text())
                self.assertNotIn("synthetic-diagnostic", self.state.read_text())

    def test_resolution_supports_node_modules_and_venv_scripts(self):
        for directory in ("node_modules/.bin", "venv/Scripts", ".venv/Scripts"):
            with self.subTest(directory=directory):
                local = self.base / directory / "fake-tool"
                local.parent.mkdir(parents=True, exist_ok=True)
                local.write_text("#!/bin/sh\necho 4.2\n")
                local.chmod(0o755)
                self.assertEqual(tool_state.resolve_executable("fake-tool", self.base), str(local))
                local.unlink()

    def test_override_pair_and_registry_owner_are_checked(self):
        self.path_patch.stop()
        with patch.dict(os.environ, {"TOOL_REGISTRY_PATH": str(self.registry)}, clear=True):
            with self.assertRaises(ValueError):
                tool_state.paths("specialist")
        self.registry.write_text('{"owner":"different-owner","tools":[]}')
        with patch.dict(os.environ, {"TOOL_REGISTRY_PATH": str(self.registry), "TOOL_STATE_PATH": str(self.state)}):
            with self.assertRaises(ValueError):
                tool_state.registry_tool("specialist", "fake")

    def test_empty_verification_output_is_not_verified(self):
        self.executable.write_text("#!/bin/sh\nexit 0\n")
        self.assertIsNone(tool_state.probe("security-standard", "fake", self.base))
        self.assertFalse(self.state.exists())

    def test_version_and_failure_state_never_store_arbitrary_output(self):
        self.executable.write_text("#!/bin/sh\necho 'fake-tool 1.2.3 token=synthetic-secret'\n")
        entry = tool_state.detect("security-standard", "fake", self.base)
        self.assertEqual(entry["version"], "1.2.3")
        tool_state.record_failure("security-standard", "fake", self.base, "token=synthetic-secret")
        self.assertNotIn("synthetic-secret", self.state.read_text())

    def test_cached_executable_cannot_redirect_execution(self):
        tool_state.detect("security-standard", "fake", self.base)
        state = json.loads(self.state.read_text())
        state["tools"]["fake"]["executable"] = sys.executable
        self.state.write_text(json.dumps(state))
        before = self.state.read_bytes()
        self.assertIsNone(tool_state.cached("security-standard", "fake", self.base, read_only=True))
        self.assertEqual(before, self.state.read_bytes())


if __name__ == "__main__":
    unittest.main()
