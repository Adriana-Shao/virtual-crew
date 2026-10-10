# Feedback triage — where a reported problem goes

Every correction the director reports gets **classified and written into the skill that owns it**.
A report that is only answered in chat and never written down will cost the same take again.

## The table

| What the director reports | Class | Written into |
|---|---|---|
| "the prompt didn't say that" — a fact was missing, a lock absent, an action vague | prompt defect | `qc-reviewer/references/failure-catalog.md` (new entry) + the relevant check in `qc-reviewer/SKILL.md` |
| the same thing drifts between shots: door form, furniture count, a prop that vanishes, wardrobe changed between two shots in one room | continuity | `continuity-supervisor` — the fact's `must_not_drift` entry in the project's `world_state.yaml`, and the format rules in `references/world-state-format.md` if the layer was missing |
| the look drifts: palette, saturation, era, anachronism, style block paraphrased per shot | look | `art-department/references/style-dna.md` (add the variant/banned element) + `art-department/SKILL.md` if a rule was missing |
| the reference plate itself is wrong (face, wardrobe, prop detail, wrong denomination) | asset problem | `asset-forge` — the plate's entry in the asset document gets a v2 prompt, and the shot list entry is flagged |
| "the model just can't do this" — written clearly, still fails, repeatedly | model limitation | `line-producer/SKILL.md` risk table (so it is forecast next time) + catalogue entry, marked as a limitation not a defect |
| an emotion word, a count, a "fast/slow" instruction misread | prompt defect (wording) | `qc-reviewer/references/failure-catalog.md`, with the physics rewrite that worked |
| a content-boundary question, "can we show this after all" | boundary | `ethics-gate` — restate the boundary once, give the non-depicting alternatives, log the decision in the project's `content_policy.md`. Do not re-litigate per shot. |
| "the round-trip is too slow / too many takes" | process | `virtual-crew/SKILL.md` (the loop) and `line-producer` (the numbers that show where the takes go) |

## How to file it

1. **Classify first, then write.** Say the class out loud ("this is a prompt defect, not a model
   limitation") — the class decides the fix.
2. **Write into the owning skill the same turn you answer.** Never "I'll note that later".
3. **Re-read the file after writing** and confirm the entry is there and not duplicated — skills get
   edited from more than one session, and a duplicate entry is worse than none.
4. **One report can produce several entries.** A take that lost a prop *and* a light is two entries
   in two different classes.
5. **Keep entries model-scoped.** Entries are re-earned when the model changes; say which model they
   came from so the next model starts a fresh section instead of inheriting stale advice.
6. **Never weaken a rule to make one take pass.** If the director overrides a rule for a shot, that
   is a project *decision* — it goes in the project's `decisions` block, not by deleting the rule.
