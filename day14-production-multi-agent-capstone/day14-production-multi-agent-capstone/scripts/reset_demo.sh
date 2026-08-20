#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

rm -f logs/*.jsonl
rm -f outputs/*.md

touch logs/.gitkeep outputs/.gitkeep

echo "Demo outputs and audit logs reset."
