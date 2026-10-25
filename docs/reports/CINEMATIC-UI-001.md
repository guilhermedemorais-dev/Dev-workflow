# CINEMATIC-UI-001: implementation and validation evidence

Date: 2026-10-25. Contract revision: 1. Branch: `feat/cinematic-ui-specialist`.
Owner authorized integration inside existing UI/UX; no merge/deploy authorization.

## Result and ownership

- Canonical cinematic skill/resources are under `plugins/ui-ux-standard/skills/cinematic-web-standard/`.
- Existing UI/UX plugin and sector retained; no new top-level plugin/sector.
- Harness selects the specialization only for approved cinematic scope. UI/UX owns design/visual acceptance, implementation writes product code, QA keeps independent functional acceptance.
- SDD routes scene contracts, budgets, mobile/reduced-motion and failure behavior in the same module Task.
- Existing OS catalogs include the three optional media helpers under the UI/UX owner. No tool/dependency/MCP was installed.
- Source skill resources preserved; frame-extraction example explicitly invokes `bash` because source scripts are not executable files by default.

## Actual sources and reuse

Read AGENTS/pipeline, canonical implementation/UI workflow and cinematic integration/media/performance references. Reused existing UI plugin's `./skills/` loader, existing capability registry, existing task schema, existing OS catalogs, and existing source scripts. No second installer, registry or product renderer was implemented. The only route-builder extension is the explicit nested source path needed to preserve the existing V2 generator model.

## Executed validation

- `python -m unittest discover -s tests -v`: **642 tests, OK, 8 skipped**, exit 0. Skips are existing native-Windows-only coverage and related platform limitations, not passes on a mocked OS.
- New cinematic tests validate numeric manifest ordering/byte sizes, gap/duplicate/strict-budget failures, nested resource closure and opt-in V2 selection where present.
- Initial full suite found absent media-helper entries in OS inventories. Added exactly those three authored paths and changed fixed inventory count from 11 to 14; exact authored-path equality test retained. Final full suite passes.
- `bash -n plugins/ui-ux-standard/skills/cinematic-web-standard/scripts/extract_frames.sh`: exit 0.
- Actual synthetic FFmpeg video (1 second, 64x64) extracted into **four numbered WebP frames**, then strict sequence validator passed. Fresh temporary output only; scripts are unchanged.
- `git diff --check`: exit 0.

## Independent review

Actual read-only reviewer `cinematic_review` inspected routing, preservation, source bundle, Task metadata and OS catalogs. Its focused cinematic/V2/preservation checks passed. It separately executed 12 platform-routing tests in each checkout, all passed. Metadata findings (allowed paths, derived criteria, existing authorization and QA applicability) were corrected. This is independent packaging/routing/helper review, not a product-browser or production-security approval.

## Limits and next gate

- Host installation/reload and actual LLM/browser behavior: NOT_VALIDATED.
- No real product page, media production, rendered visual QA or benchmark/token-savings claim.
- Native Windows/macOS execution of the new helpers: NOT_VALIDATED; Windows Bash extraction is UNSUPPORTED, WSL follows Linux routing.
- Source extraction helper replaces `frame-*.webp` in the requested output directory as in the preserved source. Run only for a Task-approved output path; never use existing unrelated media as a test fixture.
- Remote Issue: NOT_PUBLISHED; local Task/JSON state is explicit, no fabricated URL. Remote branch/PR status must come from returned GitHub evidence.
- Human review, merge and host update remain separate. No merge/deploy performed.
- Runtime token usage: NOT_AVAILABLE.
