# Skill-Owned Tools

## Goal

Each specialist owns the tooling for its domain. The Harness routes capability
to skill; the skill resolves official tool knowledge and environment-specific
installation state, executes, interprets, corrects, and revalidates.

## Sources of truth

- Versioned `references/tool-registry.json` per specialist: capabilities,
  official repositories, detection/verification, and install policy.
- Ignored `runtime-state/tool-state.json` per specialist: environment ID,
  installed version, executable path, source, method, last verification or
  failure. This file is local to the runtime and never a universal claim.
- Human Task and lean Execution Contract name only owner skill, capability,
  preferred tool, and required validation. They contain no local state.

## Flow

Resolve cached state first. A compatible executable uses the fast path without
discovery. Otherwise detect and verify an existing installation. When absent,
the owner selects an official supported installation command for the project,
installs explicitly, verifies, and persists. Installation failure is recorded
and not repeated unchanged in the same cycle. Changed environment, missing
executable, incompatible version, or broken execution invalidates state.

Validation uses real project commands. A finding is a candidate until the
specialist confirms it. On failure, analyze, fix inside scope, rerun, and record
final evidence. Escalate when scope, architecture, privilege, credentials, or
external conditions prevent a valid result.

## Boundaries

- No automatic installation merely because a registry entry exists.
- No local paths or runtime cache in versioned contracts, task, or Issue report.
- No fixed vendor mandate; registry is an initial catalog.
- No claim of PASS before revalidation.
