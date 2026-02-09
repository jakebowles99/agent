# Meeting Notes - February 9, 2026 (Monday)

## Summary

12 meetings today (2 canceled). Transcripts available for: Product Catchup, LCP Doc Extraction Standup.

**Projects Discussed:**
- [Midwich App Development](#midwich-app-development)
- [LCP Document Extraction](#lcp-document-extraction)
- [AI Readiness Score (Internal Product)](#ai-readiness-score)
- [Jensten Group](#jensten-group)
- [Euroleague Basketball RFP](#euroleague-basketball-rfp)
- [Capital Hair & Beauty](#capital-hair--beauty)
- [Synapx Internal Projects](#synapx-internal-projects)
- [Data & AI Marketing Use Cases](#data--ai-marketing-use-cases)

---

## Midwich App Development

**Meeting:** Midwich Squad - Daily Standup (08:45-09:00)
**Organizer:** Yaz Qaraqesh
**Related:** [Midwich SOW008](../projects/midwich-app-development-sow008.md)

### Status
- App discovered to be pointing to **UAT environment** using an **old database**
- Timon Wan investigating connection references
- Confirmed: `db-orders-1` is the UAT database (per Nandan Hegde)

### Actions
- [ ] **Vaishnavi MP**: Rename display name of env var `synapx_ev_OrderManagementPOsqlDatabase` to `ev_OrderManagementPOsqlDatabase`
- [ ] **Hemanth/Vaishnavi**: Confirm correct database configuration tomorrow
- [ ] **Timon**: Working with Umar directly on the issue

### Notes
- Umar experiencing errors when opening the app
- Connection references need verification between DEV/UAT/Prod

---

## LCP Document Extraction

**Meeting:** Standup - LCP Doc Extraction (11:00-11:15)
**Organizer:** Navsheen Koul
**Related:** [LCP Overview](../projects/lcp-overview.md) | [LCP Client](../clients/lcp.md)

### Transcript Highlights
- Ajay demoing Outlook plugin setup process for testing
- Plugin installation walkthrough: Add custom add-in from file
- Manifest file issue encountered during demo - needs debugging
- Similar to Nimans and Midwich Outlook plugin testing process

### Resource Change
- **Vijay G** handing over to **Katyayani Lal** - Vijay required on Midwich
- Jake and Charlie tagged for awareness
- Katyayani requesting plugin access and received field descriptions file (`Fields_With_Categories_LCP.xlsx`)

### Technical Status
- **Extraction**: Ajay tested 8 different analysers, not getting expected outcomes
- **Email PDFs**: Priority focus - Navsheen says OCs illogical to pursue until email extraction works
- **Website/Plugin**: No bugs except extraction issue

### Actions
- [ ] **Ajay**: Debug manifest file issue
- [ ] **Ajay**: Continue testing email PDF extraction with different analysers
- [ ] **Ajay**: Provide Katyayani with plugin access credentials
- [ ] **Katyayani**: Complete handover from Vijay

---

## AI Readiness Score

**Meeting:** Product Catchup (10:30-10:55)
**Organizer:** Navsheen Koul
**Attendees:** Jake Bowles, Rahul Matta

### Transcript Highlights

**Claude Code / AI Tooling Walkthrough:**
- Jake demonstrated Claude Code capabilities - creating React apps automatically
- Showed SSH key setup in Coda for cloning repos from terminal
- Recommendation: Use VS Code, Replet, and Claude Code as primary tools
- Warning: Azure VMs cost money - remember to delete when not using

**AI Readiness Score Task (Rahul):**
- Rahul asked about LLM integration for processing user questionnaire answers
- Question: Use OpenAI or Microsoft Azure Agent AI?
- Jake's guidance: LLM will be needed; specifics TBD based on requirements

### Claim Review Workflow (LCP Product)
From meeting chat - Navsheen clarifying workflow states to Rahul:
- `Needs Review` - claim awaiting analyst attention
- `In Review` (NEW) - claim being actively worked (prevents duplicate work)
- `Approved` / `Rejected` - final states

### Actions
- [ ] **Rahul**: Explore AI/LLM integration options for AI Readiness Score
- [ ] **Rahul**: Add "In Review" status to claim workflow

---

## Jensten Group

**Meetings:**
- Jensten Proposal (11:00-11:30) - Organizer: Sophia Fricker
- Jensten Check In (16:30-17:00) - Organizer: Sophia Fricker
- Jensten (17:45-18:00) - Organizer: Jake Bowles

**Related:** [Jensten Overview](../projects/jensten-overview.md) | [Jensten Client](../clients/jensten.md)

### Context
- Multiple SOWs in progress (SOW008-SOW013)
- Proposal deck deadline: Monday Feb 10 (tomorrow)
- Total estimated value: ~£450k+ (Fabric Discovery + Underwriting Reporting)

### Key Stakeholders
- **Dave**: SOW approvals
- **Graeme**: Senior stakeholder, BPO interest
- **Luke**: IT Lead

### Pending Actions
- [ ] Finalize proposal deck for Graeme by Monday
- [ ] All SOWs to Dave for review
- [ ] Record walkthrough of work/deliverables

---

## Euroleague Basketball RFP

**Meetings:**
- Euroleague BB - RFP Response Checkpoint (12:00-12:15) - Organizer: Anand Karia
- Euroleague Estimate Refinement (15:00-16:30) - Organizer: Anand Karia

**Related:** [Euroleague RFP](../projects/euroleague-basketball-rfp.md) | [Euroleague Client](../clients/euroleague-basketball.md)

### Deadline
- **Extended Deadline**: February 11, 2026 23:59 CET
- **Estimates Due**: Monday Feb 10

### RFP Scope (5 Key Areas)
1. Registration Portal
2. Competition Engine
3. Data Integration
4. Real-time APIs
5. Live Stats

### Team
- Charlie (Lead) - final say on estimates
- Jake - Technical architecture, estimates
- Anand - Development estimates, workflow analysis
- Tarun - Backend estimates
- Divya - UI/Figma designs

### Actions
- [ ] **Jake/Tarun**: Submit estimates by Monday (in days, min 0.25)
- [ ] **Anand**: Compile final response Monday afternoon
- [ ] **Charlie**: Review and bump estimates as needed

---

## Capital Hair & Beauty

**Meeting:** Capital H&B <> Synapx (14:30-15:00)
**Organizer:** Jake Bowles
**Related:** [Capital H&B Fabric](../projects/capital-hb-fabric.md) | [Capital H&B Client](../clients/capital-hb.md)

### Contract Status
- **SOW002 Signed**: February 6, 2026
- **Fixed Fee**: £21,700 + VAT
- **Kickoff**: Monday 2:30 PM (Feb 10)

### Technical Scope
- Microsoft Fabric + Power BI implementation
- Replace Phocus reporting system
- Data sources: Business Central (API), Nav (one-time), Orderwise (SQL), iTrent (API)
- F4 SKU with POC Funded Subscription ($1200)

### Discussion Topics
- Report governance and organization strategy
- Managing growing number of reports
- Establishing logical library structure early

### Actions
- [ ] Prepare report governance discussion for Monday kickoff
- [ ] Submit POC Funded Subscription request to Microsoft
- [ ] Set up Dev/Prod environments
- [ ] Begin iTrent API discovery

---

## Synapx Internal Projects

**Meeting:** Synapx Internal Projects - Weekly Status Update (13:00-14:00)
**Organizer:** Tushara Udata

### Notes
- Discussion about assigning work to Nikhil once onboarded (per Akshansh Sharma)

---

## Data & AI Marketing Use Cases

**Meeting:** Data & AI Use Cases for Marketing (09:30-09:45)
**Organizer:** Sophia Fricker

*No transcript available*

---

## Canceled Meetings
- Pipeline & Progress Weekly Review (12:00-12:30) - Canceled
- Nimans Internal Sync (17:30-17:45) - Canceled

---

## Project Sign-Offs

**Meeting:** Jake & Nandan - Weekly Project Sign Off and Resource Forecast Updates (13:00-13:30)
**Organizer:** Charlotte Price

*No transcript available - Administrative meeting for project/resource management*

---

*Generated from calendar events and available transcripts on February 9, 2026*
