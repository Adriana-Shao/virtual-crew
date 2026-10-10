#!/usr/bin/env python3
"""
extract_assets.py — inventory the assets a film needs, from a script + a storyboard.

    extract_assets.py storyboard.docx [script.docx] --out DIR [--project NAME]

Writes <out>/assets_inventory.md:
  · characters — with the wardrobe / body-state clues that decide how many *variants* each needs
  · scenes     — each needs four directional views (N/E/S/W) so no camera angle drifts
  · props      — ranked by how often the storyboard asks for them (high frequency = must exist)

Attribution rule: a clue counts for a character only when the character's name sits in the same
clause. Clauses with a look but no name are listed separately for human triage — better an honest
"unattributed" than a wrong credit.
"""

import argparse
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_project import docx_lines, parse_storyboard, parse_script, _write  # noqa: E402

GROUPS = [
    ("服装", ["工装", "T恤", "衬衫", "背心", "大裤衩", "睡衣", "牛仔裤", "外套", "棉袄", "围裙",
             "拖鞋", "人字拖", "帆布鞋", "袜子", "帽"]),
    ("身体状态", ["光着上身", "光上身", "裸身", "赤身", "伤痕", "疤", "血", "肿", "湿", "汗", "新伤"]),
    ("束缚物", ["铁链", "手铐", "挂锁", "钥匙", "铐"]),
    ("随身道具", ["帆布包", "皮包", "钱包", "漫画", "馒头", "记账本", "手机", "碗", "筷子", "照片"]),
]

PROPS = ["钱包", "皮包", "帆布包", "铁链", "挂锁", "钥匙", "手铐", "刺刀", "水果刀", "菜刀", "鞭子",
         "照片", "相框", "馒头", "酸奶", "漫画书", "记账本", "手机", "烟", "酒瓶", "茶杯", "碗", "筷子",
         "米袋", "肉", "金鱼", "轮椅", "破被", "报纸", "酒精炉", "布娃娃", "绿萝"]

SCENE_FACTS = ["门", "窗", "墙", "瓷砖", "地板", "地砖", "沙发", "茶几", "电视", "床", "柜", "桌",
               "椅", "灶", "冰箱", "水管", "镜子", "灯", "台阶", "暖气管", "贴纸", "帘"]

CLAUSE = re.compile(r"[。；！？，、\s]+")
SCRIPT_SCENE = re.compile(r"^(\d+)[.、]\s*(\S.*)$")


def clauses(text):
    return [c.strip() for c in CLAUSE.split(text) if len(c.strip()) > 1]


def hits(text):
    return {g: [w for w in words if w in text] for g, words in GROUPS if any(w in text for w in words)}


WINDOW = 5   # a clue counts for a character only when its name sits within this many chars


def collect(records, names):
    """records: [(ref, text)] · returns char->group->[(ref, words)], unattributed[(ref, clause, words)], facts.

    A clue is credited to the *nearest* name in the clause, and only within WINDOW characters.
    "文渔主观视角：门缝里光着上身…少年" therefore credits nobody — honest, not wrong.
    """
    per_char = defaultdict(lambda: defaultdict(list))
    unattributed, facts = [], []
    for ref, text in records:
        for w in SCENE_FACTS:
            if w in text and w not in facts:
                facts.append(w)
        for cl in clauses(text):
            h = hits(cl)
            if not h:
                continue
            for g, words in h.items():
                tag = "/".join(dict.fromkeys(words))
                owner, best = None, WINDOW + 1
                for pos, w in enumerate(words):
                    for n in names:
                        i = cl.find(w)
                        j = cl.find(n)
                        if i < 0 or j < 0:
                            continue
                        d = abs(i - j) if j > i else abs(j + len(n) - i)
                        if d < best:
                            owner, best = n, d
                if owner:
                    per_char[owner][g].append((ref, tag))
                else:
                    unattributed.append((ref, cl[:40], tag))
    return per_char, unattributed, facts


def build(scenes, chars, script_lines):
    names = [c["name"] for c in chars]
    # storyboard: content + the performance field (where looks often live)
    sb_records = [(f"{sc['id']}-shot{s['n']}", f"{s['content']} {s['perf']}")
                  for sc in scenes for s in sc["shots"]]
    per_char, unattributed, _ = collect(sb_records, names)

    # script scenes: prose, split on "N. 名字 时间 内外"
    script_scenes, cur = [], None
    for ln in script_lines:
        m = SCRIPT_SCENE.match(ln)
        if m and len(ln) < 40:
            cur = {"no": m.group(1), "head": m.group(2), "lines": []}
            script_scenes.append(cur)
        elif cur is not None and ln:
            cur["lines"].append(ln)
    for s in script_scenes:
        if any(k in s["head"] for k in ("【", "。")):
            continue
        ref = f"脚本s{s['no']}"
        pc, un, _ = collect([(ref, " ".join(s["lines"]))], names)
        for n, gs in pc.items():
            for g, items in gs.items():
                per_char[n][g] += items
        unattributed += un

    # scenes: fact clues
    seen = set()
    scene_rows = []
    for sc in scenes:
        facts = []
        for s in sc["shots"]:
            for w in SCENE_FACTS:
                if w in f"{s['content']}{s['perf']}" and w not in facts:
                    facts.append(w)
        scene_rows.append({"id": sc["id"], "name": sc["name"], "time": sc["time"], "place": sc["place"],
                           "shots": len(sc["shots"]), "facts": facts[:8]})
        seen.add(sc["id"])

    prop_count, prop_first = Counter(), {}
    for sc in scenes:
        for s in sc["shots"]:
            for p in PROPS:
                if p in f"{s['content']}{s['perf']}":
                    prop_count[p] += 1
                    prop_first.setdefault(p, f"{sc['id']}-shot{s['n']}")
    return per_char, unattributed, scene_rows, prop_count, prop_first


def write_inventory(out_dir, project, chars, inv, n_scenes):
    per_char, unattributed, scene_rows, prop_count, prop_first = inv
    L = [f"# {project} — 资产清单（assets inventory）", "",
         "> 由 virtual-crew/scripts/extract_assets.py 从剧本 + 分镜提取；线索按小句归属（人名在同一小句才算）。",
         "> 用途：先做资产（人物 / 场景四方向 / 道具），再做镜头提示词。", "",
         "## 一、人物（含变体线索）", ""]
    if chars:
        for c in chars:
            n = c["name"]
            L += [f"### {n}（{c['age']}岁）", "", f"- 小传摘要：{c['bio'][:110]}"]
            gs = per_char.get(n, {})
            if gs:
                L.append("- 变体线索（每条线索可能对应一条独立的资产提示词）：")
                for g, items in gs.items():
                    uniq, refs = set(), []
                    for ref, tag in items:
                        if (ref, tag) in uniq:
                            continue
                        uniq.add((ref, tag))
                        refs.append(f"{ref}（{tag}）")
                    L.append(f"  - {g}：{'；'.join(refs[:8])}")
            else:
                L.append("- 变体线索：无（按一条默认造型处理）")
            L.append("")
    else:
        L += ["（剧本里未解析到人物小传；请手工补 identity）", ""]

    if unattributed:
        seen = set()
        L += ["### 未归属的外观线索（人名不在关键词附近，需人工判断归给谁）", ""]
        for ref, cl, tag in unattributed:
            key = (tag, cl)
            if key in seen:
                continue
            seen.add(key)
            L.append(f"- {ref}：{cl}（{tag}）")
            if len(seen) >= 24:
                break
        L.append("")

    L += ["## 二、场景（每个场景需要 4 个方向：东 / 南 / 西 / 北）", ""]
    for r in scene_rows:
        L += [f"- {r['id']} {r['name']}（{r['time']}·{r['place']}）｜{r['shots']} 镜",
              f"  - 固定事实线索：{'、'.join(r['facts']) or '（分镜未给，需你补）'}",
              "  - 需要：4 张方向图（同一空间、家具位置唯一、四个方向不能互相打架）"]
    L += ["", "## 三、道具（按分镜出现频次排序；高频 = 必做）", ""]
    if prop_count:
        for p, n in prop_count.most_common():
            L.append(f"- {p}｜出现 {n} 次｜首次：{prop_first[p]}")
    else:
        L.append("- （未命中道具关键词）")
    L += ["", "## 四、结论", "",
          f"- 人物资产：{len(chars)} 个身份 + 上面列出的变体条数",
          f"- 场景方向图：{n_scenes} 个场景 × 4 方向 = {n_scenes * 4} 张",
          f"- 道具：{len(prop_count)} 类（建议出现 ≥2 次的做独立资产，其余并进场景图）", "",
          "风格统一：所有资产图共用同一条风格段（project-profile 的 look 段）。"]
    return _write(os.path.join(out_dir, "assets_inventory.md"), L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("script", nargs="?")
    ap.add_argument("--out", required=True)
    ap.add_argument("--project", default="untitled")
    a = ap.parse_args()

    scenes = parse_storyboard(docx_lines(a.storyboard))
    script_lines = docx_lines(a.script) if a.script else []
    chars = parse_script(script_lines) if script_lines else []
    inv = build(scenes, chars, script_lines)
    path = write_inventory(a.out, a.project, chars, inv, len(scenes))

    per_char, unattributed, scene_rows, prop_count, _ = inv
    print(f"characters: {len(chars)}  scenes: {len(scene_rows)}  props: {len(prop_count)}  "
          f"direction plates: {len(scene_rows) * 4}  unattributed clues: {len(unattributed)}")
    for c in chars:
        gs = ", ".join(f"{g}({len(set(r for r, _ in v))})" for g, v in per_char.get(c["name"], {}).items())
        print(f"  {c['name']}: {gs or 'no clues'}")
    print("top props: " + ", ".join(f"{p}×{n}" for p, n in prop_count.most_common(8)))
    print("wrote", path)


if __name__ == "__main__":
    main()
