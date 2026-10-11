#!/usr/bin/env bash
# demo_run.sh — the exact commands for the 30-second screen recording, in order.
# Run from the repo root:  bash scripts/demo_run.sh
# Nothing here touches private project data: it only reads the fictional example project.

set -u
cd "$(dirname "$0")/.." || exit 1

line() { printf '\n\033[1m%s\033[0m\n' "$1"; sleep 1; }

line "1 / 4   a prompt as it was first written  →  RISK: HIGH"
python3 scripts/prompt_lint.py examples/the-visitor/prompts/sc1-shot2-v1-defective.md --lang en || true
sleep 3

line "2 / 4   after the fix  →  RISK: LOW"
python3 scripts/prompt_lint.py examples/the-visitor/prompts/sc1-shot2.md --lang en || true
sleep 3

line "3 / 4   and it counts the rework"
python3 scripts/shot_log.py stats --file examples/the-visitor/shot_log.csv
sleep 3

line "4 / 4   verification: 26 checks, exit 0"
python3 scripts/verify_scripts.py | tail -4

printf '\n\033[1mGeneration stays with the director.\033[0m\n'
