# On-demand MCP lifecycle

Opt-in Environment adapter for the four reviewed Windows-native stdio providers.
It does not rewrite active configuration or install itself on startup. Direct
native, Linux and WSL routes remain available. No host-side lazy-start setting is
invented: a small Python front-end remains alive for client metadata discovery,
while the selected Node/Claude server and its owned browser processes stay stopped.

## Preparation and separate application

Reuse the native plan, stable external Node/browser/Claude installation, provider
identity/pins and global/plugin duplicate checks from the Windows migration owner.
Supply an external stable Python3.11+ installation for the front-end. Temporary or
internal Codex runtimes are prohibited in generated production configuration.
No new runtime is installed automatically.

1. `native-plan --select PROVIDER` is read-only. Review its fingerprint.
2. `native-lifecycle-prime --select PROVIDER --lifecycle-cache PRIVATE_DIRECTORY
   --approved-fingerprint FINGERPRINT` launches only selected approved upstreams
   once to initialize/list tools, then closes their owned trees and privately
   caches metadata. This preparation is execution and needs concrete approval.
3. `native-lifecycle-plan --select PROVIDER --lifecycle-cache PRIVATE_DIRECTORY
   --lifecycle-python STABLE_PYTHON` previews the front-end transport. No application.
4. Only with separate migration authorization, `native-lifecycle-apply` uses the
   reviewed lifecycle fingerprint and `--backup-dir`; existing native rollback
   restores exact original bytes and refuses intervening config changes.

All operations retain the existing CLI's required `--host codex`, `--host-config`,
`--native-prefix`, optional runtime overrides, plugin definitions and conditional
Windows10 consent. Cache writes reuse Environment's private atomic writer. Cache
contains configuration/environment only privately, never in published receipts.
Forward only the bounded OS/runtime/proxy/provider credential environment plus
explicit provider env/env_vars. Bind that same effective set, not ephemeral
Codex client variables. Effective environment/runtime/source drift fails closed
and requires explicit re-priming, never startup execution.
Inherited credentials are provider-specific: n8n receives only N8N_API_URL/KEY,
Claude receives only ANTHROPIC_API_KEY/CLAUDE_CODE_OAUTH_TOKEN, browser providers
receive neither. Explicit approved env/env_vars remain authoritative. This
selection is derived from the reviewed provider owner, not model-supplied values.
Reviewed canonical native flags such as headless/isolated remain available.
Other provider flags require a reviewed owner adapter.

## Use and release

`initialize`, `tools/list` and `_harness_status` use cached metadata and do not
start the heavy process. Upstream names, schemas and annotations remain intact,
so host permission decisions apply to the original operation. A first upstream
`tools/call` starts the owned transport and verifies handshake/metadata again.
Further calls reuse its PID and browser state. Do not finish after each browser
click: finish when the related workflow is done, cancelled or fails.

Ordinary calls use one implicit default workflow. `_harness_finish_session {}`
releases it. For shared work, `_harness_begin_session` issues random leases without
starting a server; identify a lease in `tools/call.params._meta.harness_session`,
not inside upstream arguments. `_harness_finish_session {"session": "TOKEN"}`
releases only that lease. Last release drains active calls then closes ownership.
Callers sharing one default workflow must coordinate completion; explicit leases
are necessary for independent simultaneous consumers. Independent client front-ends
are not silently conflated or given access to each other's processes.

An idle fallback expires abandoned leases after 60 seconds by default (approved
range 1–3600), only when no calls are running. Long pauses need an increased
reviewed timeout or a new workflow. After shutdown, browser handles/navigation
state are lost; no persistence is fabricated. Failed operations are never
automatically retried or replayed. EOF closes the owned transport.

Windows launches suspended, assigns a private kill-on-close JobObject, then resumes;
assignment failure terminates the new child before MCP initialization. POSIX uses
its own process group. Cleanup never accepts arbitrary PIDs, kills existing
servers, stops WSL or removes Linux data. Stdio closes first, then bounded owned
termination ensures descendants do not linger.

## Protocol and validation limits

This is a bounded tools-only MCP adapter using protocol 2024-11-05. An advertised
listChanged capability can use the bound snapshot. Pending notifications are
drained before the next tool mutation; a notification during a call triggers
read-only inventory rechecking after its response. Exact unchanged metadata
retains the workflow, actual changed metadata invalidates until explicit re-prime.
The current operation may already have applied before a change is detected;
never replay it automatically. A flood or unstable inventory fails closed.
Dynamic changed
inventories, resources/prompts/tasks and server-origin sampling/roots/elicitation
requests are not silently forwarded or approved. Incompatible upstream capability
negotiation fails preparation; unsupported runtime requests fail the call without
replay. Host approvals and Security gates remain authoritative. Provider results,
including `isError`, are returned unchanged. Unsupported operations receive a
sanitized explicit error; secret-bearing stdout/stderr is not logged by lifecycle.
Upstreams may advertise resources/prompts; this front-end deliberately exposes
only tools and makes those other methods explicitly unavailable. It does not
claim full upstream feature parity or translate them into automatic approvals.
Newer client initialization requests receive the supported 2024-11-05 version;
the client decides whether to accept that negotiation. This does not certify
an untested desktop client.

The module is internal to the existing Environment CLI, not a new independently
installed catalog tool. Generated transports invoke it by explicit Python path.
Schema/cache/process fixtures prove lifecycle behavior, not external API/model
authentication or desktop-client end-to-end certification. Record actual per-
provider handshake/call/cleanup, startup metadata without heavy PIDs, runtime
versions, unvalidated features and memory under matching conditions separately.

Sources: [MCP lifecycle](https://modelcontextprotocol.io/specification/2024-11-05/basic/lifecycle)
and [MCP tools](https://modelcontextprotocol.io/specification/2024-11-05/server/tools).
