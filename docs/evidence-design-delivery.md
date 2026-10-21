# Task #59 continuation: technical decisions and Apple HIG Designer

Source repository: Dev-workflow. Parent: `1c33d8023a46b72af7880eae7477954096741b54`.
Review branch: `fix/trivial-workflow-efficiency`, PR #60. Client date: 2026-10-20.

## Implemented

Material decisions now route from Harness and executor to the existing SDD
library's `technical-decision-procedure.md`. It requires approved PRD/spec/ADR,
actual code/config/version, applicable original documentation, alternatives,
short rationale and executed validation. It applies across architecture, stack,
API/protocols, data, dependencies, UI, security, QA and operations, not just Docker.
Unchanged verified decisions are reused. Researchable technical facts are not
questions delegated to the owner; an actual approval request includes diagnosis,
options, consequences and recommendation. Approved specs can identify code bugs
without a new business decision. Unresolved normative contradictions still block.

The final check reuses requirement → microtask → acceptance → owner/evidence
mapping, and checks scope across paths, interfaces, dependencies and resources.
No new Task schema, receipt type or runtime engine was introduced. These are
instructions and structural checks, not a universal execution firewall or proof
that every model will obey the PRD.

## Exact user-selected design skill

The owner's screenshot identifies **axiaoge2/Apple-Hig-Designer**:
https://github.com/axiaoge2/Apple-Hig-Designer
Pinned source: `ff17b91ff2903ecd52940afabf97de5a73c9cd1b`. MIT license retained.
An initial different HIG candidate was discarded before commit/publication.

Five upstream files are preserved byte-for-byte with hashes: SKILL.md (renamed
GUIDE.md to avoid independent automatic triggering), REFERENCE.md, CSS tokens,
React examples and UI patterns. The package is inside UX references, not a
second compulsory top-level skill. Screenshots/readmes were not copied.
No upstream code, installer, CSS or JSX was executed and no dependencies installed.

`apple-hig-routing.md` selects the exact package only for an Apple-style task,
approved direction or applicable platform review. It requires the guide, then
only the pertinent reference sections or resources. A web ERP with an approved
design system does not load Apple examples by default. Generation instructions
cannot turn a review into implementation. Solid backgrounds remain the default;
glass/blur requires an explicit request. PRD, stack and accessibility prevail.

This is a community design skill, not a complete, current official corpus for
every Apple product. Example tokens/durations/CSS measurements are not universal
Apple rules. Precise platform claims require current original documentation.
Apple font/SF Symbols/branding terms are separate from the repository MIT license.

Two existing UX sections were moved intact to purpose-routed references, with
relative-link fixes and replacement of the obsolete whole-inventory instruction.
Source map: `ui-ux-section-migration.json`. Tests compare against the parent commit.
UX entry file: 13,073 bytes/276 lines → 8,909 bytes/193 lines, despite the new route.
Harness entry grows from 10,975 to 11,566 bytes (163 → 169 lines) for decision and
AI-context routing. These are file sizes, not measured LLM token savings.

## Redis, retrieval and fine-tuning audit

Inspected the available Dev-workflow and local The-office plugin sources. Found
existing Potpie/lexical context retrieval, environment/tool state and Redis as
an optional BullMQ dependency reference. No Redis Harness memory/cache backend
or fine-tuning pipeline was found. An inaccessible other plugin/workstation was
not audited; no claim is made about it.

`ai-context-options.md` records conditional Redis authorization and the decision
ladder: measure a repeated/shared workload, reuse existing mechanisms, and only
add a service when needed. Exact cache keys must include project/tenant, model,
contract/source revisions and authorization/freshness; similarity is not approval
or current test evidence. Installing Redis cannot intercept all LLM calls in a
host that does not provide that integration. No Redis service was necessary or
installed for these changes.

Fine-tuning changes a model using examples, not a skill file. It needs measured
failures, permitted representative data, holdout/evals and a compatible serving
runtime. OpenAI's official SFT documentation currently states that new-user access
has ended and eligible existing customers may train until 2027-01-06, subject to
base-model shutdown. Verify account/provider availability before proposing it.
No API credential, dataset upload, paid training or fine-tuned model was used.

Primary sources inspected:
- https://redis.io/docs/latest/develop/use-cases/semantic-cache/
- https://developers.openai.com/api/docs/guides/supervised-fine-tuning
- https://developer.apple.com/design/human-interface-guidelines

Apple landing retrieval exposed JavaScript-only content and a Markdown route
that failed in this session. No current numeric HIG requirement was certified.
Repository license, source pin and files were verified from the actual clone.

## Executed validation

Linux / Python 3.12.14. `python3 -m unittest discover -s tests -v`:
666 discovered, 659 passed, 7 skipped (native Windows), exit 0.
Workflow, executor and UX quick validators passed. `git diff --check` passed.
New tests verify exact repository/pin/license and file hashes, absence of the
wrong package, conditional loading, preserved UX sections, procedure routing and
Redis/fine-tuning limits. Existing tests follow routed sources, not just entry files.

An independent agent retested the corrected package:
- Existing web ERP error copy: skip all Apple material; preserve approved rules.
- macOS navigation/keyboard planning: guide plus selected Navigation Patterns and
  macOS Adaptations sections; no CSS/React/all-resource loading.
- Identified insufficient keyboard/current-platform coverage and required original
  docs rather than claiming complete HIG compliance.
- Preserved explicit-glass-only, PRD/stack precedence and review-only authorization.

That is a real instruction-selection exercise, not application rendering or
end-user usability testing. No UI application, native host discovery, Redis runtime,
training, Windows/macOS behavior or end-to-end token benchmark was validated.
No merge/deploy. Owner review and installation/acceptance remain pending.
