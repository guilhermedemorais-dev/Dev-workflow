# Stack and Decision Matrix

Use this reference when choosing the rendering and motion stack for a cinematic page.

## Default Stack

- Framework: existing project framework; for new React work, Next.js + TypeScript is a strong default.
- Motion master timeline: GSAP.
- Scroll-linked control: GSAP ScrollTrigger.
- React integration: `@gsap/react` when React/Next.js is used.
- Photorealistic scroll scrub: Canvas 2D + pre-rendered image sequence.
- Smooth scrolling: Lenis only when justified by the experience and validated.
- Build-time media tooling: FFmpeg; Sharp only when the repo benefits from Node-side image processing.
- Repeatable browser QA: Playwright tests/CLI.
- Exploratory browser automation: Playwright MCP when persistent agent/browser state is useful.
- Performance/network/console diagnostics: Chrome DevTools MCP.

## Install Baseline

```bash
npm install gsap
npm install @gsap/react
```

Optional, only when justified:

```bash
npm install lenis
npm install motion
npm install sharp
npm install -D @playwright/test
```

Do not add optional dependencies merely because they appear in this reference.

## Renderer Decision Table

| Requirement | Preferred approach | Avoid |
| --- | --- | --- |
| Fixed-camera photorealistic evolution | Canvas 2D image sequence + ScrollTrigger | WebGL/3D unless explicitly required |
| DOM/SVG parallax and pinned storytelling | GSAP timeline + ScrollTrigger | Multiple unrelated animation engines |
| Simple element entrance/exit | Existing project motion stack | Adding GSAP only for one trivial fade |
| Frame-exact scrub | Image sequence | Naive `video.currentTime` seeking |
| Low-file-count coarse scrub | Seek-optimized video after browser QA | Assuming every codec/browser seeks identically |
| Simple progress/transform tied to scroll | CSS scroll-driven animation if target support is acceptable | JS-only solution without reason |
| Component microinteraction inside a GSAP-led cinematic page | Existing component animation or GSAP | Competing master timelines |

## Library Roles

### GSAP

Use for sequencing, complex easing, timeline labels, scroll-linked progress, pinning, snapping, and cross-browser consistency.

### ScrollTrigger

Use for scene entry/exit, scrub, pin, snap, and mapping page scroll to a GSAP timeline or playhead.

### `@gsap/react`

Use in React/Next.js for scoping and cleanup. Prefer `useGSAP()` over ad-hoc effects when available.

### Lenis

Use only when smooth scrolling materially improves the experience. Native scroll is the baseline. If Lenis is added, integrate it with ScrollTrigger correctly and verify accessibility, anchors, modals, nested scrollers, keyboard, and iOS behavior.

### Motion

Use when the project already relies on it for component animation or when a small isolated React interaction is better expressed with Motion. Do not mix Motion and GSAP on the same property/timeline without a concrete reason.

### Canvas 2D

Use for deterministic frame rendering of pre-rendered media. Keep text/CTAs in the DOM.

### FFmpeg

Use for extracting, scaling, encoding, and normalizing cinematic media. Prefer deterministic scripts over browser-based converter sites.

## 3D Gate

Do not introduce Three.js, React Three Fiber, shaders, or WebGL for a cinematic page unless the approved spec needs actual 3D camera/object interaction. Photorealistic pre-rendered media is usually cheaper to produce, easier to control, and easier to QA for scroll-driven storytelling.

## Upstream Sources

Checked 2026-09-12:

- GSAP: https://github.com/greensock/GSAP
- ScrollTrigger docs: https://gsap.com/docs/v3/Plugins/ScrollTrigger/
- GSAP image sequence helper: https://gsap.com/docs/v3/HelperFunctions/helpers/imageSequenceScrub/
- GSAP React: https://github.com/greensock/react
- Lenis: https://github.com/darkroomengineering/lenis
- Motion scroll docs: https://motion.dev/docs/react-scroll-animations
