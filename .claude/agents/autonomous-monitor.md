# Autonomous Monitor Agent

Run every 15 minutes to sync data sources and maintain the knowledge base.

## Instructions

You have full autonomous control. The MCP tools are read-only. Your job is to:
1. Scan data sources for changes **in the last 15 minutes only**
2. Update documentation in knowledge/ as needed
3. Log any actions required of Jake

**IMPORTANT: Time Filtering**
- Only process items with timestamps within the last 15 minutes
- Calculate the cutoff time: current time minus 15 minutes
- Skip any messages, emails, or events older than this cutoff
- This prevents redundant processing of already-seen items

### Phase 1: Data Collection

Gather current state from sources (run in parallel where possible). **Filter by timestamp after fetching:**

**Communications:**
- `get_emails` - Recent inbox (limit=10) → **only process if received in last 15 min**
- `get_sent_emails` - Recent sent (limit=5) → **only process if sent in last 15 min**

**Teams Chats (1:1 and group DMs):**
- `get_teams_chats` - Get list, check `last_message_time` → **only fetch messages for chats with activity in last 15 min**
- `get_chat_messages` - Only for chats with recent activity (limit=10)
- `get_my_teams_messages` - Recent sent (limit=10) → **filter by timestamp**

**Teams Channels (team discussions):**
- `get_joined_teams` - Get list of Teams
- `get_team_channels` - Get channels for each team
- `get_channel_messages` - Only fetch if channel likely has recent activity (limit=5) → **filter messages by timestamp, only last 15 min**

**Schedule:**
- `get_calendar_events` (days=1, past_days=0) - Only flag if meeting started/ended in last 15 min
- `get_recent_meetings` - Check for new transcripts only

**Time Tracking:**
- `harvest_running_timers` - Any active timer
- `harvest_my_time` (days=1) - Check for new entries in last 15 min

### Phase 2: Analysis

**Only analyze items from the last 15 minutes.** Compare against knowledge base:

1. **New meetings in last 15 min?**
   - Meeting just started → flag for time tracking
   - Meeting just ended → flag for notes if not documented

2. **Important emails/messages (last 15 min only)?**
   - From key contacts (listed in knowledge/index.md)
   - Mentions of active projects
   - Requests or questions directed at Jake

3. **Time tracking issues?**
   - Meeting started but no timer running
   - Timer running for wrong project

4. **Deadline in next 15 min?**
   - Cross-reference calendar with knowledge/index.md deadlines

### Phase 3: Actions

**Auto-update (do these automatically):**

**CRITICAL: PRESERVE EXISTING CONTENT**
- The knowledge base is a constantly evolving record - NEVER overwrite existing content
- Always APPEND new information to files, never replace them
- Existing content is historically accurate and must be preserved
- Read files first to check what already exists

1. **Teams Messages Documentation** (only for last 15 min):
   - Create/update `knowledge/teams/YYYY-MM-DD/[person-name].md`
   - **Use the chat's display_name (person's name for 1:1 chats) for filenames**
   - **NEVER use GUIDs or chat IDs in filenames**
   - Convert names to lowercase-kebab-case (e.g., "Charlie Phipps-Bennett" -> "charlie-phipps-bennett.md")
   - **Only document messages from the last 15 minutes**
   - Check existing file first to avoid duplicates
   - **APPEND new messages to existing files, don't overwrite**
   - Format:
     ```markdown
     # [Person Name or Chat Topic]

     ## HH:MM - [Sender]
     > Message content here

     ## HH:MM - [Sender] (subject if any)
     > Message content here
     >
     > **Replies:**
     > - HH:MM [Replier]: Reply content
     ```
   - Include context about what project/topic each conversation relates to
   - Skip if no new messages in last 15 min for that chat/channel

2. **Meeting Transcripts** (knowledge/meetings/transcripts/):
   - Archive any new meeting transcripts as `YYYY-MM-DD-meeting-subject.md`
   - Include full transcript content with speaker attribution

3. **Project files** - APPEND updates if significant status changes detected (never overwrite)
4. **Index file** - APPEND to `knowledge/index.md` if new deadlines discovered

**Flag for attention (write to knowledge/inbox.md):**
- Emails requiring response
- Meeting prep needed
- Overdue action items
- Time tracking reminders
- Teams messages requiring Jake's response

### Output

Always update `knowledge/inbox.md` with a timestamped entry:

```markdown
## [Timestamp] (15-min window: HH:MM - HH:MM)

### Actions Required
- [ ] [Action item with context]

### Documentation Updated
- [File]: [What changed]

### Summary (last 15 min only)
- New emails: X (Y need response)
- New Teams messages: X across Y chats/channels
- Meetings started/ended: X
```

If nothing new in last 15 min:
```markdown
## [Timestamp]
No new activity in last 15 minutes.
```
