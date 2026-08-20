#!/usr/bin/env bash
set -e

API_URL="${API_URL:-http://localhost:8000}"

echo "Checking health endpoint..."
curl -s "$API_URL/health"
echo

echo "Sending chat request..."
curl -s -X POST "$API_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"Explain FastAPI in one beginner-friendly sentence."}'
echo
