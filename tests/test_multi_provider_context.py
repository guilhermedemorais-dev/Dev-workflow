import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_script(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


provider = load_script(
    "provider_resolver",
    "plugins/dev-workflow-standard/scripts/provider-resolver.py",
)
retriever = load_script(
    "context_retriever",
    "plugins/dev-workflow-standard/scripts/context-retriever.py",
)


class ProviderResolverTests(unittest.TestCase):
    def test_registry_is_secret_free_and_has_nvidia(self):
        registry = provider.load_registry()
        nvidia = provider.provider_by_id(registry, "nvidia")
        self.assertEqual(nvidia["env_key"], "NVIDIA_API_KEY")
        self.assertIn("technology_model_hints", nvidia)
        serialized = json.dumps(registry).lower()
        self.assertNotIn("nvapi-", serialized)
        self.assertNotIn("sk-proj-", serialized)

    def test_unconfigured_provider_is_not_selected(self):
        registry = provider.load_registry()
        previous = os.environ.pop("NVIDIA_API_KEY", None)
        try:
            result = provider.select(registry, "coding", provider_id="nvidia")
        finally:
            if previous is not None:
                os.environ["NVIDIA_API_KEY"] = previous
        self.assertEqual(result["state"], "BLOCKED")

    def test_model_capabilities_are_hints_not_authority(self):
        registry = provider.load_registry()
        nvidia = provider.provider_by_id(registry, "nvidia")
        capabilities = provider.infer_capabilities(nvidia, "org/some-coder-model")
        self.assertIn("coding", capabilities)


class ContextRetrieverTests(unittest.TestCase):
    def test_local_search_respects_allowed_paths_and_required_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "docs").mkdir()
            (root / "private").mkdir()
            (root / "src" / "auth.py").write_text(
                "def authorize_checkout(user):\n    return user.can_checkout\n",
                encoding="utf-8",
            )
            (root / "docs" / "spec.md").write_text(
                "Checkout authorization is mandatory.\n",
                encoding="utf-8",
            )
            (root / "private" / "secret.py").write_text(
                "checkout hidden implementation\n",
                encoding="utf-8",
            )
            required, warnings = retriever.required_sources(
                root, ["docs/spec.md"], ["src/**", "docs/**"]
            )
            hits = retriever.local_search(
                root, "checkout authorization", ["src/**", "docs/**"], 10
            )
            self.assertEqual(warnings, [])
            self.assertEqual(required[0]["path"], "docs/spec.md")
            self.assertTrue(all(not hit.path.startswith("private/") for hit in hits))
            self.assertTrue(any(hit.path == "src/auth.py" for hit in hits))

    def test_secret_files_are_excluded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".env").write_text("API_KEY=checkout-secret", encoding="utf-8")
            (root / "safe.txt").write_text("checkout public context", encoding="utf-8")
            hits = retriever.local_search(root, "checkout", [], 10)
            self.assertEqual([hit.path for hit in hits], ["safe.txt"])


class ArchitecturalContractTests(unittest.TestCase):
    def test_capability_registry_keeps_skill_before_provider(self):
        text = (
            ROOT
            / "plugins/dev-workflow-standard/skills/dev-workflow-standard/references/provider-routing.md"
        ).read_text(encoding="utf-8")
        self.assertIn("owner_skill", text)
        self.assertIn("provider/model resolver", text)
        self.assertIn("Skills define methodology", text)

    def test_retrieval_cannot_replace_required_sources(self):
        text = (
            ROOT
            / "plugins/dev-workflow-standard/skills/dev-workflow-standard/references/context-retrieval.md"
        ).read_text(encoding="utf-8")
        self.assertIn("required_sources", text)
        self.assertIn("cannot be omitted", text)
        self.assertIn("never changes authorization", text)


if __name__ == "__main__":
    unittest.main()
