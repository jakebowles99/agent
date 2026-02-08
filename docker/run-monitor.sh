#!/bin/bash
# Run the autonomous monitoring agent using CrewAI

# Source environment variables (cron doesn't inherit container env)
# .docker-env is created by entrypoint.sh from container env vars
if [ -f /app/.docker-env ]; then
    set -a
    source /app/.docker-env
    set +a
fi

cd /app

echo "=== Monitor run: $(date) ==="

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
