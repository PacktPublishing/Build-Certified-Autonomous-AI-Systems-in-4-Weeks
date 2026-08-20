#!/usr/bin/env bash
set -e

cat > data/profile.json <<'JSON'
{
  "name": "Demo User",
  "role": "AI learner",
  "goals": [
    "Build useful AI applications",
    "Stay organized with tasks and notes",
    "Use local AI tools without paid API keys"
  ],
  "preferences": [
    "Beginner-friendly explanations",
    "Short practical steps",
    "Clear examples"
  ]
}
JSON

cat > data/tasks.json <<'JSON'
[
  {
    "id": 1,
    "title": "Review AI OS lab structure",
    "status": "open"
  },
  {
    "id": 2,
    "title": "Prepare course demo notes",
    "status": "open"
  }
]
JSON

cat > data/notes.json <<'JSON'
[
  {
    "id": 1,
    "title": "Personal AI OS idea",
    "content": "A Personal AI OS keeps memory, tasks, notes, and small specialist agents in one local command-line app."
  }
]
JSON

echo "Demo memory reset complete."
