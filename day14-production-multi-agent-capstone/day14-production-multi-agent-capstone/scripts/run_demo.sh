#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

if ! command -v ollama >/dev/null 2>&1; then
  echo "Ollama is not installed. Install Ollama first, then run this script again."
  exit 1
fi

if ! ollama list | grep -q "llama3.2:1b"; then
  echo "Pulling llama3.2:1b for the local demo..."
  ollama pull llama3.2:1b
fi

python main.py --file samples/sample_product_ideas.md
