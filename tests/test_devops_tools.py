"""DevOps catalog and real-process helper regressions, without network/infra."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/dev-workflow-standard/scripts/tool-state.py"
REGISTRY = ROOT / "plugins/devops-standard/skills/devops-standard/references/tool-registry.json"
EXPECTED_REPOS = {
    "git": "git/git", "gh": "cli/cli", "docker": "docker/cli",
    "docker-compose": "docker/compose", "terraform": "hashicorp/terraform",
    "tofu": "opentofu/opentofu", "ansible": "ansible/ansible",
    "ansible-lint": "ansible/ansible-lint", "kubectl": "kubernetes/kubernetes",
    "helm": "helm/helm", "kustomize": "kubernetes-sigs/kustomize",
    "argocd": "argoproj/argo-cd", "flux": "fluxcd/flux2",
    "actionlint": "rhysd/actionlint", "act": "nektos/act",
    "hadolint": "hadolint/hadolint", "tflint": "terraform-linters/tflint",
    "kubeconform": "yannh/kubeconform", "shellcheck": "koalaman/shellcheck",
    "promtool": "prometheus/prometheus",
}


class DevOpsRegistryTests(unittest.TestCase):
    def catalog(self):
        self.assertTrue(REGISTRY.is_file(), "DevOps tool registry is missing")
        data = json.loads(REGISTRY.read_text())
        self.assertEqual(data["schema_version"], 1)
        self.assertEqual(data["owner"], "devops-standard")
        tools = {item["id"]: item for item in data["tools"]}
        self.assertEqual(len(tools), len(data["tools"]), "duplicate tool IDs")
        return tools

    def test_exact_catalog_has_twenty_official_sources(self):
        tools = self.catalog()
        self.assertEqual(set(tools), set(EXPECTED_REPOS))
        for name, repo in EXPECTED_REPOS.items():
            with self.subTest(tool=name):
                self.assertEqual(tools[name]["repository"], "https://github.com/" + repo)

    def test_each_tool_has_capability_executable_verification_and_install_policy(self):
        for item in self.catalog().values():
            with self.subTest(tool=item["id"]):
                self.assertTrue(item["capabilities"])
                self.assertTrue(all(isinstance(cap, str) and cap for cap in item["capabilities"]))
                self.assertNotIn(" ", item["command"])
                self.assertIsInstance(item["verify_args"], list)
                self.assertTrue(item["verify_args"])
                self.assertIn("approved", item["install_policy"])
                self.assertNotIn("executable", item)
                self.assertNotIn("installed", item)

    def test_security_tools_have_single_owner(self):
        security = json.loads((ROOT / "plugins/security-standard/skills/security-standard/references/tool-registry.json").read_text())
        self.assertFalse(set(self.catalog()) & {tool["id"] for tool in security["tools"]})

    def test_compose_is_a_docker_subcommand(self):
        compose = self.catalog()["docker-compose"]
        self.assertEqual(compose["command"], "docker")
        self.assertEqual(compose["verify_args"], ["compose", "version"])

    def test_cluster_detection_is_client_only(self):
        tools = self.catalog()
        for name in ("kubectl", "argocd", "flux"):
            self.assertEqual(tools[name]["verify_args"], ["version", "--client"])

    def test_terraform_and_tofu_are_declared_alternatives(self):
        tools = self.catalog()
        self.assertEqual(tools["terraform"]["alternative_group"], "infrastructure-as-code")
        self.assertEqual(tools["tofu"]["alternative_group"], "infrastructure-as-code")

    def test_act_is_optional(self):
        self.assertTrue(self.catalog()["act"]["optional"])

    def test_nonstandard_version_flags_match_cli_interfaces(self):
        tools = self.catalog()
        self.assertEqual(tools["actionlint"]["verify_args"], ["-version"])
        self.assertEqual(tools["kubeconform"]["verify_args"], ["-v"])
        self.assertEqual(tools["helm"]["verify_args"], ["version", "--short"])


class DevOpsHelperProcessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.workspace = self.base / "project"
        self.workspace.mkdir()
        self.bin = self.base / "bin"
        self.bin.mkdir()
        self.tool = self.bin / "fixture-tool"
        self.tool.write_text(
            "#!/bin/sh\n"
            'if [ "$1" = "--version" ]; then echo 1.0; exit 0; fi\n'
            'if [ "$1" = "fail" ]; then exit 7; fi\n'
            'if [ "$1" = "check" ]; then test -f accepted; exit $?; fi\n'
            'if [ "$1" = "literal" ]; then printf "%s\\n" "$2"; exit 0; fi\n'
            "exit 9\n"
        )
        self.tool.chmod(0o755)
        self.registry = self.base / "registry.json"
        self.registry.write_text(json.dumps({"tools": [{"id": "fixture", "command": "fixture-tool",
            "verify_args": ["--version"], "repository": "https://github.com/example/fixture"}]}))
        self.state = self.base / "state.json"
        self.env = {**os.environ, "PATH": str(self.bin), "PYTHONDONTWRITEBYTECODE": "1",
                    "TOOL_REGISTRY_PATH": str(self.registry), "TOOL_STATE_PATH": str(self.state)}

    def invoke(self, action, *args, owner="dev-implementation-standard", workspace=None):
        return subprocess.run([sys.executable, str(SCRIPT), owner, "fixture", action,
            "--workspace", str(workspace or self.workspace), "--", *args], env=self.env,
            cwd=self.base, capture_output=True, text=True, timeout=10)

    def receipt(self, process):
        self.assertTrue(process.stdout.strip(), "helper did not return a structured receipt: " + process.stderr)
        return json.loads(process.stdout.strip().splitlines()[-1])

    def test_devops_owner_supported_with_installed_bundle_overrides(self):
        process = self.invoke("detect", owner="devops-standard")
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(self.receipt(process)["status"], "installed")
        self.assertEqual(json.loads(self.state.read_text())["tools"]["fixture"]["version"], "1.0")

    def test_run_uses_requested_workspace(self):
        (self.workspace / "accepted").touch()
        process = self.invoke("run", "check")
        self.assertEqual(self.receipt(process)["exit_code"], 0)
        self.assertEqual(process.returncode, 0)

    def test_cli_propagates_validator_failure(self):
        process = self.invoke("run", "fail")
        self.assertEqual(self.receipt(process)["exit_code"], 7)
        self.assertEqual(process.returncode, 7)

    def test_fail_fix_revalidate_retains_real_initial_and_final_results(self):
        first = self.invoke("run", "check")
        self.assertEqual(first.returncode, 1)
        self.assertEqual(self.receipt(first)["exit_code"], 1)
        (self.workspace / "accepted").touch()
        final = self.invoke("run", "check")
        self.assertEqual(final.returncode, 0)
        self.assertEqual(self.receipt(final)["exit_code"], 0)
        self.assertEqual(self.receipt(final)["tool_state_source"], "cached-installed")

    def test_missing_tool_never_installs(self):
        self.tool.unlink()
        process = self.invoke("run", "check")
        self.assertEqual(process.returncode, 2)
        self.assertEqual(self.receipt(process)["status"], "missing")
        self.assertFalse(self.state.exists())

    def test_cached_execution_does_not_repeat_version_probe(self):
        first = self.invoke("detect")
        self.assertEqual(first.returncode, 0)
        self.tool.write_text("#!/bin/sh\n[ \"$1\" = \"--version\" ] && exit 8\nexit 0\n")
        second = self.invoke("run", "check")
        self.assertEqual(second.returncode, 0)
        self.assertEqual(self.receipt(second)["tool_state_source"], "cached-installed")

    def test_workspace_change_does_not_reuse_other_project_state(self):
        self.assertEqual(self.invoke("detect").returncode, 0)
        other = self.base / "other"
        other.mkdir()
        process = self.invoke("run", "--version", workspace=other)
        self.assertEqual(process.returncode, 0)
        self.assertEqual(self.receipt(process)["tool_state_source"], "detected-existing")

    def test_deleted_cached_executable_becomes_missing(self):
        self.assertEqual(self.invoke("detect").returncode, 0)
        self.tool.unlink()
        process = self.invoke("run", "check")
        self.assertEqual(process.returncode, 2)
        self.assertEqual(self.receipt(process)["status"], "missing")
        self.assertEqual(json.loads(self.state.read_text())["tools"]["fixture"]["status"], "stale")

    def test_missing_workspace_returns_structured_error_without_state_writes(self):
        process = self.invoke("run", "check", workspace=self.base / "missing-project")
        self.assertNotEqual(process.returncode, 0)
        self.assertEqual(self.receipt(process)["status"], "invalid_workspace")
        self.assertFalse(self.state.exists())

    def test_file_workspace_does_not_invalidate_cached_executable(self):
        self.assertEqual(self.invoke("detect").returncode, 0)
        initial = self.state.read_bytes()
        process = self.invoke("run", "check", workspace=self.registry)
        self.assertNotEqual(process.returncode, 0)
        self.assertEqual(self.receipt(process)["status"], "invalid_workspace")
        self.assertEqual(self.state.read_bytes(), initial)
        self.assertTrue(self.tool.is_file())

    def test_arguments_are_not_evaluated_by_shell(self):
        process = self.invoke("run", "literal", "$(touch unsafe-marker)")
        self.assertEqual(process.returncode, 0)
        self.assertIn("$(touch unsafe-marker)", process.stdout)
        self.assertFalse((self.base / "unsafe-marker").exists())
        self.assertFalse((self.workspace / "unsafe-marker").exists())

    def test_compose_detection_and_execution_use_explicit_subcommand(self):
        self.tool.write_text("#!/bin/sh\n"
            '[ "$1" = "compose" ] || exit 8\n'
            '[ "$2" = "version" ] && { echo 2.0; exit 0; }\n'
            '[ "$2" = "config" ] && exit 0\nexit 9\n')
        self.registry.write_text(json.dumps({"tools": [{"id": "fixture", "command": "fixture-tool",
            "verify_args": ["compose", "version"], "repository": "https://github.com/docker/compose"}]}))
        process = self.invoke("run", "compose", "config")
        self.assertEqual(process.returncode, 0)
        self.assertEqual(self.receipt(process)["tool_version"], "2.0")
        missing_prefix = self.invoke("run", "config")
        self.assertEqual(missing_prefix.returncode, 8)


if __name__ == "__main__":
    unittest.main()
