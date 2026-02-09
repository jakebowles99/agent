"""CrewAI agent definitions for autonomous monitoring."""

import os
from pathlib import Path

from crewai import Agent, LLM
from crewai.mcp import MCPServerStdio

from src.crew.tools import get_knowledge_tools


def get_mcp_server() -> MCPServerStdio:
    """Get the MCP server configuration for Microsoft 365 and Harvest tools."""
    project_root = Path(__file__).parent.parent.parent
    mcp_server_path = project_root / "mcp_server.py"

    return MCPServerStdio(
        command="python",
        args=[str(mcp_server_path)],
        env={**os.environ},
        cache_tools_list=True,
    )


def get_llm() -> LLM:
    """Get the LLM configured for Azure OpenAI.

    Uses CrewAI's azure provider with Azure OpenAI endpoint.
    """
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
        timeout=300,  # 5 minute timeout per request
        max_retries=3,  # Retry on transient failures
    )


def create_data_collector() -> Agent:
    """Create the DataCollector agent.

    This agent gathers data from all sources (Microsoft 365, Harvest).
    It focuses on collecting recent activity within the monitoring window.
    """
    return Agent(
        role="Data Collector",
        goal="Gather all recent data from Microsoft 365 and Harvest within the last 15 minutes",
        backstory="""You are a meticulous data collector responsible for monitoring
        multiple data sources. You systematically query calendar events, emails,
        Teams messages (both chats and channels), and time tracking data.

        Your job is to gather a comprehensive snapshot of recent activity,
        filtering for items within the last 15 minutes only. You understand
        the structure of Microsoft 365 APIs and can efficiently query
        across chats, channels, and email folders.

        Available MCP tools include:
        - get_calendar_events, get_today_events - for calendar data
        - get_emails, get_sent_emails - for email data
        - get_teams_chats, get_chat_messages - for Teams DMs
        - get_joined_teams, get_team_channels, get_channel_messages - for Teams channels
        - harvest_running_timers, harvest_my_time, harvest_today_tracking - for time tracking""",
        mcps=[get_mcp_server()],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        memory=False,
    )


def create_analyst() -> Agent:
    """Create the Analyst agent.

    This agent analyzes collected data for patterns, priorities, and insights.
    It compares against the knowledge base to identify what's new or important.
    """
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
    """Create the Archivist agent.

    This agent updates the knowledge base with new information,
    ensuring proper documentation and organization.
    """
    return Agent(
        role="Archivist",
        goal="Update the knowledge base with new information while maintaining organization",
        backstory="""You are a knowledge management expert responsible for
        maintaining the markdown-based knowledge base. You ensure that:

        - New information is documented in the right location
        - Teams messages are logged with proper formatting
        - The inbox.md file is updated with action items
        - Files follow the established naming conventions
        - No duplicate entries are created
        - Context is preserved for future reference

        You write clear, concise markdown that is easy to search and reference.
        You understand the folder structure:
        - knowledge/inbox.md - action items and summaries
        - knowledge/teams/YYYY-MM-DD/ - daily Teams logs
        - knowledge/projects/ - project documentation
        - knowledge/patterns/ - detected patterns over time

        Use the knowledge tools:
        - read_knowledge - to read existing files before updating
        - write_knowledge - to create or update files
        - list_knowledge - to see what files exist in a directory""",
        tools=get_knowledge_tools(),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        memory=False,
    )


def create_all_agents() -> tuple[Agent, Agent, Agent]:
    """Create all agents for the monitoring crew.

    Returns:
        Tuple of (data_collector, analyst, archivist)
    """
    return (
        create_data_collector(),
        create_analyst(),
        create_archivist(),
    )
