---
name: virtual-crew
description: "Orchestrator for an AI film production crew: routes each shot through continuity (world-state), art department (style + assets), QC (failure catalogue) and the ethics gate, then holds the two human gates (approve the prompt; judge the clip) and drives the full loop — look up shot → draft → approve → generate → download → watch-list → structured comparison → v2 → approve/reject → archive. Use when producing shots for an AI-generated film, when asked to write the next shot's prompt, or when a generated clip needs to be checked and archived. AIGC 短片制作的总调度：按镜号走完整回合，含两处人工确认。"
version: 0.1.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [film, aigc, orchestrator, workflow, production]
    related_skills: [continuity-supervisor, art-department, qc-reviewer, line-producer, ethics-gate]
---

# Virtual Crew — the loop

This skill is the dispatcher. It does not write anything itself: it runs the order of operations and hands the work to the crew roles.

## Preconditions

1. `project-profile.yaml` exists in the project root and lists: sources, shotlist, world-state, assets, look, generation command, folders, naming, content policy.
2. `shotlist.md` and `world_state.yaml` exist (build them with `scripts/build_project.py` if they do not).

## The loop — run in this order, every shot

1. **Route by shot id.** Read the profile; locate the shot in `shotlist.md`. Missing → report what is missing, stop.
2. **Continuity** (`continuity-supervisor`): read the world-state, emit the "must be re-described in full" list, name the active variants, name the inherited state.
3. **Art department** (`art-department`): paste the style block, list the plates to attach, flag missing plates, flag the single-plate rule for single-person shots.
4. **Ethics gate** (`ethics-gate`): classify the shot against the content policy. Refuse → stop and offer non-depicting alternatives. Revise → apply the restraint clauses.
5. **QC** (`qc-reviewer`): run the 12 checks; produce the risk list with rewritten lines.
6. **Draft.** Assemble the prompt from `templates/prompt-skeleton.md`, sectioned plain text, actions per second, physics not adjectives, reverse locks present.
7. **GATE 1 — director.** Present the prompt as one copyable block, plus 3-4 confirmation points, plus the plates to attach and the filename to save the clip under. Write the approved version to `prompts/<shot id>.md` (version incremented, old versions kept). The director generates — not the agent.
8. **Watch-list.** Emit a risk-ranked, one-line-per-item list so the director knows what to look for in the render without re-reading the prompt.
9. **GATE 2 — director.** The director generates the clip with their own tool, watches it, and reports problems in plain speech. "The door's white and double" is a complete report.
10. **Comparison report** (`continuity-supervisor` + `qc-reviewer`): map that report onto recorded facts — expected → observed → severity → attribution → the exact block to paste back. Write `reports/<shot>_take<n>-qc.md`.
11. **Next version.** Prompt v(n+1) with a short change list, back to step 7. Take numbers never reuse.
12. **On approval.** Director says usable → write the shot's ending state back into the world-state, update the shotlist status.
13. **Log.** Every take appended to `shot_log.csv`: outcome, failure types, attribution. On request, report rework rounds, failure-type ranking and the high-risk forecast for upcoming shots.

## Standing rules

- The two gates are never skipped, not "just this once", not when the take looks good.
- The crew never generates. It stops at prompt + report + number; the director runs the generator.
- Never write "same as the previous shot" — re-describe in full.
- The style block and the wardrobe paragraphs are pasted verbatim, never paraphrased.
- A rejected take is data: log it, name the failure type, and add a catalogue entry when the cause is a prompt defect.
- Keep the director's round-trip short: one prompt, one short change list, one number.
