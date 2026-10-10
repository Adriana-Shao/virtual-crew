#!/usr/bin/env python3
"""
prompt_lint.py — static pre-flight check for a shot prompt.

Usage:
  prompt_lint.py PROMPT.txt [--lang zh|en] [--dialogue-count N] [--has-dialogue]

Checks (each maps to a check in skills/qc-reviewer/SKILL.md):
  1 light bound to one source, with the ban on a second source
  2 reverse locks present (named forbiddens)
  3 framing given as visible content, not only as a label
  4 no cross-shot references ("same as the previous shot" / 同上 / 一样)
  5 heuristic scan for abstract emotion words
  6 exact-number expressions
  7 dialogue marked with {…}
  8 prop existence / count clause ("only one", "no second")
  9 hand assignment ("no third hand")
 10 camera clause (locked or moving, plus bans)
 11 sound band (no music / no subtitles) and ambience bans
 12 light ban on flare in the eyes

Exit code: 0 = no HIGH, 1 = at least one HIGH.
"""

import argparse
import re
import sys

ZH = {
    "light": ["一个光源", "唯一光源", "光源只有一个"],
    "light_ban": ["不能有第二个光源", "第二个光源", "不能有别的灯"],
    "eyes": ["高光", "光斑"],
    "reverse": ["不能出现", "不能是", "禁止", "不能有第二"],
    "framing_label": ["近景", "中景", "全景", "特写"],
    "framing_visible": ["画框", "画面里是", "画面里只有", "画面范围", "头顶", "入画", "到他的"],
    "crossref": ["同上", "上一个镜头", "上一镜", "和上一个镜", "保持上一个", "跟上一个镜", "与上一镜", "和上镜一样"],
    "emotion": ["无奈", "绝望", "委屈", "悲伤", "愤怒", "紧张地", "尴尬地", "显然很", "充满"],
    "numbers": [r"\d+厘米", r"\d+度", r"大约\d+次", r"\d+\.\d+秒"],
    "prop_count": ["只能有", "只有一个", "不能出现第二个"],
    "hands": ["两只手", "十根手指", "第三只手"],
    "camera": ["不能推进", "固定机位", "固定不动", "不能摇"],
    "sound": ["没有音乐", "无音乐", "没有配乐", "没有字幕"],
    "ambience": ["苍蝇", "虫鸣", "滴水", "风声", "电流声"],
}

EN = {
    "light": ["one source", "single source", "only one light"],
    "light_ban": ["no second source", "no second light"],
    "eyes": ["flare in the eyes", "highlight in the eyes"],
    "reverse": ["must not", "no second", "only one", "forbidden"],
    "framing_label": ["close-up", "medium shot", "wide shot"],
    "framing_visible": ["in frame", "frame edge", "fills the frame", "only his hands", "visible"],
    "crossref": ["same as the previous shot", "as in the previous", "as before", "same position as", "unchanged from"],
    "emotion": ["resigned", "helpless", "bitter", "devastated", "angrily", "sadly", "obviously"],
    "numbers": [r"\d+\s?cm", r"\d+\s?degrees", r"about \d+ times", r"\d+\.\d+\s?s"],
    "prop_count": ["only one", "no second"],
    "hands": ["two hands", "ten fingers", "third hand"],
    "camera": ["locked off", "no push", "does not move", "no pan"],
    "sound": ["no music", "no score", "no subtitles"],
    "ambience": ["flies", "insects", "dripping", "wind noise", "electrical hum"],
}


def check(text, T, has_dialogue):
    low = text.lower()
    issues = []

    def present(key):
        return any(k.lower() in low for k in T[key]) or any(re.search(k, text) for k in T.get(key + "_re", []))

    if not present("light"):
        issues.append(("HIGH", "light", "no single-source statement", 'add: "one light source only, even and uniform across the frame"'))
    if not present("light_ban"):
        issues.append(("HIGH", "light", "no ban on a second light source", 'add: "no second source, no beam, no spot"'))
    if not present("eyes"):
        issues.append(("MEDIUM", "light", "no ban on flare/highlight in the eyes", 'add: "no highlight or flare in the eyes"'))
    if not present("reverse"):
        issues.append(("HIGH", "reverse locks", "no named forbiddens", 'add a [REVERSE LOCKS] list: "no second prop, no auto push-in, no cut, ..."'))
    if present("framing_label") and not present("framing_visible"):
        issues.append(("MEDIUM", "framing", "framing given only as a label", 'rewrite as visible content: "head to knees in frame"'))
    if present("crossref"):
        issues.append(("HIGH", "cross-shot reference", "refers to a previous shot", "expand the fact in full instead"))
    for w in T["emotion"]:
        if w in text:
            issues.append(("MEDIUM", "abstract emotion", f'found "{w}"', "convert to physics: mouth corners, gaze, shoulders, breath"))
            break
    for pat in T["numbers"]:
        m = re.search(pat, text)
        if m:
            issues.append(("MEDIUM", "exact number", f'found "{m.group(0)}"', 'use "a few", "barely", "a moment"'))
            break
    if has_dialogue and "{" not in text:
        issues.append(("HIGH", "dialogue", "dialogue expected but no {…} block found", "mark every line with braces, in order, once each"))
    if not present("prop_count"):
        issues.append(("MEDIUM", "props", "no prop count/existence lock", 'add: "only one X; no second X, no duplicate"'))
    if not present("hands"):
        issues.append(("LOW", "hands", "hand assignment not stated (fine if the hands do no work)", 'if they do work: "two hands, ten fingers; no third hand"'))
    if not present("camera"):
        issues.append(("MEDIUM", "camera", "camera behaviour not pinned", 'state locked or moving, plus bans'))
    if not present("sound"):
        issues.append(("HIGH", "sound band", "no sound band", 'add: "no music, no score, no melody; no subtitles, no logo"'))
    if not present("ambience"):
        issues.append(("LOW", "ambience", "ambience bans absent", "list the background sounds that must not appear"))
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("--lang", choices=["zh", "en"], default="zh")
    ap.add_argument("--has-dialogue", action="store_true")
    args = ap.parse_args()

    text = open(args.prompt, encoding="utf-8").read()
    T = ZH if args.lang == "zh" else EN
    issues = check(text, T, args.has_dialogue)

    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    issues.sort(key=lambda x: order[x[0]])
    high = sum(1 for i in issues if i[0] == "HIGH")
    risk = "HIGH" if high else ("MEDIUM" if issues else "LOW")
    print(f"PROMPT LINT — {args.prompt}   RISK: {risk}   ({len(issues)} items)")
    for sev, area, what, fix in issues:
        print(f"[{sev}] {area}: {what}")
        print(f"      fix: {fix}")
    if not issues:
        print("clean: light, reverse locks, framing, dialogue, props, hands, camera, sound")
    sys.exit(1 if high else 0)


if __name__ == "__main__":
    main()
