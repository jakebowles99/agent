#!/bin/bash
set -e

# Ensure logs directory exists
mkdir -p /app/logs

# Dump environment variables for cron (cron doesn't inherit container env)
# Filter to only include our app-specific vars
env | grep -E '^(CLAUDE_|ANTHROPIC_|AZURE_|HARVEST_|APP_)' > /app/.docker-env || true

# Set ownership for claude user
chown -R claude:claude /app

# Copy SSH keys if mounted (for git push)
if [ -d "/root/.ssh" ]; then
    cp -r /root/.ssh/* /home/claude/.ssh/ 2>/dev/null || true
    chown -R claude:claude /home/claude/.ssh
    chmod 700 /home/claude/.ssh
    chmod 600 /home/claude/.ssh/* 2>/dev/null || true
fi

# Add GitHub to known_hosts (prevents host key verification failure)
ssh-keyscan -t ed25519,rsa github.com >> /home/claude/.ssh/known_hosts 2>/dev/null || true
chown claude:claude /home/claude/.ssh/known_hosts 2>/dev/null || true

# Configure git for the claude user
gosu claude git config --global user.email "monitor@personal-agent"
gosu claude git config --global user.name "Personal Agent Monitor"
gosu claude git config --global --add safe.directory /app

# Set up cron job to run as claude user
# Note: /etc/cron.d/ format requires username field and trailing newline
printf "*/15 * * * * claude /usr/local/bin/run-monitor.sh >> /app/logs/cron.log 2>&1\n" > /etc/cron.d/monitor-cron
chmod 0644 /etc/cron.d/monitor-cron
# Don't use 'crontab' - that expects user crontab format (no username field)
# Just let cron daemon pick up the file from /etc/cron.d/

# Start cron in foreground
echo "Starting autonomous monitor (15-min intervals)..."
echo "Next run will be at the next 15-minute mark."
echo "To run immediately: docker exec personal-agent-monitor gosu claude /usr/local/bin/run-monitor.sh"

cron -f
