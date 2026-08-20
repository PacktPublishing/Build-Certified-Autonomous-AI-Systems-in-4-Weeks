#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
rm -f logs/audit_log.jsonl
printf "Demo reset complete. Audit log removed.\n"
