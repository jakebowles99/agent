FROM python:3.11-slim

# Install Node.js (required for Claude CLI)
RUN apt-get update && apt-get install -y \
    curl \
    cron \
    git \
    jq \
    openssh-client \
    gosu \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Claude CLI (CI=true prevents interactive prompts)
ENV CI=true
RUN npm install -g @anthropic-ai/claude-code --no-progress --loglevel=error

# Create non-root user (Claude CLI refuses --dangerously-skip-permissions as root)
RUN useradd -m -s /bin/bash claude && \
    mkdir -p /home/claude/.ssh /home/claude/.claude && \
    chown -R claude:claude /home/claude

WORKDIR /app

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy and setup run script
COPY docker/run-monitor.sh /usr/local/bin/run-monitor.sh
RUN chmod +x /usr/local/bin/run-monitor.sh

# Entry point
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
