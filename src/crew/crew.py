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

        Gather EVERYTHING from the last 15 minutes:

        **Emails:**
        1. get_emails(limit=20) - get recent inbox emails
        2. get_sent_emails(limit=10) - get sent emails

        **Teams Chats (DMs):**
        3. get_teams_chats(limit=20) - get chat list with last_message_time
        4. For each chat with activity in last 15 min: get_chat_messages(chat_id, limit=10)

        **Teams Channels:**
        5. get_joined_teams() - get all teams
        6. For each team: get_team_channels(team_id)
        7. For active channels: get_channel_messages(team_id, channel_id, limit=10)

        **Calendar:**
        8. get_today_events() - today's schedule

        **Time Tracking:**
        9. harvest_running_timers() - any active timer
        10. harvest_today_tracking() - today's time entries

        Return ALL items found, filtering to last 15 minutes where timestamps are available.""",
        expected_output="""Complete data dump with:
        - emails: ALL recent emails (id, timestamp, from, to, subject, preview)
        - sent_emails: ALL sent emails (id, timestamp, to, subject, preview)
        - teams_chats: ALL chat messages (chat_id, chat_name, timestamp, from, content)
        - teams_channels: ALL channel messages (team, channel, timestamp, from, subject, content)
        - calendar: today's events (id, subject, start, end, attendees)
        - harvest_timers: running timers (project, task, hours)
        - harvest_today: today's entries (project, task, hours, notes)
        - counts: {emails: X, sent: X, chat_messages: X, channel_messages: X}""",
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

        **1. Email Archive** (knowledge/emails/{date_str}.md):
        - Create/append to daily email log
        - Format each email:
          ## HH:MM - From: [sender]
          **Subject:** [subject]
          **To:** [recipients]
          > [preview/summary]

          **Project:** [related project or "Uncategorized"]
          ---

        **2. Teams Chat Archive** (knowledge/teams/{date_str}/[chat-name].md):
        - One file per chat/channel
        - Append new messages:
          ## HH:MM - [Sender]
          > [message content]

          [If reply to thread, indent under parent]

        **3. Teams Channel Archive** (knowledge/channels/{date_str}/[team]-[channel].md):
        - One file per channel with activity
        - Same format as chats

        **4. Inbox/Changelog** (knowledge/inbox.md):
        - Prepend a new entry at the TOP of the file:
          ## {timestamp}

          ### Changes This Window
          - **Emails:** X new (list subjects)
          - **Teams Chats:** X messages across Y conversations
          - **Teams Channels:** X messages in Y channels
          - **Calendar:** [any meetings started/ended]
          - **Time Tracking:** [current timer status]

          ### Action Items Detected
          - [ ] [any requests or todos found]

          ### Files Updated
          - [list each file updated with brief description]

          ---

        **5. Person Files** (knowledge/people/[name].md):
        - Update last_contact date
        - Add recent interaction summary

        **6. Project Files** (knowledge/projects/[name].md):
        - Add any relevant updates from messages

        IMPORTANT:
        - Read existing files BEFORE writing to avoid duplicates
        - Append to existing files, don't overwrite
        - Create new files/directories as needed
        - If no activity, still update inbox.md with "No new activity" entry""",
        expected_output="""Archive report:
        - files_created: [list of new files created]
        - files_updated: [list of files appended to]
        - email_count: number of emails archived
        - message_count: number of messages archived
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
