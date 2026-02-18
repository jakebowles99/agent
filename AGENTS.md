# Repository Guidelines

## Project Structure & Module Organization
- `src/` contains the Python application code.
  - `src/mcp/` MCP server implementation and tool handlers.
  - `src/microsoft/` Microsoft Graph auth and client helpers.
  - `src/harvest/` Harvest API client.
- `mcp_server.py` is the MCP server entry point; `auth_server.py` handles OAuth login.
- `knowledge/` is the markdown knowledge base (projects, people, clients, meetings, processes).
- `data/` and `logs/` store runtime state and logs; `tokens.db` holds encrypted OAuth tokens.
- `docker/` and `Dockerfile` define the monitor container.

## Build, Test, and Development Commands
- `pip install -r requirements.txt`: install Python dependencies.
- `python auth_server.py` or `python auth_server.py --headless`: complete Microsoft 365 OAuth flow.
- `python mcp_server.py`: run the MCP server locally.
- `docker compose up --build`: build and run the monitoring container (cron-driven execution).

## Coding Style & Naming Conventions
- Python uses 4-space indentation and standard PEP 8 conventions.
- Keep modules small and focused; place new MCP tools under `src/mcp/tools.py` or a new module in `src/mcp/`.
- Knowledge base files follow:
  - Projects: `knowledge/projects/project-name.md`
  - People: `knowledge/people/firstname-lastname.md`
  - Meetings: `knowledge/meetings/YYYY-MM-DD-topic.md`

## Testing Guidelines
- No automated test suite is currently configured in this repo.
- If you add tests, document the runner and add a command in this guide.
- Use quick manual checks: start `auth_server.py`, then `mcp_server.py`, and verify tool calls.

## Commit & Pull Request Guidelines
- Recent history uses `Auto-sync: YYYY-MM-DD HH:MM` commit messages.
- For human-authored commits, prefer concise, imperative summaries (e.g., `Add harvest client pagination`).
- PRs should include: a short description, key config changes (env vars), and any new MCP tools or knowledge conventions.

## Security & Configuration Tips
- Store secrets in `.env`; do not commit credentials.
- `tokens.db` is encrypted but should still be treated as sensitive.
- Ensure `APP_BASE_URL` matches your auth callback (local or public for headless flows).
