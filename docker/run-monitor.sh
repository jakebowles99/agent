#!/bin/bash
# Run the autonomous monitoring agent using CrewAI

# Source environment variables (cron doesn't inherit container env)
# .docker-env is created by entrypoint.sh from container env vars
if [ -f /app/.docker-env ]; then
    set -a
    source /app/.docker-env
    set +a
else
    echo "WARNING: /app/.docker-env not found!"
fi

# Cron runs with minimal environment - set required vars
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
export HOME="${HOME:-/root}"
export SHELL="${SHELL:-/bin/bash}"
export LANG="${LANG:-C.UTF-8}"

cd /app

echo "=== Monitor run: $(date) ==="
echo "DEBUG: AZURE_ENDPOINT=${AZURE_ENDPOINT:-(not set)}"
echo "DEBUG: AZURE_API_KEY=${AZURE_API_KEY:+[set]}"

# Quick MCP server health check - verify it can start
echo "Checking MCP server..."
if ! timeout 5 python -c "import mcp_server" 2>&1; then
    echo "ERROR: MCP server module failed to import"
    # Try to show the actual error
    python -c "import mcp_server" 2>&1 || true
fi

# Pull any remote changes first
git pull --rebase --autostash 2>/dev/null || true

# Run CrewAI monitoring crew
python -m src.crew.run 2>&1 | tee -a /app/logs/monitor-$(date +%Y%m%d).log

# Sync any knowledge base changes to git
if [[ -n $(git status --porcelain knowledge/ data/) ]]; then
  git add knowledge/ data/
  git commit -m "Auto-sync: $(date '+%Y-%m-%d %H:%M')"
  git push 2>/dev/null || echo "Push failed - will retry next sync" >&2
fi

echo "=== Monitor complete: $(date) ==="
