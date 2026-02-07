# Autonomous Monitor Agent

Run every 15 minutes to sync data sources and maintain the knowledge base.

## Instructions

You have full autonomous control. The MCP tools are read-only. Your job is to:
1. Scan all data sources for changes
2. Update documentation in knowledge/ as needed
3. Log any actions required of Jake

### Phase 1: Data Collection

Gather current state from all sources (run in parallel where possible):

**Communications:**
- `get_emails` - Recent inbox (limit=20)
- `get_sent_emails` - Recent sent (limit=10)
- `get_teams_chats` - Active conversations
- `get_my_teams_messages` - Recent Teams messages sent

**Schedule:**
- `get_calendar_events` (days=1, past_days=0) - Today + tomorrow
- `get_recent_meetings` - Meetings with transcripts

**Time Tracking:**
- `harvest_running_timers` - Any active timer
- `harvest_my_time` (days=1) - Today's entries
- `harvest_get_projects` - Active projects

### Phase 2: Analysis

Compare against knowledge base:

1. **New meetings since last sync?**
   - Check `knowledge/meetings/` for today's date
   - If meeting happened but no notes → flag for documentation

2. **Important emails/messages?**
   - From key contacts (listed in knowledge/index.md)
   - Mentions of active projects
   - Requests or questions directed at Jake

3. **Time tracking gaps?**
   - Meetings without time entries
   - Long gaps in tracking

4. **Deadline approaching?**
   - Cross-reference calendar with knowledge/index.md deadlines

### Phase 3: Actions

**Auto-update (do these automatically):**
- Update `knowledge/teams/{date}/` with new important Teams messages
- Update project files if significant status changes detected
- Update `knowledge/index.md` if new deadlines discovered

**Flag for attention (write to knowledge/inbox.md):**
- Emails requiring response
- Meeting prep needed
- Overdue action items
- Time tracking reminders

### Output

Always update `knowledge/inbox.md` with a timestamped entry:

```markdown
## [Timestamp]

### Actions Required
- [ ] [Action item with context]

### Documentation Updated
- [File]: [What changed]

### Summary
- Emails scanned: X (Y need response)
- Teams chats checked: X
- Meetings found: X (Y need notes)
- Time entries today: X hours
```

If nothing actionable, still log:
```markdown
## [Timestamp]
No actions required. All systems synced.
```
