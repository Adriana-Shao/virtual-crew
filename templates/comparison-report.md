# Comparison report template

One per take. This is the document that turns "it looks wrong" into a decision.

```
COMPARISON REPORT — <shot id> take<N>
file: <the take the director saved>
against: prompts/<shot id>.md (v<N>) + world_state.yaml
director's verdict: usable | not usable
date: 

1. ITEM BY ITEM
| # | constraint (expected) | observed | severity | attribution | fix |
|---|---|---|---|---|---|
| 1 | | | high/med/low | prompt defect / model limitation / asset problem | |
| 2 | | | | | |

2. KNOWN FAILURE HIT
- <tendency> → catalogue entry #<n>; the countermeasure exists — paste it in verbatim.

3. NEW FAILURE (added to the catalogue)
- tendency:
- countermeasure (the wording that fixed it):
- evidence: <timecode / frame>

4. NEXT VERSION — v<N+1> changes
1.
2.
type of change: added reverse lock / reframed / split the action / replaced a plate

5. STATE WRITE-BACK (only when usable)
- position / facing:
- props and condition:
- light and time:
- events now true:

6. REWORK ACCOUNTING
- take number, outcome, failure types, attribution → shot_log.csv
- rounds this shot has cost so far:
- if the same failure type recurs, the next fix must be a different approach (split / reframe / new plate), not the same words again
```

## Severity

- **high** — breaks continuity or changes story information → regenerate.
- **medium** — noticeable, survivable; fix on the next take.
- **low** — cosmetic.

## Attribution (decides how to fix)

- **prompt defect** — the prompt did not say it → add a reverse lock. *A lesson: catalogue it.*
- **model limitation** — the prompt said it and the model still cannot → redesign the shot (split, reframe, replace the approach). *Not a wording problem.*
- **asset problem** — the reference plate is wrong → remake the plate before another take.
