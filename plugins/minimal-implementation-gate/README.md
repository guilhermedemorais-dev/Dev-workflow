# Minimal Implementation Gate

Specialist companion plugin for `dev-workflow-standard`.

It adds three anti-overengineering gates to the delivery workflow:

1. `Minimal Planning Review` after scope consolidation and before specs/tasks.
2. `Minimal Implementation Gate` after human task approval and before coding.
3. `Minimal Code Review` after PR creation and before final review gates.

The goal is to reduce unnecessary scope, files, dependencies, layers and token
cost without weakening security, input validation, required tests, essential
logs, accessibility, performance-critical behavior or business rules.

This plugin does not replace `dev-workflow-standard`, `sdd-spec-factory`,
`dev-implementation-standard`, `security-standard`, `ui-ux-standard` or QA.
It only reviews complexity and returns a recommendation.
