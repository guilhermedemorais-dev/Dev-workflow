"""Package/contract invariants. Operational behavior is reviewed separately.

These tests do not claim infrastructure, authentication or production readiness.
"""

import json
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/devops-standard"
SKILL = PLUGIN / "skills/devops-standard"
SDD = ROOT / "plugins/sdd-spec-factory/skills/sdd-spec-factory"
DOMAINS = (
    "git-release", "ci-cd", "containers", "deployments", "server-operations",
    "infrastructure-as-code", "kubernetes", "gitops", "cloud", "observability",
    "backup-disaster-recovery", "incident-response", "devops-operating-model",
)


class DevOpsPackageTests(unittest.TestCase):
    def test_three_manifests_resolve_same_skill(self):
        for relative in ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
            data = json.loads((PLUGIN / relative).read_text())
            self.assertEqual(data["name"], "devops-standard")
            self.assertEqual(data["version"], "0.1.0")
            self.assertTrue((PLUGIN / data["skills"] / "devops-standard/SKILL.md").is_file())

    def test_marketplaces_have_unique_resolving_entry(self):
        for relative in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
            data = json.loads((ROOT / relative).read_text())
            entries = [item for item in data["plugins"] if item["name"] == "devops-standard"]
            self.assertEqual(len(entries), 1)
            source = entries[0]["source"]
            path = source["path"] if isinstance(source, dict) else source
            self.assertEqual((ROOT / path).resolve(), PLUGIN.resolve())
            self.assertIn(entries[0]["category"], ("Productivity", "development"))
            if isinstance(source, dict):
                self.assertEqual(entries[0]["policy"], {"installation": "AVAILABLE", "authentication": "ON_INSTALL"})

    def test_frontmatter_and_compact_canonical_skill(self):
        text = (SKILL / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\nname: devops-standard\n"))
        self.assertIn("description:", text.split("---", 2)[1])
        self.assertLess(len(text.splitlines()), 500)
        self.assertEqual(len(list(PLUGIN.rglob("SKILL.md"))), 1)

    def test_agent_metadata_invokes_exact_skill(self):
        text = (SKILL / "agents/openai.yaml").read_text()
        self.assertIn("$devops-standard", text)
        self.assertIn("display_name:", text)
        self.assertIn("short_description:", text)

    def test_required_domains_are_discoverable(self):
        text = (SKILL / "SKILL.md").read_text()
        for domain in DOMAINS:
            with self.subTest(domain=domain):
                self.assertTrue((SKILL / "references" / (domain + ".md")).is_file())
                self.assertIn(domain + ".md", text)

    def test_local_markdown_resource_links_resolve(self):
        for path in PLUGIN.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                destination = target.split("#", 1)[0]
                if not destination:
                    continue
                with self.subTest(file=str(path.relative_to(ROOT)), target=target):
                    self.assertTrue((path.parent / destination).exists())

    def test_pinned_provenance_and_restricted_exclusion(self):
        origin = (SKILL / "references/ORIGIN.md").read_text()
        for revision in ("9ba44de0d197c52eb94ecd0c12c8bb394c97d242",
                         "8dc5de47c1db00f8ba01806f5dddd798fc78cf22",
                         "d78be9481b889e11186ec4578b4f5e9301396e25"):
            self.assertIn(revision, origin)
        self.assertIn("NOASSERTION", origin)
        self.assertIn("devops-review", origin)
        self.assertFalse(any(path.name == "devops-review" for path in PLUGIN.rglob("*")))

    def test_full_mit_notices_preserved(self):
        notice = (PLUGIN / "THIRD_PARTY_NOTICES.md").read_text()
        for term in ("Vasiliy Uvarov", "Permission is hereby granted, free of charge",
                     'THE SOFTWARE IS PROVIDED "AS IS"', "AUTHORS OR COPYRIGHT HOLDERS"):
            self.assertIn(term, notice)

    def test_selected_templates_are_real_and_traced(self):
        origin = (SKILL / "references/ORIGIN.md").read_text()
        for name in ("ci-cd-plan.md", "backup-restore-plan.md"):
            self.assertTrue((SKILL / "templates" / name).is_file())
            self.assertIn(name, origin)
        self.assertIn("1cfb8fca3ff704bfb4175ce24567d800fb0bd0f9", origin)
        self.assertIn("71da242bdcbfbe6ec337777d204a9691a9f8e686", origin)

    def test_no_automatic_execution_surface_or_duplicate_installer(self):
        for name in (".mcp.json", "hooks", "scripts", "mcpServers"):
            self.assertFalse((PLUGIN / name).exists())
        self.assertFalse((SKILL / "scripts").exists())
        for manifest in (PLUGIN / ".codex-plugin/plugin.json", PLUGIN / ".claude-plugin/plugin.json"):
            self.assertFalse({"hooks", "mcpServers", "apps"} & json.loads(manifest.read_text()).keys())

    def test_runtime_state_is_ignored_not_tracked(self):
        target = "plugins/devops-standard/skills/devops-standard/runtime-state/tool-state.json"
        check = subprocess.run(["git", "check-ignore", target], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(check.returncode, 0, check.stderr)
        tracked = subprocess.run(["git", "ls-files", target], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(tracked.stdout, "")


class DevOpsIntegrationTests(unittest.TestCase):
    def test_execution_contract_is_lean_and_references_existing_sources(self):
        path = ROOT / "docs/execution/TASK-006.json"
        contract = json.loads(path.read_text())
        self.assertLess(path.stat().st_size, 5000)
        self.assertEqual(contract["task_id"], "TASK-006")
        for reference in [contract["task_path"], *contract["specs"], *contract["docs"], *contract["required_skills"]]:
            self.assertTrue((ROOT / reference).is_file(), reference)
        for validation in contract["required_validations"]:
            self.assertLessEqual(validation.keys(), {"owner", "capability", "preferred_tool"})

    def test_sdd_example_validation_pairs_exist_in_owner_catalog(self):
        tools = {item["id"]: item for item in json.loads((SKILL / "references/tool-registry.json").read_text())["tools"]}
        text = (SDD / "references/devops-planning.md").read_text()
        rows = re.findall(r"\| [^|\n]+ \| devops-standard \| ([^|]+) \| ([^|]+) \|", text)
        self.assertGreaterEqual(len(rows), 7)
        for capability, tool in rows:
            self.assertIn(capability.strip(), tools[tool.strip()]["capabilities"])
        example = json.loads(re.search(r'`(\{"owner":"devops-standard"[^`]+)`', text).group(1))
        self.assertIn(example["capability"], tools[example["preferred_tool"]]["capabilities"])

    def test_sdd_conditional_reference_is_resolvable(self):
        skill = (SDD / "SKILL.md").read_text()
        self.assertIn("references/devops-planning.md", skill)
        self.assertIn("Do not add", skill)
        reference = (SDD / "references/devops-planning.md").read_text()
        self.assertIn("DevOps N/A", reference)

    def test_existing_receipt_and_execution_states_are_reused(self):
        skill = (SKILL / "SKILL.md").read_text()
        self.assertIn("EXECUTION_RECEIPT", skill)
        self.assertIn("SKILL_RECEIPT", skill)
        self.assertFalse(any(path.name.startswith("DEVOPS_RECEIPT") for path in PLUGIN.rglob("*")))
        self.assertIn("devops-standard", (ROOT / "plugins/dev-workflow-standard/skills/dev-workflow-standard/references/capability-registry.md").read_text())

    def test_readme_and_agent_map_expose_real_skill(self):
        for name in ("README.md", "AGENTS.md", "docs/workflow-pipeline.md"):
            text = (ROOT / name).read_text()
            self.assertIn("devops-standard", text)
            self.assertIn("NOT VALIDATED", text)

    def test_environment_not_duplicated_on_absent_base(self):
        self.assertFalse((PLUGIN / "skills/dev-environment-standard").exists())
        self.assertFalse(list(PLUGIN.rglob("mcp-library.json")))
        self.assertIn("NOT VALIDATED", (SKILL / "SKILL.md").read_text())
        self.assertIn("dev-environment-standard", (SKILL / "SKILL.md").read_text())

    def test_security_owner_and_no_parallel_review_gate(self):
        text = (ROOT / "plugins/security-standard/skills/security-standard/SKILL.md").read_text()
        self.assertIn("devops-standard", text)
        self.assertIn("publication gate", text)
        self.assertIn("security-standard", (SKILL / "SKILL.md").read_text())


if __name__ == "__main__":
    unittest.main()
