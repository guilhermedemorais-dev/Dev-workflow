"""Read the routed Harness contract for structural assertions, never for execution.

Agents select one phase; tests inspect the union to preserve legacy coverage.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / 'plugins/dev-workflow-standard/skills/dev-workflow-standard'


def harness_contract():
    migration = json.loads((ROOT / 'docs/workflow-section-migration.json').read_text())
    paths = dict.fromkeys(row['destination'] for row in migration['sections'])
    return '\n'.join((HARNESS / path).read_text() for path in paths)
