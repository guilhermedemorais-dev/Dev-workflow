# Performance and Accessibility

Use this reference for motion-heavy implementation and QA.

## Budgets Are Project-Specific

Do not pretend one universal number fits every experience. Define budgets in the task/spec. If none exist, propose conservative targets and mark them for approval.

At minimum track:

- critical bytes required before first meaningful scene
- total bytes per chapter
- total sequence bytes by desktop/mobile variant
- frame count
- largest frame
- decoded-memory strategy
- LCP candidate and loading priority
- CLS during loader/scene transitions

## Loading Strategy

Do not block on the entire site's cinematic media.

Preferred pattern:

1. render shell, semantic copy, and poster/first frame
2. load a small critical frame window
3. start experience
4. preload the next chapter while the current chapter is being consumed
5. cap decoded-image cache

## Canvas Memory

High-DPR mobile devices can make a 2D canvas surprisingly expensive. Bound DPR where visual quality remains acceptable and avoid storing hundreds of decoded full-resolution images simultaneously.

## Mobile

Treat mobile as a first-class variant:

- smaller source dimensions
- fewer frames if needed
- shorter or removed pinning
- simpler copy choreography
- reliable touch scrolling
- orientation-change handling

## Reduced Motion

When `prefers-reduced-motion: reduce` is active:

- remove or greatly reduce scrub/pinning
- show representative static states/posters
- keep full content readable in normal flow
- keep links/forms/CTAs functional
- avoid auto-playing decorative motion

## Keyboard and Focus

- pinned scenes must not break tab order
- focus must not move into visually hidden content unexpectedly
- anchor navigation must reach the expected content
- ESC/modals/navigation must work even when smooth scrolling is active

## SEO and Semantics

- essential copy remains DOM text
- headings preserve document hierarchy
- images/posters have appropriate alternatives where meaningful
- canvas is not the only source of substantive information

## Failure Resilience

Test:

- one missing frame
- partial CDN failure
- slow 4G-like network
- cached repeat visit
- JavaScript error in the cinematic layer

The page should degrade to useful content instead of becoming an expensive black rectangle.
