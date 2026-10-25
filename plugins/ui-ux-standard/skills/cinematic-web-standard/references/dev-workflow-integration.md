# Dev-workflow Integration

Use this reference when adding the skill to the user's Dev-workflow repository.

## Recommended Placement

Given the existing specialist layout, place the skill under the UI/UX plugin:

```text
plugins/
  ui-ux-standard/
    skills/
      ui-ux-standard/
      cinematic-web-standard/
        SKILL.md
        agents/openai.yaml
        references/
        scripts/
```

This keeps cinematic motion as a UI/UX specialization while leaving execution ownership with `dev-implementation-standard`.

## Delegation Model

`dev-workflow-standard`

- decides whether the task requires cinematic/scrollytelling specialization
- includes `cinematic-web-standard` in the mandatory skill list

`sdd-spec-factory`

- captures scene contracts, performance budgets, media requirements, mobile behavior, and reduced-motion acceptance criteria in the approved spec/task

`ui-ux-standard`

- owns visual direction, approved references, mockups, design tokens, media prompts, and final visual QA criteria

`cinematic-web-standard`

- chooses the motion renderer/pipeline within the approved design
- defines scene contracts and media pipeline details
- defines motion/performance/accessibility validation
- does not approve its own design

`dev-implementation-standard`

- implements the approved task
- reads this skill as a mandatory skill when delegated
- records `SKILL_RECEIPT`
- runs the scripts/tests/QA required by the task
- does not widen architecture or scope

`security-standard`

- reviews external media/CDN/tool/MCP/security concerns where the task requires it

## Task Additions

For cinematic work, the task/spec should include these fields when relevant:

```markdown
## Cinematic / Scrollytelling
- Narrative chapters:
- Renderer per chapter:
- Scroll/pin behavior:
- Desktop behavior:
- Mobile behavior:
- Reduced-motion fallback:
- Media source / production status:
- Critical preload budget:
- Total chapter media budget:
- Required browser QA:
- Required performance evidence:
```

## Mandatory Receipt

The executor should include:

```markdown
### CINEMATIC_RECEIPT
- Skill: cinematic-web-standard
- Skill path:
- Upstream GSAP skills loaded:
- References loaded:
- Renderer decision:
- Lenis decision: not used / used + justification
- 3D/WebGL decision: not used / explicitly approved
- Media scripts executed:
```

## Marketplace Integration

If the repository requires every specialist to be a top-level plugin, wrap this skill in its own plugin directory and add that plugin to the marketplace manifest instead. The default recommendation is to keep it under `ui-ux-standard` because the current responsibility model already treats UI/visual specialists as companions to the main development workflow.

Do not modify the marketplace merely to make the skill discoverable if the plugin loader already scans nested `skills/` directories.
