# GSAP and ScrollTrigger Patterns

Use this reference when implementing or reviewing cinematic scroll motion.

## Core Rules

- Register plugins once before use.
- Use one timeline for a scene/chapter instead of many unrelated delayed tweens.
- Prefer transform and opacity properties for motion.
- Use labels and timeline positions for choreography.
- Use `scrub` when progress must track scroll.
- Use `pin` only where the narrative benefits; do not trap users in huge pinned distances without reason.
- Use `gsap.matchMedia()` or equivalent responsive branches for materially different desktop/mobile motion.
- Refresh ScrollTrigger only when layout/media changes require it; avoid refresh loops.

## React / Next.js

Prefer `@gsap/react` when available.

```tsx
"use client";

import { useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(ScrollTrigger, useGSAP);

export function Scene() {
  const root = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: root.current,
        start: "top top",
        end: "+=2000",
        scrub: true,
        pin: true,
      },
    });

    tl.from("[data-copy]", { autoAlpha: 0, y: 24 })
      .to("[data-copy]", { autoAlpha: 0, y: -16 }, "+=0.6");
  }, { scope: root });

  return <section ref={root}>...</section>;
}
```

Keep GSAP browser-only. Do not execute ScrollTrigger during server rendering.

## Image Sequence Playhead Pattern

Drive a small object, not the DOM itself:

```ts
const playhead = { frame: 0 };

gsap.to(playhead, {
  frame: frameCount - 1,
  ease: "none",
  snap: "frame",
  onUpdate: renderFrame,
  scrollTrigger: {
    trigger: section,
    start: "top top",
    end: "+=3000",
    scrub: true,
    pin: true,
  },
});
```

The official GSAP image-sequence helper uses the same basic idea: map scroll progress to a frame index and draw the requested image to a canvas.

## Lenis Integration

If Lenis is approved, synchronize a single scroll source:

```ts
const lenis = new Lenis();
lenis.on("scroll", ScrollTrigger.update);

gsap.ticker.add((time) => {
  lenis.raf(time * 1000);
});

gsap.ticker.lagSmoothing(0);
```

Do not also run Lenis with a separate uncontrolled RAF loop.

## Frequent Failure Modes

- creating ScrollTriggers on every render
- forgetting cleanup on route changes
- using selector strings without a component scope
- pinning a section whose height changes after image/font load without refresh handling
- preloading hundreds of full-resolution images at once
- animating `top`, `left`, `width`, or `height` continuously when transforms suffice
- using a smooth-scroll library and ScrollTrigger without synchronization
- stacking GSAP, Motion, CSS transitions, and browser smooth scrolling on the same property
- relying on a desktop pin distance for mobile
- making essential content readable only while a precise animation frame is visible

## Reduced Motion

Provide a meaningful static/low-motion path. A common strategy is to keep normal document flow and disable scrub/pin when reduced motion is requested.

## Upstream Sources

Checked 2026-09-12:

- https://gsap.com/docs/v3/Plugins/ScrollTrigger/
- https://gsap.com/docs/v3/HelperFunctions/helpers/imageSequenceScrub/
- https://github.com/greensock/react
- https://github.com/darkroomengineering/lenis
