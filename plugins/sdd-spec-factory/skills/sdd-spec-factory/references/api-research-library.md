# API Research Library

Use this library during planning or spec discovery when a requirement needs an
external API, integration, data source, validation service or test endpoint.
It is a library of discovery sources, not an approved dependency list or an
installed MCP inventory. Do not research APIs for unrelated tasks.

During planning and spec creation, consult these sources and prioritize free APIs
or APIs with a suitable free tier to validate application features and test the
application, when relevant. Confirm current limits and use synthetic data, never
real customer data. Prefer local tests or mocks when they adequately satisfy the
acceptance criteria; a free external API is an option, not a mandatory dependency.

## Discovery sources

| Source | URL | Use |
| --- | --- | --- |
| Inventário de APIs Gratuitas | https://github.com/philipecomputacao/inventario-apis-gratuitas | Broad API/service discovery, including Brazilian sources and a separate MCP collection. |
| PublicAPIs.io Development | https://publicapis.io/category/development | Find development, testing and validation API candidates by category. |

These third-party directories are leads, not authoritative provider
documentation. Listings, free-tier claims, prices, quotas and availability may
be stale. Sponsored placement does not establish suitability or trust. Follow
each candidate to its official provider documentation before recommending it.
Do not bulk import or mirror entire catalogs into a spec, MCP Library or context.

## API, mock and MCP are different

- **API integration:** an application calls a provider for a scoped requirement.
  A service that validates addresses or emails is still an external data recipient.
- **Mock/test endpoint:** provides synthetic responses for development. It does
  not validate real business data or prove a production integration works.
- **MCP server:** exposes capabilities to an agent through MCP. An ordinary API
  is not automatically an MCP and does not need an MCP wrapper to be useful.

Discovery does not grant trust, permissions or execution authority. Keep these
sources outside the environment MCP Library and specialist tool registries.
Only a separately reviewed MCP candidate may enter that library; configuration
and installation remain subject to the environment consent/policy gates.

## Planning/spec procedure

1. State the requirement and acceptance criterion: what needs validating or
   integrating, required data/coverage, and why existing project tools or mocks
   are insufficient. Reuse existing integrations first.
2. Search these sources only when relevant, shortlist a few useful candidates,
   then inspect official provider documentation. A directory description is not
   proof that an endpoint, feature or free plan exists today.
3. Check provider identity/maintenance, endpoint/version, input/output contract,
   authentication, scopes, pricing and free-tier limits, rate limits, licensing
   and commercial terms. Check data handling/retention and permissions. Distinguish
   data validation from identity verification or other stronger guarantees.
4. Define a minimal validation plan: sandbox or mock first, synthetic data,
   expected success/error cases, timeout/rate-limit handling and fallback. Do not
   transmit credentials, private source, personal data or real customer records
   to a candidate just to evaluate it. Read-only requests can still disclose data
   or consume quota. Obtain task authorization before any external API call with
   side effects, account creation, payment or sensitive data.
5. Record the comparison, recommendation and evidence in the existing spec or
   `docs/modules/<module>/research.md`; do not create a new document tree merely
   to save two links. Record candidates rejected and why. A research recommendation
   is not approval to install, connect, purchase or deploy.
6. Hand the selected, approved integration and test plan to the implementation
   specialist. Use the environment specialist only when an actual runtime/tool/MCP
   prerequisite is missing. Do not install anything during directory research.

If browsing, provider documentation or credentials are unavailable, mark the
affected claims **NOT VALIDATED**, state the gap and use a mock or defer selection.
Do not fabricate validation, claim a free tier is unlimited, or repeat already
valid research without a changed requirement/provider or stale evidence.

## Candidate evidence template

Copy only the fields relevant to the existing spec/research record:

```text
Requirement / acceptance criterion:
Candidate / provider:
Kind: API | mock/test endpoint | MCP
Discovery source URL:
Official documentation URL / endpoint version:
Checked at (date):
Authentication / permissions required (no credentials):
Pricing / free-tier limits / rate limits:
License / commercial terms:
Data sent / retention / privacy constraints:
Input / expected output and errors:
Validation plan (synthetic data, sandbox, fallback):
Validation evidence: command/check + result, or NOT VALIDATED + reason
Decision: candidate | recommended | rejected | deferred
Reason / alternatives / remaining gaps:
Approval required before implementation or external actions:
```

Research metadata belongs in versioned specs only when public and nonsecret.
Credentials and private runtime observations remain in approved local storage.
