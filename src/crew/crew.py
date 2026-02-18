"""CrewAI crew orchestration for autonomous monitoring."""

from datetime import datetime, timezone
from crewai import Crew, Process, Task

from src.crew.agents import create_specialized_agents, create_all_agents


def create_specialized_tasks(email_agent, chat_agent, channel_agent, context_agent, person_agent, project_agent, client_agent, inbox_agent) -> list[Task]:
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
        description=f"""Process emails from today. Time: {timestamp} UTC

1. Call get_emails(limit=50, since_start_of_day=True) for inbox
2. Call get_sent_emails(limit=50, since_start_of_day=True) for sent
3. Read knowledge/emails/{date_str}.md first to see what's already archived
4. Only archive NEW emails not already in the file (match by subject + sender + time)
5. Append new emails to knowledge/emails/{date_str}.md using append=True
6. Return count of NEW emails processed (not total)

If no NEW emails, report "0 new emails" and skip archiving.""",
        expected_output="""Report: email_count, sent_count, new_emails_archived, files_updated""",
        agent=email_agent,
    )

    # Task 2: Process Teams chats
    chat_task = Task(
        description=f"""Process Teams DM chats from today. Time: {timestamp} UTC

1. Call get_teams_chats(limit=100, since_start_of_day=True)
2. For each chat with activity, call get_chat_messages(chat_id, limit=500, since_start_of_day=True)
3. For each chat, read knowledge/teams/{date_str}/[display-name].md first to see what's already archived
4. Only archive NEW messages not already in the file (match by timestamp + sender)
5. Append new messages to knowledge/teams/{date_str}/[display-name].md using append=True

CRITICAL: Use the chat's display_name field for filename (person's name for 1:1 chats).
Convert to kebab-case. NEVER use chat ID or GUID in filename.

If no NEW messages, report "0 new messages".""",
        expected_output="""Report: message_count, new_messages_archived, chat_count, files_updated""",
        agent=chat_agent,
    )

    # Task 3: Process Teams channels
    channel_task = Task(
        description=f"""Process Teams channel messages from today. Time: {timestamp} UTC

1. Call get_joined_teams() to get team list
2. For each team, call get_team_channels(team_id)
3. For each channel, call get_channel_messages(team_id, channel_id, limit=500, since_start_of_day=True)
4. For each channel file, read knowledge/channels/{date_str}/[team]-[channel].md first
5. Only archive NEW messages not already in the file (match by timestamp + sender)
6. Append new messages using append=True

If no NEW messages, report "0 new messages".""",
        expected_output="""Report: message_count, new_messages_archived, channel_count, files_updated""",
        agent=channel_agent,
    )

    # Task 4: Process calendar, Harvest, transcripts
    context_task = Task(
        description=f"""Process calendar, time tracking, and transcripts for today. Time: {timestamp} UTC

STEP 1 — Calendar & Harvest:
1. Call get_today_events() for calendar events
2. Call harvest_running_timers() for active timer
3. Call harvest_today_tracking() for today's time entries
4. Archive time entries to knowledge/harvest/{date_str}.md using append=True
   Format: ## HH:MM - [Project] / [Task] — [hours]h [notes]

STEP 2 — Meeting summaries:
5. Call get_meetings_for_date(date="{date_str}", limit=200) to enumerate today's online meetings
6. For EACH meeting returned:
   a. Call get_meeting_summary(subject=subject, organizer_email=organizer_email)
   b. Archive to knowledge/meetings/{date_str}-[subject-slug].md (append=True)
   Format: # [Subject] **Date:** {date_str} **Attendees:** [list] ## Summary [insights]

STEP 3 — Transcripts:
7. Call get_all_transcripts(limit=200) for available transcripts
8. For EACH transcript from today:
   a. Call get_transcript_by_meeting_id(meeting_id) to get the full transcript content
   b. Archive to knowledge/meetings/transcripts/{date_str}-[subject-slug].md (append=True)
   Format: # Transcript: [Subject] **Date:** {date_str} ## Content [transcript text]

DEDUPLICATION: Before archiving, read the target file first. Skip if content already exists.

Report calendar status, timer status, meeting count, and transcript count.""",
        expected_output="""Report: calendar_events, running_timer, meetings_archived, transcript_count, harvest_entries, files_updated""",
        agent=context_agent,
    )

    # Task 5: Manage person profiles
    person_task = Task(
        description=f"""Extract and manage person profiles from collected data. Time: {timestamp} UTC

Review the outputs from previous tasks and ensure ALL people have profiles in knowledge/people/.

1. From email_task: Extract sender names/emails, all recipients
2. From chat_task: Extract people from each chat's display_name and message senders
3. From channel_task: Extract message senders from channel posts
4. From context_task: Extract meeting attendees and organizers

For EACH person found:
- Call ensure_person_profile(name=..., email=..., company=..., context=..., interaction_note=...)
- The tool handles duplicates - call it for everyone

SKIP system names like "Microsoft", "Teams", "Bot", "Notifications"

Report: profiles_created, profiles_updated, profiles_skipped""",
        expected_output="""Report: profiles_created, profiles_updated, total_people_processed""",
        agent=person_agent,
        context=[email_task, chat_task, channel_task, context_task],
    )

    # Task 6: Manage project profiles
    project_task = Task(
        description=f"""Extract and manage project profiles from collected data and Harvest. Time: {timestamp} UTC

1. Call harvest_get_projects() to get all active Harvest projects with client names
2. Review the outputs from previous tasks for project mentions
3. For each project found, call ensure_project_profile(name=..., client=..., status=..., activity_note=...)

The tool handles duplicates — call it for every project.

Report: projects_created, projects_updated, total_projects_processed""",
        expected_output="""Report: projects_created, projects_updated, total_projects_processed""",
        agent=project_agent,
        context=[email_task, chat_task, channel_task, context_task],
    )

    # Task 7: Update client profiles
    client_task = Task(
        description=f"""Update client profiles for today. Time: {timestamp} UTC

1. Call harvest_get_projects() to get active projects and client names
2. Call read_daily_knowledge(date="{date_str}") to find client mentions
3. For each client found, link relevant people and projects and call ensure_client_profile(...)

Report: clients_created, clients_updated, total_clients_processed""",
        expected_output="""Report: clients_created, clients_updated, total_clients_processed""",
        agent=client_agent,
        context=[email_task, chat_task, channel_task, context_task, person_task, project_task],
    )

    # Task 8: Update inbox with summary and regenerate index
    inbox_task = Task(
        description=f"""Update knowledge/inbox.md and knowledge/index.md. Time: {timestamp} UTC

PART 1 — Inbox changelog:
1. Call read_daily_knowledge(date="{date_str}") to retrieve the full day's archived content
2. Based on previous task outputs and the daily content, create a changelog entry
3. PREPEND it to inbox.md.

Format:
## {timestamp}

### Changes Today
- **Emails:** [count from email task]
- **Teams Chats:** [count from chat task]
- **Teams Channels:** [count from channel task]
- **Transcripts:** [count from context task]
- **People Profiles:** [count from person task]
- **Project Profiles:** [count from project task]
- **Client Profiles:** [count from client task]
- **Calendar:** [status from context task]
- **Time Tracking:** [timer status from context task]

### Action Items Detected
- [ ] [any requests found in messages]

### Files Updated
- [list all files updated by previous tasks]

---

Read inbox.md first, then prepend the new entry at the TOP.

PART 2 — Regenerate index.md:
1. Call list_knowledge("projects") to get all project files
2. Call list_knowledge("clients") to get all client files
3. Call list_knowledge("people") to get key people (read a few to identify key contacts)
4. Regenerate knowledge/index.md with up-to-date tables:
   - Active Projects table (name, client, status)
   - Clients table (name, key contact, active project)
   - Key People section (internal team + key external contacts)
   - Recent Meetings (last 7 meeting files)
   - Upcoming Deadlines (from calendar/context task)
5. Write the full index.md (overwrite is OK for index — it's regenerated each run)
6. Set the "Last Updated" date to {date_str}.""",
        expected_output="""Report: inbox_updated, index_regenerated, summary""",
        agent=inbox_agent,
        context=[email_task, chat_task, channel_task, context_task, person_task, project_task, client_task],
    )

    return [email_task, chat_task, channel_task, context_task, person_task, project_task, client_task, inbox_task]


def create_specialized_crew() -> Crew:
    """Create the specialized monitoring crew with smaller tasks."""
    email_agent, chat_agent, channel_agent, context_agent, person_agent, project_agent, client_agent, inbox_agent = create_specialized_agents()
    tasks = create_specialized_tasks(email_agent, chat_agent, channel_agent, context_agent, person_agent, project_agent, client_agent, inbox_agent)

    return Crew(
        agents=[email_agent, chat_agent, channel_agent, context_agent, person_agent, project_agent, client_agent, inbox_agent],
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
        description=f"""Collect data from today. Time: {timestamp} UTC

Use since_start_of_day=True on all tools.

1. get_emails(limit=50, since_start_of_day=True)
2. get_sent_emails(limit=50, since_start_of_day=True)
3. get_teams_chats(limit=50, since_start_of_day=True) - note: returns display_name
4. For each chat: get_chat_messages(chat_id, limit=50, since_start_of_day=True)
5. get_joined_teams(), get_team_channels(), get_channel_messages(since_start_of_day=True, limit=50)
6. get_today_events()
7. harvest_running_timers()
8. harvest_today_tracking()
9. get_all_transcripts(limit=200)""",
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
