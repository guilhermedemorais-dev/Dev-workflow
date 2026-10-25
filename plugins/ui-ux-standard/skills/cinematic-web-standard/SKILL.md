---
name: cinematic-web-standard
description: "Use for premium cinematic/scrollytelling web experiences, scroll-scrubbed image sequences, GSAP/ScrollTrigger, Canvas 2D, optional Lenis smooth scrolling, media pipelines, and browser performance/visual QA. Apply when implementing or reviewing scroll-driven storytelling, pinned scenes, image/video sequences, cinematic landing pages, interactive timelines, or motion-heavy React/Next.js UI. Companion to ui-ux-standard and dev-implementation-standard; prefer pre-rendered 2D media over WebGL/3D unless 3D is explicitly required."
---

# Cinematic Web Standard

Build cinematic web experiences as engineered products, not as a pile of effects. Keep motion tied to narrative, measurable performance, accessibility, and deterministic media states.

## Ownership

Own:

- scrollytelling architecture and scene choreography
- GSAP core, timelines, ScrollTrigger, React cleanup, and performance patterns
- Canvas 2D image-sequence scrubbing for photorealistic experiences
- media preparation contracts for video-to-frames and frame manifests
- optional Lenis integration when smooth-scroll behavior is justified
- scroll-motion accessibility and reduced-motion fallbacks
- runtime visual, interaction, and performance QA for motion-heavy pages
- browser-agent/MCP guidance for exploratory QA and performance inspection

Do not own:

- product scope or final copy approval
- backend/domain architecture
- tokenomics, business rules, or data contracts
- final visual identity approval
- WebGL/Three.js work unless the approved spec explicitly requires it

## Required Context

Before implementing, read the approved task/spec and the current UI/design context. If this skill is used inside Dev-workflow, also read the mandatory `dev-workflow-standard`, `dev-implementation-standard`, and `ui-ux-standard` skills delegated by the task.

If official GSAP agent skills are installed, load the relevant upstream skills instead of re-deriving API details:

- `gsap-core`
- `gsap-timeline`
- `gsap-scrolltrigger`
- `gsap-react`
- `gsap-performance`
- `gsap-plugins` only when needed

See `references/upstream-agent-skills.md`.

## Non-Negotiables

- Prefer GSAP + ScrollTrigger for complex cinematic scroll-linked timelines.
- Prefer Canvas 2D + pre-rendered image sequence for photorealistic frame-accurate scrub experiences.
- Do not introduce Three.js, React Three Fiber, shaders, or WebGL unless explicitly required by the approved spec.
- Do not add Lenis by default. Start with native scrolling; add Lenis only when the experience benefits and QA confirms no accessibility or nested-scroll regressions.
- Keep important copy and CTAs in semantic HTML/React. Do not bake essential text into video or canvas.
- Treat media as a pipeline with budgets, not as arbitrary files dropped into `public/`.
- Keep camera, composition, environment, and subject identity stable across keyframes when the sequence represents biological/product evolution.
- Implement `prefers-reduced-motion` and a usable non-scrub fallback.
- Validate desktop and mobile separately. A desktop sequence is not automatically a mobile sequence.
- Avoid animating layout-heavy properties when transforms/opacity can achieve the same visual result.
- Clean up every GSAP context, ScrollTrigger, listener, animation frame, observer, and preloader when components unmount.

## Rendering Decision Gate

Choose one primary renderer per scene. Do not mix libraries because they happen to be installed.

1. **Photorealistic continuous evolution or product reveal**
   - Use Canvas 2D + image sequence + GSAP ScrollTrigger.
   - Use this as the default for fixed-camera tree growth, manufacturing, product assembly, environmental change, or cinematic morph sequences.

2. **Simple DOM/SVG motion, pinned sections, text choreography, parallax**
   - Use GSAP timeline + ScrollTrigger.

3. **Simple component entrance/exit animation with no master scroll timeline**
   - Existing project motion library may be reused.
   - Do not add Motion solely for one effect when GSAP already owns the page timeline.

4. **Video scrub**
   - Use only when imprecise seeking is acceptable, the media is encoded for seeking, and browser/device QA passes.
   - Prefer image sequences when deterministic frame selection matters.

5. **Native CSS scroll-driven animation**
   - Consider for simple progressive transforms where target-browser support and fallback are acceptable.
   - Do not force JS where CSS alone is sufficient.

Read `references/stack-and-decision.md` before choosing a renderer for a new experience.

## Workflow

### 1. Discover

- Inspect the route, component tree, styling stack, existing motion utilities, loading behavior, and asset strategy.
- Identify the narrative chapters and the scroll ownership boundary for each chapter.
- Record the intended desktop/mobile behavior and reduced-motion behavior.
- Confirm whether the media already exists or must be produced.

### 2. Design the Scene Contract

For each scene, define:

- scene ID and narrative purpose
- trigger start/end
- pinned or normal-flow behavior
- renderer: DOM/SVG, Canvas image sequence, or video
- input media and aspect ratios
- keyframe states
- copy/CTA layer
- loading strategy
- mobile behavior
- reduced-motion fallback
- acceptance evidence

For biological/evolution sequences, define named states first and generate transitions second. Do not ask generative video to invent the entire lifecycle in one uncontrolled clip.

### 3. Prepare Media

For image-sequence scenes:

1. Produce stable keyframes with the same camera, environment, lighting intent, and subject identity.
2. Generate short transitions between adjacent keyframes when required.
3. Extract a purposeful frame rate. Do not blindly ship 30 FPS.
4. Generate a manifest with frame order and file sizes.
5. Validate the sequence against the media budget.

Use:

- `scripts/extract_frames.sh`
- `scripts/make_manifest.py`
- `scripts/validate_sequence.py`

Read `references/image-sequence-pipeline.md`.

### 4. Implement Motion

- Register GSAP plugins once in the client runtime.
- In React/Next.js, isolate browser-only animation code and use GSAP context / `useGSAP` cleanup patterns.
- Use timelines for multi-step choreography; avoid chains of unrelated delays.
- Tie scroll progress to a small playhead object for image sequences, then draw only the requested frame.
- Size canvas for device pixel ratio without allowing unbounded memory usage.
- Use `requestAnimationFrame` discipline; do not create competing RAF loops without reason.
- Lazy-load future chapters and prioritize the first meaningful scene.
- Keep scroll progress deterministic across refresh/resize and call refresh only when layout/media changes require it.

Read `references/gsap-scrolltrigger.md`.

### 5. Integrate Smooth Scrolling Only If Needed

If Lenis is justified:

- use one scroll source of truth
- synchronize Lenis with ScrollTrigger correctly
- disable duplicate RAF ownership
- test keyboard navigation, anchors, nested scroll areas, modal locking, iOS, and reduced motion
- verify the experience still works with Lenis removed

If there is no measurable or experiential improvement, remove Lenis.

### 6. Enforce Performance and Accessibility

- Keep the first scene interactive before preloading the whole journey.
- Preload a small critical window, then stream future frames by chapter.
- Avoid keeping every full-resolution frame decoded in memory.
- Provide mobile-specific dimensions or reduced frame density when needed.
- Respect reduced motion and allow normal page navigation without the cinematic layer.
- Preserve semantic reading order, focus order, and working CTAs.
- Do not lock the user inside a pinned section indefinitely.

Read `references/performance-accessibility.md`.

### 7. Validate in Runtime

Use the repo's existing tests first. For interactive/browser QA:

- Prefer Playwright tests/CLI for repeatable acceptance checks.
- Use Playwright MCP when an agent benefits from persistent exploratory browser state.
- Use Chrome DevTools MCP for traces, network analysis, console inspection, and performance diagnostics.
- Do not install both browser MCPs merely to duplicate the same task.

Read `references/mcp-browser-tooling.md`.

Minimum runtime checks:

- desktop and mobile viewport
- scroll forward and backward
- resize/orientation change
- refresh in the middle of the journey
- keyboard navigation
- reduced motion
- slow network / cold cache
- console errors
- missing/corrupt media behavior
- memory growth while traversing long sequences
- layout stability and loading transitions

## Dev-workflow Handoff

When used inside Dev-workflow, return evidence that can be consumed by `dev-implementation-standard` and `ui-ux-standard`:

- `CINEMATIC_RECEIPT`: renderer choice, libraries used, upstream skills loaded, references read
- `SCENE_CONTRACTS`: scene IDs and motion/media behavior
- `MEDIA_BUDGET`: frame counts, encoded size, critical preload size, mobile variant status
- `MOTION_QA`: tested viewports, reduced motion, reverse scroll, resize, cold load
- `PERFORMANCE_QA`: browser evidence, trace/network findings, unresolved risks
- `UNRESOLVED_DECISIONS`: anything requiring product/design/architecture approval

See `references/dev-workflow-integration.md` for the recommended placement and delegation model.

## Resources

- `references/stack-and-decision.md`: renderer/library decision matrix
- `references/gsap-scrolltrigger.md`: GSAP/ScrollTrigger implementation patterns and pitfalls
- `references/image-sequence-pipeline.md`: video/keyframes to optimized image sequence workflow
- `references/cinematic-storytelling.md`: scene/keyframe continuity and scrollytelling structure
- `references/performance-accessibility.md`: budgets, loading, mobile, reduced motion, memory
- `references/mcp-browser-tooling.md`: Playwright MCP, Chrome DevTools MCP, and MCP SDK guidance
- `references/upstream-agent-skills.md`: official GSAP skills and optional scrollytelling skill ecosystem
- `references/dev-workflow-integration.md`: integration with the user's Dev-workflow plugin structure
- `scripts/extract_frames.sh`: extract WebP frames from a source video with FFmpeg
- `scripts/make_manifest.py`: generate deterministic frame manifests
- `scripts/validate_sequence.py`: validate naming, gaps, dimensions metadata when available, and media budget
