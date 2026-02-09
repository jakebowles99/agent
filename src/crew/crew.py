"""CrewAI crew orchestration for autonomous monitoring."""

from datetime import datetime, timezone
from crewai import Crew, Process, Task

from src.crew.agents import create_all_agents


def create_tasks(data_collector, analyst, archivist) -> list[Task]:
    """Create the task pipeline for the monitoring crew.

    Tasks are executed sequentially:
    1. Data collection from all sources
    2. Analysis and categorization
    3. Full knowledge base archival
    """
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%d %H:%M")
    date_str = now.strftime("%Y-%m-%d")

    # Task 1: Collect ALL data from sources
    collect_task = Task(
        description=f"""Collect ALL data from all sources for the monitoring window.
        Current time: {timestamp} UTC

        IMPORTANT: Use since_minutes=15 on ALL tools that support it to STRICTLY filter to the last 15 minutes only.

        **Emails:**
        1. get_emails(limit=20, since_minutes=15) - get inbox emails from last 15 min
        2. get_sent_emails(limit=10, since_minutes=15) - get sent emails from last 15 min

        **Teams Chats (DMs):**
        3. get_teams_chats(limit=20, since_minutes=15) - get chats with activity in last 15 min
           - Each chat returns: id, display_name (person's name for 1:1, topic for groups), members, chat_type
        4. For each chat returned: get_chat_messages(chat_id, limit=10, since_minutes=15)

        **Teams Channels:**
        5. get_joined_teams() - get all teams
        6. For each team: get_team_channels(team_id)
        7. For each channel: get_channel_messages(team_id, channel_id, limit=10, since_minutes=15)

        **Calendar:**
        8. get_today_events() - today's schedule (for context only)

        **Time Tracking:**
        9. harvest_running_timers() - any active timer
        10. harvest_today_tracking() - today's time entries

        **Meeting Transcripts:**
        11. get_all_transcripts(limit=10) - get available meeting transcripts
        12. For new transcripts: get_transcript_by_meeting_id(meeting_id) - fetch full transcript content

        CRITICAL: Only process items from the last 15 minutes. The since_minutes parameter enforces this strictly.""",
        expected_output="""Data from the last 15 minutes only:
        - emails: emails received in last 15 min (id, timestamp, from, to, subject, preview) - may be empty
        - sent_emails: emails sent in last 15 min (id, timestamp, to, subject, preview) - may be empty
        - teams_chats: chat messages from last 15 min with display_name for each chat (chat_id, display_name, members, timestamp, from, content) - may be empty
        - teams_channels: channel messages from last 15 min (team, channel, timestamp, from, subject, content) - may be empty
        - calendar: today's events for context (id, subject, start, end, attendees)
        - harvest_timers: running timers (project, task, hours)
        - harvest_today: today's entries (project, task, hours, notes)
        - transcripts: available meeting transcripts (meeting_id, subject, transcript_content)
        - counts: {emails: X, sent: X, chat_messages: X, channel_messages: X, transcripts: X}
        Note: Counts may be 0 if no activity in the 15-minute window.""",
        agent=data_collector,
    )

    # Task 2: Analyze and categorize
    analyze_task = Task(
        description=f"""Analyze and categorize ALL collected data.
        Current time: {timestamp} UTC

        For EVERY item collected, determine:
        1. Which project/client does it relate to? (check knowledge/projects/)
        2. Which person is involved? (check knowledge/people/)
        3. Is there an action item or request?
        4. What's the sentiment/urgency?

        Also check:
        - Read knowledge/index.md for context on active projects and key contacts
        - Any time tracking gaps? (meeting happening but no timer?)
        - Any patterns across the messages?

        Categorize everything - nothing should be left uncategorized.""",
        expected_output="""Categorized data:
        - by_project: dict of project_name -> [items relating to that project]
        - by_person: dict of person_name -> [items from/about that person]
        - action_items: list of items that need response/action
        - meetings: calendar events with any notes needed
        - time_tracking: current state and any issues
        - uncategorized: items that don't fit existing categories (flag for new project/person)""",
        agent=analyst,
        context=[collect_task],
    )

    # Task 3: Archive EVERYTHING to knowledge base
    archive_task = Task(
        description=f"""Archive ALL collected data to the knowledge base.
        Current time: {timestamp} UTC
        Date: {date_str}

        You have FULL CONTROL of the knowledge base. Document EVERYTHING.

        **CRITICAL: PRESERVE EXISTING CONTENT**
        - The knowledge base is a constantly evolving record of important information
        - NEVER overwrite or replace existing content - always APPEND new information
        - When updating a file, use write_knowledge with append=True
        - Existing content is historically accurate and must be preserved
        - Only add NEW information that wasn't already documented

        **1. Email Archive** (knowledge/emails/{date_str}.md):
        - APPEND to daily email log (use append=True)
        - Format each email:
          ## HH:MM - From: [sender]
          **Subject:** [subject]
          **To:** [recipients]
          > [preview/summary]

          **Project:** [related project or "Uncategorized"]
          ---

        **2. Teams Chat Archive** (knowledge/teams/{date_str}/[display-name].md):
        - Use the chat's display_name field for the filename (person's name for 1:1 chats)
        - Convert display_name to lowercase-kebab-case for filename (e.g., "Charlie Phipps-Bennett" -> "charlie-phipps-bennett.md")
        - NEVER use chat IDs or GUIDs in filenames
        - APPEND new messages (use append=True):
          ## HH:MM - [Sender]
          > [message content]

          [If reply to thread, indent under parent]

        **3. Teams Channel Archive** (knowledge/channels/{date_str}/[team]-[channel].md):
        - One file per channel with activity
        - Same format as chats, APPEND only

        **4. Meeting Transcripts** (knowledge/meetings/transcripts/{date_str}-[meeting-subject].md):
        - Archive any new meeting transcripts
        - Include full transcript content with speaker attribution
        - Format:
          # [Meeting Subject]
          **Date:** {date_str}
          **Attendees:** [list from transcript]

          ## Transcript
          [Full transcript content]

        **5. Inbox/Changelog** (knowledge/inbox.md):
        - Prepend a new entry at the TOP of the file:
          ## {timestamp}

          ### Changes This Window
          - **Emails:** X new (list subjects)
          - **Teams Chats:** X messages across Y conversations
          - **Teams Channels:** X messages in Y channels
          - **Transcripts:** X new meeting transcripts
          - **Calendar:** [any meetings started/ended]
          - **Time Tracking:** [current timer status]

          ### Action Items Detected
          - [ ] [any requests or todos found]

          ### Files Updated
          - [list each file updated with brief description]

          ---

        **6. Person Files** (knowledge/people/[name].md):
        - APPEND new information only
        - Add recent interaction summary at the end
        - DO NOT rewrite the entire file

        **7. Project Files** (knowledge/projects/[name].md):
        - APPEND any relevant updates from messages
        - DO NOT rewrite existing content

        IMPORTANT RULES:
        - ALWAYS read existing files BEFORE writing to check for duplicates
        - ALWAYS use append=True when updating existing files
        - NEVER overwrite historical content - it is valuable context
        - Create new files/directories only when needed
        - If no activity in the 15-minute window, update inbox.md with "No new activity" entry
        - Only archive items from the 15-minute window - do NOT archive older items
        - Use person names (display_name) not GUIDs for file naming""",
        expected_output="""Archive report:
        - files_created: [list of new files created]
        - files_updated: [list of files appended to]
        - email_count: number of emails archived
        - message_count: number of messages archived
        - transcript_count: number of transcripts archived
        - inbox_entry: the changelog entry added
        - errors: any issues encountered""",
        agent=archivist,
        context=[collect_task, analyze_task],
    )

    return [collect_task, analyze_task, archive_task]


def create_crew() -> Crew:
    """Create the monitoring crew.

    Returns:
        The configured Crew ready to run.
    """
    # Create agents (they handle MCP internally via mcps parameter)
    data_collector, analyst, archivist = create_all_agents()

    # Create tasks
    tasks = create_tasks(data_collector, analyst, archivist)

    # Create crew
    # Note: memory=False because CrewAI's built-in memory requires OpenAI embeddings
    # We use our own memory layer in src/crew/memory.py instead
    return Crew(
        agents=[data_collector, analyst, archivist],
        tasks=tasks,
        process=Process.sequential,
        memory=False,
        verbose=True,
    )


def run_crew_with_context() -> str:
    """Run the monitoring crew.

    This is the main entry point.

    Returns:
        The result from the crew execution.
    """
    crew = create_crew()
    result = crew.kickoff()
    return result
