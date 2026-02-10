# Meeting Notes - February 10, 2026 (Monday)

## Summary

12 meetings today (4 canceled). Copilot insights available for: SOW Agent, Capital H&B Handover.

**Projects Discussed:**
- [SOW Agent Tool](#sow-agent-tool)
- [Capital Hair & Beauty Handover](#capital-hair--beauty-handover)
- [Midwich Daily Standup](#midwich-daily-standup)
- [LCP Document Extraction](#lcp-document-extraction)
- [Euroleague Basketball RFP](#euroleague-basketball-rfp)

---

## SOW Agent Tool

**Meeting:** SOW Agent (09:00-09:30)
**Organizer:** Prathap Reddy
**Attendees:** Jake Bowles, Prathap Reddy

### Key Insights

**Automated Statement of Work Generation:**
- Tool generates SOW document within 15-20 seconds
- Provides direct SharePoint share path upon completion
- Automatically populates cloud migration service and client representative fields
- Document intelligence summarizes uploaded documents and auto-fills fields

**Current Status:**
- Response time now meets expectations (15-20 seconds)
- Font formatting issues resolved - now produces correct font
- Architecture diagrams confirmed NOT required in SOW

**Areas Needing Work:**
- Background, scope, deliverables, out-of-scope items, and rate cut need to be "perfectly included"
- Prathap to update these sections

### Deployment Plan
- Updates to be completed today/tomorrow
- Deployment focus Thursday and Friday
- Deployment will be handled in Phone Report role and within Teams

### Actions
- [ ] **Prathap**: Update document to include background, scope, deliverables, out of scope, and rate cut
- [ ] **Prathap**: Notify Jake once updates are finished
- [ ] **Prathap**: Provide progress update today or tomorrow
- [ ] **Prathap**: Focus on deployment tasks Thursday/Friday

---

## Capital Hair & Beauty Handover

**Meeting:** Capital H&B Handover (09:30-10:00)
**Organizer:** Jake Bowles
**Attendees:** Jake Bowles, Nandan Hegde, Gagan M
**Related:** [Capital H&B Fabric](../projects/capital-hb-fabric.md) | [Capital H&B Client](../clients/capital-hb.md)

### Project Overview

**Client Background:**
- Major UK wholesaler of hair and beauty products
- Both wholesale and retail operations
- Annual turnover: ~£30 million
- Not data-driven; CEO Harry prefers printed Excel spreadsheets

**Key Stakeholders:**
- **Cristian**: Keen on moving to Fabric
- **Harry**: Founder/CEO - prefers traditional methods
- **Matt**: Participated in discovery phase

**Project Objective:** Deliver Power BI reports using Microsoft Fabric for historical and ongoing reporting

### Data Sources

| Source | Type | Integration Method | Status |
|--------|------|-------------------|--------|
| **iTrent** | HR & Payroll | API | Awaiting client documentation |
| **Business Central** | ERP (migrating from NAV) | Scheduled API loads | In progress |
| **NAV/SQL NAV** | Legacy ERP | One-time load | Planned |
| **OrderWise** | Sales Management | SQL Server via on-prem gateway | Ready |

### Resource Allocation

| Resource | Role | Delivery Model | Notes |
|----------|------|----------------|-------|
| **Saumya** | Backend data ingestion | Fixed price (~25 days) | First tasks: Fabric capacity, workspaces, metadata-driven framework |
| **Danya Kumar** | Power BI report development | TNM | Flexible for evolving requirements |
| **Nandan** | Code review (backend) | - | Also reviewing Fabric setup |
| **Gagan** | Project management | Fixed (3-4 days estimated) | First Fabric project - needs guidance |

### Technical Setup

**Environment Structure:**
- Two environments: Dev and Prod (despite client preference for single)
- Required for audit and pipeline requirements

**Service Accounts:**
- Three accounts created: Admin, Dev, Prod
- **BLOCKER**: Conditional access policies need removal before Azure subscription setup

**Technology Choices:**
- Azure Data Factory for Fabric capacity management (resume/pause)
- X Scale NOT part of implementation
- Reference: Glass Moon project for SQL-based ingestion approach

### Project Delivery

**Documentation:**
- BRD is primary reference for report requirements
- Data flow references should be interpreted as Fabric processes
- All client changes must be documented (frequent requirement changes expected)

**Meeting Cadence:**
- Starting with daily meetings during initial setup/data integration
- Will reassess and potentially switch to weekly after first week

**Tracking:**
- All work items in client's ADO tenant
- Gagan preparing Excel import if needed
- Charge codes to be split between fixed and TNM elements

### Actions
- [ ] **Nandan**: Obtain iTrent documentation from client (database access & extraction methods)
- [ ] **Nandan**: Coordinate with Matt to remove conditional access from service accounts
- [ ] **Andy**: Set up Azure subscription once conditional access resolved
- [ ] **Jake**: Clarify Power BI Pro licence availability for service accounts
- [ ] **Nandan**: Provide timeline breakdown for data ingestion activities
- [ ] **Jake**: Clarify charge code splitting with Charlotte
- [ ] **Nandan**: Confirm ADO environment (prod vs dev) for work items, inform Gagan
- [ ] **Nandan, Jake**: Provide Fabric guidance to Gagan throughout project

---

## Midwich Daily Standup

**Meeting:** Midwich Squad - Daily Standup (08:45-09:00)
**Organizer:** Yaz Qaraqesh
**Related:** [Midwich SOW008](../projects/midwich-app-development-sow008.md)

*No transcript available - transcription not enabled*

---

## LCP Document Extraction

**Meeting:** LCP Finance Doc Extraction Handover (09:30-10:20)
**Organizer:** Navsheen Koul
**Related:** [LCP Overview](../projects/lcp-overview.md)

*No transcript available - transcription not enabled*

**Note:** Standup - LCP Doc Extraction was canceled and replaced by this handover meeting.

---

## Euroleague Basketball RFP

**Meeting:** FW: Euroleague BB - RFP response checkpoint (11:00-11:15)
**Meeting:** Euroleague BB - RFP response checkpoint (14:00-14:30)
**Organizer:** Anand Karia
**Related:** [Euroleague RFP](../projects/euroleague-basketball-rfp.md)

*No transcript available yet - afternoon meeting may still be generating insights*

---

## Canceled Meetings
- Standup - LCP Doc Extraction (09:30-10:00) - Replaced by handover
- Product Catchup (10:30-10:55)
- Seras Fabric Discovery Weekly Catchup (10:30-11:00)

---

## Upcoming Today

| Time | Meeting | Notes |
|------|---------|-------|
| 15:30-16:00 | Interview - Azure SME (Rahul Mahajan) | Technical interview |
| 16:00-17:00 | Partner Voice Webcast | Microsoft - Data movement preview |

---

*Generated from calendar events and Copilot insights on February 10, 2026*
