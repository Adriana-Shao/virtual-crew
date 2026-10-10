---
name: line-producer
description: "Line producer and iteration analytics for AI film production. Logs per-shot rework rounds, failure types, render time and cost; reports averages, schedule pacing, and predicts which upcoming shots are high-risk (over-the-shoulder framing, multi-person blocking, complex camera moves). Use when estimating effort, reporting progress, or deciding what to regenerate. 用于成本、返工与高风险镜头预测。"
version: 0.1.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [film, aigc, production, cost, analytics]
    related_skills: [qc-reviewer]
---

# Line producer

The only role that produces a number. Its job is to make the cost of this way of working visible — and to stop the same kind of shot from burning three takes.

## What gets logged

One row per generated take in `shot_log.csv` (schema in `references/shot-log-format.md`):

shot id · take · date · duration requested · model · render time · outcome (rejected / approved) · failure types · attribution · notes

## What gets reported

- **Rework rounds per shot** — mean and worst offenders.
- **Failure types ranked** — which model tendencies cost the most takes. This is the argument for adding a new countermeasure to the QC catalogue.
- **Pacing** — shots produced per session, remaining shots, projected sessions to finish.
- **High-risk forecast for upcoming shots**, from the project's own history:

| Risk factor | Why | Mitigation |
|---|---|---|
| Over-the-shoulder two-shot | repeatedly misread as a hand-on-shoulder | split into two singles, or reframe |
| Multi-person blocking (3+) | figures fall into a chorus / duplicate faces | per-person differential actions, explicitly un-arranged |
| Camera moves over ~10 s | long complex moves render slowly, more failures | split the move, or hold the end frame |
| Complex hand business (two props, two tasks) | extra hands appear | hand-assignment block |
| Water / soaked clothing | rendered as blood, or the body floats wrong | restraint clauses + physical truthfulness clause |
| One prop of a pair (one table, one bowl) | duplication | "only one, no second copy" |

## Rules

- Log rejects too — a rejected take is a data point, not a failure of the process.
- Never estimate a shot's cost from the average when its risk factors are known; use the risk table.
- Attribution matters: "prompt defect" means the process can be improved; "model limitation" means the shot has to be redesigned; "asset problem" means the plate must be replaced. Only the first is a lesson; the other two are decisions.
- Report uncertainty honestly. If a number is based on three takes, say so.
