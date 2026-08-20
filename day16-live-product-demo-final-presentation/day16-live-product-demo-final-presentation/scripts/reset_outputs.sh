#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
rm -f outputs/final_demo_script.md \
      outputs/judge_rubric.md \
      outputs/launch_post.md \
      outputs/improvement_plan.md

echo "Day 16 generated outputs cleared."
