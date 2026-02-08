FROM python:3.11-slim

# Install system dependencies
# Note: Node.js/Claude CLI removed - using CrewAI instead
RUN apt-get update && apt-get install -y \
    curl \
    cron \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create data directory for memory persistence
RUN mkdir -p /app/data /app/logs

# Copy and setup run script
COPY docker/run-monitor.sh /usr/local/bin/run-monitor.sh
RUN chmod +x /usr/local/bin/run-monitor.sh

# Entry point
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
