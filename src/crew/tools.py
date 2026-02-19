"""CrewAI tools wrapping existing Microsoft Graph and Harvest clients.

These tools wrap the existing async clients with proper schemas
for Azure OpenAI function calling compatibility.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from src.config import settings
from src.harvest.client import HarvestClient
from src.microsoft.auth import MicrosoftAuth
from src.microsoft.copilot_client import MeetingInsightsClient
from src.microsoft.graph_client import GraphClient

logger = logging.getLogger(__name__)

# Default user ID for single-user mode
DEFAULT_USER_ID = "default"

# Knowledge base path
KNOWLEDGE_BASE_PATH = Path("knowledge")


def _run_async(coro):
    """Run an async coroutine synchronously."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, coro)
                return future.result()
        return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


def _start_of_day_utc() -> datetime:
    """Return the UTC start-of-day timestamp for today."""
    now = datetime.now(timezone.utc)
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


async def _get_graph_client() -> GraphClient | None:
    """Get an authenticated Graph client."""
    auth = MicrosoftAuth()
    token = await auth.get_access_token(DEFAULT_USER_ID)
    if not token:
        logger.error("Microsoft 365 not connected - no access token")
        return None
    return GraphClient(token)


def _get_harvest_client() -> HarvestClient | None:
    """Get a Harvest client if configured."""
    if not settings.harvest_account_id or not settings.harvest_access_token:
        logger.warning("Harvest not configured")
        return None
    return HarvestClient(settings.harvest_account_id, settings.harvest_access_token)


async def _get_meetings_client() -> MeetingInsightsClient | None:
    """Get an authenticated Meetings/Transcripts client."""
    auth = MicrosoftAuth()
    token = await auth.get_access_token(DEFAULT_USER_ID)
    if not token:
        logger.error("Microsoft 365 not connected - no access token")
        return None
    return MeetingInsightsClient(token)


# ==================== CALENDAR TOOLS ====================


class GetCalendarEventsInput(BaseModel):
    """Input for getting calendar events."""
    days: int = Field(default=1, description="Days to look ahead")
    past_days: int = Field(default=0, description="Days to look back")


class GetCalendarEventsTool(BaseTool):
    """Get calendar events from Microsoft 365."""

    name: str = "get_calendar_events"
    description: str = "Get calendar events. Use days/past_days to control the time range."
    args_schema: Type[BaseModel] = GetCalendarEventsInput

    def _run(self, days: int = 1, past_days: int = 0) -> str:
        async def _fetch():
            client = await _get_graph_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            events = await client.get_calendar_events(days=days, past_days=past_days)
            return json.dumps(events, default=str)
        return _run_async(_fetch())


class GetTodayEventsTool(BaseTool):
    """Get today's calendar events."""

    name: str = "get_today_events"
    description: str = "Get all calendar events for today."

    def _run(self) -> str:
        async def _fetch():
            client = await _get_graph_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            events = await client.get_today_events()
            return json.dumps(events, default=str)
        return _run_async(_fetch())


# ==================== EMAIL TOOLS ====================


class GetEmailsInput(BaseModel):
    """Input for getting emails."""
    limit: int = Field(default=10, description="Maximum emails to return")
    folder: str = Field(default="inbox", description="Mail folder: inbox, sentitems, drafts")
    since_minutes: int | None = Field(default=None, description="Only return emails from the last N minutes")
    since_start_of_day: bool = Field(default=False, description="Only return emails from the start of today (UTC)")


class GetEmailsTool(BaseTool):
    """Get emails from Microsoft 365."""

    name: str = "get_emails"
    description: str = "Get emails from a folder. Supports inbox, sentitems, drafts. Use since_minutes or since_start_of_day to filter to recent emails only."
    args_schema: Type[BaseModel] = GetEmailsInput

    def _run(
        self,
        limit: int = 10,
        folder: str = "inbox",
        since_minutes: int | None = None,
        since_start_of_day: bool = False,
    ) -> str:
        async def _fetch():
            client = await _get_graph_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            emails = await client.get_emails(limit=limit, folder=folder)

            # Filter by time if since_minutes is specified
            cutoff = None
            if since_start_of_day:
                cutoff = _start_of_day_utc()
            elif since_minutes is not None:
                cutoff = datetime.now(timezone.utc) - timedelta(minutes=since_minutes)

            if cutoff and emails:
                filtered = []
                for email in emails:
                    received = email.get("received", "")
                    if received:
                        try:
                            # Parse ISO format timestamp
                            email_time = datetime.fromisoformat(received.replace("Z", "+00:00"))
                            if email_time >= cutoff:
                                filtered.append(email)
                        except (ValueError, TypeError):
                            pass  # Skip emails with unparseable timestamps
                emails = filtered

            return json.dumps(emails, default=str)
        return _run_async(_fetch())


class GetSentEmailsInput(BaseModel):
    """Input for getting sent emails."""
    limit: int = Field(default=10, description="Maximum emails to return")
    since_minutes: int | None = Field(default=None, description="Only return emails from the last N minutes")
    since_start_of_day: bool = Field(default=False, description="Only return emails from the start of today (UTC)")


class GetSentEmailsTool(BaseTool):
    """Get sent emails."""

    name: str = "get_sent_emails"
    description: str = "Get emails you have sent. Use since_minutes or since_start_of_day to filter to recent emails only."
    args_schema: Type[BaseModel] = GetSentEmailsInput

    def _run(
        self,
        limit: int = 10,
        since_minutes: int | None = None,
        since_start_of_day: bool = False,
    ) -> str:
        async def _fetch():
            client = await _get_graph_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            emails = await client.get_sent_emails(limit=limit)

            # Filter by time if since_minutes is specified
            cutoff = None
            if since_start_of_day:
                cutoff = _start_of_day_utc()
            elif since_minutes is not None:
                cutoff = datetime.now(timezone.utc) - timedelta(minutes=since_minutes)

            if cutoff and emails:
                filtered = []
                for email in emails:
                    sent = email.get("sent", "")
                    if sent:
                        try:
                            email_time = datetime.fromisoformat(sent.replace("Z", "+00:00"))
                            if email_time >= cutoff:
                                filtered.append(email)
                        except (ValueError, TypeError):
                            pass
                emails = filtered

            return json.dumps(emails, default=str)
        return _run_async(_fetch())


# ==================== TEAMS TOOLS ====================


class GetTeamsChatsInput(BaseModel):
    """Input for getting Teams chats."""
    limit: int = Field(default=10, description="Maximum chats to return")
    since_minutes: int | None = Field(default=None, description="Only return chats with activity in the last N minutes")
    since_start_of_day: bool = Field(default=False, description="Only return chats with activity since start of today (UTC)")


class GetTeamsChatsTool(BaseTool):
    """Get recent Teams chats."""

    name: str = "get_teams_chats"
    description: str = "Get recent Teams chat conversations (1:1 and group DMs). Use since_minutes or since_start_of_day to filter to chats with recent activity only."
    args_schema: Type[BaseModel] = GetTeamsChatsInput

    def _run(
        self,
        limit: int = 10,
        since_minutes: int | None = None,
        since_start_of_day: bool = False,
    ) -> str:
        async def _fetch():
            client = await _get_graph_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            chats = await client.get_teams_chats(limit=limit)

            # Filter by last message time if since_minutes is specified
            cutoff = None
            if since_start_of_day:
                cutoff = _start_of_day_utc()
            elif since_minutes is not None:
                cutoff = datetime.now(timezone.utc) - timedelta(minutes=since_minutes)

            if cutoff and chats:
                filtered = []
                for chat in chats:
                    last_msg_time = chat.get("last_message_time", "")
                    if last_msg_time:
                        try:
                            chat_time = datetime.fromisoformat(last_msg_time.replace("Z", "+00:00"))
                            if chat_time >= cutoff:
                                filtered.append(chat)
                        except (ValueError, TypeError):
                            pass
                chats = filtered

            return json.dumps(chats, default=str)
        return _run_async(_fetch())


class GetChatMessagesInput(BaseModel):
    """Input for getting chat messages."""
    chat_id: str = Field(description="The chat ID to get messages from")
    limit: int = Field(default=20, description="Maximum messages to return")
    since_minutes: int | None = Field(default=None, description="Only return messages from the last N minutes")
    since_start_of_day: bool = Field(default=False, description="Only return messages since start of today (UTC)")


class GetChatMessagesTool(BaseTool):
    """Get messages from a specific Teams chat."""

    name: str = "get_chat_messages"
    description: str = "Get messages from a specific Teams chat by ID. Use since_minutes or since_start_of_day to filter to recent messages only."
    args_schema: Type[BaseModel] = GetChatMessagesInput

    def _run(
        self,
        chat_id: str,
        limit: int = 20,
        since_minutes: int | None = None,
        since_start_of_day: bool = False,
    ) -> str:
        async def _fetch():
            client = await _get_graph_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            messages = await client.get_chat_messages(chat_id=chat_id, limit=limit)

            # Filter by time if since_minutes is specified
            cutoff = None
            if since_start_of_day:
                cutoff = _start_of_day_utc()
            elif since_minutes is not None:
                cutoff = datetime.now(timezone.utc) - timedelta(minutes=since_minutes)

            if cutoff and messages:
                filtered = []
                for msg in messages:
                    created = msg.get("created", "")
                    if created:
                        try:
                            msg_time = datetime.fromisoformat(created.replace("Z", "+00:00"))
                            if msg_time >= cutoff:
                                filtered.append(msg)
                        except (ValueError, TypeError):
                            pass
                messages = filtered

            return json.dumps(messages, default=str)
        return _run_async(_fetch())


# ==================== TEAMS CHANNELS TOOLS ====================


class GetJoinedTeamsTool(BaseTool):
    """Get Teams that you are a member of."""

    name: str = "get_joined_teams"
    description: str = "Get Teams (workspaces) that you are a member of."

    def _run(self) -> str:
        async def _fetch():
            client = await _get_graph_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            teams = await client.get_joined_teams()
            return json.dumps(teams, default=str)
        return _run_async(_fetch())


class GetTeamChannelsInput(BaseModel):
    """Input for getting team channels."""
    team_id: str = Field(description="The Team ID")


class GetTeamChannelsTool(BaseTool):
    """Get channels for a specific Team."""

    name: str = "get_team_channels"
    description: str = "Get channels for a specific Team by ID."
    args_schema: Type[BaseModel] = GetTeamChannelsInput

    def _run(self, team_id: str) -> str:
        async def _fetch():
            client = await _get_graph_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            channels = await client.get_team_channels(team_id=team_id)
            return json.dumps(channels, default=str)
        return _run_async(_fetch())


class GetChannelMessagesInput(BaseModel):
    """Input for getting channel messages."""
    team_id: str = Field(description="The Team ID")
    channel_id: str = Field(description="The Channel ID")
    limit: int = Field(default=20, description="Maximum messages to return")
    since_minutes: int | None = Field(default=None, description="Only return messages from the last N minutes")
    since_start_of_day: bool = Field(default=False, description="Only return messages since start of today (UTC)")


class GetChannelMessagesTool(BaseTool):
    """Get messages from a Teams channel."""

    name: str = "get_channel_messages"
    description: str = "Get messages from a Teams channel. Use since_minutes or since_start_of_day to filter to recent messages only."
    args_schema: Type[BaseModel] = GetChannelMessagesInput

    def _run(
        self,
        team_id: str,
        channel_id: str,
        limit: int = 20,
        since_minutes: int | None = None,
        since_start_of_day: bool = False,
    ) -> str:
        async def _fetch():
            client = await _get_graph_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            messages = await client.get_channel_messages(
                team_id=team_id, channel_id=channel_id, limit=limit
            )

            # Filter by time if since_minutes is specified
            cutoff = None
            if since_start_of_day:
                cutoff = _start_of_day_utc()
            elif since_minutes is not None:
                cutoff = datetime.now(timezone.utc) - timedelta(minutes=since_minutes)

            if cutoff and messages:
                filtered = []
                for msg in messages:
                    created = msg.get("created", "")
                    if created:
                        try:
                            msg_time = datetime.fromisoformat(created.replace("Z", "+00:00"))
                            if msg_time >= cutoff:
                                filtered.append(msg)
                        except (ValueError, TypeError):
                            pass
                messages = filtered

            return json.dumps(messages, default=str)
        return _run_async(_fetch())


class GetChannelMessageRepliesInput(BaseModel):
    """Input for getting channel message replies."""
    team_id: str = Field(description="The Team ID")
    channel_id: str = Field(description="The Channel ID")
    message_id: str = Field(description="The parent message ID to get replies for")
    limit: int = Field(default=50, description="Maximum replies to return")


class GetChannelMessageRepliesTool(BaseTool):
    """Get replies to a specific Teams channel message thread."""

    name: str = "get_channel_message_replies"
    description: str = "Get replies to a specific channel message thread. Use after get_channel_messages to fetch reply threads for messages with reply_count > 0."
    args_schema: Type[BaseModel] = GetChannelMessageRepliesInput

    def _run(self, team_id: str, channel_id: str, message_id: str, limit: int = 50) -> str:
        async def _fetch():
            client = await _get_graph_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            replies = await client.get_channel_message_replies(
                team_id=team_id, channel_id=channel_id, message_id=message_id, limit=limit
            )
            return json.dumps(replies, default=str)
        return _run_async(_fetch())


# ==================== HARVEST TOOLS ====================


class HarvestGetProjectsTool(BaseTool):
    """Get Harvest projects."""

    name: str = "harvest_get_projects"
    description: str = "Get active projects from Harvest with client and budget info."

    def _run(self) -> str:
        async def _fetch():
            client = _get_harvest_client()
            if not client:
                return json.dumps({"error": "Harvest not configured"})
            projects = await client.get_projects()
            return json.dumps(projects, default=str)
        return _run_async(_fetch())


class HarvestMyTimeInput(BaseModel):
    """Input for getting my time entries."""
    days: int = Field(default=7, description="Days to look back")


class HarvestMyTimeTool(BaseTool):
    """Get current user's recent time entries."""

    name: str = "harvest_my_time"
    description: str = "Get the current user's recent time entries from Harvest."
    args_schema: Type[BaseModel] = HarvestMyTimeInput

    def _run(self, days: int = 7) -> str:
        async def _fetch():
            client = _get_harvest_client()
            if not client:
                return json.dumps({"error": "Harvest not configured"})
            entries = await client.get_my_time_entries(days=days)
            return json.dumps(entries, default=str)
        return _run_async(_fetch())


class HarvestRunningTimersTool(BaseTool):
    """Get any currently running Harvest timers."""

    name: str = "harvest_running_timers"
    description: str = "Find any currently running timers in Harvest."

    def _run(self) -> str:
        async def _fetch():
            client = _get_harvest_client()
            if not client:
                return json.dumps({"error": "Harvest not configured"})
            timers = await client.get_running_timers()
            return json.dumps(timers, default=str)
        return _run_async(_fetch())


class HarvestTodayTrackingTool(BaseTool):
    """Get time entries being tracked today."""

    name: str = "harvest_today_tracking"
    description: str = "Get time entries being tracked today in Harvest."

    def _run(self) -> str:
        async def _fetch():
            client = _get_harvest_client()
            if not client:
                return json.dumps({"error": "Harvest not configured"})
            entries = await client.get_today_time_entries()
            return json.dumps(entries, default=str)
        return _run_async(_fetch())


# ==================== MEETING & TRANSCRIPT TOOLS ====================


class GetMeetingSummaryInput(BaseModel):
    """Input for getting meeting summary with Copilot AI insights."""
    subject: str = Field(description="Meeting subject to search for")
    organizer_email: str | None = Field(default=None, description="Optional organizer email for better matching")


class GetMeetingSummaryTool(BaseTool):
    """Get meeting summary including Copilot AI insights (action items, meeting notes)."""

    name: str = "get_meeting_summary"
    description: str = """Get a meeting summary with Copilot AI-generated insights including:
    - Action items with owners
    - Meeting notes with structured subpoints
    - Transcript preview if available
    Search by meeting subject. Returns formatted summary."""
    args_schema: Type[BaseModel] = GetMeetingSummaryInput

    def _run(self, subject: str, organizer_email: str | None = None) -> str:
        async def _fetch():
            client = await _get_meetings_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})

            result = await client.get_meeting_summary(
                subject=subject,
                organizer_email=organizer_email,
            )
            return json.dumps(result, default=str)
        return _run_async(_fetch())


class GetRecentMeetingsInput(BaseModel):
    """Input for getting recent meetings."""
    days_back: int = Field(default=7, description="Days to look back")
    limit: int = Field(default=10, description="Maximum meetings to return")


class GetRecentMeetingsTool(BaseTool):
    """Get recent Teams meetings from calendar."""

    name: str = "get_recent_meetings"
    description: str = "Get recent Teams online meetings from calendar. Use to find meeting IDs and subjects."
    args_schema: Type[BaseModel] = GetRecentMeetingsInput

    def _run(self, days_back: int = 7, limit: int = 10) -> str:
        async def _fetch():
            client = await _get_meetings_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})

            meetings = await client.get_recent_meetings(days_back=days_back, limit=limit)
            return json.dumps(meetings, default=str)
        return _run_async(_fetch())


class GetMeetingsForDateInput(BaseModel):
    """Input for getting meetings for a specific date."""
    date: str = Field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"), description="Date in YYYY-MM-DD")
    limit: int = Field(default=200, description="Maximum meetings to return")


class GetMeetingsForDateTool(BaseTool):
    """Get Teams online meetings for a specific date."""

    name: str = "get_meetings_for_date"
    description: str = "Get Teams online meetings for a specific date. Returns meeting IDs, subjects, times, and organizer info."
    args_schema: Type[BaseModel] = GetMeetingsForDateInput

    def _run(self, date: str, limit: int = 200) -> str:
        async def _fetch():
            client = await _get_meetings_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            meetings = await client.get_meetings_for_date(date_str=date, limit=limit)
            return json.dumps(meetings, default=str)
        return _run_async(_fetch())


class GetAllTranscriptsInput(BaseModel):
    """Input for getting all transcripts."""
    limit: int = Field(default=200, description="Maximum transcripts to return")


class GetAllTranscriptsTool(BaseTool):
    """Get all available meeting transcripts."""

    name: str = "get_all_transcripts"
    description: str = "Get all available meeting transcripts. Returns a list of transcripts with meeting info."
    args_schema: Type[BaseModel] = GetAllTranscriptsInput

    def _run(self, limit: int = 50) -> str:
        async def _fetch():
            client = await _get_meetings_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            transcripts = await client.get_all_transcripts(limit=limit)
            return json.dumps(transcripts, default=str)
        return _run_async(_fetch())


class GetTranscriptByMeetingIdInput(BaseModel):
    """Input for getting a transcript by meeting ID."""
    meeting_id: str = Field(description="The online meeting ID")


class GetTranscriptByMeetingIdTool(BaseTool):
    """Get transcript for a specific meeting."""

    name: str = "get_transcript_by_meeting_id"
    description: str = "Get the full transcript for a specific meeting by its meeting ID."
    args_schema: Type[BaseModel] = GetTranscriptByMeetingIdInput

    def _run(self, meeting_id: str) -> str:
        async def _fetch():
            client = await _get_meetings_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})

            # Get transcripts for this meeting
            transcripts = await client.get_meeting_transcripts(meeting_id)
            if not transcripts:
                return json.dumps({"error": f"No transcripts found for meeting {meeting_id}"})

            # Get the content of the first transcript
            transcript = transcripts[0]
            transcript_id = transcript.get("id")
            content = await client.get_transcript_content(meeting_id, transcript_id)

            return json.dumps({
                "meeting_id": meeting_id,
                "transcript_id": transcript_id,
                "content": content,
            }, default=str)
        return _run_async(_fetch())


# ==================== KNOWLEDGE BASE TOOLS ====================


class ReadKnowledgeInput(BaseModel):
    """Input for reading knowledge files."""
    path: str = Field(description="Path relative to knowledge/ directory")


class ReadKnowledgeTool(BaseTool):
    """Read a file from the knowledge base."""

    name: str = "read_knowledge"
    description: str = "Read a markdown file from the knowledge base. Path is relative to knowledge/."
    args_schema: Type[BaseModel] = ReadKnowledgeInput

    def _run(self, path: str) -> str:
        file_path = KNOWLEDGE_BASE_PATH / path
        if not file_path.exists():
            return json.dumps({"error": f"File not found: {path}"})

        try:
            content = file_path.read_text()
            return json.dumps({
                "path": path,
                "content": content,
                "size": len(content),
            })
        except Exception as e:
            return json.dumps({"error": f"Failed to read {path}: {str(e)}"})


class WriteKnowledgeInput(BaseModel):
    """Input for writing knowledge files."""
    path: str = Field(description="Path relative to knowledge/ directory")
    content: str = Field(description="Content to write")
    append: bool = Field(default=False, description="Append instead of overwrite")


class WriteKnowledgeTool(BaseTool):
    """Write a file to the knowledge base."""

    name: str = "write_knowledge"
    description: str = "Write or update a markdown file in the knowledge base. Path is relative to knowledge/."
    args_schema: Type[BaseModel] = WriteKnowledgeInput

    def _run(self, path: str, content: str, append: bool = False) -> str:
        file_path = KNOWLEDGE_BASE_PATH / path

        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if append and file_path.exists():
                existing = file_path.read_text()
                content = existing + "\n" + content

            file_path.write_text(content)
            return json.dumps({
                "success": True,
                "path": path,
                "size": len(content),
                "action": "appended" if append else "written",
            })
        except Exception as e:
            return json.dumps({"error": f"Failed to write {path}: {str(e)}"})


class ListKnowledgeInput(BaseModel):
    """Input for listing knowledge files."""
    directory: str = Field(default="", description="Directory relative to knowledge/")


class ListKnowledgeTool(BaseTool):
    """List files in the knowledge base."""

    name: str = "list_knowledge"
    description: str = "List files in a knowledge base directory."
    args_schema: Type[BaseModel] = ListKnowledgeInput

    def _run(self, directory: str = "") -> str:
        dir_path = KNOWLEDGE_BASE_PATH / directory
        if not dir_path.exists():
            return json.dumps({"error": f"Directory not found: {directory}"})

        try:
            files = []
            for item in dir_path.iterdir():
                files.append({
                    "name": item.name,
                    "is_directory": item.is_dir(),
                    "size": item.stat().st_size if item.is_file() else None,
                })
            return json.dumps({
                "directory": directory or "/",
                "files": sorted(files, key=lambda x: (not x["is_directory"], x["name"])),
            })
        except Exception as e:
            return json.dumps({"error": f"Failed to list {directory}: {str(e)}"})


# ==================== DAILY KNOWLEDGE AGGREGATION ====================


class ReadDailyKnowledgeInput(BaseModel):
    """Input for reading all knowledge files for a given day."""
    date: str | None = Field(
        default=None,
        description="Date in YYYY-MM-DD. Defaults to today (UTC).",
    )


class ReadDailyKnowledgeTool(BaseTool):
    """Read all knowledge files for a given day."""

    name: str = "read_daily_knowledge"
    description: str = (
        "Read all knowledge base content for a given day (emails, teams, channels, meetings). "
        "Returns file paths and full content."
    )
    args_schema: Type[BaseModel] = ReadDailyKnowledgeInput

    def _run(self, date: str | None = None) -> str:
        date_str = date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        base = KNOWLEDGE_BASE_PATH

        files_to_read: list[Path] = []
        missing: list[str] = []
        errors: list[str] = []

        # Single-file locations
        email_path = base / "emails" / f"{date_str}.md"
        if email_path.exists():
            files_to_read.append(email_path)
        else:
            missing.append(f"emails/{date_str}.md")

        # Directory locations
        teams_dir = base / "teams" / date_str
        if teams_dir.exists() and teams_dir.is_dir():
            files_to_read.extend(sorted(teams_dir.glob("*.md")))
        else:
            missing.append(f"teams/{date_str}/")

        channels_dir = base / "channels" / date_str
        if channels_dir.exists() and channels_dir.is_dir():
            files_to_read.extend(sorted(channels_dir.glob("*.md")))
        else:
            missing.append(f"channels/{date_str}/")

        # Meetings (summaries and transcripts)
        meetings_dir = base / "meetings"
        if meetings_dir.exists() and meetings_dir.is_dir():
            files_to_read.extend(sorted(meetings_dir.glob(f"{date_str}-*.md")))
        else:
            missing.append("meetings/")

        transcripts_dir = base / "meetings" / "transcripts"
        if transcripts_dir.exists() and transcripts_dir.is_dir():
            files_to_read.extend(sorted(transcripts_dir.glob(f"{date_str}-*.md")))
        else:
            missing.append("meetings/transcripts/")

        results = []
        for file_path in files_to_read:
            try:
                content = file_path.read_text()
                rel_path = str(file_path.relative_to(base))
                results.append({
                    "path": rel_path,
                    "size": len(content),
                    "content": content,
                })
            except Exception as e:
                errors.append(f"{file_path}: {str(e)}")

        return json.dumps({
            "date": date_str,
            "count": len(results),
            "files": results,
            "missing": missing,
            "errors": errors,
        })


# ==================== PERSON PROFILE TOOLS ====================


def _name_to_kebab(name: str) -> str:
    """Convert a name to kebab-case filename."""
    import re
    # Remove any special characters except spaces and hyphens
    cleaned = re.sub(r"[^a-zA-Z\s\-]", "", name)
    # Convert to lowercase and replace spaces with hyphens
    kebab = cleaned.lower().strip().replace(" ", "-")
    # Remove double hyphens
    kebab = re.sub(r"-+", "-", kebab)
    return kebab


class EnsurePersonProfileInput(BaseModel):
    """Input for ensuring a person profile exists."""
    name: str = Field(description="Full name of the person (e.g., 'Fraser Smith')")
    email: str | None = Field(default=None, description="Email address if known")
    company: str | None = Field(default=None, description="Company/organization if known")
    role: str | None = Field(default=None, description="Job role/title if known")
    context: str | None = Field(default=None, description="How you encountered this person (e.g., 'Teams chat', 'Email from')")
    interaction_note: str | None = Field(default=None, description="Brief note about the interaction")


class EnsurePersonProfileTool(BaseTool):
    """Ensure a person has a profile in the knowledge base, creating one if needed."""

    name: str = "ensure_person_profile"
    description: str = """Ensure a person has a profile in knowledge/people/.
    If the profile doesn't exist, creates a new one with basic info.
    If it exists, appends a new interaction note.
    Use this for every person you encounter in emails, Teams messages, or meetings.
    Returns the profile path and whether it was created or updated."""
    args_schema: Type[BaseModel] = EnsurePersonProfileInput

    def _run(
        self,
        name: str,
        email: str | None = None,
        company: str | None = None,
        role: str | None = None,
        context: str | None = None,
        interaction_note: str | None = None,
    ) -> str:
        # Skip if name is empty or looks like a system/bot/noise
        skip_names = {
            "unknown", "system", "bot", "microsoft", "teams", "notifications",
            "no-reply", "noreply", "admin", "support", "info", "calendar",
            "outlook", "sharepoint", "onedrive", "power automate", "power bi",
            "adobe", "zoom", "slack", "google", "automated", "do not reply",
        }
        if not name or len(name.strip()) <= 2 or name.lower().strip() in skip_names:
            return json.dumps({"skipped": True, "reason": "Invalid, system, or too-short name"})

        # Skip names that look like email artifacts or noise
        import re
        cleaned_name = name.strip()
        if re.match(r'^[a-zA-Z]{1,2}$', cleaned_name):  # Single/double letter names
            return json.dumps({"skipped": True, "reason": "Name too short"})
        if '@' in cleaned_name:  # Raw email addresses
            return json.dumps({"skipped": True, "reason": "Raw email address, not a name"})
        if re.match(r'^(via |sent by )', cleaned_name, re.IGNORECASE):
            return json.dumps({"skipped": True, "reason": "Not a person name"})

        filename = _name_to_kebab(name) + ".md"
        file_path = KNOWLEDGE_BASE_PATH / "people" / filename

        today = datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        if file_path.exists():
            # Profile exists - append interaction note if provided
            if interaction_note:
                try:
                    existing = file_path.read_text()

                    # Check if we already have an interaction noted at this timestamp
                    if now_time in existing:
                        return json.dumps({
                            "action": "skipped",
                            "reason": "Interaction already noted for this timestamp",
                            "path": f"people/{filename}",
                        })

                    # Append to recent interactions section
                    interaction_entry = f"\n- **{now_time}:** {interaction_note}"

                    if "## Recent interactions" in existing:
                        # Insert after the section header
                        parts = existing.split("## Recent interactions")
                        updated = parts[0] + "## Recent interactions" + interaction_entry + parts[1]
                    else:
                        # Add the section before the last line (assuming ---\n*Last Updated*)
                        if "---" in existing:
                            parts = existing.rsplit("---", 1)
                            updated = parts[0] + "## Recent interactions" + interaction_entry + "\n\n---" + parts[1]
                        else:
                            updated = existing + f"\n\n## Recent interactions{interaction_entry}\n"

                    # Update the last updated date
                    if "*Last Updated:" in updated:
                        import re
                        updated = re.sub(
                            r"\*Last Updated: \d{4}-\d{2}-\d{2}\*",
                            f"*Last Updated: {today}*",
                            updated
                        )

                    file_path.write_text(updated)
                    return json.dumps({
                        "action": "updated",
                        "path": f"people/{filename}",
                        "name": name,
                    })
                except Exception as e:
                    return json.dumps({"error": f"Failed to update profile: {str(e)}"})

            return json.dumps({
                "action": "exists",
                "path": f"people/{filename}",
                "name": name,
            })

        # Create new profile
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Determine person type
            person_type = "Unknown"
            if email:
                if "@synapx.com" in email.lower():
                    person_type = "Internal - Colleague"
                else:
                    person_type = "External - Contact"

            profile_content = f"""# {name}

## Basic Info
- **Role**: {role or "Unknown"}
- **Company**: {company or "Unknown"}
- **Type**: {person_type}
"""
            if email:
                profile_content += f"""
## Contact
- **Email**: {email}
"""

            if context or interaction_note:
                profile_content += f"""
## Recent interactions
- **{now_time}:** {interaction_note or f"First encountered via {context}"}
"""

            profile_content += f"""
---
*Last Updated: {today}*
"""

            file_path.write_text(profile_content)
            return json.dumps({
                "action": "created",
                "path": f"people/{filename}",
                "name": name,
            })
        except Exception as e:
            return json.dumps({"error": f"Failed to create profile: {str(e)}"})


# ==================== PROJECT PROFILE TOOLS ====================


class EnsureProjectProfileInput(BaseModel):
    """Input for ensuring a project profile exists."""
    name: str = Field(description="Project name (e.g., 'Nimans Slipstream')")
    client: str | None = Field(default=None, description="Client name if known")
    status: str | None = Field(default=None, description="Current project status")
    summary: str | None = Field(default=None, description="Brief project overview")
    activity_note: str | None = Field(default=None, description="Brief note about today's activity")


class EnsureProjectProfileTool(BaseTool):
    """Ensure a project has a profile in the knowledge base."""

    name: str = "ensure_project_profile"
    description: str = """Ensure a project has a profile in knowledge/projects/.
    If the profile doesn't exist, creates one with basic info.
    If it exists, appends a new activity note under Timeline / Log.
    Use this for every project found in Harvest, emails, or meetings."""
    args_schema: Type[BaseModel] = EnsureProjectProfileInput

    def _run(
        self,
        name: str,
        client: str | None = None,
        status: str | None = None,
        summary: str | None = None,
        activity_note: str | None = None,
    ) -> str:
        if not name:
            return json.dumps({"skipped": True, "reason": "Missing project name"})

        filename = _name_to_kebab(name) + ".md"
        file_path = KNOWLEDGE_BASE_PATH / "projects" / filename

        today = datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        if file_path.exists():
            if activity_note:
                try:
                    existing = file_path.read_text()

                    # Skip if we already have a note at this timestamp
                    if now_time in existing:
                        return json.dumps({
                            "action": "skipped",
                            "reason": "Activity already noted for this timestamp",
                            "path": f"projects/{filename}",
                        })

                    entry = f"\n### {today}\n- {activity_note}\n"

                    if "## Timeline / Log" in existing:
                        parts = existing.split("## Timeline / Log", 1)
                        updated = parts[0] + "## Timeline / Log" + entry + parts[1]
                    else:
                        updated = existing.rstrip() + f"\n\n## Timeline / Log{entry}"

                    if "*Last Updated:" in updated:
                        import re
                        updated = re.sub(
                            r"\*Last Updated: [^*]+\*",
                            f"*Last Updated: {today}*",
                            updated
                        )

                    file_path.write_text(updated)
                    return json.dumps({
                        "action": "updated",
                        "path": f"projects/{filename}",
                        "name": name,
                    })
                except Exception as e:
                    return json.dumps({"error": f"Failed to update project: {str(e)}"})

            return json.dumps({
                "action": "exists",
                "path": f"projects/{filename}",
                "name": name,
            })

        # Create new project profile
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

            client_link = ""
            if client:
                client_slug = _name_to_kebab(client)
                client_link = f"- **Client:** [{client}](../clients/{client_slug}.md)\n"

            profile_content = f"""# {name}

## Context
{summary or "Project context to be captured."}

{client_link}"""

            if status:
                profile_content += f"- **Status:** {status}\n"

            if activity_note:
                profile_content += f"""
## Timeline / Log

### {today}
- {activity_note}
"""

            profile_content += f"""
---
*Last Updated: {today}*
"""

            file_path.write_text(profile_content)
            return json.dumps({
                "action": "created",
                "path": f"projects/{filename}",
                "name": name,
            })
        except Exception as e:
            return json.dumps({"error": f"Failed to create project: {str(e)}"})


# ==================== CLIENT PROFILE TOOLS ====================


class ClientLink(BaseModel):
    """Link to a related knowledge item."""
    name: str = Field(description="Display name for the link")
    path: str = Field(description="Path relative to knowledge/ (e.g., people/jane-doe.md)")


class EnsureClientProfileInput(BaseModel):
    """Input for ensuring a client profile exists."""
    name: str = Field(description="Client/company name (e.g., 'Pro Global')")
    summary: str | None = Field(default=None, description="Short overview of the client/company")
    people: list[ClientLink] = Field(default_factory=list, description="People associated with this client")
    projects: list[ClientLink] = Field(default_factory=list, description="Projects associated with this client")
    activity_notes: list[str] = Field(default_factory=list, description="Recent activity notes to append")


class EnsureClientProfileTool(BaseTool):
    """Ensure a client has a profile in the knowledge base, creating one if needed."""

    name: str = "ensure_client_profile"
    description: str = """Ensure a client has a profile in knowledge/clients/.
    Creates a new profile if missing and updates relevant sections if it exists.
    Use this for every client encountered in Harvest projects or communications."""
    args_schema: Type[BaseModel] = EnsureClientProfileInput

    def _run(
        self,
        name: str,
        summary: str | None = None,
        people: list[ClientLink] | None = None,
        projects: list[ClientLink] | None = None,
        activity_notes: list[str] | None = None,
    ) -> str:
        if not name:
            return json.dumps({"skipped": True, "reason": "Missing client name"})

        filename = _name_to_kebab(name) + ".md"
        file_path = KNOWLEDGE_BASE_PATH / "clients" / filename

        today = datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        people = people or []
        projects = projects or []
        activity_notes = activity_notes or []

        def _normalize_link(path: str) -> str:
            if path.startswith("../"):
                return path
            return f"../{path}"

        def _build_links(items: list[ClientLink], empty_label: str) -> str:
            if not items:
                return f"- {empty_label}"
            lines = []
            for item in items:
                link_path = _normalize_link(item.path)
                lines.append(f"- [{item.name}]({link_path})")
            return "\n".join(lines)

        people_section = _build_links(people, "None yet.")
        projects_section = _build_links(projects, "None yet.")

        new_activity_lines = []
        for note in activity_notes:
            if note:
                new_activity_lines.append(f"- **{now_time}:** {note}")
        activity_block = "\n".join(new_activity_lines)

        def _replace_section(content: str, heading: str, body: str) -> str:
            import re
            pattern = rf"(^## {re.escape(heading)}\\n)([\\s\\S]*?)(?=^## |\\Z)"
            replacement = rf"## {heading}\n{body}\n\n"
            if re.search(pattern, content, flags=re.MULTILINE):
                return re.sub(pattern, replacement, content, flags=re.MULTILINE)
            return content + f"\n## {heading}\n{body}\n\n"

        if file_path.exists():
            existing = file_path.read_text()

            if summary:
                existing = _replace_section(existing, "Company Overview", summary.strip())

            existing = _replace_section(existing, "Relevant People", people_section)
            existing = _replace_section(existing, "Relevant Projects", projects_section)

            if activity_block:
                # Append new activity lines if not already present
                if "## Recent Activity" in existing:
                    import re
                    pattern = r"(^## Recent Activity\n)([\s\S]*?)(?=^## |\Z)"
                    match = re.search(pattern, existing, flags=re.MULTILINE)
                    if match:
                        current = match.group(2)
                        additions = []
                        for line in new_activity_lines:
                            if line not in current:
                                additions.append(line)
                        if additions:
                            updated_block = match.group(1) + current.rstrip() + "\n" + "\n".join(additions) + "\n\n"
                            existing = re.sub(pattern, updated_block, existing, flags=re.MULTILINE)
                else:
                    existing = _replace_section(existing, "Recent Activity", activity_block)

            if "*Last Updated:" in existing:
                import re
                existing = re.sub(
                    r"\*Last Updated: \d{4}-\d{2}-\d{2}\*",
                    f"*Last Updated: {today}*",
                    existing,
                )
            else:
                existing += f"\n---\n*Last Updated: {today}*\n"

            file_path.write_text(existing)
            return json.dumps({
                "action": "updated",
                "path": f"clients/{filename}",
                "name": name,
            })

        # Create new profile
        file_path.parent.mkdir(parents=True, exist_ok=True)

        overview = summary.strip() if summary else "Overview to be captured."
        profile_content = f"""# {name}

## Company Overview
{overview}

## Relevant People
{people_section}

## Relevant Projects
{projects_section}
"""

        if activity_block:
            profile_content += f"""
## Recent Activity
{activity_block}
"""

        profile_content += f"""
---
*Last Updated: {today}*
"""

        file_path.write_text(profile_content)
        return json.dumps({
            "action": "created",
            "path": f"clients/{filename}",
            "name": name,
        })


# ==================== UTILITY FUNCTIONS ====================


def get_all_tools() -> list[BaseTool]:
    """Get all available CrewAI tools."""
    return [
        # Calendar
        GetCalendarEventsTool(),
        GetTodayEventsTool(),
        # Email
        GetEmailsTool(),
        GetSentEmailsTool(),
        # Teams Chats
        GetTeamsChatsTool(),
        GetChatMessagesTool(),
        # Teams Channels
        GetJoinedTeamsTool(),
        GetTeamChannelsTool(),
        GetChannelMessagesTool(),
        GetChannelMessageRepliesTool(),
        # Harvest
        HarvestGetProjectsTool(),
        HarvestMyTimeTool(),
        HarvestRunningTimersTool(),
        HarvestTodayTrackingTool(),
        # Meetings & Transcripts
        GetMeetingSummaryTool(),
        GetRecentMeetingsTool(),
        GetMeetingsForDateTool(),
        GetAllTranscriptsTool(),
        GetTranscriptByMeetingIdTool(),
        # Knowledge Base
        ReadKnowledgeTool(),
        WriteKnowledgeTool(),
        ListKnowledgeTool(),
        ReadDailyKnowledgeTool(),
        EnsurePersonProfileTool(),
        EnsureProjectProfileTool(),
        EnsureClientProfileTool(),
    ]


def get_data_collection_tools() -> list[BaseTool]:
    """Get tools for data collection."""
    return [
        GetCalendarEventsTool(),
        GetTodayEventsTool(),
        GetEmailsTool(),
        GetSentEmailsTool(),
        GetTeamsChatsTool(),
        GetChatMessagesTool(),
        GetJoinedTeamsTool(),
        GetTeamChannelsTool(),
        GetChannelMessagesTool(),
        GetChannelMessageRepliesTool(),
        HarvestRunningTimersTool(),
        HarvestTodayTrackingTool(),
        HarvestMyTimeTool(),
        # Meetings & Transcripts
        GetMeetingSummaryTool(),
        GetRecentMeetingsTool(),
        GetMeetingsForDateTool(),
        GetAllTranscriptsTool(),
        GetTranscriptByMeetingIdTool(),
    ]


def get_analysis_tools() -> list[BaseTool]:
    """Get tools for analysis."""
    return [
        ReadKnowledgeTool(),
        ListKnowledgeTool(),
        ReadDailyKnowledgeTool(),
        GetCalendarEventsTool(),
        GetEmailsTool(),
        GetTeamsChatsTool(),
        GetChatMessagesTool(),
        HarvestGetProjectsTool(),
        # Meeting insights
        GetMeetingSummaryTool(),
        GetRecentMeetingsTool(),
    ]


def get_knowledge_tools() -> list[BaseTool]:
    """Get tools for knowledge base management."""
    return [
        ReadKnowledgeTool(),
        WriteKnowledgeTool(),
        ListKnowledgeTool(),
        ReadDailyKnowledgeTool(),
    ]


def get_person_tools() -> list[BaseTool]:
    """Get tools for person profile management."""
    return [
        EnsurePersonProfileTool(),
        ReadKnowledgeTool(),
        WriteKnowledgeTool(),
        ListKnowledgeTool(),
        ReadDailyKnowledgeTool(),
    ]


def get_client_tools() -> list[BaseTool]:
    """Get tools for client profile management."""
    return [
        EnsureClientProfileTool(),
        HarvestGetProjectsTool(),
        ReadKnowledgeTool(),
        WriteKnowledgeTool(),
        ListKnowledgeTool(),
        ReadDailyKnowledgeTool(),
    ]


def get_project_tools() -> list[BaseTool]:
    """Get tools for project profile management."""
    return [
        EnsureProjectProfileTool(),
        HarvestGetProjectsTool(),
        ReadKnowledgeTool(),
        WriteKnowledgeTool(),
        ListKnowledgeTool(),
        ReadDailyKnowledgeTool(),
    ]
