# Derived context and deterministic template pilot

These are opt-in local utilities. They do not replace canonical docs, the Harness execution contract, context routing, or human acceptance. The pilot is deliberately conservative: derived context contains exact excerpts selected from source files; it does not ask a model to rewrite policy or summarize decisions.

## Derived context

`plugins/dev-workflow-standard/scripts/derive_context.py` creates an artifact from a JSON plan containing canonical source paths, exact 1-based line ranges with purposes, curated positive retrieval assertions, and mutation controls. The artifact records each source SHA-256 and the plan SHA-256. It is valid only while both remain unchanged; `--verify` reruns the checks. A stale source returns the current canonical source text on stdout and a nonzero exit code. Failed curated evaluation also prints the original source text and writes no artifact.

The runnable sample plan is `docs/examples/derived-context-plan.example.json`. From the repository root:

```sh
python3 plugins/dev-workflow-standard/scripts/derive_context.py \
  --plan docs/examples/derived-context-plan.example.json \
  --output /tmp/derived-context.json
python3 plugins/dev-workflow-standard/scripts/derive_context.py \
  --verify /tmp/derived-context.json
```

Keep plans and artifacts with the same review boundary as their source material. Known secret paths and common key/token shapes are blocked, but this heuristic is not a secret scanner; select only reviewed, non-sensitive sources. The tool records literal assertions and mutation checks, not broad semantic equivalence. A human must curate query cases to include decisions, permissions, exceptions, negations, numbers and pending questions relevant to the intended use. Any missing coverage or disagreement means use the original source.

The pilot's context size is the UTF-8 byte count of the selected excerpts; the comparison size is the byte count of the full source set, measured with the same method. The sample artifact records this local byte ratio, not universal savings, model-token reduction, fewer interventions or improved task outcomes. To claim an operational benefit, compare the same task, source revision, model/runtime and budget over repeated runs; record context bytes, generated artifacts, human interventions, task requirements recovered, regressions, elapsed time and cost/tokens when the runtime exposes them. No workflow baseline or operational savings result has been measured in this repository.

## Deterministic template rendering

`plugins/dev-workflow-standard/scripts/render_deterministic_template.py` accepts a UTF-8 template, a JSON field schema, and a JSON values object. It requires exact field-set equality, validates type, length, enum/pattern/range constraints, escapes values for the declared destination, performs one substitution pass, and atomically replaces the output only after all validation succeeds. Static template bytes are preserved. New outputs use mode `0600`; existing output mode is preserved. Values are data and are never parsed as template instructions.

The existing Task template now uses `{{task_id}}` and `{{task_title}}`, with an explicit schema at `plugins/sdd-spec-factory/templates/task-template.schema.json`:

```sh
python3 plugins/dev-workflow-standard/scripts/render_deterministic_template.py \
  --template plugins/sdd-spec-factory/templates/task-template.md \
  --schema plugins/sdd-spec-factory/templates/task-template.schema.json \
  --values docs/examples/task-template-values.example.json --output /tmp/TASK-123.md
```

Add a field only when the template explicitly declares it in its schema and its destination escaping/validation is understood. Static approved decisions and acceptance criteria stay in the template. This is a small substitution helper, not a general template language or a security boundary for arbitrary Markdown consumers.

## Adoption and limits

- The context pilot remains opt-in until real retrieval evaluations show that source meaning is preserved for the target use cases. Hashes prove freshness, not correctness.
- A pilot artifact cannot be cited as the sole source for high-impact or disputed decisions. Return to canonical sources whenever evidence is missing or conflicting.
- Do not put secrets or sensitive user data in plans, derived artifacts, values files or generated outputs.
- Rendering does not grant permission to publish, execute commands, or change acceptance criteria.
- Specialist gates remain based on changed surface and risk. TRIVIAL work does not need a ten-sector matrix, but relabeling cannot waive a triggered security, data, contract or UI review.

## Source review, 2026-10-15

- GitHub Next's [Knowledge Compressor article](https://githubnext.com/posts/knowledge-compressor/) describes question/answer checks against both the original and compressed article, with negative evidence feeding iteration. This pilot checks curated literal facts and mutations; it does not run fresh model answer trials or prove semantic equivalence, so it remains opt-in.
- GitHub Next's [Sparkle Pills article](https://githubnext.com/posts/sparkle-pills/) recommends deterministic code to preserve static text while replacing named slots. This renderer uses a stricter allowlist/schema and does not generate slot values with a model. No upstream code was copied.
- GitHub Next's [`evergreen` repository](https://github.com/githubnext/evergreen/tree/489a9dab2b343fb4444de1c45b889f1f520c96d0) was checked at commit `489a9dab2b343fb4444de1c45b889f1f520c96d0`. Its PR workflow checks leases/current head before work and reloads/verifies writes. This repo adopts only the manual freshness and ambiguous-retry rules in `harness-execution.md`; no lease engine, workflow, token or automation dependency was added.
- `rig`, `agentics`, and `gh-aw` were not incorporated or executed. Their current `HEAD` values on 2026-10-15 were respectively `c00c90c32596a5e6835b98b4bef7a1db471c79ef`, `b4e175bab6674279e0fe158f7dc877b77bc9d92f`, and `56a8d2b93f37634d540b6731ff84050f9dba27b3`; no replacement benchmark was run.

Conditional experiments not adopted for this delivery: `rig` adds a separate execution engine without a demonstrated gap in the current Harness; `agentics` and `gh-aw` require CI/workflow integration outside the approved local patch; `Goal`, `Autoloop`, and `Crane` add persistent orchestration without a concrete state-recovery case; CAO adds multi-agent infrastructure without a multi-repository requirement. The required five-case, three-run comparative benchmark was not run because these candidates were not selected for integration and no isolated benchmark environment/budget was approved. These are scope and evidence decisions, not claims that the tools are inferior.
