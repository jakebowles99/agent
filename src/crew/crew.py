"""CrewAI crew orchestration for autonomous monitoring."""

from datetime import datetime, timezone
from crewai import Crew, Process, Task

from src.crew.agents import create_specialized_agents, create_all_agents


def create_specialized_tasks(email_agent, chat_agent, channel_agent, context_agent, inbox_agent) -> list[Task]:
    """Create tasks for the specialized crew structure.

    Each agent handles collection AND archiving for their domain,
    keeping context sizes small. Tasks run sequentially but each
    task is self-contained.
    """
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%d %H:%M")
    date_str = now.strftime("%Y-%m-%d")

    # Task 1: Process emails
    email_task = Task(
        description=f"""Process emails from last 15 minutes. Time: {timestamp} UTC

1. Call get_emails(limit=20, since_minutes=15) for inbox
2. Call get_sent_emails(limit=10, since_minutes=15) for sent
3. Archive any emails found to knowledge/emails/{date_str}.md using append=True
4. Return count of emails processed

If no emails in last 15 min, report "0 emails" and skip archiving.""",
        expected_output="""Report: email_count, sent_count, files_updated""",
        agent=email_agent,
    )

    # Task 2: Process Teams chats
    chat_task = Task(
        description=f"""Process Teams DM chats from last 15 minutes. Time: {timestamp} UTC

1. Call get_teams_chats(limit=20, since_minutes=15)
2. For each chat with activity, call get_chat_messages(chat_id, limit=10, since_minutes=15)
3. Archive to knowledge/teams/{date_str}/[display-name].md

CRITICAL: Use the chat's display_name field for filename (person's name for 1:1 chats).
Convert to kebab-case. NEVER use chat ID or GUID in filename.

Use append=True. If no messages, report "0 messages".""",
        expected_output="""Report: message_count, chat_count, files_updated""",
        agent=chat_agent,
    )

    # Task 3: Process Teams channels
    channel_task = Task(
        description=f"""Process Teams channel messages from last 15 minutes. Time: {timestamp} UTC

1. Call get_joined_teams() to get team list
2. For each team, call get_team_channels(team_id)
3. For each channel, call get_channel_messages(team_id, channel_id, limit=10, since_minutes=15)
4. Archive any messages to knowledge/channels/{date_str}/[team]-[channel].md

Use append=True. If no messages, report "0 messages".""",
        expected_output="""Report: message_count, channel_count, files_updated""",
        agent=channel_agent,
    )

    # Task 4: Process calendar, Harvest, transcripts
    context_task = Task(
        description=f"""Process calendar, time tracking, and transcripts. Time: {timestamp} UTC

1. Call get_today_events() for calendar
2. Call harvest_running_timers() for active timer
3. Call harvest_today_tracking() for today's entries
4. Call get_all_transcripts(limit=10) for meeting transcripts
5. For any new transcripts, fetch content and archive to knowledge/meetings/transcripts/{date_str}-[subject].md

Report current calendar status and timer status.
Use append=True for existing files.""",
        expected_output="""Report: calendar_events, running_timer, transcript_count, files_updated""",
        agent=context_agent,
    )

    # Task 5: Update inbox with summary
    inbox_task = Task(
        description=f"""Update knowledge/inbox.md with activity summary. Time: {timestamp} UTC

Based on previous task outputs, create a changelog entry and PREPEND it to inbox.md.

Format:
## {timestamp}

### Changes This Window
- **Emails:** [count from email task]
- **Teams Chats:** [count from chat task]
- **Teams Channels:** [count from channel task]
- **Transcripts:** [count from context task]
- **Calendar:** [status from context task]
- **Time Tracking:** [timer status from context task]

### Action Items Detected
- [ ] [any requests found in messages]

### Files Updated
- [list all files updated by previous tasks]

---

Read inbox.md first, then prepend the new entry at the TOP.""",
        expected_output="""Report: inbox_updated, summary""",
        agent=inbox_agent,
        context=[email_task, chat_task, channel_task, context_task],
    )

    return [email_task, chat_task, channel_task, context_task, inbox_task]


def create_specialized_crew() -> Crew:
    """Create the specialized monitoring crew with smaller tasks."""
    email_agent, chat_agent, channel_agent, context_agent, inbox_agent = create_specialized_agents()
    tasks = create_specialized_tasks(email_agent, chat_agent, channel_agent, context_agent, inbox_agent)

    return Crew(
        agents=[email_agent, chat_agent, channel_agent, context_agent, inbox_agent],
        tasks=tasks,
        process=Process.sequential,
        memory=False,
        verbose=True,
    )


# ==================== LEGACY CREW (for reference) ====================


def create_tasks(data_collector, analyst, archivist) -> list[Task]:
    """Create tasks for the legacy 3-agent crew structure."""
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%d %H:%M")
    date_str = now.strftime("%Y-%m-%d")

    collect_task = Task(
        description=f"""Collect data from last 15 minutes. Time: {timestamp} UTC

Use since_minutes=15 on all tools.

1. get_emails(limit=20, since_minutes=15)
2. get_sent_emails(limit=10, since_minutes=15)
3. get_teams_chats(limit=20, since_minutes=15) - note: returns display_name
4. For each chat: get_chat_messages(chat_id, limit=10, since_minutes=15)
5. get_joined_teams(), get_team_channels(), get_channel_messages(since_minutes=15)
6. get_today_events()
7. harvest_running_timers()
8. harvest_today_tracking()
9. get_all_transcripts(limit=10)""",
        expected_output="""JSON with all collected data and counts""",
        agent=data_collector,
    )

    analyze_task = Task(
        description=f"""Analyze collected data. Time: {timestamp} UTC

Identify project, person, action items for each item.
Read knowledge/index.md for context.""",
        expected_output="""JSON with categorized data""",
        agent=analyst,
        context=[collect_task],
    )

    archive_task = Task(
        description=f"""Archive to knowledge base. Date: {date_str}

CRITICAL: Use append=True, never overwrite. Use display_name for filenames.

- Emails: knowledge/emails/{date_str}.md
- Teams: knowledge/teams/{date_str}/[display-name].md (kebab-case)
- Channels: knowledge/channels/{date_str}/[team]-[channel].md
- Transcripts: knowledge/meetings/transcripts/{date_str}-[subject].md
- Inbox: knowledge/inbox.md (prepend changelog)""",
        expected_output="""JSON with files_created, files_updated, counts""",
        agent=archivist,
        context=[collect_task, analyze_task],
    )

    return [collect_task, analyze_task, archive_task]


def create_crew() -> Crew:
    """Create the monitoring crew (uses specialized crew by default)."""
    return create_specialized_crew()


def create_legacy_crew() -> Crew:
    """Create the legacy 3-agent crew."""
    data_collector, analyst, archivist = create_all_agents()
    tasks = create_tasks(data_collector, analyst, archivist)

    return Crew(
        agents=[data_collector, analyst, archivist],
        tasks=tasks,
        process=Process.sequential,
        memory=False,
        verbose=True,
    )


def run_crew_with_context() -> str:
    """Run the monitoring crew."""
    crew = create_crew()
    result = crew.kickoff()
    return result
