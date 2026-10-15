# TASK-055 Security receipt

Contract revision: 1. Execution list: `native-security`. Observed 2026-10-14.
SECURITY_STATUS: PASS for the bounded configuration/install/rollback change
review. This is neither production approval nor an active-notebook migration.

## SKILL_RECEIPT and authority

Security Standard SKILL read completely. Required phase references applied:
review-pipeline, coverage-model, finding-standard, false-positive-validation,
stack-profiles and report-template. The current canonical JSON and Harness
dispatch explicitly attest revision-1 local normative equivalence. No remote
Issue exists for this local-only contract; remote synchronization is not claimed.

Mode: Change Review. Risk: HIGH, because credential-bearing configuration,
executable selection, package installation and private backups cross sensitive
local trust boundaries. No active config, cache, credentials, Linux data,
existing process trees, GitHub objects or TASK-054 work was modified by Security.
Only this receipt was written. No application/package-wide audit was requested.

## Protected boundary and traced controls

Assets: credential-bearing TOML/environment, existing preferences, user runtime
selection, approved executable identity, private backup and subsequent edits.
Actor: authorized local operator. Inputs: explicit provider IDs, config/prefix,
effective plugin definitions, native overrides, fingerprint and rollback receipt.
Effects: selected npm installation or private atomic config replacement.

- Explicit unique known provider selection produces pinned argument arrays,
  invokes subprocess without a shell and never adds permission bypass flags.
  npm package lifecycle code remains part of the explicitly approved package
  installation trust boundary; this review does not certify dependencies.
- Stable external executable discovery rejects Codex cache/temp paths. Invalid
  explicit overrides fail closed. Missing native prerequisites do not select WSL.
- Package name/version/entrypoint are checked against reviewed metadata; package
  script resolves inside its package directory. Fingerprints bind config,
  adapter source, supplied plugin definitions, package metadata/entrypoints and
  discovered Node/npm/Claude/browser bytes, plus the plan/selection/host facts.
- Known global/plugin aliases collide before mutation. Caller must enumerate
  effective plugin definitions; absence of a supplied manifest is not universal
  proof of no plugin registration. Unsupported wrapper options are rejected.
- Structured WSL argv is parsed rather than executed. Shell wrappers and unknown
  positional/options require manual reconciliation; inline env precedence is
  preserved privately. Existing disabled/preference/TOML fields are retained.
- CLI strips private generated content before JSON printing; fixed generic
  errors and captured installer output avoid credential/raw-command disclosure.
- Existing atomic writer creates protected owner/SYSTEM Windows DACL before
  writing bytes, validates file identity/reparse safety and atomically replaces.
  Backup is byte-exact, its hash is checked during rollback; config hashes are
  rechecked before commit/restore, and duplicate backup receipts are rejected.

## Independent validation and correction trace

The initial 17-test native suite passed, but independent fixture review found
two missing safeguards. These were reported to Harness and fixed by
Implementation, not silently patched by Security:

1. A same-path fixture `claude.exe` byte replacement originally retained the
   approval fingerprint. Fingerprints now include actual executable bytes;
   package manifests cannot choose an unreviewed alternative entrypoint.
2. A config edit injected during backup reading was originally overwritten by
   rollback. Rollback now rechecks the config after verifying backup integrity.

These are bounded approval-integrity/preservation defects with deterministic
local evidence, not assertions of remotely exploitable compromise. After the
fix, independently rerunning the same isolated reproductions showed executable
replacement invalidates approval and rollback rejects/preserves the late edit.
The fixtures used only a TemporaryDirectory and synthetic executable/config
bytes; no actual notebook settings or secret was copied.

Final independent command: bundled Python 3.11-compatible proof runner,
`-m unittest discover -s tests -p test_windows_native_mcp.py -v`.
Result: **26 tests PASS**, 0.584 seconds. Bundled Python is a test executor,
not a generated MCP runtime dependency. The earlier PATH Python resolved to
the Microsoft Store alias and failed; no installation was performed to hide it.
Meaningful cases include secret sentinel non-disclosure/preservation, byte-exact
rollback, late-edit rejection, executable/package drift, approved selection,
global/plugin collisions, shell/unknown-argument rejection and native overrides.

## Frozen artifacts reviewed

SHA256 of final independently tested files:

| File | SHA256 |
| --- | --- |
| `plugins/dev-environment-standard/skills/dev-environment-standard/scripts/native_mcp.py` | `c66ba5156384bf9a979b958066c3a6b2423bffc21abba6a53d40e2343ab23ac3` |
| `plugins/dev-environment-standard/skills/dev-environment-standard/scripts/environment.py` | `daed63796482e6a1e7361f8165260bd4a1769c196501498df9f62f6336950896` |
| `tests/test_windows_native_mcp.py` | `0a988efa75bc7432aa451a5609342cd4d03456898df0f3981ba954b5235de6a2` |
| `docs/windows-native-mcp-migration.md` | `475c610cb0ba5fa1c5b9f31bf1d17c69380910a6cf3d428ed60ad637606fea3f` |

## Coverage and limits

| Layer/surface | Status | Evidence or limit |
| --- | --- | --- |
| Banco | NOT_APPLICABLE | No database/product schema changes |
| API/Backend | REVIEWED | CLI parser, provider identity, argv, wrapper/env normalization |
| Frontend/UI | NOT_APPLICABLE | No product UI changes; browser fixture proof belongs to runtime owner |
| Infra/DevOps | REVIEWED | Native discovery, selected installation/configuration, private atomic backup/rollback |
| Dependencias/Supply Chain | REVIEWED, bounded | Pinned identity/entrypoint and explicit approval; full dependency vulnerability audit excluded |
| Privacidade/Observabilidade | REVIEWED | Secret-preserving content, stripped plans, generic errors, no subprocess output logging |

Runtime owner receipt records actual Windows 10 handshakes and representative
operations for four integrations, no owned WSL launches and unchanged active
config digest. Those tests do not certify all tools, upstream Windows-10 support,
Claude account/model execution, authenticated n8n management or memory savings.
No active migration means its production before/after comparison remains
NOT_VALIDATED. Linux/WSL routes were preserved; new Linux/macOS live handshake
testing is outside this Security execution.

Residual writer constraint: these are hash guards plus atomic replacement,
not an OS-wide transaction lock against another writer changing config after
the last guard. A later authorized migration must serialize edits/client writes.
Executable/entrypoint hashes do not attest the entire transitive package tree.
No unresolved release-blocking finding remains in this bounded reviewed slice.
Any code/hash drift requires renewed relevant verification before using this
receipt. Harness owns overall acceptance and the user's later migration decision.

## Superseding final review after real-metadata correction

The preceding 26-test hashes describe the earlier frozen candidate, not final
acceptance of later source changes. A real generated-transport proof exposed
Chrome's two-bin manifest and harmless `./` entrypoint prefixes. These functional
failures were retained, then Implementation corrected selection using each
reviewed provider's explicit `bin_key`; the canonical path is still allowlisted
and hashed. No arbitrary bin value, traversal, absolute path or backslash path
is permitted. Only harmless POSIX `./` normalization is accepted.

The migration policy moved byte-identically into Environment-owned references
and is a mandatory local SKILL link; the root docs file is a pointer. This fixes
plugin-distribution availability without duplicating policy or changing trust.

Independent final verification: **28 native tests PASS**, 0.485 seconds, plus
five isolated negative entrypoint fixtures PASS: parent traversal, absolute
path, backslashes, arbitrary script and wrong bin key all rejected. Existing
runtime-byte/rollback-late-edit regression checks remain in the passing suite.
The no-active-migration constraint and all coverage/residual limits above apply.
Final SECURITY_STATUS: **PASS for this final bounded artifact**, replacing the
earlier candidate's source binding. Whole-package/API/auth assurance is excluded.

| Final file | SHA256 |
| --- | --- |
| `plugins/dev-environment-standard/skills/dev-environment-standard/scripts/native_mcp.py` | `56364ef284715afe1d4facc1e1f3775b81c399dbd1c71f6259c344c0c88fdbb8` |
| `plugins/dev-environment-standard/skills/dev-environment-standard/scripts/environment.py` | `daed63796482e6a1e7361f8165260bd4a1769c196501498df9f62f6336950896` |
| `tests/test_windows_native_mcp.py` | `57ec7be42dc59672ffeda2cb98dd59d06948b4112b18b18dd9855ca2236d73dd` |
| `plugins/dev-environment-standard/skills/dev-environment-standard/references/windows-native-mcp-migration.md` | `475c610cb0ba5fa1c5b9f31bf1d17c69380910a6cf3d428ed60ad637606fea3f` |
| `docs/windows-native-mcp-migration.md` | `87630d3ae6cbbbe3275175f9f06fcb0dc23ba9e63e5bb0992023c78beb918db9` |
