# Windows native MCP migration and rollback

This owner is Environment Bootstrap, not the OS catalog. The catalog alone cannot
change an executor. Run Python 3.11+ natively on Windows with the explicit source
checkout. No active configuration is migrated by this update.

## Reviewed routes and limits

| Integration | Pinned route | Requirements / limits |
| --- | --- | --- |
| Playwright MCP | @playwright/mcp 0.0.83, Node direct package JS | Node 18+; current upstream supports Windows 11+, not Windows 10. Windows 10 is a conditional candidate requiring explicit consent and actual runtime proof. Reuse selected installed Edge/Chrome. |
| Chrome DevTools MCP | chrome-devtools-mcp 1.10.1, Node direct package JS | Node 20.19+, 22.12+ or 23+; actual Chrome required. Do not infer Edge compatibility. |
| n8n MCP | n8n-mcp 2.93.0, Node direct dist/mcp/stdio-wrapper.js | Node 20+; verified third-party project, not n8n's official remote MCP. stdio defaults preserve user environment values; tools list does not prove authenticated n8n API access. |
| Claude Code | native claude.exe, mcp serve | Official Windows 10 1809+ route. Native sandbox is unsupported; never bypass executor permission controls or add unsafe permission flags. Official native installation is a manual handoff. |

Sources: [Playwright](https://github.com/microsoft/playwright-mcp),
[Chrome DevTools](https://github.com/ChromeDevTools/chrome-devtools-mcp),
[n8n MCP](https://github.com/czlonkowski/n8n-mcp),
[Claude Code](https://code.claude.com/docs/en/setup).
The adapter distinguishes WINDOWS_NATIVE, WSL and LINUX. Legacy Linux/WSL
prepare routes remain available; Windows target routes cannot silently create
npx/WSL wrappers. Stable external Node and its matching npm-cli.js are reused,
not Codex internal runtimes or transient npx paths. Choose a durable user-owned
prefix outside temporary/cache/Codex installation directories.

## Explicit installation and migration

PowerShell examples are templates, not instructions to apply this notebook now.
Set `$envScript` to the canonical environment.py path, `$configPath` to the reviewed
Codex TOML, and `$prefixPath` to durable external storage. Do not put credentials
in these commands. The commands accept only catalog provider IDs.

```powershell
py -3.11 $envScript native-install-plan --host codex --host-config $configPath --native-prefix $prefixPath --select n8n --json
py -3.11 $envScript native-install --host codex --host-config $configPath --native-prefix $prefixPath --select n8n --approved-fingerprint REVIEWED_INSTALL_FINGERPRINT --json
py -3.11 $envScript native-plan --host codex --host-config $configPath --native-prefix $prefixPath --select n8n --json
py -3.11 $envScript native-apply --host codex --host-config $configPath --native-prefix $prefixPath --select n8n --approved-fingerprint REVIEWED_CONFIG_FINGERPRINT --backup-dir PRIVATE_BACKUP_DIRECTORY --json
py -3.11 $envScript native-rollback --host codex --host-config $configPath --native-prefix $prefixPath --rollback-receipt RETURNED_RECEIPT_PATH --json
```

Repeat `--select` for explicitly selected integrations; no selection is rejected.
Add `--allow-conditional-windows10` only for reviewed Playwright Windows 10 use.
Use --native-node, --native-claude and --native-browser for reviewed durable
external paths when they are not on PATH. Runtime/browser file bytes are bound
to the approved fingerprint, not only their names. Chrome DevTools with an
explicit Edge override is a conditional locally tested candidate requiring
--allow-conditional-windows10; upstream Chrome support is not claimed for Edge.
Add each effective plugin-supplied MCP JSON using `--plugin-config PATH`; effective
manifest definitions must be enumerated by the executor, not presumed absent.
Alias/package identity collisions across global and plugin definitions block
migration until explicitly reconciled. Wrapper process repetition is not proof
of duplicate server instances: inspect PID, parent PID, session/client owner and
command chain first. The CLI never starts servers during diagnosis/planning.

Installation executes the exact selected pinned argument-array plan after its
fingerprint is approved; captured installer output is not logged. Claude's
native official installer requires separate approved execution. Missing native
runtime/browser/package prerequisites remain blockers, never WSL fallbacks.

Migration changes only reviewed command/args and registration, preserving disabled
flags, unknown TOML fields, comments, credentials and environment. A simple WSL
exec route may carry reviewed headless/isolated preferences. Structured `env
KEY=value ... executable` is normalized privately, with inline values retaining
precedence. Shell strings, arbitrary options and complex TOML assignments stop
for manual normalization rather than silently dropping credentials/preferences.
No unsupported Edge substitution or `--no-sandbox` flag is introduced.

Plans report sanitized identities, transport and credential presence only; raw
configuration/content never appears in CLI reports. Fingerprints cover selected
commands, runtime paths, package/source/config/plugin definitions. Changes after
planning require a new reviewed plan. Private backup plus rollback receipt are
written before mutation using the existing restrictive file helper. Rollback
checks backup integrity and the exact post-migration hash; subsequent edits block
rollback instead of overwriting newer settings. Rollback rechecks the target after reading/verifying the backup. Atomic replacement
prevents partial writes; an irreducible check-to-replace concurrency window remains,
so the executor must serialize configuration writers during application/rollback.
Original bytes and newline style
are restored, including CRLF and Unicode. Protect backups as credentials.

## Startup and runtime evidence

Codex MCP `enabled=false` is an explicit client selection control. No verified
lazy process-start contract is assumed: tool discovery/deferred tool presentation
is not proof of lazy server spawning. Enable only task-selected integrations;
others remain at their existing choice until the user explicitly requests a
selection change. The adapter does not silently disable unrelated definitions.

Installation/configuration returns NOT_VALIDATED. Run MCP initialize, tools/list
and an authorized harmless representative tools/call separately for every selected
server; record exact package/browser/Windows edition/build versions and executable
paths. A version command or tools/list alone does not prove the representative
operation or authentication. Inspect owned process trees for absence of wsl.exe.
Compare process count and working-set memory under the same client/session/server
conditions before/after. Do not attribute another application's WSL consumption
to this plugin; vmmem aggregate is not per-tool evidence. Active notebook before/
after migration comparison remains pending until separately authorized. Isolated
native process validation cannot claim active-client migration savings.
