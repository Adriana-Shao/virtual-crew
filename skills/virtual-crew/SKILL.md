---
name: virtual-crew
description: "Orchestrator for an AI film production crew. Stage A: extract the asset layer from the script and storyboard (character identities and variants, four directional views per location, props) into an asset document in the project folder. Stage B: per shot, route through continuity (world-state), art department (style + assets), QC (failure catalogue) and the ethics gate, then hold the two human gates (approve the prompt; judge the clip) and run the loop — look up shot → draft → approve → the director generates → watch-list → structured comparison → v(n+1) → approve/reject → write state back → log → triage the feedback into the owning skill. Use when starting an AI-generated film, when asked for asset prompts or a shot's prompt, or when a reported problem has to be classified and written into the skills. AIGC 短片制作的资产+镜头总调度，含两处人工确认与反馈归档。"
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

1. `project-profile.yaml` exists in the project root and lists: sources, shotlist, world-state, assets, look, generation driver, folders, naming, content policy.
2. `shotlist.md` and `world_state.yaml` exist (build them with `scripts/build_project.py` if they do not).

## Stage A — assets first (once per film, before any shot prompt)

1. Run `scripts/extract_assets.py` on the script + storyboard → `assets_inventory.md` (characters with variant clues, the scene list, props ranked by frequency).
2. Load `asset-forge`: write the asset document into the project folder, using `templates/asset-prompt-document.md` — character identities, **one prompt per variant** (every wardrobe or face change gets its own), **four directional prompts per location** (N/E/S/W, with a layout note so the four views cannot contradict each other), and prop prompts.
3. Hand it over and stop. The director generates the plates one at a time. Shot work does not begin until the plates a shot needs exist.

## Stage B — the per-shot loop (run in this order, every shot)

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
14. **Triage.** Classify every problem the director reports and write it into the skill that owns it — `references/feedback-triage.md` says which. Answering in chat alone does not count: the entry has to land in the file, and be re-read to confirm.

## Standing rules

- The two gates are never skipped, not "just this once", not when the take looks good.
- The crew never generates. It stops at prompt + report + number; the director runs the generator.
- Never write "same as the previous shot" — re-describe in full.
- The style block and the wardrobe paragraphs are pasted verbatim, never paraphrased.
- A rejected take is data: log it, name the failure type, and add a catalogue entry when the cause is a prompt defect.
- Keep the director's round-trip short: one prompt, one short change list, one number.
