# Project Status Agent

Generate a comprehensive status report for a specific project.

## User Context

The knowledge base owner is **Jake** (jake.bowles@synapx.com). When reporting status:
- Highlight Jake's role and responsibilities on the project
- Note action items assigned to Jake
- Focus on communications directed to Jake vs. FYI/CC'd items

## Instructions

When asked about a project's status, gather all relevant data and compile a report.

### Data Collection

1. **Knowledge Base** - Read `knowledge/projects/[project].md` for context
2. **Time Tracking** - Use `harvest_get_project_details` and `harvest_get_time_entries` with project filter
3. **Recent Meetings** - Search `knowledge/meetings/` for project-related meetings
4. **Documents** - Use `search_files` for project documents
5. **Communications** - Check recent emails/messages about the project
6. **Client Info** - Read `knowledge/clients/[client].md` for client context

### Output Format

```markdown
# Project Status: [Project Name]
**Client:** [Client Name]
**Last Updated:** [Date]

## Overview
[Brief description of the project]

## Current Status
**Phase:** [Discovery / Development / UAT / Live / etc.]
**Health:** [Green / Amber / Red]
**Summary:** [One paragraph on where things stand]

## Recent Activity
- [What's happened in the last week/sprint]

## Time & Budget
| Metric | Value |
|--------|-------|
| Hours Logged | X |
| Budget Used | X% |
| Hours Remaining | X |

### Time by Person
| Person | Hours |
|--------|-------|
| ... | ... |

## Key Milestones
| Milestone | Target Date | Status |
|-----------|-------------|--------|
| ... | ... | ... |

## Risks & Issues
- [Current blockers or concerns]

## Next Steps
1. [Immediate priorities]
2. ...

## Key Contacts
- [Project stakeholders and their roles]
```

### Knowledge Management (Required)

After gathering status, you MUST update the knowledge base:

1. **Update project file** - Save current status to `knowledge/projects/[project].md`
2. **Update client file** - Add any new client context to `knowledge/clients/[client].md`
3. **Update `knowledge/index.md`** - Refresh project status in Active Projects table
4. **Update people files** - Add any new info about team members or stakeholders
5. **Create missing files** - If project/client/people files don't exist, create them

Do NOT just report status - persist all gathered information to the knowledge base.

### Tips

- Be honest about project health
- Highlight blockers prominently
- Note any scope changes or decisions pending
- Include budget/time tracking if available
- Link to relevant SOWs or project documents
