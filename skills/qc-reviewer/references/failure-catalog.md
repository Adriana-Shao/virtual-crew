# Failure catalogue

Observed model tendency → the countermeasure that was written into the prompt. Every entry earned its place: it cost at least one regenerated take.

Collected against one text-to-video model (see the project profile; entries are model-specific by nature — the structure transfers, the trends must be re-earned when the model changes).

## Entries

| Observed tendency | Countermeasure written into the prompt |
|---|---|
| A chain coiled round a wrist renders as handcuffs | "coiled many times flat against the skin, loose end hanging; not handcuffs — no shackle, no lock, no ring" + "never disappears, never loosens, never moves" |
| "Fast" head or body movement renders as a whole-body jolt / flinch | Separate speed from amplitude: "only the head moves; torso, shoulders, arms, legs stay completely still; no jolt, no shake, no shudder, no shrug"; speed = "snappy, one beat, not slow"; amplitude = "small, normal, no head-snap" |
| A slow push-in stops at the chest, the facial expression unreadable | Define the end frame by what must be visible: "lands on his face — face centred, eyes and mouth clearly readable, frame to just above the chest" + "must not stop at the chest, must not settle on a mid-shot" |
| Wet ground / soaked clothing renders as blood | "clear water soak only — transparent, not red, not rust-coloured; no blood, no pooling; no wounds on the body" |
| Several background figures staged like a chorus | Per-person differentiation: "one reacts sooner, one later, different amplitude; never simultaneous, never in a row, never the same pose" |
| A single door renders as a double door / a second seam appears | "one panel only, full height, not two panels, does not open from the middle, one seam only" + hinge side, handle side, which side the seam is on |
| A knife's edge and spine are swapped | Dedicated orientation block: "the edge (thin, sharpened side) faces inward against the skin; the spine (thick, blunt side) faces outward toward the lens; fingers grip the handle only" |
| Dialogue does not match the mouth | Dedicated lip-sync clause: "mouth opens and closes, jaw moves, each syllable's shape is visible; motion, mouth and audio happen together" + ban on "sound first, mouth later" |
| A knife-to-throat or self-harm beat renders as gore | Restraint per the project's content rules: the blade grazes the top layer of skin only; bleeding = "a few pin-prick red beads on the skin surface, not flowing, not running down, not pooling"; and "only this one graze — no second cut, no sawing" |
| Snatching a weapon from someone draws blood | Name the grip: "he grabs the wrist of the hand holding the knife — not the blade — and pulls the hand away; then grips the handle" + "the edge must not touch anyone's skin; no new wound, no new bleeding" |
| A night scene renders as daytime or gets brightened | "It is night, the sky is dark" + light comes only from the reference's single source + "no daylight, no second source, no car headlights, no flashlight, nothing that brightens the frame" |
| A background that must match a reference gets replaced or invented | "The background is copied strictly from the uploaded reference — identical, not to be changed, nothing may be added that is not in the reference (no shop signs, no other doors, no extra objects)" |
| A prop carried on the body disappears mid-shot | "Stays on him throughout: does not disappear, does not slip off, does not float away, does not change hands" |
| A body sinking underwater renders with the legs floating up | "The whole body sinks as one unit — head, torso and both legs descend together; the legs do not float up, the body does not turn over, does not float on the surface" |
| Off-screen shouting/ambience sounds like it is right next to the camera | Give direction and distance: "the sound comes from off-screen, further away; it is not loud, not close" + bind it to an action in time |

## How to add an entry

1. The director reports what the clip actually did (plain language is fine).
2. Write the **tendency** as the model's habit, not as the shot's topic ("a chain renders as handcuffs", not "shot 22 was wrong").
3. Write the **countermeasure** as text that goes into the prompt: the positive statement *and* the ban, in the wording that worked.
4. Record the attribution: prompt defect / model limitation / asset problem. Only prompt defects become catalogue entries; the other two go to the shot report and the asset list.
5. Keep the entry model-scoped. If a different model is used, start a new section rather than overwriting.

## Severity convention (used in drift reports)

- HIGH — breaks continuity or story information → regenerate.
- MEDIUM — noticeable, survivable, worth fixing on the next take.
- LOW — cosmetic.
