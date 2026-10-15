# TASK-056 real Windows10 lifecycle evidence

Revision1 local validation. Windows10 Home Single Language/CoreSingleLanguage,
22H2, build19045.6466, independently re-read from host registry. Native Node24.22.0,
Edge155.0.4283.45, PlaywrightMCP0.0.83, ChromeDevToolsMCP1.10.1, n8nMCP2.93.0,
ClaudeCode2.1.300. Python3.12.14 bundled QA interpreter used only for this proof;
production generation rejects internal/temporary runtimes and requires a stable
external Python3.11+ installation. No production runtime configured or installed.

Executed the actual native adapter's reviewed `prepare` and `lifecycle_prime`
against private isolated fixture configs, then launched the actual stdio proxy.
Each selected prime initialized/listed metadata and stopped its owned native tree.
Proxy initialize/tools-list/status returned cached metadata with no Node/Claude/
browser child. A Windows conhost companion belongs to the lightweight front-end,
it is neither a second integration nor a browser. No secret-bearing commands,
environment or upstream stderr were logged.

Actual operations: Playwright navigate then snapshot of an owned loopback HTML
page; Chrome DevTools new_page then take_snapshot of the same fixture; n8n public
tools_documentation/search_nodes; Claude Read of an owned fixture file, zero LLM
requests. Browser state persisted and each workflow reused exactly one upstream
PID. Explicit finish returned STOPPED, all previously observed owned upstream/
browser PIDs absent, no owned wsl.exe descendant in any integration.

## Scoped working-set observations, MiB

| Integration | Result | Initial lightweight front-end and conhost | Running heavy owned subtree | After finish lightweight front-end and conhost | Remaining heavy PIDs |
| --- | --- | ---: | ---: | ---: | ---: |
| playwright | PASS | 32.19 | 585.97 | 32.59 | 0 |
| chrome-devtools | PASS | 32.17 | 601.75 | 32.62 | 0 |
| n8n | PASS | 32.12 | 255.11 | 32.55 | 0 |
| claude-code | PASS | 32.36 | 152.33 | 32.85 | 0 |

These are scoped working-set snapshots under the same preserved host config,
not private-memory allocations or a whole-machine benchmark. Front-end and heavy
subtree columns are separate sets. Lightweight front-ends remain available for
their live MCP connections. Existing applications and WSL clients remained intact;
aggregate vmmem cannot be assigned to the plugin. No production savings claimed.

## Integrity and limitations

Source hashes before/after proof match exactly; owned-machine config SHA256 remains
`3a2c503b50d5b423c7b50d3f4c823c2e713d14a9c84caf85fe3773d248c6e362`.
Sanitized per-provider process/PID/memory/source evidence is recorded in
`TASK-056-runtime-evidence.json`. Raw proof artifact remains in local outputs as
`TASK-056-native-lifecycle-evidence.json`, SHA256
`0164ccdc8e690bbaaf05282fb7f74e4125a9583eeff47b97a1cb8ccf09b705dc`.

Playwright/Edge on Windows10 remain actual local conditional proofs, not blanket
vendor support certification. n8n authenticated instance, Claude model/API auth,
active Codex client migration/approval UI, real POSIX/macOS execution and total
machine RAM savings are NOT_VALIDATED. Existing Linux/WSL direct routes were
preserved and structural regressions are covered by the full suite separately.
The adapter runs from the canonical checkout and reuses its Harness private-state
helper; this is not a standalone copied Python executable.

Historical failures were retained: initial listChanged rejection, tools/resources
capability rejection, an overly strict verifier treating conhost as a heavy
integration, harmless Playwright notifications and source-change-during-prime
refusal. Corrections compare exact metadata without replaying mutations; final
four-provider proof passed on unchanged source. No active config/cache migration,
existing server termination, WSL data removal or remote publication occurred.
