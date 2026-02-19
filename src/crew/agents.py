"""Agent definitions for the monitoring crew."""

import os
from pathlib import Path

from crewai import Agent, LLM
from crewai.mcp import MCPServerStdio

from src.crew.tools import get_knowledge_tools, get_person_tools, get_client_tools, get_project_tools


def get_mcp_server() -> MCPServerStdio:
    """Get the MCP server config for Microsoft 365 and Harvest tools."""
    project_root = Path(__file__).parent.parent.parent
    mcp_server_path = project_root / "mcp_server.py"

    return MCPServerStdio(
        command="python",
        args=[str(mcp_server_path)],
        env={**os.environ},
        cache_tools_list=True,
    )


def get_llm() -> LLM:
    """Get the LLM configured for Azure OpenAI."""
    api_key = os.getenv("AZURE_API_KEY")
    endpoint = os.getenv("AZURE_ENDPOINT")
    api_version = os.getenv("AZURE_API_VERSION", "2024-12-01-preview")
    deployment = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt5.2")

    if not api_key or not endpoint:
        raise ValueError(
            "Azure OpenAI not configured. "
            "Set AZURE_API_KEY and AZURE_ENDPOINT"
        )

    return LLM(
        model=f"azure/{deployment}",
        api_key=api_key,
        endpoint=endpoint,
        api_version=api_version,
        timeout=600,
        max_retries=5,
    )


# ==================== SPECIALIZED COLLECTORS ====================


def create_email_agent() -> Agent:
    """Agent that collects and archives emails."""
    return Agent(
        role="Email Processor",
        goal="Collect today's emails and archive them",
        backstory="""You collect and archive emails. Use since_minutes=90 to fetch recent activity.

Tools:
- get_emails(limit=50, since_minutes=90) - inbox emails
- get_sent_emails(limit=50, since_minutes=90) - sent emails
- write_knowledge - to archive (use append=True)
- read_knowledge - check existing files first

Archive to: knowledge/emails/YYYY-MM-DD.md
Format: ## HH:MM - From: [sender] **Subject:** [subject] > [preview]

DEDUPLICATION: Before appending, read the existing file and skip any emails
whose subject line already appears in it. Only append genuinely new content.

ALWAYS use append=True. Never overwrite existing content.""",
        mcps=[get_mcp_server()],
        tools=get_knowledge_tools(),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        memory=False,
    )


def create_teams_chat_agent() -> Agent:
    """Agent that collects and archives all Teams chats."""
    return Agent(
        role="Teams Chat Processor",
        goal="Collect ALL of today's Teams chats (1:1, group, and meeting chats) and archive them",
        backstory="""You collect and archive ALL Teams chat conversations — 1:1 DMs, group chats, and meeting chats.

Tools:
- get_teams_chats(limit=100, since_minutes=90) - returns ALL chat types with display_name field
- get_chat_messages(chat_id, limit=500, since_minutes=90) - messages for each chat
- write_knowledge - to archive (use append=True)
- read_knowledge - check existing files first

IMPORTANT: Process EVERY chat returned, regardless of chat_type. This includes:
- oneOnOne: 1:1 direct messages
- group: group DM conversations  
- meeting: in-meeting chat messages from Teams meetings

CRITICAL FILE NAMING RULES:
1. Each chat object has a "display_name" field - THIS IS THE PERSON'S NAME
2. For 1:1 chats, display_name = the other person's full name (e.g., "Fraser Smith")
3. For group chats, display_name = the chat topic (e.g., "Project Team")
4. For meeting chats, display_name = the meeting subject
5. YOU MUST use display_name for the filename, converted to lowercase-kebab-case

EXAMPLES:
- display_name: "Fraser Smith" -> filename: "fraser-smith.md"
- display_name: "Charlie Phipps-Bennett" -> filename: "charlie-phipps-bennett.md"
- display_name: "Marketing Team" -> filename: "marketing-team.md"
- display_name: "Weekly Standup" -> filename: "weekly-standup.md"

NEVER use:
- chat_id in filename
- GUIDs like "19:4260f6a8-1c91-4928-a81e..." in filename
- "oneOnOne" prefix in filename

Archive to: knowledge/teams/YYYY-MM-DD/[display-name-in-kebab-case].md

Format:
# Teams Chat — [display_name]

## HH:MM - [Sender Name]
> [message content]

DEDUPLICATION: Before appending, read the existing file and skip any messages
whose timestamp + sender already appears in it. Only append genuinely new messages.

ALWAYS use append=True. Never overwrite existing content.""",
        mcps=[get_mcp_server()],
        tools=get_knowledge_tools(),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        memory=False,
    )


def create_teams_channel_agent() -> Agent:
    """Agent that collects and archives Teams channel messages."""
    return Agent(
        role="Teams Channel Processor",
        goal="Collect today's Teams channel messages including reply threads and archive them",
        backstory="""You collect and archive Teams channel messages.

Tools:
- get_joined_teams() - list of teams
- get_team_channels(team_id) - channels in each team
- get_channel_messages(team_id, channel_id, limit=500, since_minutes=90) - messages
- get_channel_message_replies(team_id, channel_id, message_id, limit=50) - replies to a message thread
- write_knowledge - to archive (use append=True)
- read_knowledge - check existing files first

IMPORTANT: After getting channel messages, check each message's reply_count field.
If reply_count > 0, call get_channel_message_replies to fetch the full thread.

Archive to: knowledge/channels/YYYY-MM-DD/[team]-[channel].md

Format:
## HH:MM - [Sender] > [message content]
### Replies:
> **HH:MM - [Reply Sender]:** [reply content]

DEDUPLICATION: Before appending, read the existing file and skip any messages
whose timestamp + sender already appears in it. Only append genuinely new messages.

ALWAYS use append=True. Never overwrite existing content.""",
        mcps=[get_mcp_server()],
        tools=get_knowledge_tools(),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        memory=False,
    )


def create_context_agent() -> Agent:
    """Agent that collects calendar, Harvest, and transcript data."""
    return Agent(
        role="Context Processor",
        goal="Collect calendar events, time tracking, Copilot meeting summaries, and full transcripts",
        backstory="""You collect contextual data: calendar, Harvest time tracking, Copilot AI meeting summaries, and full transcripts.

Tools:
- get_today_events() - today's calendar
- harvest_running_timers() - active timers
- harvest_today_tracking() - today's time entries
- get_meetings_for_date(date=YYYY-MM-DD, limit=200) - enumerate today's online meetings
- get_meeting_summary(subject, organizer_email=None) - Copilot AI insights including action items, notes, and transcript preview
- get_all_transcripts(limit=200) - available transcripts metadata
- get_transcript_by_meeting_id(meeting_id) - full transcript content
- write_knowledge - to archive (use append=True)
- read_knowledge - check existing files first

You MUST complete ALL three steps in order:
1. Calendar + Harvest time entries → archive to knowledge/harvest/YYYY-MM-DD.md
2. Meeting summaries with Copilot AI insights → archive to knowledge/meetings/YYYY-MM-DD-[subject-slug].md
   IMPORTANT: Include ALL Copilot-generated content: action items, follow-ups, meeting notes, discussion points, and transcript previews
3. Full transcripts → fetch content and archive to knowledge/meetings/transcripts/YYYY-MM-DD-[subject-slug].md

Do NOT stop after step 1. Steps 2 and 3 are critical.
DEDUPLICATION: Before archiving, read the target file first. Skip if content already exists.
ALWAYS use append=True for existing files. Never overwrite.""",
        mcps=[get_mcp_server()],
        tools=get_knowledge_tools(),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        memory=False,
    )


def create_inbox_agent() -> Agent:
    """Agent that updates the inbox with a summary."""
    return Agent(
        role="Inbox Updater",
        goal="Update inbox.md with summary of all activity",
        backstory="""You create a summary entry in knowledge/inbox.md.

Tools:
- read_daily_knowledge(date=YYYY-MM-DD) - retrieve the full day's archived content
- read_knowledge - read previous task outputs and existing inbox
- write_knowledge - update inbox.md

Use read_daily_knowledge for the full day's content, then read the outputs from previous tasks
and create a changelog entry.
PREPEND (not append) the entry to the TOP of inbox.md.

Format:
## YYYY-MM-DD HH:MM

### Changes Today
- **Emails:** X new (list subjects)
- **Teams Chats:** X messages across Y conversations
- **Teams Channels:** X messages in Y channels
- **Transcripts:** X new
- **Clients:** X profiles updated
- **Calendar:** [status]
- **Time Tracking:** [current timer or none]

### Action Items Detected
- [ ] [any requests found]

### Files Updated
- [list files]

---

If no activity, write "No new activity today." """,
        tools=get_knowledge_tools(),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        memory=False,
    )


def create_person_agent() -> Agent:
    """Agent that manages person profiles in the knowledge base."""
    return Agent(
        role="Person Profile Manager",
        goal="Ensure all people encountered in communications have profiles in the knowledge base",
        backstory="""You manage person profiles in the knowledge base.

Your job is to:
1. Review the outputs from previous collection tasks (emails, Teams chats, channels)
2. Extract ALL people mentioned (senders, recipients, people mentioned in content)
3. Use ensure_person_profile to create/update their profiles

Tools:
- ensure_person_profile(name, email, company, role, context, interaction_note) - MAIN TOOL
- read_knowledge - check existing profiles
- list_knowledge - see what profiles exist
- write_knowledge - for manual updates if needed

EXTRACTION RULES:
1. From emails: Extract sender name & email, all recipients
2. From Teams chats: Extract the chat display_name (the person's name), and all message senders
3. From Teams channels: Extract all message senders with their display names
4. From meeting transcripts: Extract organizer, attendees, and people mentioned

For EACH person extracted, call ensure_person_profile with:
- name: Their full name (required)
- email: Their email address if visible
- company: Their company (check email domain - @synapx.com = "Synapx")
- context: How you found them ("Email from", "Teams chat with", "Teams channel message")
- interaction_note: Brief summary of the interaction (e.g., "Discussed project timeline")

IMPORTANT:
- Call ensure_person_profile for EVERY person - it handles duplicates
- Skip system names like "Microsoft", "Teams", "Bot", etc.
- Use full names, not usernames or email prefixes
- If unsure of a name, use what you have (better to create a profile than miss someone)

After processing, report how many profiles were created vs updated.""",
        mcps=[get_mcp_server()],
        tools=get_person_tools(),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        memory=False,
    )


def create_client_agent() -> Agent:
    """Agent that manages client profiles in the knowledge base."""
    return Agent(
        role="Client Profile Manager",
        goal="Ensure all clients encountered in communications and Harvest have profiles with linked people and projects",
        backstory="""You manage client profiles in the knowledge base.

Your job is to:
1. Call harvest_get_projects() to list active Harvest projects and their client names
2. Call read_daily_knowledge(date=YYYY-MM-DD) to find client mentions for today
3. Use list_knowledge on people/ and projects/ to find relevant links
4. For each client found, call ensure_client_profile with:
   - name: client name
   - people: list of people links related to the client (name + path)
   - projects: list of project links related to the client (name + path)
   - summary: brief overview if obvious from existing client profile
   - activity_notes: brief bullets about today's interactions

Rules:
- Client filenames are kebab-case in knowledge/clients/
- Always link people with ../people/<name>.md and projects with ../projects/<name>.md
- Prefer existing knowledge/clients/<client>.md summary if present
- Keep activity notes short and factual
""",
        mcps=[get_mcp_server()],
        tools=get_client_tools(),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        memory=False,
    )


def create_project_agent() -> Agent:
    """Agent that manages project profiles in the knowledge base."""
    return Agent(
        role="Project Profile Manager",
        goal="Ensure all projects encountered in Harvest and communications have profiles in the knowledge base",
        backstory="""You manage project profiles in the knowledge base.

Your job is to:
1. Call harvest_get_projects() to list active Harvest projects
2. Review the outputs from previous collection tasks (emails, Teams, meetings)
3. For each project mentioned, call ensure_project_profile with relevant details

Tools:
- ensure_project_profile(name, client, status, summary, activity_note) - MAIN TOOL
- harvest_get_projects() - get active projects from Harvest
- read_knowledge - check existing project profiles
- list_knowledge - see what project profiles exist
- read_daily_knowledge - get today's archived content for context

EXTRACTION RULES:
1. From Harvest: Get project name, client name, active status
2. From emails/chats: Look for project names mentioned in context of previous tasks
3. From meetings: Extract projects discussed based on meeting subjects and summaries

For EACH project, call ensure_project_profile with:
- name: Project name (required)
- client: Client company name
- status: Current status if known (e.g., "Active", "Draft", "SOW pending")
- summary: Brief description of the project
- activity_note: What happened today related to this project

IMPORTANT:
- Call ensure_project_profile for every project - it handles duplicates
- Skip internal/admin projects unless they have significant activity
- Use human-readable project names, not Harvest IDs
""",
        mcps=[get_mcp_server()],
        tools=get_project_tools(),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        memory=False,
    )


# ==================== LEGACY AGENTS (for compatibility) ====================


def create_data_collector() -> Agent:
    """Create the DataCollector agent (legacy)."""
    return Agent(
        role="Data Collector",
        goal="Gather all data from Microsoft 365 and Harvest for today",
        backstory="""You are a meticulous data collector responsible for monitoring
        multiple data sources. You systematically query calendar events, emails,
        Teams messages (both chats and channels), time tracking data, and meeting transcripts.

        Your job is to gather a comprehensive snapshot of today's activity,
        filtering for items from the start of today (UTC). You understand
        the structure of Microsoft 365 APIs and can efficiently query
        across chats, channels, and email folders.

        IMPORTANT: When collecting Teams chats, each chat returns a display_name field
        which contains the person's name (for 1:1 chats) or the chat topic. Use this
        for identification, not the chat ID.

        Available MCP tools include:
        - get_calendar_events, get_today_events - for calendar data
        - get_emails, get_sent_emails - for email data
        - get_teams_chats, get_chat_messages - for Teams DMs (note: includes display_name and members)
        - get_joined_teams, get_team_channels, get_channel_messages - for Teams channels
        - harvest_running_timers, harvest_my_time, harvest_today_tracking - for time tracking
        - get_all_transcripts, get_transcript_by_meeting_id - for meeting transcripts""",
        mcps=[get_mcp_server()],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        memory=False,
    )


def create_analyst() -> Agent:
    """Create the Analyst agent (legacy)."""
    return Agent(
        role="Analyst",
        goal="Identify patterns, priorities, and actionable insights from collected data",
        backstory="""You are an analytical expert who excels at finding patterns
        and extracting meaningful insights from data. You have access to the
        knowledge base and can compare new data against historical context.

        You identify:
        - Important messages requiring attention
        - Meetings that need documentation
        - Time tracking discrepancies
        - Emerging patterns in communication
        - Deadlines and commitments

        You are concise and focus on actionable insights rather than noise.

        Use read_knowledge and list_knowledge to access the knowledge base
        for historical context and existing documentation.""",
        mcps=[get_mcp_server()],
        tools=get_knowledge_tools(),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        memory=False,
    )


def create_archivist() -> Agent:
    """Create the Archivist agent (legacy)."""
    return Agent(
        role="Archivist",
        goal="Update the knowledge base with new information while PRESERVING all existing content",
        backstory="""You are a knowledge management expert responsible for
        maintaining the markdown-based knowledge base. Your PRIMARY DIRECTIVE is to
        NEVER lose or overwrite existing information.

        CRITICAL RULES:
        - ALWAYS use append=True when calling write_knowledge on existing files
        - NEVER rewrite entire files - only add new content at the end
        - Existing content is historically accurate and valuable - preserve it
        - Read files first to check what already exists before writing

        File Naming Rules:
        - For Teams chats, use the display_name field (person's name) not chat IDs
        - Convert names to lowercase-kebab-case (e.g., "John Smith" -> "john-smith.md")
        - NEVER use GUIDs or technical IDs in filenames

        You ensure that:
        - New information is APPENDED to the right location
        - Teams messages are logged with proper formatting using person names
        - The inbox.md file is updated with action items (prepend new entries)
        - Files follow human-readable naming conventions
        - No duplicate entries are created
        - All historical context is preserved

        You write clear, concise markdown that is easy to search and reference.
        You understand the folder structure:
        - knowledge/inbox.md - action items and summaries
        - knowledge/teams/YYYY-MM-DD/ - daily Teams logs (named by person/topic)
        - knowledge/projects/ - project documentation
        - knowledge/meetings/transcripts/ - meeting transcripts
        - knowledge/patterns/ - detected patterns over time

        Use the knowledge tools:
        - read_knowledge - ALWAYS read existing files before updating
        - write_knowledge - use append=True to add to existing files
        - list_knowledge - see what files exist in a directory""",
        tools=get_knowledge_tools(),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        memory=False,
    )


def create_all_agents():
    """Create all agents for the legacy crew structure."""
    return create_data_collector(), create_analyst(), create_archivist()


def create_specialized_agents():
    """Create specialized agents for the parallel crew structure."""
    return (
        create_email_agent(),
        create_teams_chat_agent(),
        create_teams_channel_agent(),
        create_context_agent(),
        create_person_agent(),
        create_project_agent(),
        create_client_agent(),
        create_inbox_agent(),
    )
