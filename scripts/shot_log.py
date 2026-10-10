#!/usr/bin/env python3
"""
shot_log.py — append takes to shot_log.csv and report the numbers.

Usage:
  shot_log.py log   --file shot_log.csv --shot sc5-shot3 --take 2 --duration 6 --model M \
                    --render 395 --outcome rejected --failures prop_orientation \
                    --attribution "model limitation" --notes "blade edge/spine swapped"
  shot_log.py stats --file shot_log.csv

Append-only: existing rows are never edited.
"""

import argparse
import csv
import os
import sys
from collections import Counter

FIELDS = ["shot_id", "take", "date", "duration_s", "model", "render_s",
          "outcome", "failure_types", "attribution", "notes"]


def cmd_log(a):
    exists = os.path.exists(a.file)
    with open(a.file, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if not exists:
            w.writeheader()
        w.writerow({
            "shot_id": a.shot, "take": a.take, "date": a.date, "duration_s": a.duration,
            "model": a.model, "render_s": a.render, "outcome": a.outcome,
            "failure_types": a.failures or "", "attribution": a.attribution or "",
            "notes": a.notes or "",
        })
    print(f"logged {a.shot} take{a.take} → {a.outcome}")


def cmd_stats(a):
    if not os.path.exists(a.file):
        sys.exit(f"no log at {a.file}")
    rows = list(csv.DictReader(open(a.file, encoding="utf-8")))
    if not rows:
        sys.exit("log is empty")

    by_shot = {}
    for r in rows:
        by_shot.setdefault(r["shot_id"], []).append(r)

    approved, rejected = [], []
    for shot, takes in by_shot.items():
        ok = [t for t in takes if t["outcome"] == "approved"]
        (approved if ok else rejected).append((shot, takes))

    n_ok = len(approved)
    reworks_ok = sum(len(t) - 1 for _, t in approved)
    print(f"shots logged:      {len(by_shot)}   approved: {n_ok}   unfinished: {len(rejected)}")
    if n_ok:
        print(f"mean takes per approved shot: {round(sum(len(t) for _, t in approved)/n_ok, 2)}")
        print(f"mean rework rounds:           {round(reworks_ok/n_ok, 2)}")

    render = [int(r["render_s"]) for r in rows if r["render_s"].isdigit() and int(r["render_s"]) > 0]
    if render:
        print(f"mean render per take:         {round(sum(render)/len(render))} s   (total {sum(render)} s)")

    c = Counter()
    for r in rows:
        for f in (r["failure_types"] or "").split(";"):
            if f.strip():
                c[f.strip()] += 1
    if c:
        print("\ntop failure types (→ candidate catalogue entries):")
        for k, v in c.most_common(10):
            print(f"  {v:>3}  {k}")

    att = Counter(r["attribution"] for r in rows if r["attribution"])
    if att:
        print("\nattribution:")
        for k, v in att.most_common():
            print(f"  {v:>3}  {k}")

    if rejected:
        print("\nunfinished shots:")
        for shot, takes in rejected:
            print(f"  {shot}  ({len(takes)} takes)")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(required=True)

    p = sub.add_parser("log")
    p.add_argument("--file", default="shot_log.csv")
    p.add_argument("--shot", required=True)
    p.add_argument("--take", required=True)
    p.add_argument("--date", default="")
    p.add_argument("--duration", default="")
    p.add_argument("--model", default="")
    p.add_argument("--render", default="0")
    p.add_argument("--outcome", required=True, choices=["not_generated", "rejected", "approved"])
    p.add_argument("--failures", default="")
    p.add_argument("--attribution", default="")
    p.add_argument("--notes", default="")
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("stats")
    p.add_argument("--file", default="shot_log.csv")
    p.set_defaults(func=cmd_stats)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
