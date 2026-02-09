"""Proactive insight generation.

Scheduled analysis that generates:
- Daily digests written to knowledge/inbox.md
- Weekly patterns written to knowledge/patterns/weekly-YYYY-WW.md
- Project health analysis based on communication patterns
"""

import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

from crewai import Agent, Crew, Process, Task

from src.crew.agents import get_llm, get_mcp_server
from src.crew.memory import get_memory
from src.crew.tools import get_knowledge_tools

logger = logging.getLogger(__name__)

KNOWLEDGE_DIR = Path("knowledge")


def create_insight_agent() -> Agent:
    """Create an agent specialized in generating insights."""
    return Agent(
        role="Strategic Analyst",
        goal="Generate actionable insights from work data patterns",
        backstory="""You are a strategic analyst who excels at finding
        meaningful patterns in work data. You can identify:

        - Communication patterns (who talks to whom, about what)
        - Project health indicators (activity levels, response times)
        - Time allocation trends
        - Emerging priorities and potential issues

        You write concise, actionable insights in markdown format.
        You focus on what matters and avoid noise.""",
        mcps=[get_mcp_server()],
        tools=get_knowledge_tools(),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        memory=False,
    )


def run_daily_digest() -> str:
    """Generate a daily digest of activity.

    This provides a summary of the day's communications, meetings,
    and any patterns detected. Written to knowledge/inbox.md.
    """
    logger.info("Generating daily digest...")

    agent = create_insight_agent()

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")

    task = Task(
        description=f"""Generate a daily digest for {date_str}.

        Gather and analyze:
        1. Get today's calendar events (get_today_events)
        2. Get emails from today (get_emails with search for today's date)
        3. Get Teams activity from today's logs (read_knowledge teams/{date_str}/)
        4. Get time tracking for today (harvest_today_tracking)

        Then analyze:
        - What were the key meetings/events?
        - Who did we communicate with most?
        - What projects got attention?
        - Any unresolved items?

        Format as a daily digest for knowledge/inbox.md.""",
        expected_output=f"""A markdown daily digest formatted as:

        # Daily Digest - {date_str}

        ## Schedule Summary
        - [key meetings and their outcomes]

        ## Communication Highlights
        - [important emails and messages]
        - [key people contacted]

        ## Time Allocation
        - [how time was spent by project]

        ## Open Items
        - [ ] [things that need follow-up]

        ## Tomorrow's Focus
        - [suggested priorities for tomorrow]""",
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    # Write to inbox.md
    inbox_path = KNOWLEDGE_DIR / "inbox.md"
    try:
        existing = inbox_path.read_text() if inbox_path.exists() else ""
        new_content = f"{result}\n\n---\n\n{existing}"
        inbox_path.write_text(new_content)
        logger.info(f"Daily digest written to {inbox_path}")
    except Exception as e:
        logger.error(f"Failed to write daily digest: {e}")

    return result


def run_weekly_patterns() -> str:
    """Analyze the week's patterns and write to knowledge/patterns/.

    This looks for:
    - Communication patterns
    - Project activity trends
    - Time allocation patterns
    - Emerging themes
    """
    logger.info("Analyzing weekly patterns...")

    memory = get_memory()
    stats = memory.get_statistics()
    recent_runs = memory.get_recent_runs(count=10)

    agent = create_insight_agent()

    now = datetime.now(timezone.utc)
    week_num = now.strftime("%Y-W%W")
    week_start = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")
    week_end = now.strftime("%Y-%m-%d")

    task = Task(
        description=f"""Analyze patterns for week {week_num} ({week_start} to {week_end}).

        Historical context from memory:
        - Total monitoring runs: {stats.get('total_runs', 0)}
        - Emails processed: {stats.get('emails_processed', 0)}
        - Messages processed: {stats.get('messages_processed', 0)}

        Recent run summaries:
        {json.dumps(recent_runs, indent=2)}

        Gather this week's data:
        1. Get calendar events for the week (get_calendar_events days=7 past_days=7)
        2. List Teams logs for the week (list_knowledge teams/)
        3. Get Harvest time entries for the week (harvest_get_time_entries from={week_start} to={week_end})
        4. Read existing patterns (list_knowledge patterns/)

        Identify patterns:
        - Who are the most frequent contacts?
        - Which projects are getting the most attention?
        - What times are most active?
        - Any communication gaps or concerns?
        - Are there emerging themes in discussions?""",
        expected_output=f"""A markdown pattern analysis formatted as:

        # Weekly Patterns - Week {week_num}

        ## Communication Patterns
        - Top contacts this week: [list with frequency]
        - Communication channels used: [breakdown]

        ## Project Activity
        - Most active projects: [list with hours/messages]
        - Projects needing attention: [any that are quiet]

        ## Time Patterns
        - Total tracked hours: X
        - Busiest days: [list]
        - Time by client: [breakdown]

        ## Emerging Themes
        - [recurring topics in discussions]
        - [trends spotted]

        ## Recommendations
        - [actionable suggestions based on patterns]""",
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    # Write to patterns directory
    patterns_dir = KNOWLEDGE_DIR / "patterns"
    patterns_dir.mkdir(exist_ok=True)
    pattern_file = patterns_dir / f"weekly-{week_num}.md"

    try:
        pattern_file.write_text(str(result))
        logger.info(f"Weekly patterns written to {pattern_file}")
    except Exception as e:
        logger.error(f"Failed to write weekly patterns: {e}")

    return result


def run_project_health() -> str:
    """Analyze project health based on communication patterns.

    Flags projects that might need attention based on:
    - Declining communication
    - No recent time tracking
    - Overdue items mentioned
    """
    logger.info("Analyzing project health...")

    agent = create_insight_agent()

    task = Task(
        description="""Analyze project health across all active projects.

        Gather data:
        1. Get active Harvest projects (harvest_get_projects)
        2. Get recent time entries (harvest_get_time_entries for last 14 days)
        3. Read project files (list_knowledge projects/)
        4. Get recent emails mentioning projects (get_emails with search)

        For each project, assess:
        - Recent activity level (time tracked, messages)
        - Last communication date
        - Any mentioned blockers or issues
        - Budget status if available

        Flag any projects that show warning signs:
        - No activity in 7+ days
        - Sudden drop in communication
        - Budget concerns
        - Mentioned deadlines approaching""",
        expected_output="""A project health report formatted as:

        # Project Health Report

        ## Healthy Projects
        - [project]: [activity summary]

        ## Needs Attention
        - [project]: [concern] - [recommendation]

        ## At Risk
        - [project]: [critical issues] - [urgent action needed]

        ## Action Items
        - [ ] [specific follow-up actions]""",
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    # Write to inbox as an alert
    inbox_path = KNOWLEDGE_DIR / "inbox.md"
    try:
        existing = inbox_path.read_text() if inbox_path.exists() else ""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        new_content = f"## {now} - Project Health Check\n\n{result}\n\n---\n\n{existing}"
        inbox_path.write_text(new_content)
        logger.info("Project health report written to inbox")
    except Exception as e:
        logger.error(f"Failed to write project health: {e}")

    return result


def should_run_daily_digest() -> bool:
    """Check if daily digest should run (once per day, evening)."""
    memory = get_memory()
    last_run = memory.get_last_run()

    if not last_run:
        return True

    last_timestamp = last_run.get("timestamp", "")
    if not last_timestamp:
        return True

    try:
        last_dt = datetime.fromisoformat(last_timestamp.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)

        # Run if last run was on a different day
        return last_dt.date() < now.date()
    except Exception:
        return True


def should_run_weekly_patterns() -> bool:
    """Check if weekly patterns should run (once per week, Friday/Sunday)."""
    now = datetime.now(timezone.utc)
    # Run on Friday (4) or Sunday (6)
    return now.weekday() in (4, 6)


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m src.crew.insights <command>")
        print("Commands: daily, weekly, health")
        sys.exit(1)

    command = sys.argv[1]

    if command == "daily":
        result = run_daily_digest()
    elif command == "weekly":
        result = run_weekly_patterns()
    elif command == "health":
        result = run_project_health()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

    print(result)
