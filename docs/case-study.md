# Running an AI film like a production
### A case study in method, not in tooling

*Draft v1 — numbers marked `[TO FILL]` come from a real take log and must not be invented.*

---

## 1. Context

I directed a ~20-minute narrative short made with a text-to-video model: cold, hand-held realism,
no score, no subtitles, 16:9. The storyboard runs to 18 scenes and **210 shots**, parsed from my own
script and shot table (874 seconds of listed screen time; the cut runs longer).

The interesting problem was never "can a model make a shot". It was that a film is a web of
obligations — a door that must stay the same door, a chain that must not become handcuffs, a
character whose face must survive a wardrobe change — and a generator holds **none** of them in mind.
Every one of those obligations has to be written down, written into each prompt, and checked after
each take. That is production work, not prompting.

So I built the production crew instead of a prompt trick: five roles, a state file, a failure
catalogue, and two hard human gates.

## 2. The division of labour

The rule I set at the start, and kept: **I write the rules, I audit the result; the model executes.**

- The **model** renders a shot from a prompt and attached reference plates.
- **I** decide what each shot must contain, approve the prompt, generate the clip in my own tool,
  watch it, and judge it usable or not.
- **The crew** (these skills) does the paperwork: looks up the shot, expands continuity, checks the
  prompt against the failure catalogue, produces the asset document, and counts the rework.

Nothing in the pipeline generates on my behalf. Two gates are never automated: **approve the prompt**,
**judge the clip**. Everything else is bookkeeping, and bookkeeping is what I refuse to do by hand.

## 3. The pipeline

**Stage A — assets, before any shot.** From the script and storyboard the crew extracts:
character identities and their variants, four directional views per location, and the props. Output is
one asset document (markdown + Word), saved in the project. For this film: **128 asset prompts**
(13 character identities, 14 variants, 76 view plates = 19 spaces × 4 directions, 25 props).

Two decisions in Stage A do most of the work:

- **Identity vs variant.** The identity prompt pins the face — bone structure, brow, eyes, nose,
  mouth, chin, skin, hair, body, hands, and the marks that make it unmistakable (a mole under the
  left eye, a broken scar in one eyebrow, missing teeth). The variant prompt describes *only the
  delta* — this outfit, this soaked state, this restraint — and says: copy the uploaded identity
  plate, same person. Faces stop drifting because nothing invites the model to re-invent one.
- **Four directions per location.** Each room gets a layout note (what is on each wall, where the
  door is, which side the seam is on) and then four prompts written against it, so a scene cannot
  change shape when the camera turns around.

**Stage B — per shot.** Look the shot up in the shotlist; read the world-state; emit the list of facts
that must be re-described in full (the generator has no memory, so "same as before" is a wasted
token); pick the variant; attach exactly the plates the shot needs; run the QC checks; hand me a
prompt with three or four confirmation points. I approve, generate, watch, report problems in plain
speech, and the crew turns that into a structured comparison report plus the next version.

## 4. The rule system

Four rules carried more weight than any prompt phrasing:

1. **Physical truthfulness.** No adjectives where physics will do. "Resigned" becomes mouth corners,
   gaze, shoulder height, breath. "Fast" is split into speed and amplitude — otherwise "fast" renders
   as a whole-body jolt.
2. **Framing by visibility, not by label.** Not "close-up" but "his face fills the centre, frame edge
   just above the chest" — a label is a suggestion, a description is a constraint.
3. **Reverse locks.** Every shot names what must *not* happen: no second light source, no duplicated
   furniture, no extra hand, no cut, no auto push-in, the chain is not handcuffs, the water is not
   blood. Roughly half my rework traced back to a missing lock.
4. **No cross-shot references, ever.** Position, facing, wardrobe, props and light source are written
   out in full in every prompt, because there is no "previous shot" as far as the model is concerned.

A single style band (era, palette, saturation, single-light rule, sound band) is pasted verbatim into
every prompt — asset and shot alike — so colour cannot drift between plates.

## 5. The QC loop, and how a failure becomes a rule

The catalogue is the part I am most comfortable putting in front of a reviewer, because it cannot be
faked: **15 entries, each one paid for by at least one regenerated take.** Examples: a chain wrapped
around a wrist renders as handcuffs; a slow push-in stops at the chest and the expression is lost;
wet ground renders as blood; three background figures fall into a chorus; a body sinking underwater
renders with the legs floating up.

The loop is: I watch the take and describe what is wrong in plain language → the crew maps it onto the
recorded facts (expected / observed / severity / attribution) → if the cause is a **prompt defect**, a
catalogue entry is written and every future prompt carries the countermeasure; if it is a **model
limitation**, the shot is redesigned (split, reframe, new plate); if it is an **asset problem**, the
plate is regenerated. Only the first kind is a lesson. Attributing the other two to "bad prompting"
would have wasted days.

## 6. Boundaries, decided once

One scene in the script would have required depicting the sexual abuse of a 12-year-old. I ruled it
out of production before shooting started: no prompt, no storyboard, no reference image, no
compromise. What the film does instead is refuse to show it — the cut moves over the night, the
audio carries the aftermath, and the next scene plays on the child's behaviour — and the film's most
important beat (the perpetrator stopping) is carried by a reaction, not by an act. The boundary is
written into the project's content policy and, once stated, is not renegotiated shot by shot.

I put this in a portfolio piece deliberately. Knowing where the workflow must *not* go is part of
running it.

## 7. What it cost

Honest accounting, from the take log:

- Shots in the film: **210** (18 scenes).
- Assets required before shooting: **128** prompts (identity / variant / view / prop).
- Rework rounds per approved shot: **`[TO FILL]`** (from `shot_log.csv`)
- Mean takes per approved shot: **`[TO FILL]`**
- Top failure types by takes lost: **`[TO FILL]`**
- Total render time: **`[TO FILL]`**

Filling those fields is not decoration: they are the difference between "I made a tool" and "I ran a
production". The log is append-only, rejected takes included.

## 8. What I would do differently

- **Do the assets first, properly.** Identity plates before any shot is the single highest-leverage
  rule. Early shots that improvised a look had to be re-shot once the plate existed.
- **Write the failure catalogue as I go, not at the end.** A tendency noticed on take 1 and written
  down saves take 3 of the next shot that shares it.
- **Count from day one.** Attribution (prompt defect / model limitation / asset problem) is only
  useful if it is recorded while the take is fresh.
- **Keep the human in the loop at the two places it matters, and nowhere else.** Driving the render
  queue from an agent added latency and no judgement; watching the clip myself was faster and caught
  more.

## Appendix — the artefacts

- The crew: `virtual-crew` — five role skills, four templates, five scripts, and a fictional example
  project with a worked comparison report.
- Verification: `make verify` (25 checks) and `make lint`, run in this repository.
- Evidence to add before submission: two or three before/after frame pairs (failed take vs approved
  take, cropped to the technical detail — a door form, a prop, a hand), and the filled cost table.
