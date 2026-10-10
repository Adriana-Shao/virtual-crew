# Style DNA — reusable look blocks

The style block is the cheapest consistency tool in the whole workflow: one paragraph, pasted verbatim into every prompt, identical wording. What follows is the shape and some reusable variants.

## Shape

```
STYLE
<era> realism, <country/region> <decade>, <palette: hues + saturation>, <surface texture/grain>,
<what the camera feels like: handheld / locked>.
LIGHT
exactly one source per shot, <source and colour temperature>, even and uniform across the frame;
no second source, no local highlight, no spot, no beam, no flare or highlight in the eyes.
BAND
no music, no score, no melody; no subtitles, no watermark, no logo.
```

## Reusable variants

- **Cold 1990s-2000s interior** — "turn-of-the-millennium realism, cold grey-blue, low saturation, slightly soft; one ceiling source, cool white".
- **Night exterior, practical light** — "night, sky fully dark; light comes only from the practical source named in the shot; no daylight, no second source"; add "and the frame must not be so dark that the action cannot be read".
- **Underwater** — "all of the frame is below the surface; the only light is what filters down from the surface above; visibility limited, suspended particles visible; not clear, not blue-and-tropical".
- **Fluorescent institutional** — "sickly green-white fluorescence, slight flicker; flat, unflattering, no fill".
- **Interrogation/police spill** — "red and blue alternating spill across faces and ground, soft and diffused, no beams, no spotlights"; the source object itself stays out of frame.

## Rules that keep a look from drifting

1. One block, verbatim, in every prompt. Paraphrasing per shot is how looks drift.
2. Never add a second light for convenience — write the shot so one source can carry it.
3. Colour words are absolute: say "deep blue, no pattern" rather than "a nice blue".
4. For anything made of an identifiable material (tile, timber, vinyl, enamel), state the material, not the mood.
5. If a plate exists only to fix the palette, mark it in the prompt as a lighting/palette reference only, so the model does not copy its contents.
