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


class GetEmailsTool(BaseTool):
    """Get emails from Microsoft 365."""

    name: str = "get_emails"
    description: str = "Get emails from a folder. Supports inbox, sentitems, drafts. Use since_minutes to filter to recent emails only."
    args_schema: Type[BaseModel] = GetEmailsInput

    def _run(self, limit: int = 10, folder: str = "inbox", since_minutes: int | None = None) -> str:
        async def _fetch():
            client = await _get_graph_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            emails = await client.get_emails(limit=limit, folder=folder)

            # Filter by time if since_minutes is specified
            if since_minutes is not None and emails:
                cutoff = datetime.now(timezone.utc) - timedelta(minutes=since_minutes)
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


class GetSentEmailsTool(BaseTool):
    """Get sent emails."""

    name: str = "get_sent_emails"
    description: str = "Get emails you have sent. Use since_minutes to filter to recent emails only."
    args_schema: Type[BaseModel] = GetSentEmailsInput

    def _run(self, limit: int = 10, since_minutes: int | None = None) -> str:
        async def _fetch():
            client = await _get_graph_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            emails = await client.get_sent_emails(limit=limit)

            # Filter by time if since_minutes is specified
            if since_minutes is not None and emails:
                cutoff = datetime.now(timezone.utc) - timedelta(minutes=since_minutes)
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


class GetTeamsChatsTool(BaseTool):
    """Get recent Teams chats."""

    name: str = "get_teams_chats"
    description: str = "Get recent Teams chat conversations (1:1 and group DMs). Use since_minutes to filter to chats with recent activity only."
    args_schema: Type[BaseModel] = GetTeamsChatsInput

    def _run(self, limit: int = 10, since_minutes: int | None = None) -> str:
        async def _fetch():
            client = await _get_graph_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            chats = await client.get_teams_chats(limit=limit)

            # Filter by last message time if since_minutes is specified
            if since_minutes is not None and chats:
                cutoff = datetime.now(timezone.utc) - timedelta(minutes=since_minutes)
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


class GetChatMessagesTool(BaseTool):
    """Get messages from a specific Teams chat."""

    name: str = "get_chat_messages"
    description: str = "Get messages from a specific Teams chat by ID. Use since_minutes to filter to recent messages only."
    args_schema: Type[BaseModel] = GetChatMessagesInput

    def _run(self, chat_id: str, limit: int = 20, since_minutes: int | None = None) -> str:
        async def _fetch():
            client = await _get_graph_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            messages = await client.get_chat_messages(chat_id=chat_id, limit=limit)

            # Filter by time if since_minutes is specified
            if since_minutes is not None and messages:
                cutoff = datetime.now(timezone.utc) - timedelta(minutes=since_minutes)
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


class GetChannelMessagesTool(BaseTool):
    """Get messages from a Teams channel."""

    name: str = "get_channel_messages"
    description: str = "Get messages from a Teams channel. Use since_minutes to filter to recent messages only."
    args_schema: Type[BaseModel] = GetChannelMessagesInput

    def _run(self, team_id: str, channel_id: str, limit: int = 20, since_minutes: int | None = None) -> str:
        async def _fetch():
            client = await _get_graph_client()
            if not client:
                return json.dumps({"error": "Microsoft 365 not connected"})
            messages = await client.get_channel_messages(
                team_id=team_id, channel_id=channel_id, limit=limit
            )

            # Filter by time if since_minutes is specified
            if since_minutes is not None and messages:
                cutoff = datetime.now(timezone.utc) - timedelta(minutes=since_minutes)
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


# ==================== TRANSCRIPT TOOLS ====================


class GetAllTranscriptsInput(BaseModel):
    """Input for getting all transcripts."""
    limit: int = Field(default=50, description="Maximum transcripts to return")


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
        # Harvest
        HarvestGetProjectsTool(),
        HarvestMyTimeTool(),
        HarvestRunningTimersTool(),
        HarvestTodayTrackingTool(),
        # Transcripts
        GetAllTranscriptsTool(),
        GetTranscriptByMeetingIdTool(),
        # Knowledge Base
        ReadKnowledgeTool(),
        WriteKnowledgeTool(),
        ListKnowledgeTool(),
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
        HarvestRunningTimersTool(),
        HarvestTodayTrackingTool(),
        HarvestMyTimeTool(),
        # Transcripts
        GetAllTranscriptsTool(),
        GetTranscriptByMeetingIdTool(),
    ]


def get_analysis_tools() -> list[BaseTool]:
    """Get tools for analysis."""
    return [
        ReadKnowledgeTool(),
        ListKnowledgeTool(),
        GetCalendarEventsTool(),
        GetEmailsTool(),
        GetTeamsChatsTool(),
        GetChatMessagesTool(),
        HarvestGetProjectsTool(),
    ]


def get_knowledge_tools() -> list[BaseTool]:
    """Get tools for knowledge base management."""
    return [
        ReadKnowledgeTool(),
        WriteKnowledgeTool(),
        ListKnowledgeTool(),
    ]
