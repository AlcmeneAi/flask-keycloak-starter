#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
fi
python app.py
