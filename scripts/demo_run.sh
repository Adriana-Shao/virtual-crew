#!/usr/bin/env bash
# demo_run.sh — the commands behind the demo, in order.
#
#   bash scripts/demo_run.sh            # timed run (~30 s), for screen recording
#   bash scripts/demo_run.sh --pause    # wait for Enter between steps, for screenshots
#
# Nothing here touches private project data: it only reads the fictional example project.

set -u
cd "$(dirname "$0")/.." || exit 1

PAUSE=0
[ "${1:-}" = "--pause" ] && PAUSE=1

line() {
  printf '\n\033[1m%s\033[0m\n' "$1"
  if [ "$PAUSE" = "1" ]; then
    read -r -p "        ── 截图后按回车继续 ── " _ || true
  else
    sleep 1
  fi
}

shot() {  # print the command, run it, then pause before the next section
  printf '\033[32m$ %s\033[0m\n' "$1"
  eval "$1" || true
}

line "1 / 4   a prompt as it was first written  →  RISK: HIGH"
shot "python3 scripts/prompt_lint.py examples/the-visitor/prompts/sc1-shot2-v1-defective.md --lang en"
[ "$PAUSE" = "0" ] && sleep 3

line "2 / 4   after the fix  →  RISK: LOW"
shot "python3 scripts/prompt_lint.py examples/the-visitor/prompts/sc1-shot2.md --lang en"
[ "$PAUSE" = "0" ] && sleep 3

line "3 / 4   and it counts the rework"
shot "python3 scripts/shot_log.py stats --file examples/the-visitor/shot_log.csv"
[ "$PAUSE" = "0" ] && sleep 3

line "4 / 4   verification: 27 checks, exit 0"
shot "python3 scripts/verify_scripts.py | tail -4"

printf '\n\033[1mGeneration stays with the director.\033[0m\n'
