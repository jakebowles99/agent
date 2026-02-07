# Personal Second Brain

A markdown-based second brain that integrates with Microsoft 365 and Harvest via MCP (Model Context Protocol). Claude Code is the primary interface for accessing work data and managing knowledge.

## Features

- **Claude Code Interface** - Natural language access to your work data
- **Microsoft 365 Integration** - Calendar, emails, Teams chats, OneDrive/SharePoint files
- **Meeting Insights** - Transcripts and Copilot-generated summaries
- **Harvest Time Tracking** - Projects, time entries, team utilization
- **Knowledge Base** - Markdown notes organized by project, person, client, etc.
- **Custom Agents** - Specialized workflows for common tasks

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Claude Code   │────▶│   MCP Server     │────▶│  Microsoft 365  │
│                 │◀────│  (personal-tools)│◀────│   Graph API     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────┐
                        │   Harvest   │
                        │     API     │
                        └─────────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```bash
# Microsoft 365 OAuth (required)
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id

# App Settings
APP_SECRET_KEY=your-secret-key-for-token-encryption
APP_BASE_URL=http://localhost:8000

# Harvest (optional)
HARVEST_ACCOUNT_ID=your-account-id
HARVEST_ACCESS_TOKEN=your-access-token
```

### 3. Authenticate with Microsoft 365

```bash
python auth_server.py            # Opens browser automatically
python auth_server.py --headless # For headless/remote servers
```

For headless mode, copy the printed auth URL and open it in any browser.
Tokens are stored in `tokens.db`.

### 4. Use with Claude Code

The MCP server is configured in `.mcp.json`. When you open the project in Claude Code, approve the `personal-tools` server when prompted.

To auto-approve, add to `.claude/settings.local.json`:
```json
{
  "enableAllProjectMcpServers": true
}
```

## Azure AD Configuration

Register an Azure AD application at [Azure Portal](https://portal.azure.com):

1. Go to Azure Active Directory > App registrations
2. Create a new registration
3. Add redirect URI: `http://localhost:8000/auth/callback` (or your `APP_BASE_URL`)
4. Create a client secret under "Certificates & secrets"
5. Add API permissions:
   - `Calendars.Read`
   - `Mail.Read`
   - `Chat.Read`
   - `Files.Read.All`
   - `OnlineMeetings.Read`
   - `OnlineMeetingTranscript.Read.All`

## MCP Tools

### Calendar
- `get_calendar_events` - Get events (past and/or future)
- `get_today_events` - Today's schedule
- `get_events_for_date` - Events for a specific date
- `get_past_events` - Recent past events

### Email
- `get_emails` - Emails from any folder (inbox, sentitems, drafts, etc.)
- `get_sent_emails` - Emails you have sent
- `get_email_details` - Full email content by ID
- `get_messages_from_person` - Emails and Teams messages from a person

### Teams
- `get_teams_chats` - Recent chat conversations
- `get_chat_messages` - Messages from a specific chat
- `get_my_teams_messages` - Teams messages you have sent

### Files (OneDrive/SharePoint)
- `search_files` - Search for documents
- `get_recent_files` - Recently accessed files
- `read_document` - Search and read document content
- `get_file_content` - Get file by ID

### Meetings & Transcripts
- `get_recent_meetings` - Teams meetings from calendar
- `get_meeting_summary` - Copilot AI insights + transcript
- `get_all_transcripts` - Available transcripts
- `get_transcript_by_meeting_id` - Transcript for specific meeting
- `get_meetings_for_date` - Meetings on a specific date

### Harvest Time Tracking
- `harvest_get_projects` - Active projects
- `harvest_get_project_details` - Project with budget status
- `harvest_get_time_entries` - Time entries with filters
- `harvest_get_team` - Team members
- `harvest_get_team_member` - Member with assignments
- `harvest_team_report` - Team utilization
- `harvest_project_report` - Project hours summary
- `harvest_today_tracking` - Today's time entries
- `harvest_my_time` - Current user's entries
- `harvest_running_timers` - Active timers
- `harvest_client_report` - Time by client

### Utility
- `check_connection_status` - Check Microsoft/Harvest connection

## Knowledge Base

Store notes in the `knowledge/` directory:

```
knowledge/
├── index.md         # Quick reference and overview
├── projects/        # Project notes and context
├── people/          # Information about colleagues
├── clients/         # Client profiles and history
├── meetings/        # Meeting notes and action items
├── decisions/       # Key decisions with reasoning
└── processes/       # Workflows and procedures
```

Works great with [Obsidian](https://obsidian.md/) as a vault.

## Custom Agents

Specialized agents in `.claude/agents/`:

| Agent | Purpose |
|-------|---------|
| `weekly-summary` | Summarize a week's activities |
| `daily-briefing` | Morning overview |
| `meeting-prep` | Prepare for upcoming meetings |
| `meeting-notes` | Extract and save meeting notes |
| `person-context` | Gather context about someone |
| `project-status` | Status report for a project |
| `triage` | Prioritize incoming work |
| `time-review` | Analyze time tracking data |

Use with `/agent <name>` or ask naturally.

## Project Structure

```
personal-agent/
├── mcp_server.py          # MCP server entry point
├── auth_server.py         # OAuth authentication server
├── tokens.db              # Encrypted OAuth tokens
├── .mcp.json              # MCP server config
├── .claude/agents/        # Custom Claude Code agents
├── knowledge/             # Markdown knowledge base
└── src/
    ├── config.py          # Settings from .env
    ├── mcp/
    │   ├── server.py      # MCP server implementation
    │   └── tools.py       # Tool handlers
    ├── microsoft/
    │   ├── auth.py        # OAuth + token storage
    │   ├── graph_client.py    # Graph API client
    │   └── copilot_client.py  # Meeting transcripts + AI
    └── harvest/
        └── client.py      # Harvest API client
```

## Troubleshooting

### "Microsoft 365 not connected" Error
Run `python auth_server.py` to authenticate.

### "Harvest not configured" Error
Set `HARVEST_ACCOUNT_ID` and `HARVEST_ACCESS_TOKEN` in `.env`.

### Token Refresh Issues
Delete `tokens.db` and re-authenticate.

### MCP Server Not Connecting
1. Approve the MCP server when prompted by Claude Code
2. Check Python and dependencies are installed
3. Run `python mcp_server.py` manually to see errors

## License

MIT
