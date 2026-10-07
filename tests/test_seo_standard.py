import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_seo_standard_structure():
    base = ROOT / "plugins" / "seo-standard"
    assert (base / "skills" / "seo-standard" / "SKILL.md").is_file()
    assert (base / "runtime" / "bootstrap.py").is_file()
    assert (base / "runtime" / "seo-gateway.py").is_file()
    assert (base / "vendor" / "beyondseo" / "beyondseo-2.9.1-skill.zip").is_file()
    assert (base / "vendor" / "beyondseo" / "LICENSE").stat().st_size > 0

def test_seo_standard_lock_and_registries():
    lock = json.loads((ROOT / "plugins" / "seo-standard" / "runtime" / "runtime.lock.json").read_text())
    assert lock["version"] == "2.9.1"
    assert lock["sha256"] == "e9ab0e9e3a2ef46a9e3b3b3e4699b988fa256dcac91ef5e3539b49b850ac5010"

    codex = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text())
    claude = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    assert any(p["name"] == "seo-standard" for p in codex["plugins"])
    assert any(p["name"] == "seo-standard" for p in claude["plugins"])

    registry = (ROOT / "plugins" / "dev-workflow-standard" / "skills" / "dev-workflow-standard" / "references" / "capability-registry.md").read_text()
    assert "seo-standard" in registry

def test_selected_beyondseo_playbooks_present():
    root = ROOT / "plugins" / "seo-standard" / "skills" / "seo-standard" / "vendor" / "beyondseo" / "playbooks"
    expected = [
        root / "audit" / "conversion-seo-audit.md",
        root / "audit" / "technical-seo-audit.md",
        root / "audit" / "schema-audit.md",
        root / "aeo-geo" / "answer-engine-optimization.md",
        root / "aeo-geo" / "generative-engine-optimization.md",
        root / "keyword-research" / "search-intent-analysis.md",
    ]
    assert all(p.is_file() and p.stat().st_size > 0 for p in expected)
