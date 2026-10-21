#!/bin/sh
# Validate changed theme files with the Shopify AI Toolkit's Liquid validator (full theme mode)
# and Shopify Theme Check. Store-independent: use while no development store is available.
#
# usage: sh scripts/validate-theme.sh <artifact-id> <revision> <file1,file2,...>
# Requires the shopify-ai-toolkit plugin (claude plugin install shopify-ai-toolkit@claude-plugins-official)
# with its validator dependencies installed (npm install in the skill directory).
# Privacy: the toolkit validator sends the validated code to shopify.dev; no prompt is sent.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="$(ls -d "$HOME"/.claude/plugins/cache/claude-plugins-official/shopify-ai-toolkit/*/skills/shopify 2>/dev/null | tail -1)"
if [ -z "$SKILL" ]; then echo "shopify-ai-toolkit not installed"; exit 2; fi
node "$SKILL/scripts/validate.mjs" --api liquid --theme-path "$ROOT" --files "$3" \
  --model claude-opus-5-5 --client-name claude-code --client-version 2.1.304 \
  --artifact-id "$1" --revision "$2" | grep -E "Overall Status|Status:|Details:|Error|line" || true
cd "$ROOT" && shopify theme check --output text 2>/dev/null | grep -E "inspected|errors|warnings" || true
