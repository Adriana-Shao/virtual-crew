# Comparison report — sc1-shot2 · take 2

```
COMPARISON REPORT — sc1-shot2 take2
file: pending/sc1_s2_take2.mp4
against: prompts/sc1-shot2.md (v2) + world_state.yaml (Son = V02_soaked)
director's verdict: not usable
date: 2026-09-21

1. ITEM BY ITEM
| # | constraint (expected)                          | observed                                   | severity | attribution     | fix |
|---|------------------------------------------------|--------------------------------------------|----------|-----------------|-----|
| 1 | light: exactly one source, warm lamp, low      | lamp warmth on him, plus a hard white rim- | high     | prompt defect   | add the ban on any second source and on rim light; name the source again in the framing block |
|   |                                                | light from the doorway behind him          |          |                 |     |
| 2 | he does not come in                            | he steps two paces inside the room         | high     | prompt defect   | state the refusal as a physical fact: "his weight stays on the back foot; his feet do not cross the threshold" |
| 3 | bag stays on the shoulder                      | bag on the floor inside the doorway        | high     | prompt defect   | repeat the standing rule inside the action block, not only in reverse locks |
| 4 | wet = clear water, not blood                   | wet and dark, but no red                    | ok       |                 |     |
| 5 | framing: head to knees, locked off             | framing correct, camera locked              | ok       |                 |     |

2. KNOWN FAILURE HIT
- "an off-screen doorway invents its own light" → catalogue entry #11 ("A night scene renders as daytime or gets brightened");
  extend that entry: a bright off-screen doorway is the same habit.

3. NEW FAILURE (added to the catalogue)
- tendency: a door standing open behind a character generates a hard rim-light even when the shot
  specifies one warm source
- countermeasure: name the doorway's light state explicitly — "the doorway behind him is dark; no
  light comes from the doorway; no rim-light on his shoulders or hair"
- evidence: 00:01–00:04

4. NEXT VERSION — v3 changes
1. reverse locks: add "no rim-light; the doorway behind him is dark"
2. action 0–3s: add "his weight stays on the back foot; his feet do not cross the threshold"
3. action 3–6s: repeat the bag rule where the bag is mentioned

5. STATE WRITE-BACK
- not written: take rejected, the world does not advance

6. ARCHIVING
- pending → rejected (take kept as sc1_s2_take2.mp4)
- shot_log.csv appended: take 2, failure_types "light_second_source;action_refusal;prop_missing",
  attribution "prompt defect"
```

## What this report is for

Three constraints fired, all three attributed as **prompt defects** — meaning the process can be
fixed, not just this shot. The fixes are written as text to paste back in, which is what makes the
next take cheaper than the last. A take that is rejected on a *model limitation* or an *asset
problem* is handled differently: redesign the shot, or remake the plate — never by rewriting the
same words harder.
