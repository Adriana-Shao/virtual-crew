# Virtual Crew

**An agent crew for AI film production — a director keeps judgement, agents keep the paper-trail.**
把 AIGC 短片的工作流拆成剧组的岗位职责，每个岗位做成一个可安装的 agent skill。

Most AI-film workflows demo a model. This one documents the **method**: how a shot gets specified, checked, generated, inspected against a written contract, reworked, and archived — with the human decision points named explicitly.

## The crew

| Skill | Role | What it owns |
|---|---|---|
| `continuity-supervisor` | 场记 | The world-state: who is where, in what wardrobe, holding what, under which light, and which set facts may not drift. Expands continuity into fully re-described prompt sections (models have no memory of previous shots). Flags drift after generation. |
| `art-department` | 美术指导 | Style DNA (palette / era / single-light rule), the asset list a shot needs, which reference plates are missing, and style drift or anachronism in generated frames. |
| `qc-reviewer` | 审片 | Static pre-flight check of a prompt against a catalogue of observed model failure modes, with rewritten lines. |
| `line-producer` | 制片 | Per-shot rework rounds, failure types, render time; averages, pacing risk, and which upcoming shots are high-risk. |
| `ethics-gate` | 伦理闸门 | Content-boundary check before generation: pass / revise / refuse, plus non-depicting alternatives. |

## The loop

```
shot id ──▶ look up (shotlist + world-state)
        ──▶ draft prompt (continuity + art + QC checks)
        ──▶ GATE 1: director approves or edits          ◀── human
        ──▶ submit generation ──▶ auto-download to pending/
        ──▶ generate a watch-list (risk-ranked, one line each)
        ──▶ GATE 2: director watches, reports problems  ◀── human
        ──▶ structured comparison report ──▶ prompt v2 ──▶ regenerate
        ──▶ director says "usable" ──▶ rename (scene+shot) into usable/
                                     else ──▶ rejected/
        ──▶ update world-state + shot log
```

Two gates are deliberately human: **approve the prompt** and **judge usability**. Everything else — lookup, drafting, downloading, report structuring, naming, archiving, logging — is automated.

## Install

```bash
git clone <this-repo> virtual-crew
cp -r virtual-crew/skills/*  ~/.hermes/skills/         # or your agent's skill directory
cp virtual-crew/project-profile.example.yaml  <your-project>/project-profile.yaml
```

Then edit `project-profile.yaml` (paths, model, generation command) and start a session:

> "shot sc1-shot11 — write the prompt"

## Repo layout

```
make verify       # ad-hoc verification of scripts/ (exit 0 = pass) — see scripts/verify_scripts.py
make lint         # syntax-check the scripts

skills/           the five crew roles (SKILL.md + references/)
templates/        prompt skeleton, QC checklist, watch-list, report templates, world-state template
scripts/          build_project.py (parse script+storyboard → shotlist + world-state skeleton)
                  prompt_lint.py · continuity_diff.py · shot_log.py
examples/         the-visitor/ — a small fictional project showing the data layer
assets/           before-after/ (failure vs fixed frames) · demo/
project-profile.example.yaml
```

## Scope and honest limits

- The **method and tooling** are project-agnostic; the **project layer** (script, storyboard, world-state, assets, style DNA) is data you re-supply per film.
- The failure catalogue is model-specific. Entries here were collected against one text-to-video model; the structure transfers, the entries must be re-earned when you change models.
- No model is called for QC in this repo: the director watches and reports, the agent structures the report. An optional vision-model mode is deliberately out of scope so that no frame of an unreleased film leaves the machine.
- Generation is out of scope by default: the crew stops at "prompt + reports". A generation command can be wired in per project (`project-profile.yaml`), still behind GATE 1.

## License

Code (`scripts/`) MIT. Documentation and skill text (`skills/`, `templates/`, `README.md`) CC BY-NC 4.0 — no commercial use.
