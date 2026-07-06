#!/usr/bin/env bash
# Fails (exit 1) if any author-private string is found in the repo. Run before every push; wired into CI.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PATTERN='-Users-ck|/Users/ck|Charandeep|ck-delta|drishti|tatkaal|lakshay|zerodha|stratzy|backtest-engine|delta-mcp|delta-bybit|r2\.dev|openrouter|\bdhan\b|groww|ck-form|aindrila|bajao|stocky-terminal|charandeep|pookie|chonky'
hits=$(grep -rInE "$PATTERN" "$ROOT" --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.next --exclude=privacy-scan.sh 2>/dev/null || true)
if [ -n "$hits" ]; then
  echo "❌ privacy-scan FAILED — author-private strings found:"; echo "$hits"; exit 1
fi
echo "✅ privacy-scan passed — no author-private strings found."
