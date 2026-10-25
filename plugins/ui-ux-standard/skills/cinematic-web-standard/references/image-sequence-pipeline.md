# Image Sequence Pipeline

Use this reference for photorealistic scroll-scrub media.

## Principle

Treat the lifecycle as named visual states first, then create controlled transitions between adjacent states. This is especially important for biological growth, product assembly, architectural transformation, restoration, or any sequence where identity must remain stable.

Bad pipeline:

```text
one prompt -> one long generative video -> hope continuity survives
```

Preferred pipeline:

```text
keyframe 00
  -> short transition
keyframe 01
  -> short transition
keyframe 02
  -> short transition
...
  -> extract purposeful frames
  -> optimize
  -> validate
  -> manifest
```

## Keyframe Contract

For every adjacent state, preserve unless the story explicitly changes it:

- camera position and focal intent
- horizon/perspective
- environment geometry
- house/background/props
- lighting direction and time-of-day intent
- subject identity/species/product identity
- frame aspect ratio

Change only the intended state variable.

Example for tree growth:

- Phase 01: planted seedling
- Phase 02: adaptation / established roots
- Phase 03: initial growth
- Phase 04: young tree
- Phase 05: canopy formation
- Phase 06: established tree
- Phase 07: flowering
- Phase 08: fruiting
- Phase 09: mature tree

## Video Generation

Generate short clips between adjacent states rather than one long lifecycle. A locked or tightly controlled camera is easier to scrub and easier to stitch.

## Frame Extraction

Use `scripts/extract_frames.sh`.

Example:

```bash
bash scripts/extract_frames.sh growth-01-02.mp4 public/cinematic/scene-01 12 1920 82
```

Arguments:

1. input video
2. output directory
3. FPS (default 12)
4. max width (default 1920)
5. WebP quality (default 82)

For mobile, generate a smaller variant, for example 960 px wide.

## Frame Density

Do not assume 30 FPS. Scroll-scrub footage often works well with 10-15 FPS worth of source frames because scroll progress is not normal playback. Choose density by visual change, not habit.

Use more frames when:

- the subject changes rapidly
- camera motion exists
- thin/high-frequency detail flickers

Use fewer frames when:

- the camera is fixed
- motion is slow
- the scene spends time on copy rather than visual transformation

## Manifest

Generate a deterministic manifest:

```bash
python scripts/make_manifest.py public/cinematic/scene-01 > public/cinematic/scene-01/manifest.json
```

The manifest records ordered frames and byte sizes so the runtime can preload windows predictably.

## Validation

Run:

```bash
python scripts/validate_sequence.py public/cinematic/scene-01 --max-total-mb 35 --max-frame-kb 350
```

Fix gaps and oversized media before implementation. Do not wave through an oversized sequence and hope CDN cache will turn physics into a suggestion.

## Runtime Loading Strategy

- load poster / first frame immediately
- preload a small critical window
- begin the scene when the critical window is ready
- load future frame windows while the user reads the current chapter
- keep a bounded decoded-image cache
- drop stale decoded frames when memory pressure matters
- use separate mobile dimensions/frame density if needed

## Output Formats

- Prefer WebP or AVIF when the target browsers and pipeline support them reliably.
- Keep a fallback only if required by target support.
- Avoid PNG for long photographic sequences unless alpha or lossless fidelity is actually required.

## Canvas Rendering

Use `object-fit`-equivalent math so the sequence can cover the viewport without stretching. Redraw on resize/orientation changes. Bound device-pixel-ratio scaling to protect memory on high-DPR phones.

## Failure Fallback

If a frame fails:

- keep the most recent valid frame
- report/log the missing frame in development
- do not blank the canvas
- ensure the DOM content remains navigable
