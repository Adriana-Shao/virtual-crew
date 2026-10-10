---
name: qc-reviewer
description: "Pre-generation QC for text-to-video prompts. Static-checks a prompt for missing light constraints, missing negative constraints ('reverse locks'), framing defined by a label instead of by what is visible, abstract emotion words, cross-shot references such as 'same as the previous shot', exact numbers, and missing dialogue lines; returns a risk list with rewritten lines and the matching evidence from an empirically collected failure catalogue. Use before submitting any prompt for generation, or after a clip comes back wrong. 交付前提示词体检，防止重复踩同一个坑。"
version: 0.1.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [film, aigc, qc, prompt-engineering, failure-modes]
    related_skills: [continuity-supervisor, ethics-gate]
---

# QC reviewer

A prompt that reads well to a human can fail as an instruction. This role checks the prompt **before** it is submitted, against a catalogue of failure modes that were actually observed in generated clips — not against theory.

## The check list

Run all of these, in order. Report only the ones that fire, plus a one-line "clean" summary of the rest.

| # | Check | What fires |
|---|---|---|
| 1 | **Light** | No explicit single-source statement, or no ban on a second source / beam / flare in the eyes. |
| 2 | **Reverse locks** | The prompt says what must happen but not what must *not* happen. Every shot needs named forbiddens. |
| 3 | **Framing by visibility** | Framing given only as a label ("close-up", "medium"). Rewrite as what is visible ("head to knees in frame"). |
| 4 | **Cross-shot references** | Any "same as before / unchanged / as in the previous shot". Must be expanded in full. |
| 5 | **Abstract emotion** | Words like resigned, helpless, bitter, wary. Convert to physics (mouth corners, gaze, shoulder height, breath). |
| 6 | **Exact numbers** | "3 seconds", "about three times", "5 cm". Generators over-literalise counts. Use small/vague ("a few", "barely"). |
| 7 | **Dialogue** | Every line present, in order, said once, `{}`-marked; no lines borrowed from another shot; lip-sync clause present; no "same as" for a repeated line. |
| 8 | **Prop continuity** | Props in hand, where they are, in what condition, and the ban on them vanishing / changing hands / duplicating. |
| 9 | **Hand assignment** | Multi-task shots: which hand does what, and "no third hand / no extra fingers". |
| 10 | **Camera clause** | Move or lock stated explicitly, plus the bans (no auto push-in, no cut, no whip to the wrong subject). |
| 11 | **Catalogue match** | Does any block resemble a known failure in `references/failure-catalog.md`? If yes, the countermeasure must be present verbatim. |
| 12 | **Sound band** | No-music/no-subtitle band present; ambience bans preserved; and any off-screen voice has a direction and a timing bound to an action. |

## Report format

```
QC — <shot id> v<N>                  RISK: LOW | MEDIUM | HIGH
[1] MISSING REVERSE LOCK (light)                     HIGH
    issue:    no ban on a second light source
    fix:      add → "only one light source; no second source, no beam, no flare in the eyes"
[2] FRAMING BY LABEL                                 MEDIUM
    issue:    "close-up" (the model compresses labels)
    fix:      replace → "his face fills the centre of the frame, eyes and mouth clearly readable,
               frame edge just above his chest"
CLEAN: reverse locks (props), dialogue, hand assignment, camera, sound band
```

Rules for the report:

- Every item carries the **rewritten line** — the director pastes it, never rewrites it themselves.
- Grade severity by consequence: HIGH = the shot's information breaks or it will be regenerated; MEDIUM = noticeable; LOW = cosmetic.
- When the honest fix is not a wording change, say so in the attribution field: **prompt defect** (add a lock) / **model limitation** (change approach: split the shot, change the plate, accept it) / **asset problem** (the reference plate itself is wrong).
- If two or more HIGH risks share one cause, say it once at the top instead of repeating it per block.

## Rules

- Never silently rewrite the director's intent. Flag, propose, let them decide.
- Never remove a clause the director asked for; if it conflicts with a lock, say so explicitly.
- After a clip comes back wrong, this role writes the *new* entry into `references/failure-catalog.md` (tendency → countermeasure → evidence) so the same failure cannot cost a second take.
