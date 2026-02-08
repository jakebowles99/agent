#!/bin/bash
set -e

# Ensure directories exist
mkdir -p /app/logs /app/data

# Dump environment variables for cron (cron doesn't inherit container env)
# Filter to only include our app-specific vars
env | grep -E '^(AZURE|ANTHROPIC_|HARVEST_|APP_)' > /app/.docker-env || true

# Set up SSH keys for git push (if mounted at /mnt/ssh)
if [ -d "/mnt/ssh" ] && [ "$(ls -A /mnt/ssh 2>/dev/null)" ]; then
    mkdir -p /root/.ssh
    cp /mnt/ssh/* /root/.ssh/ 2>/dev/null || true
    chmod 700 /root/.ssh
    chmod 600 /root/.ssh/* 2>/dev/null || true
    # Add GitHub to known_hosts (prevents host key verification failure)
    ssh-keyscan -t ed25519,rsa github.com >> /root/.ssh/known_hosts 2>/dev/null || true
fi

# Configure git
git config --global user.email "monitor@personal-agent"
git config --global user.name "Personal Agent Monitor"
git config --global --add safe.directory /app

# Set up cron job
echo "*/15 * * * * /usr/local/bin/run-monitor.sh >> /app/logs/cron.log 2>&1" > /etc/cron.d/monitor-cron
chmod 0644 /etc/cron.d/monitor-cron
# Don't use 'crontab' - that expects user crontab format (no username field)
# Just let cron daemon pick up the file from /etc/cron.d/

# Start cron in foreground
echo "Starting CrewAI autonomous monitor (15-min intervals)..."
echo "Next run will be at the next 15-minute mark."
echo "To run immediately: docker exec personal-agent-monitor /usr/local/bin/run-monitor.sh"

cron -f
