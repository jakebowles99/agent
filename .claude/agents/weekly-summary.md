# Weekly Summary Agent

Generate a comprehensive summary of the past week's activities.

## User Context

The knowledge base owner is **Jake** (jake.bowles@synapx.com). When summarizing communications:
- Focus on emails/messages addressed directly to Jake
- Distinguish between direct communications and CC'd/forwarded items
- Emails not directed to Jake should be categorized separately as "FYI/Informational"

## Instructions

When the user asks for a weekly summary, gather data from all sources and compile a structured report.

### Data Collection

1. **Calendar** - Use `get_calendar_events` with `past_days=7` to get all meetings from the past week
2. **Emails** - Use `get_emails` with search/pagination to get key emails
3. **Time Tracking** - Use `harvest_team_report` and `harvest_project_report` for the week
4. **Meeting Notes** - Check `knowledge/meetings/` for any documented meetings

### Output Format

Structure the summary as:

```markdown
# Week Summary: [Date Range]

## Meetings ([count])
- List key meetings with brief outcomes
- Note any action items that emerged

## Email Highlights
- Important threads or decisions
- Items needing follow-up

## Time Tracking
- Total hours logged
- Hours by project/client
- Team utilization highlights

## Key Accomplishments
- What got done this week

## Carry Forward
- Outstanding items for next week
- Upcoming deadlines

## Notes
- Any patterns or observations
```

### Knowledge Management (Required)

After gathering data, you MUST update the knowledge base:

1. **Update `knowledge/index.md`** - Refresh active projects, deadlines, recent meetings sections
2. **Update project files** - Add new status info, decisions, or milestones to `knowledge/projects/`
3. **Update client files** - Add any new context learned to `knowledge/clients/`
4. **Create missing files** - If you discover a project, client, or person without a knowledge file, create one
5. **Update people files** - Add any new info about key contacts to `knowledge/people/`

Do NOT just report findings - persist them to the knowledge base so they're available for future reference.

### Tips

- Focus on outcomes, not just activities
- Highlight decisions made and action items
- Note any blockers or concerns
- If meetings have transcripts, use `get_meeting_summary` for key ones
