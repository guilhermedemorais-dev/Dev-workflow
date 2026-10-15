# TASK-055 Windows-native runtime receipt

Task revision 1, scope `native-runtime`, observed 2026-10-14. Actual native
Windows execution, not inferred from package metadata or mocked subprocesses.
Active configuration and installed plugin cache were not migrated.

## Host and isolated preparation

- Windows 10 Home Single Language, CoreSingleLanguage, 22H2, build 19045.6466.
- Existing Microsoft Edge 155.0.4283.45 at Program Files (x86), reused headless
  with isolated profiles. No user browser profile reused.
- No stable standalone Node found in the locations checked. Current PATH Node
  was Codex-internal, npm/npx absent. Prepared official portable Node 24.22.0
  with npm 11.19.1 under `%LOCALAPPDATA%/EngineeringHarness/native-validation`.
- Node archive SHA256 `f9683a19877e12a9b167305c8db71040d812876359de21f0d2e97c3f321f80c3`
  matched the same-version official `https://nodejs.org/dist/v24.22.0/SHASUMS256.txt`.
- Installed only selected pinned packages in distinct user-scoped validation
  prefixes: `@playwright/mcp@0.0.83`, `chrome-devtools-mcp@1.10.1`,
  `n8n-mcp@2.93.0`. Package locks retained outside Git. Actual package engines:
  Playwright `>=18`; Chrome DevTools `^20.19.0 || ^22.12.0 || >=23`;
  n8n MCP `>=20.0.0`. Node satisfies all three.
- Official Claude Code native binary 2.1.300, SHA256
  `56810a111c01dcd218b42727c23fd8763be42320038b1adcac93cf599fac2de2`,
  matched `https://downloads.claude.ai/claude-code-releases/2.1.300/manifest.json`.
- No persistent PATH/registry changes. Native Node direct invocation, no cmd/npm
  wrapper requirement at runtime. Bundled Python was a proof client only, not a
  generated configuration dependency or installation default.

## Actual protocol and operations

All four servers received real JSON-RPC `initialize`, followed by
`notifications/initialized`, `tools/list` and the operations below. The client
checks JSON-RPC errors, MCP `isError`, timeout and expected fixture content.

| Integration | Actual proof | Result | Remaining limits |
| --- | --- | --- | --- |
| Playwright MCP 0.0.83 | `browser_navigate` and `browser_snapshot` on owned loopback HTML fixture through existing Edge | PASS | Local Windows 10 candidate proof, not a declaration of upstream Windows 10 support; server reports Playwright engine `1.64.0-alpha-1790635538000`, not stable certification |
| Chrome DevTools MCP 1.10.1 | `new_page` and `take_snapshot` on same fixture through existing Edge CDP | PASS | Custom Edge worked here; does not expand upstream Chrome support guarantees or validate every CDP tool |
| n8n MCP 2.93.0 | `tools_documentation` and `search_nodes` for webhook, documentation mode | PASS | External n8n instance API/auth and workflow mutation NOT_VALIDATED |
| Claude Code 2.1.300 native | `Read` of owned fixture in isolated config directory | PASS | Account authentication/model execution NOT_VALIDATED; zero LLM requests |

The first Chrome client call omitted now-required `pageId`. That operation
correctly returned `isError` and was recorded FAILED. The client was corrected
to read the created page identifier; only Chrome was rerun, and passed. Original
failure remains in the initial evidence. No server error was relabeled PASS.

## Processes, preservation and memory

Owned native process trees were inspected while each integration ran. No tree
contained `wsl.exe`. Each proof server was started sequentially and only its
owned PID tree was stopped. Zero recorded owned descendant PIDs remained after
cleanup; existing WSL/Codex servers and other applications were not stopped.

Observed process working-set sums during each isolated proof: Playwright
595,181,568 bytes; Chrome DevTools 629,145,600 bytes; n8n MCP 267,177,984 bytes;
Claude 149,209,088 bytes. These are snapshots, not peak/private-memory metrics,
and sums may count shared pages.

The same active Codex configuration was maintained before/after proof. Existing
Windows `wsl.exe` count stayed 24, `wslhost.exe` stayed 14. Aggregate `vmmem`
working set was 430,854,144 bytes before and 432,099,328 after. Background Edge
process count changed from 27 to 11, so the whole-system comparison was not
controlled enough to infer savings. Earlier diagnosis observed vmmem around
1.88 GiB, demonstrating that aggregate VM working set changes independently.
Production before/after improvement remains NOT_VALIDATED until a separately
authorized active migration and controlled client restart.

Read-only diagnosis found three distinct four-integration launch waves under
the same Codex parent, and three actual Linux servers per integration. Parent
and child WSL commands are transport topology, not configuration duplication.
Independent waves may represent different MCP clients/sessions; their exact
client ownership was not established. No cached Guilherme `.mcp.json` was
found. The effective four WSL definitions reside in global `config.toml`.

Global active config SHA256 before and after all preparation/proofs:
`3A2C503B50D5B423C7B50D3F4C823C2E713D14A9C84CAF85FE3773D248C6E362`.
Credentials were not copied into proof environments, and no secret values or
raw command lines were logged. WSL distributions/data preserved.

## Reproducible evidence outside Git

In the parent chat workspace `outputs/`:

- `windows-native-diagnosis.json` and `windows-native-diagnosis.md`, sanitized
  host/config/process baseline and Linux PID classification.
- `native_mcp_validation.py`, actual protocol client and owned loopback fixture.
- `windows-native-runtime-evidence-initial.json`, complete initial pass/failure.
- `windows-native-runtime-evidence-chrome-retry.json`, corrected Chrome proof.
- `windows-native-runtime-evidence.json`, merged passing operations, before/after
  safe PID/memory snapshots, no-WSL trees, remaining-PID and config-digest checks.

Native validation prepares dependencies but does not verify the new plugin
migration generator. That contract requires the separately reported behavioral
tests and independent QA. Linux/WSL runtime routes were preserved, but no new
Linux handshake or macOS machine test was run by this runtime owner.
