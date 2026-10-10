---
name: art-department
description: "Art department and look-lock for AI-generated film. Injects the project's style DNA (palette, saturation, era accuracy, single-light rule, period set dressing), extracts the asset list a shot requires, tracks which reference plates are still missing, and flags style drift or anachronism in generated frames. Use when starting a new shot, when the look drifts between shots, or when deciding which assets and reference images to attach. 用于风格统一与资产（人物／场景／道具）管理。"
version: 0.1.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [film, aigc, art-direction, style, assets]
    related_skills: [continuity-supervisor, qc-reviewer]
---

# Art department

Two jobs: keep the look identical from shot to shot, and make sure the plates a shot needs actually exist before the shot is generated.

## Job 1 — inject the style DNA

Every prompt carries the same style block, written once in the project profile and pasted verbatim. It states palette, saturation, era, texture, and the light rule. Example shape:

```
STYLE — <era> realism, <palette>, low saturation, <grain/texture>.
Light: exactly one source per shot, even and uniform across the frame;
no second source, no local highlight, no spot, no beam, no flare in the eyes.
```

Never let a shot restate the look in its own words. One block, copied.

## Job 2 — assets

For each shot, output:

```
ART — <shot id>
plates needed:  <character likeness(es)> · <scene plate> · <prop plates>
attach:         exactly these, nothing more
missing:        <plates that do not exist yet → goes on the todo list>
warnings:       <e.g. "single-person shot: attach one character plate only —
                 multiple plates contaminate each other">
```

Rules that came out of real failures:

- **Single-person shots take exactly one character plate.** Extra plates get blended.
- **A prop plate is only attached when the prop is the subject**; otherwise the prop lives in the wardrobe paragraph.
- **A scene plate is for a place, not a mood.** If a plate is needed only for lighting, say so in the prompt: "this image is a lighting and palette reference only".
- **Reference image vs. shot requirement**: when the reference contains something the shot must change (a note denomination, a colour, a time of day), the prompt must say *what to copy* and *what to replace* — never just "copy the reference strictly".

## Job 3 — drift and anachronism

When a clip comes back (from the director's description, or from frames if a vision model is enabled), check:

- palette / saturation drift against the style block
- era breaks: modern objects, current-day signage, contemporary vehicles, LED lighting, phone models out of period
- set dressing that contradicts the scene's established facts (furniture count, wall colour, floor material)

Report as one line each: `expected → observed → fix`, and promote any repeated break into the scene's `must_not_drift` list.

## Output discipline

- Never invent an asset that does not exist; list it as missing instead.
- Never change the style block per shot for convenience — if a shot genuinely needs a different look, that is a director decision and gets logged.
