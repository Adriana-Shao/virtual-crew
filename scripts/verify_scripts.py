#!/usr/bin/env python3
"""
verify_scripts.py — self-contained checks for this repo's scripts.

    python3 scripts/verify_scripts.py        # exit 0 = all pass

Ad-hoc verification, not a full test suite: it builds a synthetic .docx in a temp dir,
exercises the parsers and writers, checks the linter's severity/case handling, and
round-trips the shot log. Everything it creates is removed at the end.
"""
import csv
import contextlib
import io
import os
import re
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_project as BP          # noqa: E402
import extract_assets as EX         # noqa: E402
import md_to_docx as MD             # noqa: E402
import prompt_lint as PL            # noqa: E402
import shot_log as SL               # noqa: E402

fails = []


def check(name, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + name + (f"   [{detail}]" if detail and not cond else ""))
    if not cond:
        fails.append(name)


def make_docx(path, body_xml):
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("word/document.xml",
                   '<?xml version="1.0"?><w:document><w:body>' + body_xml + '</w:body></w:document>')


tmp = tempfile.mkdtemp(prefix="hermes-verify-vc-")
try:
    # ── storyboard: shot blocks; script: bios behind soft breaks ─────────────
    sb = ("<w:p><w:t>场景1：测试巷 · 夜 · 外</w:t></w:p>"
          "<w:p><w:t>1</w:t></w:p><w:p><w:t>画面甲</w:t></w:p><w:p><w:t>中景</w:t></w:p>"
          "<w:p><w:t>动作甲</w:t></w:p><w:p><w:t>固定机位</w:t></w:p><w:p><w:t>3</w:t></w:p><w:p><w:t>声音甲</w:t></w:p>"
          "<w:p><w:t>场景2：测试家 · 日 · 内</w:t></w:p>"
          "<w:p><w:t>1</w:t></w:p><w:p><w:t>画面乙</w:t></w:p><w:p><w:t>特写</w:t></w:p>"
          "<w:p><w:t>动作乙</w:t></w:p><w:p><w:t>手持</w:t></w:p><w:p><w:t>4</w:t></w:p><w:p><w:t>声音乙</w:t></w:p>")
    sc = "<w:p><w:t>陈宇 —— 18岁。说明一</w:t><w:br/><w:t>文渔 —— 48岁。说明二</w:t></w:p>"

    sb_path, sc_path = os.path.join(tmp, "sb.docx"), os.path.join(tmp, "sc.docx")
    make_docx(sb_path, sb)
    make_docx(sc_path, sc)

    scenes = BP.parse_storyboard(BP.docx_lines(sb_path))
    chars = BP.parse_script(BP.docx_lines(sc_path))

    check("storyboard: scenes parsed", len(scenes) == 2, str(len(scenes)))
    check("storyboard: shots parsed", sum(len(s["shots"]) for s in scenes) == 2,
          str([len(s["shots"]) for s in scenes]))
    check("storyboard: header split into name/time/place",
          (scenes[0]["name"], scenes[0]["time"], scenes[0]["place"]) == ("测试巷", "夜", "外"),
          str(scenes[0]))
    check("storyboard: duration parsed", scenes[0]["shots"][0]["duration"] == "3", str(scenes[0]["shots"][0]))
    check("script: bios behind <w:br/> extracted",
          [c["name"] for c in chars] == ["陈宇", "文渔"], str([c["name"] for c in chars]))
    check("script: ages parsed", [c["age"] for c in chars] == ["18", "48"], str(chars))

    out = os.path.join(tmp, "out")
    p1, total, secs = BP.write_shotlist(scenes, out, "test")
    BP.write_world_state(scenes, chars, out, "test")
    BP.write_assets_todo(scenes, chars, out)
    check("writers: three files written with right totals",
          all(os.path.exists(os.path.join(out, f)) for f in
              ("shotlist.md", "world_state.skeleton.yaml", "assets_todo.md"))
          and (total, secs) == (2, 7), f"total={total} secs={secs}")

    # ── prompt_lint ──────────────────────────────────────────────────────────
    clean = ("[STYLE] one source per shot; No second source, no beam, no spot; no flare in the eyes\n"
             "[REVERSE LOCKS] only one bag; no second bag\n"
             "[CAMERA] locked off; does not move\n"
             "[SOUND] no music, no score, no subtitles; no flies, no dripping-tap sound\n"
             "two hands, ten fingers")
    clean_path = os.path.join(tmp, "clean.txt")
    open(clean_path, "w").write(clean)
    issues = PL.check(clean, PL.EN, has_dialogue=False)
    check("lint: capitalised ban recognised",
          not any(a == "light" and "second" in w for _, a, w, _ in issues), str(issues))
    check("lint: clean prompt has no HIGH", not any(s == "HIGH" for s, *_ in issues), str(issues))

    bad = "中景，拍他。他无奈地站着。"
    issues_bad = PL.check(bad, PL.ZH, has_dialogue=True)
    areas = {a for _, a, _, _ in issues_bad}
    check("lint: defective prompt raises HIGH", "HIGH" in {s for s, *_ in issues_bad}, str(issues_bad))
    check("lint: abstract emotion flagged", "abstract emotion" in areas, str(issues_bad))
    check("lint: missing dialogue braces flagged", "dialogue" in areas, str(issues_bad))

    rc = 0
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            sys.argv = ["prompt_lint.py", clean_path, "--lang", "en"]
            PL.main()
    except SystemExit as e:
        rc = e.code
    check("lint: CLI exits 0 on a clean prompt", rc == 0, str(rc))

    # risk aggregation: LOW-only items must not read as MEDIUM
    low_only = "one source per shot; no second source; no flare in the eyes\nonly one bag\nlocked off; does not move\nno music, no subtitles; no flies"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            sys.argv = ["prompt_lint.py"]
            open(os.path.join(tmp, "low.txt"), "w").write(low_only)
            sys.argv = ["prompt_lint.py", os.path.join(tmp, "low.txt"), "--lang", "en"]
            PL.main()
        except SystemExit:
            pass
    check("lint: LOW-only prompt reports RISK: LOW", "RISK: LOW" in buf.getvalue(), buf.getvalue()[:80])

    # ── extract_assets ───────────────────────────────────────────────────────
    sc = [{"id": "sc1", "name": "x", "time": "夜", "place": "外",
           "shots": [{"n": "1", "content": "陈宇光着上身站在门边", "perf": ""},
                     {"n": "2", "content": "他的钱包放在台阶上。", "perf": ""}]}]
    ch = [{"name": "陈宇", "age": "18", "bio": ""}, {"name": "文渔", "age": "48", "bio": ""}]
    pc, un, rows_, props, first = EX.build(sc, ch, [])
    check("assets: clue credited to the nearest name",
          ("sc1-shot1", "光着上身") in pc["陈宇"].get("身体状态", []), str(dict(pc)))
    check("assets: unnamed clue goes to triage, not to a character",
          any("钱包" in t for _, _, t in un) and not pc["文渔"], str(un[:3]))
    check("assets: props ranked with first appearance",
          props["钱包"] == 1 and first["钱包"] == "sc1-shot2", str(dict(props)))
    inv_path = EX.write_inventory(out, "t", ch, (pc, un, rows_, props, first), len(sc))
    check("assets: inventory document written", os.path.exists(inv_path))

    # ── md_to_docx ───────────────────────────────────────────────────────────
    md = os.path.join(tmp, "doc.md")
    open(md, "w", encoding="utf-8").write(
        "# T\n\n## H\n\n### P\n\n- item **bold** and *italic*\n- wrapped **bold\n  across lines**\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n> quote\n")
    dx = MD.convert(md, os.path.join(tmp, "doc.docx"))
    with zipfile.ZipFile(dx) as z:
        names = set(z.namelist())
        xml = z.read("word/document.xml").decode("utf-8")
    check("docx: valid package parts",
          {"[Content_Types].xml", "word/document.xml", "word/styles.xml"} <= names, str(sorted(names)))
    check("docx: headings, table, bold, italic, quote rendered",
          "Heading1" in xml and "Heading3" in xml and "<w:tbl>" in xml and "<w:b/>" in xml and "<w:i/>" in xml,
          xml[:200])
    plain = re.sub(r"<[^>]+>", "", xml)
    check("docx: text round-trips", "T" in plain and "bold" in plain and "quote" in plain, plain[:120])
    check("docx: no markdown asterisks left", "*" not in plain, plain[:160])
    check("docx: CJK-safe fonts in styles", "SimSun" in zipfile.ZipFile(dx).read("word/styles.xml").decode())

    # images: ![caption](png) must be embedded, not dropped
    import base64
    img = os.path.join(tmp, "img.png")
    open(img, "wb").write(base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFAAH/q842iQAAAABJRU5ErkJggg=="))
    md2 = os.path.join(tmp, "img.md")
    open(md2, "w", encoding="utf-8").write(
        "before\n\n![Figure 1 — a caption that wraps\nacross two lines](img.png)\n\nafter\n")
    dx2 = MD.convert(md2, os.path.join(tmp, "img.docx"))
    with zipfile.ZipFile(dx2) as z:
        names2 = set(z.namelist())
        rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
        xml2 = z.read("word/document.xml").decode("utf-8")
    check("docx: image embedded as media part", "word/media/image1.png" in names2, str(sorted(names2)))
    check("docx: image relationship declared", "relationships/image" in rels and "media/image1.png" in rels)
    check("docx: drawing element + caption present",
          "<w:drawing>" in xml2 and "Figure 1 — a caption" in xml2, xml2[:160])
    check("docx: png content type declared",
          "image/png" in zipfile.ZipFile(dx2).read("[Content_Types].xml").decode())

    # images: JPEG must embed too (the director's screenshots are .jpg)
    jpg = os.path.join(tmp, "img.jpg")
    open(jpg, "wb").write(base64.b64decode(
        "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIs"
        "IxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAABAAEBAREA/8QAFAABAAAAAAAAAAAAAAAAAAAACf/EABQQAQAA"
        "AAAAAAAAAAAAAAAAAAD/2gAIAQEAAD8AKp//2Q=="))
    md3 = os.path.join(tmp, "img3.md")
    open(md3, "w", encoding="utf-8").write("before\n\n![Figure 2 — jpeg](img.jpg)\n\nafter\n")
    dx3 = MD.convert(md3, os.path.join(tmp, "img3.docx"))
    with zipfile.ZipFile(dx3) as z:
        names3 = set(z.namelist())
        xml3 = z.read("word/document.xml").decode("utf-8")
        ct3 = z.read("[Content_Types].xml").decode("utf-8")
    check("docx: jpeg embedded as media part", "word/media/image1.jpg" in names3, str(sorted(names3)))
    check("docx: jpeg drawing present", "<w:drawing>" in xml3 and "Figure 2 — jpeg" in xml3)
    check("docx: jpeg content type declared", "image/jpeg" in ct3)

    # ── shot_log ─────────────────────────────────────────────────────────────
    log = os.path.join(tmp, "shot_log.csv")
    for take, outcome in ((1, "rejected"), (2, "rejected"), (3, "approved")):
        SL.cmd_log(type("A", (), {
            "file": log, "shot": "sc1-shot2", "take": str(take), "date": "d", "duration": "6",
            "model": "m", "render": "400", "outcome": outcome,
            "failures": "light_second_source" if outcome == "rejected" else "",
            "attribution": "prompt defect" if outcome == "rejected" else "", "notes": ""}))
    rows = list(csv.DictReader(open(log)))
    check("log: header written once, 3 rows appended",
          len(rows) == 3 and list(rows[0]) == SL.FIELDS, str(len(rows)))

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        SL.cmd_stats(type("A", (), {"file": log}))
    s = buf.getvalue()
    check("stats: approved/unfinished counted", "approved: 1" in s and "unfinished: 0" in s, s[:120])
    check("stats: mean takes per approved shot", "mean takes per approved shot: 3.0" in s, s[:160])
    check("stats: failure type ranked", "light_second_source" in s, s[:200])
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print()
print("ALL PASS" if not fails else "FAILURES: " + ", ".join(fails))
print("(ad-hoc verification of scripts/*.py — not a test suite)")
sys.exit(1 if fails else 0)
