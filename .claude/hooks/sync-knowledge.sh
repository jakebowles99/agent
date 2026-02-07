#!/bin/bash
# Sync knowledge base changes to git
# Triggered by PostToolUse hook on Edit/Write

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only sync files in the knowledge/ directory
if [[ ! "$FILE_PATH" =~ ^.*/knowledge/.* ]]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR" || exit 0

# Pull first to get any remote changes
git pull --rebase --autostash 2>/dev/null || true

# Stage and commit the changed file
git add "$FILE_PATH"

# Only commit if there are staged changes
if ! git diff --cached --quiet; then
  FILENAME=$(basename "$FILE_PATH")
  git commit -m "Update knowledge: $FILENAME"

  # Push to remote
  git push 2>/dev/null || echo "Push failed - will retry next sync" >&2
fi

exit 0
