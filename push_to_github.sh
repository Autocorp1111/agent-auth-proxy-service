#!/bin/bash
# Push railway.toml fix from WSL / Linux

set -e

PROJECT_DIR="/mnt/e/Agents/project/agent-auth-proxy"
COMMIT_MESSAGE="fix: add explicit startCommand in railway.toml"

echo "=== Push Railway Fix ==="
echo

cd "$PROJECT_DIR" || { echo "ERROR: Cannot enter project directory"; exit 1; }

if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "ERROR: Not a git repository"
    exit 1
fi

echo "Adding railway.toml..."
git add railway.toml

if git diff --cached --quiet; then
    echo "No changes to commit."
else
    echo "Committing..."
    git commit -m "$COMMIT_MESSAGE"
fi

echo "Pushing..."
git push

echo
echo "=== Done ==="