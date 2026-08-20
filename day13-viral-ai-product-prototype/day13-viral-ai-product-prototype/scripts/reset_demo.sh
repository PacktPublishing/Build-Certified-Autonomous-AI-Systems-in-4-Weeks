#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
printf '{}\n' > product_ideas.json
cat > product_brief.md <<'EOF'
# Product Brief

Run the app and generate product ideas to replace this file with the selected capstone idea.
EOF
printf "Demo reset complete. product_ideas.json and product_brief.md were reset.\n"
