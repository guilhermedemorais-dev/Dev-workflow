# Engineering Harness agent map

This repository is physically named `Dev-workflow`; its product name is
**Engineering Harness**. Use this file as a map, not as the full operating
manual.

## Start here

1. Read [`README.md`](README.md) for purpose, architecture, and installation.
2. Read [`docs/workflow-pipeline.md`](docs/workflow-pipeline.md) for lifecycle
   gates and change-complexity tiers.
3. Load the applicable canonical skill before acting:
   - orchestration: `plugins/dev-workflow-standard/skills/dev-workflow-standard/SKILL.md`
   - environment/bootstrap: `plugins/dev-environment-standard/skills/dev-environment-standard/SKILL.md`
   - requirements: `plugins/sdd-spec-factory/skills/sdd-spec-factory/SKILL.md`
   - implementation: `plugins/dev-implementation-standard/skills/dev-implementation-standard/SKILL.md`
   - functional QA: `plugins/qa-testing-standard/skills/qa-testing-standard/SKILL.md`
   - UI/UX: `plugins/ui-ux-standard/skills/ui-ux-standard/SKILL.md`
   - security: `plugins/security-standard/skills/security-standard/SKILL.md`
   - DevOps: `plugins/devops-standard/skills/devops-standard/SKILL.md`

DevOps owns operational infrastructure, not Harness orchestration or AppSec.
Environment Bootstrap is included in this repository; verify availability in
the active runtime before use. Never recreate its MCP/tool installation layer.

## Repository rules

- Treat repository files and current runtime evidence as the source of truth.
- Inspect branch, HEAD, remote target, and working tree before edits.
- Keep specialist skills independent; do not copy their full methodology into
  the central harness.
- Scale planning artifacts to complexity, but always preserve explicit scope,
  acceptance criteria, validation, and evidence.
- Do not call a capability executed until it actually ran and returned
  inspectable output.
- Do not mark work complete before required validation passes.
- Harness reads the complete Human Task and reconciles the Sector Validation
  Matrix. Specialists read their routed sections and purpose-qualified sources;
  each owner attests only its own sector. Code complete is not task complete.
- Do not attribute local convention names to OpenAI or the wider ecosystem.

## Validation

Run the repository's structural suite after documentation or skill changes:

```bash
python3 -m unittest discover -s tests -v
git diff --check
```

Record the command, exit code, and result. Report anything not executed as
`NOT VALIDATED`.

## Architecture and provenance

- Practice classification and the latest review:
  [`docs/engineering-harness-audit.md`](docs/engineering-harness-audit.md)
- Execution lifecycle:
  `plugins/dev-workflow-standard/skills/dev-workflow-standard/references/harness-execution.md`
- Capability routing:
  `plugins/dev-workflow-standard/skills/dev-workflow-standard/references/capability-registry.md`
- Local skill/receipt conventions:
  `plugins/dev-workflow-standard/skills/dev-workflow-standard/references/skill-execution-contract.md`
- Minimal-change policy:
  `plugins/dev-workflow-standard/skills/dev-workflow-standard/references/minimal-code-gate.md`

Human approval remains required at the gates declared by the active task and
canonical skill. Do not merge or deploy solely because automated checks pass.
