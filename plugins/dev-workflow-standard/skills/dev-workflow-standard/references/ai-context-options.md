# Context retrieval, Redis and fine-tuning: selection boundaries

Consult only for a demonstrated context-retrieval, repeated-query or model-quality
gap. These are different mechanisms, not a mandatory stack for every skill.

## Existing Harness baseline

The current implementation uses `context-retriever.py` (Potpie when healthy,
bounded lexical fallback), tool/environment state and versioned references.
Redis appears as an external dependency of the optional BullMQ source catalog;
it is not configured as a Harness memory/cache backend. No fine-tuning training
pipeline or trained-model integration was found in the inspected plugin sources.
This audit says nothing about an inaccessible other plugin or local workstation.

## Decision ladder

1. Correct conflicting instructions, select relevant context and measure failures.
2. Reuse the project library and existing retrieval/cache before adding services.
3. If repeated retrieval/queries dominate and concurrency justifies shared state,
   evaluate Redis against the existing local cache and mature retrieval tooling.
   Record a measured workload, hit rate, memory/latency budget and simpler option.
4. For response reuse, prefer exact context-sensitive keys for engineering work:
   project/tenant, model, prompt/skill version, contract revision, source/code hash,
   authorization scope and tool-state freshness. Set TTL, invalidation and memory
   limits. Never cache secrets or use an answer from another project as authority.
5. Semantic similarity alone is insufficient for a patch, approval or PASS.
   A similar request against a different code/spec revision can require another
   result. Cached search facts may support a decision; current tests, source
   inspection and permission checks must still run. Cache outage is a miss or
   documented fallback, never silent stale acceptance.

Redis can store data, vectors and reusable responses. It does not train a model,
remove required prompt context automatically or make an agent follow the PRD.
This plugin is an instruction/tool bundle, not an interception layer around all
host LLM requests. Adding a Redis container alone cannot cache those requests.
The owner's conditional authorization permits a justified Redis integration;
this revision does not install one because no workload/host integration need was
demonstrated. Do not replace existing retrieval to justify an unnecessary service.

## Fine-tuning

Fine-tuning changes a model using examples; editing skills or indexing documents
does not. Consider it only for a persistent, measured behavior/formatting failure
after fixing prompts/retrieval, with representative permitted training examples,
a separate holdout/eval set and a provider/runtime that can serve the trained ID.
It does not keep changing PRDs, code or vendor documentation current. Use retrieval
for that information. Do not upload project/customer material or start paid
training merely because this reference exists; data rights, privacy, provider
availability, budget and deployment approval must be explicit.

Official OpenAI SFT documentation inspected 2026-10-20 states that self-service
fine-tuning is winding down, new users cannot access it and eligible existing
customers can create jobs until 2027-01-06, subject to base-model shutdown. Verify
current provider/model support before proposing an implementation. No account
eligibility, model availability or training execution was validated here.

## Sources and evidence

- Redis semantic caching: https://redis.io/docs/latest/develop/use-cases/semantic-cache/
- OpenAI SFT and evaluation prerequisite: https://developers.openai.com/api/docs/guides/supervised-fine-tuning

These sources describe capabilities and constraints, not measured savings for
this Harness. Do not reuse vendor example percentages as project benchmarks.
