# Interview and authorized inventory

Use these topics as a coverage map, not a fixed questionnaire. Start with
available project evidence; ask up to three unresolved business decisions per
round with alternatives and a recommendation where useful.

1. Business problem, intended outcome, production scope and exclusions.
2. Actors and external systems: goals, responsibilities, permissions and data
   visibility. Reuse approved identity/RBAC/platform decisions.
3. End-to-end journeys across modules: trigger, preconditions, main path,
   alternatives, failures, recovery and observable result for each actor.
4. Shared entities, ownership, lifecycles, invariants, cross-module interfaces.
5. Professional capabilities where relevant: audit, filters/search, pagination,
   import/export, notifications, accessibility, recovery, privacy and operation.
   Present missing capabilities as proposals with purpose, not automatic scope.
6. Functional/visual references, source rights/access, reuse and evidence gaps.
7. Complete module inventory, urgency reason/deadline/impact, dependencies.
8. Working capacity, external waiting, resources, risks, estimate confidence.

For existing software, first inventory supplied app/code/data/docs/integrations.
For each capability record evidence path + revision, observed coverage, limits
and one recommendation: MAINTAIN, COMPLETE, FIX, REFACTOR, REPLACE or RETIRE.
Separate visible interface, code found and tested behavior. Include missing
access as UNKNOWN. RETIRE is a recommendation, never permission to remove data.
Do not execute downloaded code or connect production services merely to inspect.

Research reference implementations beyond README: relevant implementation,
schemas/migrations, API contracts, examples and tests. A screenshot/scrape cannot
establish hidden rules or full backend behavior. Save a concise source record in
the project library and cross-check contradictions before making a requirement.

Each decision has ID, status (APPROVED/PROPOSED/UNKNOWN/EXCLUDED), source, rationale
and impact. Ask when a gap changes scope, business rules, urgency feasibility or
acceptance. Technical details derivable from approved context can be researched
and proposed without repeatedly asking the user to write the specification.
