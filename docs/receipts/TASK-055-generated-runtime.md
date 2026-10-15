# TASK-055 generated transport integration proof

Contract revision1, local native-runtime validation scope. On Windows10 Home
Single Language22H2 build19045.6466, the actual final NativeMCP.prepare code
generated transport definitions from self-owned synthetic Codex TOML fixtures
using the observed WSL `-d kali-linux -- /home/.../executable` shape. Explicit
external Node24.22.0/npm11.19.1, Claude2.1.300 and installed Edge155.0.4283.45
overrides selected; Playwright/Edge conditional consent supplied for this test.
No active notebook config was copied or migrated; fixtures contain no real secrets.

Actual installed npm package.json metadata was read by the generator. Chrome's
two-bin dictionary and leading ./ initially caused a real generator rejection.
Implementation now selects the exact reviewed bin_key, normalizes benign ./
and rejects traversal/absolute/arbitrary entrypoints. Initial Playwright PASS
and subsequent Chrome generator failure remain historical in outputs; final
code generated all four native transports and executed all four proofs again.

| Generated integration | Real protocol/operation | Final result |
| --- | --- | --- |
| Playwright0.0.83 | initialize, tools/list, navigate and snapshot on owned loopback HTML | PASS |
| Chrome DevTools1.10.1 | initialize, tools/list, new_page and take_snapshot with returned pageId | PASS |
| n8n MCP2.93.0 | initialize, tools/list, tools_documentation and search_nodes | PASS |
| Claude Code2.1.300 | initialize, tools/list, Read of owned fixture | PASS |

Evidence script outputs/native_generated_validation.py outside repository;
sanitized evidence outputs/windows-native-generated-evidence.json under the
parent workspace. It invokes actual returned command/args, not a parallel
hard-coded transport. All MCP isError/protocol/timeouts and fixture content
checked. Every owned process tree had zero wsl.exe descendants, and the final
snapshot contained zero recorded owned PIDs after cleanup. Existing servers
were not stopped. No credentials, model requests or external n8n API calls used.

Active config before/after SHA256:
3a2c503b50d5b423c7b50d3f4c823c2e713d14a9c84caf85fe3773d248c6e362.
Installed plugin cache, PATH and registry unchanged. Tool assets remain isolated
in persistent user-scoped validation storage; active-client rollout NOT_VALIDATED.

Support limits remain: upstream Playwright currently requires Windows11+ and
reports an alpha engine; this is only a local Windows10 operational proof. Edge
CDP works here but is not a declaration of official Chrome MCP Edge support.
External n8n instance/auth, Claude model/auth, all tools and Linux/WSL handshakes
NOT_VALIDATED. Existing Linux/WSL code paths are covered by structural regression,
not fresh Linux platform certification. Memory evidence from the separate
runtime receipt does not establish controlled production savings.
