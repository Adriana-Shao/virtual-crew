# Example project — "The Visitor"（虚构示例）

This folder is **fictional and sanitised**. It exists to show the *data layer* that the crew
skills operate on: a script, a shotlist, a world-state file, a shot prompt, and one comparison
report from a take that came back wrong.

Nothing here comes from a real production: no personal names, no real reference imagery, no
third-party material. The project is deliberately small — one scene, six shots.

```
script.md                      short script: two characters, one scene
shotlist.md                    the shot index (shot / framing / duration / content / variant / status)
world_state.yaml               identity + variants + one scene + props + events
prompts/sc1-shot2.md           a finished shot prompt, in the house format
reports/sc1_s2_take2-qc.md     a comparison report: what the take did wrong, and the fix
shot_log.csv                   take log, with one rejected take and one approved
```

## How this folder would be produced in practice

```bash
python3 ../../scripts/build_project.py script.docx storyboard.docx \
        --out examples/the-visitor --project "The Visitor"
```

That generates `shotlist.md` + `world_state.skeleton.yaml` + `assets_todo.md`; the skeleton is
then filled in by hand (variants, wardrobe paragraphs, scene facts). Everything after that —
prompt drafts, watch-lists, comparison reports, archiving — comes from the crew skills.

## What to look at first

`reports/sc1_s2_take2-qc.md`. It is the artefact that shows what this workflow is actually for:
a take that looked plausible, a specific recorded fact it violated, the severity, and the exact
prompt block that fixes it.
