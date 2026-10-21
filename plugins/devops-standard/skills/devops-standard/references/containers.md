# Containers

Preserve the current Docker/Compose/Coolify/Portainer architecture. Identify
Docker context/daemon and exact containers/images/volumes before any operation;
local CLI does not imply a local daemon. Never delete persistent volumes or
prune the host to fix a build without separate target-specific authorization.

Before approving a Compose configuration change, compare reviewed baseline and
proposed rendered JSON using this owner's `scripts/compose-scope.py` from the
active bundle or explicit checkout. Declare exact allowed resource names from
the Task, never derive permission from the proposed diff. Example:

```bash
python3 scripts/compose-scope.py --before baseline.json --after proposed.json --allow-services api
```

The script rejects undeclared additions, removals and modifications of services,
volumes, networks, secrets, configs and top-level fields. Exit 0 means only that
the rendered difference fits the supplied scope; exit 1 is out of scope and exit 2
is invalid/unreadable input. An allowed service can still introduce dangerous
mounts or privilege changes, so retain Security review and the Task's constraints.
Do not use this check to authorize start, restart, install, prune or deployment.
It neither invokes Docker nor blocks another tool from invoking Docker.

Use normalized output from the same approved Compose renderer/version and
project context for both inputs, inspecting render inputs before execution.
Rendered JSON may include interpolated secrets: keep snapshots in ignored local
storage with restrictive permissions and remove them after review. Never publish
their contents. The report contains resource names and hashes, not config values.
Do not change the baseline or broaden allow-lists merely to obtain exit 0.

Validation sequence: inspect Dockerfile/Compose, `hadolint Dockerfile`, approved
`docker build`, `docker compose config --quiet`, then isolated smoke/health.
Build steps execute code and can access network/secrets; review inputs first.
Use disposable synthetic data, bounded resources and loopback ports when a
local runtime test is authorized. Avoid privileged containers and host mounts.
Compose config may interpolate secrets; prefer quiet validation and sanitize
any diagnostic output. Build/config success does not prove service health.

Verify entrypoint, non-root compatibility, actual health endpoint, resource
limits, image digest and mounted storage permissions. Route image scanning,
secrets and security hardening to security-standard; do not duplicate its tools.
Push/recreate/restart/deploy are mutations, not validation defaults. Plan
rollback with the previous artifact/config and data compatibility beforehand.
