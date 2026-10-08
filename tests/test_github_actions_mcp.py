"""Safety and idempotency checks for GitHub Actions MCP host configuration."""
import importlib.util
import json
from pathlib import Path
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/dev-environment-standard/skills/dev-environment-standard/scripts/github_actions_mcp.py"
SPEC = importlib.util.spec_from_file_location("github_actions_mcp", SCRIPT)
mcp = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mcp)


class GitHubActionsMcpTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_codex_adds_only_filter_headers_and_preserves_auth_and_servers(self):
        path = self.root / "config.toml"
        path.write_text('''model = "keep"\n\n[mcp_servers.github]\nurl = "https://api.githubcopilot.com/mcp/"\nhttp_headers = { Authorization = "Bearer fixture-secret", "X-MCP-Tools" = "get_me" }\n\n[mcp_servers.other]\nurl = "https://example.test/mcp"\n''')
        self.assertTrue(mcp.update_codex(path))
        data = tomllib.loads(path.read_text())
        github = data["mcp_servers"]["github"]
        self.assertEqual(github["http_headers"]["Authorization"], "Bearer fixture-secret")
        self.assertEqual(github["http_headers"]["X-MCP-Tools"], "get_me,actions_list,actions_get,get_job_logs")
        self.assertEqual(github["http_headers"]["X-MCP-Exclude-Tools"], "actions_run_trigger")
        self.assertEqual(github["http_headers"]["X-MCP-Readonly"], "true")
        self.assertEqual(data["mcp_servers"]["other"]["url"], "https://example.test/mcp")
        self.assertEqual(data["model"], "keep")
        self.assertNotIn("actions_run_trigger", github["http_headers"]["X-MCP-Tools"])
        self.assertFalse(mcp.update_codex(path))

    def test_claude_new_headers_preserve_other_config_and_are_idempotent(self):
        path = self.root / "mcp.json"
        path.write_text(json.dumps({"mcpServers": {
            "github": {"type": "http", "url": "https://api.githubcopilot.com/mcp/",
                       "headers": {"Authorization": "Bearer fixture-secret"}},
            "other": {"command": "fixture", "args": []}}, "keep": True}))
        self.assertTrue(mcp.update_claude(path))
        data = json.loads(path.read_text())
        github = data["mcpServers"]["github"]
        self.assertEqual(github["headers"]["Authorization"], "Bearer fixture-secret")
        self.assertEqual(github["headers"]["X-MCP-Tools"], mcp.TOOLS)
        self.assertEqual(github["headers"]["X-MCP-Exclude-Tools"], "actions_run_trigger")
        self.assertEqual(github["headers"]["X-MCP-Readonly"], "true")
        self.assertEqual(data["mcpServers"]["other"], {"command": "fixture", "args": []})
        self.assertTrue(data["keep"])
        self.assertFalse(mcp.update_claude(path))

    def test_fresh_codex_install_adds_single_uncredentialed_readonly_server(self):
        path = self.root / "config.toml"
        path.write_text('model = "keep"\n')
        self.assertTrue(mcp.update_codex(path))
        data = tomllib.loads(path.read_text())
        server = data["mcp_servers"]["github"]
        self.assertEqual(server["url"], mcp.ENDPOINT)
        self.assertEqual(server["http_headers"]["X-MCP-Tools"], mcp.TOOLS)
        self.assertNotIn("Authorization", server["http_headers"])
        self.assertEqual(data["model"], "keep")
        self.assertFalse(mcp.update_codex(path))

    def test_absent_codex_config_is_created_without_credentials(self):
        path = self.root / "new-config.toml"
        self.assertTrue(mcp.update_codex(path))
        server = tomllib.loads(path.read_text())["mcp_servers"]["github"]
        self.assertEqual(server["url"], mcp.ENDPOINT)
        self.assertNotIn("Authorization", server["http_headers"])
        self.assertFalse(mcp.update_codex(path))

    def test_absent_actions_read_is_reported_only_for_that_repository(self):
        denied = mcp.classify_repository_access("owner/private-a", 200, 200, 403, 403)
        allowed = mcp.classify_repository_access("owner/private-b", 200, 200, 200, 200)
        self.assertEqual(denied["status"], "DENIED_PERMISSION_OR_POLICY")
        self.assertEqual(allowed["status"], "VERIFIED_READ")
        self.assertEqual(denied["repository"], "owner/private-a")
        self.assertEqual(mcp.classify_repository_access("owner/private-c", 404, 404, 404, 404)["status"],
                         "NOT_FOUND_OR_NO_REPOSITORY_ACCESS")

    def test_nonofficial_existing_endpoint_is_not_overwritten(self):
        path = self.root / "config.toml"
        path.write_text('[mcp_servers.github]\nurl = "https://example.test/mcp"\n')
        before = path.read_text()
        with self.assertRaises(ValueError):
            mcp.update_codex(path)
        self.assertEqual(path.read_text(), before)


if __name__ == "__main__":
    unittest.main()
