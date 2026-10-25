# Cinematic Storytelling

Use this reference when turning a product/project narrative into scroll-driven scenes.

## Build Chapters, Not Effects

Every chapter needs one narrative job. Motion should reveal, connect, or demonstrate that job.

A useful chapter contract:

```text
ID
purpose
visual state at entry
visual state at exit
copy shown during the chapter
interaction ownership
scroll distance
mobile variant
reduced-motion fallback
acceptance evidence
```

## Evolution Narratives

When the experience represents real-world evolution, use stable named states. The cinematic sequence and the application's domain/event model can share the same conceptual milestones without making the marketing animation the source of truth.

Examples:

- seedling -> planted -> adapted -> young -> established -> flowering -> fruiting -> mature
- raw material -> assembly -> test -> deployment -> operation
- damaged habitat -> intervention -> regeneration -> monitoring -> restored state

Do not compress meaningful domain states merely because a video generator can morph them together.

## Scroll Mapping

Map scroll distance according to narrative density, not clip duration.

- short text + visible transformation: shorter chapter
- dense explanation + subtle transformation: longer chapter
- major reveal: allow pause/pin but keep an escape route

## Copy Layer

Keep essential copy in HTML. Canvas/video is a visual layer, not the document.

Prefer:

- concise chapter headline
- one supporting paragraph or compact data point
- explicit CTA only when it belongs to the current narrative stage

Avoid placing six floating cards on every frame. Cinematic does not mean a dashboard got lost in a forest.

## Continuity

For fixed-location evolution:

- lock camera and framing
- lock background architecture and large landscaping elements
- allow natural secondary motion only when it does not hide the main state change
- keep color grade coherent
- avoid generative changes to logos, signs, buildings, people, or geography unless intentional

## Presentation Mode

A cinematic site may also support a presentation mode:

- scene-by-scene navigation via keyboard/controls
- deterministic chapter starts
- fullscreen-friendly typography
- no requirement to precisely scroll while presenting
- same source content and assets as the public page where practical

Do not maintain a separate throwaway presentation if the same scene system can support both modes cleanly.
