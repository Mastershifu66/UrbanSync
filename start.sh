#!/bin/bash
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
if [[ "$(uname)" != "Darwin" ]]; then echo "Use the separate terminal commands in README.md."; exit 1; fi
osascript -e "tell application \"Terminal\" to do script \"cd '$ROOT/backend' && (test -d .venv || python3 -m venv .venv) && source .venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload\""
osascript -e "tell application \"Terminal\" to do script \"cd '$ROOT/frontend' && npm install && npm run dev\""
