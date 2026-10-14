# Platform tool routing, local authorized task

Status: local implementation authorized; remote Issue/PR/publication pending.
Contract revision: 1. Base: 43685daa26c39e56c948ee5d7a759e8b6c2aa21e.

The user explicitly authorized preparing and testing locally while the GitHub connector is disconnected on 2026-10-12. This exception permits local work only, never publication, merge, or claims of complete remote governance. The direct request authorizes the architecture below and excludes implementing the Windows 10 version for now.

## Approved scope and specification

1. Package separate compatibility catalogs named `Tools (Linux)`, `Tools (Windows)`, `Tools (macOS)` inside dev-environment-standard. Inventory all authored executable entrypoints, including Python, Node and shell; exclude vendored dependencies and retain specialist ownership of external-tool registries.
2. Preserve existing shared scripts and paths. The folders select compatible canonical implementations and future adapters; do not duplicate code, create nonexistent Windows/macOS implementations, or change plugin manifests for each user's OS.
3. Extend the existing ignored environment state with a platform binding and selected catalog. First preparation detects the actual execution OS and stores the selection. Reuse it without network discovery or repeated prompts; invalidate on relevant interpreter/runtime/OS/catalog/source drift or actual failure. Linux in WSL is a Linux runtime and must not be represented as native Windows support.
4. Expose exact selected folder, tool eligibility, reason, validation status and reusable state in preparation/status output. Unvalidated platform/tool paths do not count as compatible; do not globally block unrelated compatible external tools or read-only diagnosis.
5. Update bootstrap/Harness instructions so the agent uses the persisted compatible route. Clarify that retrieval via Potpie/local lexical context is supplemental and does not replace environment state.
6. Add README compatibility notice: Linux Mint is user-reported operational, release/distro versions unrecorded; Ubuntu 24.04 WSL has executed suite evidence; native Windows 10/11 and macOS not homologated. Do not claim this task implements Windows support.
7. Add a version/update history grounded in observed commits and manifests. Distinguish unreleased changes from published history, preserve existing manifest versions, explain version/change-note updates for future releases. No updater/webhook or CI platform expansion now.

## Sectors

Database: N/A, no database. Backend: environment CLI selection/cache. Frontend/UI: N/A, no interface. Tests: portable cache/selection/catalog checks plus Linux full-suite regression and Windows baseline evidence. Security: validate catalog paths within plugin root, reject malformed/traversing catalogs, never persist secrets, no implicit installation. Observability: sanitized platform/status receipts. DevOps: N/A, no CI/infrastructure changes. Pending: remote Issue/PR linkage; native Windows/macOS adaptation and real validation deferred. Risk: breaking paths, stale platform binding, confusing catalog availability with runtime compatibility, wrongly blocking unrelated tools.

## Acceptance

- All authored executable entrypoints classified by owner/path with truthful per-platform status.
- Three named folders packaged, canonical paths preserved, no duplicated scripts.
- Stored selection reused with no repeated discovery/prompt; relevant drift invalidates it.
- Unknown/malformed catalog never results in a supported route, path traversal rejected.
- Tests cover Linux, Windows, macOS selection branches without claiming mocked native certification.
- Full suite on native Linux filesystem has no new failures; Windows repeat remains explicit baseline.
- README and CHANGELOG distinguish reported, tested, not validated and unreleased.
- Local reviewable patch and report exported; installation/push/merge not performed.

## Required sources

AGENTS.md; README.md; docs/workflow-pipeline.md; dev-environment-standard SKILL.md and scripts/environment.py; dev-workflow-standard references/context-retrieval.md and skill-owned-tools.md; scripts/tool-state.py; tests/test_environment_bootstrap.py; original Windows/Linux test logs under chat outputs.

## Authorization and equivalence receipt

The local execution contract mirrors this complete local task under revision 1. Its canonical-normative text is this file plus the approved scope above. GitHub human representation is explicitly pending under the user's exception; no equivalence to a nonexistent Issue is claimed. Only one implementation list, platform-tools, is authorized. Required reviewers: functional QA, bounded security review and Harness reconciliation before delivery claims.
