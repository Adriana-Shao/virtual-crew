# shot_log.csv — schema and example

One row per generated take.

```csv
shot_id,take,date,duration_s,model,render_s,outcome,failure_types,attribution,notes
sc1-shot11,1,2026-09-21,3,<model>,0,not_generated,,,prompt drafted, awaiting approval
sc5-shot3,1,2026-09-21,6,<model>,420,rejected,prop_orientation,model limitation,"blade edge and spine swapped"
sc5-shot3,2,2026-09-21,6,<model>,395,rejected,prop_orientation,model limitation,"same block, second attempt"
sc5-shot3,3,2026-09-21,6,<model>,410,approved,,,"orientation block rewritten; third take clean"
sc14-shot9,1,2026-09-21,15,<model>,900,rejected,sinking_posture;ambience_level,prompt defect,"legs floated up; off-screen voices too loud/close"
sc14-shot9,2,2026-09-21,15,<model>,880,approved,,,"whole-body sinking clause + distance clause added"
```

## Fields

| Field | Notes |
|---|---|
| `shot_id` | `sc<scene>-shot<n>` |
| `take` | increments per generation; never reused |
| `duration_s` | requested duration |
| `render_s` | wall-clock time for the take (0 if not generated) |
| `outcome` | `not_generated` · `rejected` · `approved` |
| `failure_types` | `;`-separated slugs: `prop_orientation`, `prop_missing`, `set_drift`, `framing`, `lip_sync`, `pacing`, `sinking_posture`, `ambience_level`, `extra_limbs`, `style_drift`, `anachronism`, `gore_restraint`, `dialogue_missing` |
| `attribution` | `prompt defect` · `model limitation` · `asset problem` (empty for approved) |
| `notes` | one line: what happened, what fixed it |

## Rolling metrics (computed from the file)

- rework rounds per shot = number of takes − 1 (approved) or number of takes (abandoned)
- mean renders per approved shot
- top failure types by count → feeds the QC catalogue and the risk table
- total render time per session, per scene, per film

## Conventions

- A take that is regenerated with an unchanged prompt is still a new row (its failure counts as a model limitation, not a prompt defect).
- Approved takes are the only ones whose ending state is written back into `world_state.yaml`.
- Keep the file append-only: no editing of past rows, only adding.
