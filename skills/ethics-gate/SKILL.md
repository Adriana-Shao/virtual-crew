---
name: ethics-gate
description: "Content-boundary gate for AI film production. Checks each prompt against the project's stated content policy before generation and returns pass / revise / refuse, together with non-depicting alternatives (omit the beat, cut away, transition over it, substitute a reaction shot). Use before writing prompts for any sensitive scene, or when a script beat crosses the project's stated limits. 敏感内容闸门：生成前判定通过／修改／拒绝，并给出不呈现的替代方案。"
version: 0.1.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [film, aigc, ethics, content-policy, safety]
    related_skills: [qc-reviewer]
---

# Ethics gate

A working method for a probabilistic image generator needs a boundary that is decided **once, in writing, before production** — not re-argued shot by shot under deadline pressure.

## Procedure

1. Read the project's content policy (`content_policy.file` in the profile).
2. For the shot in question, classify: **within scope** · **needs revision** · **out of scope**.
3. If within scope: pass, and note any restraint clauses the prompt must carry (violence kept non-graphic, injuries limited to named small details, no gore).
4. If needs revision: return the revised framing — usually restraint clauses, off-screen treatment, or a reframe that preserves the story beat.
5. If out of scope: refuse the prompt, and do not design the shot. Offer non-depicting alternatives instead, and log the decision.

## Non-depicting alternatives (the toolkit)

- **Omit the beat** and let the cut imply it.
- **Cut away**: hold on a neutral object or an empty space while the audio carries it.
- **Transition over it**: end on a light/time change (the following morning) rather than the event.
- **Substitute a reaction shot**: the consequence instead of the act — a character's behaviour afterwards, without the triggering action on screen.
- **Record, don't depict**: the world-state records that an event happened (because later shots inherit its consequences: injuries, blood, a police report), while the film never shows it.

## Rules

- A boundary is **decided once** and does not get renegotiated per shot. If pressed — "it's for the story", "it's not really that" — restate the boundary in one sentence and move straight to the alternatives. Do not re-argue it each time.
- The boundary is not a judgement about the film; it is a production rule, like a stunt-safety rule.
- Record the decision: shot id, classification, alternative chosen. A documented boundary is also a portfolio asset — it shows the workflow knows where its limits are.
- Never write, storyboard, or describe the depiction you refused. Not as a "compromise", not for reference, not "just for the shot list".
- Everything outside the boundary is produced normally. One boundary does not shrink the project.
