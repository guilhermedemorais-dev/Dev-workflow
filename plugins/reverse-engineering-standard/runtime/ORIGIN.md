# REA runtime origin

- Upstream: https://github.com/morluto/rea
- Package: rea-agents
- Pinned runtime version: 4.1.0
- License: MIT
- Upstream skill version: 26
- Upstream tool catalog: 130 MCP tools

## What is reused

The Dev Workflow reverse-engineering module reuses the REA analysis engine and
its context-producing capability families through a local gateway:

- native/binary analysis
- artifact/package inspection
- JavaScript/Electron analysis
- managed/.NET analysis
- Android/JADX analysis
- firmware inspection/extraction
- browser/Electron/V8 runtime observation
- evidence comparison and reconstruction workflows

## What is not duplicated

REA agent setup, marketplace registration, upstream onboarding, telemetry and
general orchestration are not adopted because those responsibilities already
belong to the Engineering Harness.

The local gateway is the stable Dev Workflow contract. The runtime package is
version-pinned so a future source mirror or replacement engine can be swapped
without changing Task/skill/provider semantics.

Preserve the upstream MIT license and attribution when redistributing reused
runtime material.
