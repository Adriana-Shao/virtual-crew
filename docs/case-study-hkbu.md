# A verifiable pipeline for AI film production
### Version for HKBU — MSc in AI and Digital Media
*Xinrui Shao · case study · 2026*

---

## 1. Context

I produced *Demon*, a ~20-minute narrative short generated with a text-to-video model across 18 scenes
and 210 shots. The generator is non-deterministic, stateless between calls, and cannot be asked to
"keep it consistent" — properties that make it a very ordinary engineering problem wearing an
unfamiliar costume: **requirements have to be externalised, and failures have to be attributable.**

This case study describes the pipeline I built to do that, what it measured, and what it does not
claim.

## 2. Problem framing

Given a generator with no memory, a shot is not a request — it is a contract. Every contract has
clauses: what is in frame, which hand does what, which light source exists, which prop is held and in
what condition, and which of those facts is being inherited from an earlier shot in the same place.

Three failure modes dominate, and they need different fixes:

| Failure mode | Example | Correct response |
|---|---|---|
| Prompt defect | a wet floor renders as blood because the prompt never said "water, not blood" | add a reverse lock; write the failure into the catalogue |
| Model limitation | a wooden door specified as single-panel keeps rendering as a double door | redesign the shot: reframe, split it, or replace the plate |
| Asset problem | the reference plate itself is wrong (a note denomination, a face) | remake the plate before another take |

Collapsing these three into "the model is bad at doors" is the single most expensive mistake in this
workflow: it produces rewrites where redesigns were needed.

## 3. The system

**Roles as modules.** Seven skills: an orchestrator plus an asset forge, continuity supervisor, art
department, QC reviewer, line producer and an ethics gate. Each owns one artefact and one decision
class, so a correction lands in exactly one place.

**A data layer, not a prompt file.** Four artefacts persist between sessions:

1. a shot index parsed from the script and storyboard (shot id, framing, duration, content, sound);
2. a world-state file in three layers — permanent identity, story variants (outfit, soaked, beaten,
   bound), and per-shot position/facing — where each variant stores a canonical wardrobe paragraph
   that is pasted verbatim into prompts;
3. an asset inventory with attribution heuristics (a clue is credited to the nearest named character
   within a character window; everything else goes to a human triage list rather than being guessed);
4. an append-only take log recording outcome, failure types and attribution per take.

**Human-in-the-loop by design.** Two gates: approve the prompt, judge the clip. QC is performed by
the director and reported in plain speech; the system converts that into a structured comparison
report. No vision model is invoked — deliberately, so that no frame of an unreleased film leaves the
machine. The repository contains no API keys and calls no model: it stops at prompt, report and number.

## 4. Implementation

Six Python scripts, standard library only, no `pip install`:

- `build_project.py` — parses a storyboard `.docx` into a shot index and a world-state skeleton
  (handles the soft-line-break encoding that Word uses, which naive paragraph splitting loses);
- `extract_assets.py` — builds the asset inventory: characters, variant clues, scenes, props ranked by
  frequency, with nearest-name clause attribution and an explicit "unattributed" list;
- `prompt_lint.py` — 12 pre-flight checks (single light source, reverse locks present, framing by
  content rather than label, cross-shot references, abstract emotion words, exact numbers, dialogue
  braces, prop existence, hand assignment, camera clause, catalogue match, sound band) with severity
  classes and rewritten lines;
- `md_to_docx.py` — writes a valid `.docx` package directly (zip + OOXML) for the asset document the
  director copies prompts out of;
- `shot_log.py` — appends takes and reports mean takes per approved shot, rework rounds and a
  failure-type ranking;
- `verify_scripts.py` — the harness behind `make verify`.

**Verification.** `make verify` runs 27 checks: synthetic-docx parsing, character extraction across
soft breaks, writer outputs, linter severity and case handling, the document package structure, CJK
font configuration, and an append-only take-log round trip. It is labelled ad-hoc verification, not a
test suite — it exercises the changed behaviour, not the space of inputs.

![Figure 1 — the prompt linter on a shot as first written: 11 defects, each with the rewritten line,
then the same shot clean.](figures/fig1-prompt-lint-before-after.png)

![Figure 2 — `make verify`: 27 checks over the parsers, the linter, the document writer and the take
log; exit 0.](figures/fig3-verification.png)

## 5. Results and measurement

| Measure | Value |
|---|---|
| Shots in the film | 210 across 18 scenes |
| Asset prompts generated before shooting | 128 (13 identities, 14 variants, 76 four-direction location views, 25 props) |
| Failure catalogue entries | 15, each traceable to a real failed take |
| Verification checks | 27 (`make verify`) |
| Mean takes per approved shot | `[TO FILL]` |
| Rework rounds per approved shot | `[TO FILL]` |
| Top failure types by takes lost | `[TO FILL]` |
| Total render time | `[TO FILL]` |

The fields marked `[TO FILL]` are left empty on purpose: they come from the take log and are not
invented. The measurement matters for the same reason attribution does — it is what tells you whether
the next improvement should be a rewritten clause, a different shot design, or a new plate.

![Figure 3 — the take log after four takes: rework rounds, the failure types that cost them, and the
attribution that decides the fix.](figures/fig2-rework-accounting.png)

## 6. Limitations and threats to validity

- **Single case.** One film, one director, one generator. The pipeline's structure is the claim; the
  catalogue's contents are not.
- **Model-specific catalogue.** The 15 entries describe one model's habits. Changing models does not
  transfer the entries — it starts a new section in the catalogue, which is exactly why the catalogue
  is versioned by model rather than averaged.
- **Human QC.** No automated vision check, by choice. This bounds throughput (the director is the
  bottleneck) and removes an obvious measurement channel; a local vision model could lift this without
  sending frames off-machine, and is a candidate next step.
- **Ad-hoc verification.** 27 checks, not a suite; failure modes in the parsers' degenerate inputs are
  not exhausted.

## 7. What generalises, and next steps

What generalises is the pipeline, not the catalogue: externalise requirements into a persistent data
layer; make failures attributable before making them rarer; keep the human at the two decisions that
require judgement; measure the loop.

Next steps: (1) apply the pipeline to a second script and a second model, and compare rework rounds
per shot; (2) add a local vision-QC mode under the same privacy constraint (frames never leave the
machine); (3) promote the most frequent prompt defects into lint rules so they are caught statically
rather than in a take.

**Links.** Repository: `<repo link>` · 60-second walkthrough: `<video link>` · Film: *Demon* (2026)
