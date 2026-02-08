#!/bin/bash
# Run the autonomous monitoring agent

# Source environment variables (cron doesn't inherit container env)
# .docker-env is created by entrypoint.sh from container env vars
if [ -f /app/.docker-env ]; then
    set -a
    source /app/.docker-env
    set +a
fi

# Ensure PATH includes python and node binaries
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

cd /app

echo "=== Monitor run: $(date) ==="

# Quick MCP server health check - verify it can start
echo "Checking MCP server..."
if ! timeout 5 python -c "import mcp_server" 2>&1; then
    echo "ERROR: MCP server module failed to import"
    # Try to show the actual error
    python -c "import mcp_server" 2>&1 || true
fi

# Pull any remote changes first
git pull --rebase --autostash 2>/dev/null || true

# Run Claude with the monitor agent, full autonomy
# Model (Opus) is set via ANTHROPIC_DEFAULT_OPUS_MODEL env var for Foundry
claude --dangerously-skip-permissions \
  --model opus \
  --allowedTools "mcp__personal-tools__*,Edit,Write,Read,Glob,Grep" \
  -p "Run /agent autonomous-monitor" \
  --output-format json \
  2>&1 | tee -a /app/logs/monitor-$(date +%Y%m%d).json

# Sync any knowledge base changes to git
if [[ -n $(git status --porcelain knowledge/) ]]; then
  git add knowledge/
  git commit -m "Auto-sync: $(date '+%Y-%m-%d %H:%M')"
  git push 2>/dev/null || echo "Push failed - will retry next sync" >&2
fi

echo "=== Monitor complete: $(date) ==="
