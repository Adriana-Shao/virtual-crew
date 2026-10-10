#!/usr/bin/env python3
"""
build_project.py — turn a script + a storyboard (both .docx) into a project skeleton.

Outputs, into --out DIR:
  shotlist.md                scene/shot index (shot no. / framing / duration / content / variant / status)
  world_state.skeleton.yaml  three-layer state file, scenes + characters pre-filled
  assets_todo.md             plates that must exist before shooting

Usage:
  build_project.py storyboard.docx [script.docx] --out DIR [--project NAME] [--id-prefix sc]

No third-party dependencies (stdlib only): .docx is read straight out of the zip.
"""

import argparse
import html
import os
import re
import zipfile

# ────────────────────────── docx extraction ──────────────────────────

def docx_lines(path):
    """Return the document's text as a list of lines (paragraphs and soft breaks)."""
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    xml = re.sub(r"<w:tab[^>]*/>", "\t", xml)
    xml = re.sub(r"<w:(?:br|cr)[^>]*/>", "\n", xml)   # soft line breaks (Word uses these a lot)
    xml = xml.replace("</w:p>", "\n")
    xml = re.sub(r"<[^>]+>", "", xml)
    text = html.unescape(xml)
    return [ln.strip() for ln in text.split("\n")]


# ────────────────────────── storyboard parsing ──────────────────────────

SCENE_RE = re.compile(r"^场景\s*(\d+)\s*[：:]\s*(.*)$")
INT_RE = re.compile(r"^\d{1,3}$")


def parse_storyboard(lines):
    """Scenes → shots. A shot is a bare integer followed by six field lines:
    content / framing / performance / camera / duration / sound."""
    scenes, cur = [], None
    n = len(lines)
    i = 0
    while i < n:
        ln = lines[i]
        if not ln:
            i += 1
            continue
        m = SCENE_RE.match(ln)
        if m:
            head = m.group(2)
            parts = [p.strip() for p in re.split(r"[·|]", head) if p.strip()]
            cur = {
                "id": "sc" + m.group(1),
                "raw": ln,
                "name": parts[0] if parts else "",
                "time": parts[1] if len(parts) > 1 else "",
                "place": parts[2] if len(parts) > 2 else "",
                "shots": [],
            }
            scenes.append(cur)
            i += 1
            continue
        if cur is None:
            i += 1
            continue
        if INT_RE.match(ln):
            idxs = [j for j in range(i + 1, min(i + 8, n)) if lines[j] != ""]
            if len(idxs) >= 5:
                vals = [lines[j] for j in idxs]
                content, framing, perf, cam, dur = vals[:5]
                sound = vals[5] if len(vals) > 5 else ""
                if re.fullmatch(r"\d{1,3}", dur) or dur in ("—", "-"):
                    cur["shots"].append({
                        "n": ln, "content": content, "framing": framing,
                        "perf": perf, "camera": cam, "duration": dur, "sound": sound,
                    })
                    i = idxs[min(len(idxs), 6) - 1] + 1
                    continue
        i += 1
    return scenes


# ────────────────────────── script parsing ──────────────────────────

CHAR_RE = re.compile(r"^([\u4e00-\u9fa5A-Za-z·\s]{2,8})\s*——\s*(\d{1,3})\s*岁[。，,、]?\s*(.*)$")


def parse_script(lines):
    chars = []
    for ln in lines:
        m = CHAR_RE.match(ln)
        if m:
            chars.append({"name": m.group(1).strip(), "age": m.group(2), "bio": m.group(3).strip()})
    return chars


# ────────────────────────── writers ──────────────────────────

def _write(path, lines):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    return path


def write_shotlist(scenes, out_dir, project):
    L = [f"# {project} — shotlist", "",
         "> Built by virtual-crew/scripts/build_project.py from the storyboard.",
         "> Status: todo | drafted | generated | approved | excluded.",
         "> Variant column refers to world_state.yaml entries.", ""]
    total = secs = 0
    for sc in scenes:
        L += [f"## {sc['id']} — {sc['name']} · {sc['time']} · {sc['place']}", "",
              "| shot | framing | dur(s) | content | variant | status |",
              "|---|---|---|---|---|---|"]
        for s in sc["shots"]:
            c = s["content"].replace("|", "/")
            c = c[:60] + ("…" if len(c) > 60 else "")
            L.append(f"| {s['n']} | {s['framing']} | {s['duration']} | {c} |  | todo |")
            total += 1
            if s["duration"].isdigit():
                secs += int(s["duration"])
        L.append("")
    L += ["## Totals", f"- scenes: {len(scenes)}", f"- shots: {total}",
          f"- duration: {secs} s ≈ {round(secs/60, 1)} min"]
    path = os.path.join(out_dir, "shotlist.md")
    _write(path, L)
    return path, total, secs


def write_world_state(scenes, chars, out_dir, project):
    L = ["# world_state.yaml — skeleton, fill as you go",
         "# identity (never changes) · variants (change with events) · state_by_shot (position & facing)",
         "# Read before writing every prompt; write back only after a take is approved.", "",
         "version: 1", f'project: "{project}"', "updated: \"\"", "",
         "precedence:",
         "  - decisions file first, then the script for plot and dialogue,",
         "    then the storyboard for framing/camera/duration/sound, then assets and reference images",
         "",
         "global_look:",
         '  era: ""', '  palette: ""', '  ratio: "16:9"', '  model: ""', '  camera_style: ""',
         '  light_rule: "one source per shot; no second source, no local highlight, no beam, no flare in the eyes"',
         '  audio_band: "no music, no score, no melody; no subtitles, no watermark, no logo"', "",
         "decisions: []", "", "scenes:"]
    for sc in scenes:
        L += [f"  - id: {sc['id']}",
              f'    name: "{sc["name"]}"',
              f'    time: "{sc["time"]}"',
              f'    place: "{sc["place"]}"',
              "    established_facts: []      # door form, floor, furniture count, light",
              "    must_not_drift: []         # the facts that have burned you before"]
    L += ["", "characters:"]
    if chars:
        for c in chars:
            L += [f"  {c['name']}:",
                  "    identity:",
                  f'      age: "{c["age"]}"',
                  f'      role: "{c["bio"][:80]}"',
                  '      body: ""', '      hair: ""', '      permanent_marks: []',
                  '      likeness_assets: []', '      voice_assets: []',
                  "    variants:",
                  "      V01_default:",
                  '        wardrobe_paragraph: ""   # canonical — paste verbatim into prompts',
                  '        body_state: ""', '        restraints: ""', '        props_held: []',
                  '        attach_assets: []', '        used_in: []',
                  "    state_by_shot: {}"]
    else:
        L += ["  # no character bios found in the script; add identity blocks by hand"]
    L += ["", "props: []", "", "events_done: []", "", "not_revealed_to_audience: []", "",
          "content_policy:",
          "  file: content_policy.md",
          "  ruled_out: []"]
    path = os.path.join(out_dir, "world_state.skeleton.yaml")
    _write(path, L)
    return path


def write_assets_todo(scenes, chars, out_dir):
    L = ["# Assets todo", "", "Plates that must exist before the shots that need them.", "",
         "## Characters (likeness + voice)", ""]
    for c in chars or []:
        L.append(f"- [ ] {c['name']}（{c['age']}岁）— likeness plate, voice plate")
    L += ["", "## Scenes (place plates)", ""]
    for sc in scenes:
        L.append(f"- [ ] {sc['id']} {sc['name']}（{sc['time']}·{sc['place']}）")
    L += ["", "## Props", "", "- [ ] (list the props that must be generated as plates)"]
    path = os.path.join(out_dir, "assets_todo.md")
    _write(path, L)
    return path


# ────────────────────────── main ──────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("script", nargs="?")
    ap.add_argument("--out", required=True)
    ap.add_argument("--project", default="untitled")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    scenes = parse_storyboard(docx_lines(args.storyboard))
    chars = parse_script(docx_lines(args.script)) if args.script else []

    p1, total, secs = write_shotlist(scenes, args.out, args.project)
    p2 = write_world_state(scenes, chars, args.out, args.project)
    p3 = write_assets_todo(scenes, chars, args.out)

    print(f"scenes={len(scenes)} shots={total} duration={secs}s ({round(secs/60,1)} min)")
    print(f"characters detected: {', '.join(c['name'] for c in chars) or 'none'}")
    for p in (p1, p2, p3):
        print("wrote", p)


if __name__ == "__main__":
    main()
