# Demo recording script

**Already captured:** the four screenshots in `docs/figures/` (`step1-agent-shot-prompt.jpg`,
`step2-agent-qc-report.jpg`, `step3-agent-comparison.jpg`, `step4-terminal-verify.jpg`) — three from
the crew in a session, one from the terminal. These are what the README and the case study use.

**Optional extra:** a 30-second screen recording, if a moving demo is wanted for an interview.
Record it by rehearsing once with `bash scripts/demo_run.sh`, then capturing the same run.

---

## Before you hit record (5 minutes)

1. **Do Not Disturb on** (System Settings → Focus). A notification mid-recording kills the take.
2. Terminal: dark theme, font size ~16 (readable on a phone), window roughly 1200×700, scrolled to the
   top. Hide the sidebar so no private path shows.
3. Resize the browser/other apps away. Only the terminal should be visible.
4. Run the rehearsal once: `cd ~/Desktop/virtual-crew && bash scripts/demo_run.sh`
   It touches **only the fictional example project** — no `Demon` data, no private paths, no keys.
5. Recording: macOS `⌘⇧5` → Record Selected Portion → drag the terminal window → Record.
   Speak or caption afterwards; silence is fine.

---

## The 30 seconds, shot by shot

| Time | On screen | Caption (put on screen in post, or say it) |
|---|---|---|
| 0–3 s | Terminal, one command typed: `bash scripts/demo_run.sh` | "Four commands. Thirty seconds." |
| 3–12 s | Section 1 scrolls: a prompt as first written → **RISK: HIGH (11 items)** with named fixes (no light ban, cross-shot reference, abstract emotion "devastated", framing by label, no sound band) | "This is what a human skim misses." |
| 12–18 s | Section 2: the same shot after the fix → **RISK: LOW (1 item)** | "The fixes are written for me, not just flagged." |
| 18–25 s | Section 3: the take log numbers — 4 takes logged, mean takes per approved shot 1.67, failure types ranked, attribution "prompt defect" | "And it counts the rework — by cause, not just by count." |
| 25–30 s | Section 4: `make verify` → **ALL PASS (27 checks)** + closing line "Generation stays with the director." | "The method is verified. The film is still mine." |

**Do not**: open the film project, show file paths from your own machine, or show any generated clip
of `Demon`. This clip is about the method.

---

## Optional 60-second version ("agent mode")

Only if the crew is installed into your agent (`cp -r skills/* ~/.hermes/skills/`). Adds a screen
showing the agent actually running:

1. (0–15 s) In the agent session, type: **`shot sc1-shot2 — write the prompt`**
   → the crew prints the continuity list, the plates to attach, the prompt, and the QC report.
2. (15–35 s) Type a plain-language problem: **`the door is white and double, and the bag is missing`**
   → a comparison report appears (expected / observed / severity / attribution) with prompt v2.
3. (35–60 s) Same terminal sections as the 30-second version: the numbers and `make verify`.

---

## Where the file goes

- `assets/demo/crew-demo.mp4` — the clip itself
- `assets/demo/crew-demo.gif` — optional, for the README's Demo section
- Then say the word and I will wire the GIF into the README and drop the placeholder note.
