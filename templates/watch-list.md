# Watch-list template

Generated automatically after each take, from the shot's constraints. Risk-ranked so the director knows what to look at first. One line per item, plain language, no jargon.

```
WATCH-LIST — <shot id> take<N>
file: <the file the director saved, e.g. takes/sc1_s11_take1.mp4>
against: prompts/<shot id>.md (v<N>) + world_state.yaml
report to: reports/<shot id>_take<N>-qc.md

HIGH RISK (one miss = regenerate)
1. [ ] <fact class>: <what to check, in one line>
2. [ ] ...
3. [ ] ...

MEDIUM (noticeable, survivable)
4. [ ] ...
5. [ ] ...

DIALOGUE / SOUND (if any)
- [ ] all lines present, none added, said once
- [ ] mouth matches the words
- [ ] no music, no stray voices

BEYOND THE LIST
- anything that feels wrong but is not on the list — say it anyway; those become
  new catalogue entries and are the most valuable feedback of all.
```

## How the list is built

1. Take the shot's reverse locks and its riskiest constraints (from the QC report) — those are HIGH.
2. Add the continuity facts most likely to drift in this set (the scene's `must_not_drift`).
3. Add dialogue/sound checks only if the shot has them.
4. Cap it at ~10 lines. A watch-list nobody reads is worse than none.

The director answers in plain speech ("the door's white and double"). The agent does the mapping, the severities and the fix — never the other way round.
