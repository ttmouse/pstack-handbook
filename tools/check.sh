#!/bin/sh
# diagrams → build → verify 一条命令，退出码即结论：0 全绿，非 0 停在哪一步就是哪步坏。
set -e
cd "$(dirname "$0")/.."
python3 tools/diagrams.py
python3 tools/build.py
exec node .claude/skills/verify/scripts/verify.mjs "$@"
