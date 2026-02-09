"""Agent definitions for the monitoring crew."""

import os
from crewai import Agent, LLM
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

from src.crew.tools import get_knowledge_tools


def get_mcp_server_params() -> StdioServerParameters:
    """Get the MCP server parameters for Microsoft 365 and Harvest tools."""
    return StdioServerParameters(
        command="python",
        args=["/app/mcp_server.py"] if os.path.exists("/app/mcp_server.py") else ["mcp_server.py"],
        env={**os.environ},
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
        goal="Collect emails from last 15 minutes and archive them",
        backstory="""You collect and archive emails. Use since_minutes=15 parameter.

Tools:
- get_emails(limit=20, since_minutes=15) - inbox emails
- get_sent_emails(limit=10, since_minutes=15) - sent emails
- write_knowledge - to archive (use append=True)
- read_knowledge - check existing files first

Archive to: knowledge/emails/YYYY-MM-DD.md
Format: ## HH:MM - From: [sender] **Subject:** [subject] > [preview]

ALWAYS use append=True. Never overwrite existing content.""",
        mcps=[MCPServerAdapter(get_mcp_server_params())],
        tools=get_knowledge_tools(),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        memory=False,
    )


def create_teams_chat_agent() -> Agent:
    """Agent that collects and archives Teams DM chats."""
    return Agent(
        role="Teams Chat Processor",
        goal="Collect Teams DM chats from last 15 minutes and archive them",
        backstory="""You collect and archive Teams direct message chats.

Tools:
- get_teams_chats(limit=20, since_minutes=15) - returns chats with display_name field
- get_chat_messages(chat_id, limit=10, since_minutes=15) - messages for each chat
- write_knowledge - to archive (use append=True)
- read_knowledge - check existing files first

IMPORTANT: Each chat has a display_name field containing the person's name (for 1:1)
or chat topic (for groups). Use this for filenames, NOT the chat ID or GUID.

Archive to: knowledge/teams/YYYY-MM-DD/[display-name].md
- Convert display_name to lowercase-kebab-case (e.g., "Charlie Phipps-Bennett" -> "charlie-phipps-bennett.md")
- NEVER use GUIDs or chat IDs in filenames

Format: ## HH:MM - [Sender] > [message content]

ALWAYS use append=True. Never overwrite existing content.""",
        mcps=[MCPServerAdapter(get_mcp_server_params())],
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
        goal="Collect Teams channel messages from last 15 minutes and archive them",
        backstory="""You collect and archive Teams channel messages.

Tools:
- get_joined_teams() - list of teams
- get_team_channels(team_id) - channels in each team
- get_channel_messages(team_id, channel_id, limit=10, since_minutes=15) - messages
- write_knowledge - to archive (use append=True)
- read_knowledge - check existing files first

Archive to: knowledge/channels/YYYY-MM-DD/[team]-[channel].md
Format: ## HH:MM - [Sender] > [message content]

ALWAYS use append=True. Never overwrite existing content.""",
        mcps=[MCPServerAdapter(get_mcp_server_params())],
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
        goal="Collect calendar events, time tracking, and meeting transcripts",
        backstory="""You collect contextual data: calendar, Harvest time tracking, and transcripts.

Tools:
- get_today_events() - today's calendar
- harvest_running_timers() - active timers
- harvest_today_tracking() - today's time entries
- get_all_transcripts(limit=10) - available transcripts
- get_transcript_by_meeting_id(meeting_id) - full transcript content
- write_knowledge - to archive (use append=True)
- read_knowledge - check existing files first

Archive transcripts to: knowledge/meetings/transcripts/YYYY-MM-DD-[subject].md
Format: # [Subject] **Date:** YYYY-MM-DD **Attendees:** [list] ## Transcript [content]

Report calendar events and time tracking status in your output.

ALWAYS use append=True for existing files. Never overwrite.""",
        mcps=[MCPServerAdapter(get_mcp_server_params())],
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
- read_knowledge - read previous task outputs and existing inbox
- write_knowledge - update inbox.md

Read the outputs from previous tasks and create a changelog entry.
PREPEND (not append) the entry to the TOP of inbox.md.

Format:
## YYYY-MM-DD HH:MM

### Changes This Window
- **Emails:** X new (list subjects)
- **Teams Chats:** X messages across Y conversations
- **Teams Channels:** X messages in Y channels
- **Transcripts:** X new
- **Calendar:** [status]
- **Time Tracking:** [current timer or none]

### Action Items Detected
- [ ] [any requests found]

### Files Updated
- [list files]

---

If no activity, write "No new activity in last 15 minutes." """,
        tools=get_knowledge_tools(),
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
        goal="Gather all recent data from Microsoft 365 and Harvest within the last 15 minutes",
        backstory="""You are a meticulous data collector responsible for monitoring
        multiple data sources. You systematically query calendar events, emails,
        Teams messages (both chats and channels), time tracking data, and meeting transcripts.

        Your job is to gather a comprehensive snapshot of recent activity,
        filtering for items within the last 15 minutes only. You understand
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
        mcps=[MCPServerAdapter(get_mcp_server_params())],
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
        mcps=[MCPServerAdapter(get_mcp_server_params())],
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
        create_inbox_agent(),
    )
