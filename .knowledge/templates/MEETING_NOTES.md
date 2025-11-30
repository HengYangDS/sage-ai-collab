# Meeting Notes Template

> **Purpose**: Template for documenting meetings and discussions
> **Use When**: Recording decisions, action items, and discussions from meetings

---

## Table of Contents

- [Overview](#overview)
- [Attendees](#attendees)
- [Agenda](#agenda)
- [Discussion Notes](#discussion-notes)
- [Decisions Made](#decisions-made)
- [Action Items](#action-items)
- [Parking Lot](#parking-lot)
- [Next Meeting](#next-meeting)
- [Attachments](#attachments)
- [Instructions](#instructions)
- [Attendees](#attendees)
- [Agenda](#agenda)
- [Discussion Notes](#discussion-notes)
- [Decisions Made](#decisions-made)
- [Action Items](#action-items)
- [Next Meeting](#next-meeting)
- [Meeting Types](#meeting-types)
- [Best Practices](#best-practices)

## Overview

This template helps create consistent meeting notes that capture key information, decisions, and action items for future
reference.

---

## Template

```markdown
# Meeting: [Meeting Title]

> **Date**: [YYYY-MM-DD]
> **Time**: [HH:MM] - [HH:MM] ([Timezone])
> **Location**: [Room/Virtual Link]
> **Type**: [Standup | Planning | Review | Decision | Brainstorm | 1:1]

---

## Attendees

### Present

- [Name] ([Role]) — Facilitator
- [Name] ([Role])
- [Name] ([Role])

### Absent

- [Name] ([Role]) — [Reason if known]

---

## Agenda

1. [Topic 1] — [Time allocation] — [Owner]
2. [Topic 2] — [Time allocation] — [Owner]
3. [Topic 3] — [Time allocation] — [Owner]
4. Open Discussion
5. Action Items Review

---

## Discussion Notes

### [Topic 1]

**Context**: [Brief background]

**Discussion**:

- [Key point discussed]
- [Key point discussed]
- [Different viewpoint raised]

**Outcome**: [Decision made or next steps]

### [Topic 2]

**Context**: [Brief background]

**Discussion**:

- [Key point discussed]
- [Key point discussed]

**Outcome**: [Decision made or next steps]

---

## Decisions Made

| # | Decision | Rationale | Owner |
|---|----------|-----------|-------|
| D1 | [Decision description] | [Why this was decided] | [Person] |
| D2 | [Decision description] | [Why this was decided] | [Person] |

---

## Action Items

| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| A1 | [Action description] | [Person] | [YYYY-MM-DD] | ⬜ Open |
| A2 | [Action description] | [Person] | [YYYY-MM-DD] | ⬜ Open |
| A3 | [Action description] | [Person] | [YYYY-MM-DD] | ⬜ Open |

### Carried Over from Previous

| # | Action | Owner | Original Due | New Due | Status |
|---|--------|-------|--------------|---------|--------|
| A0 | [Carried action] | [Person] | [Date] | [Date] | 🔄 In Progress |

---

## Parking Lot

Items to discuss later:

- [Topic for future discussion]
- [Topic for future discussion]

---

## Next Meeting

- **Date**: [YYYY-MM-DD]
- **Time**: [HH:MM] ([Timezone])
- **Proposed Agenda**:
    1. [Topic]
    2. Action Items Review

---

## Attachments

- [Link to presentation]
- [Link to document]
- [Link to diagram]

---

*Notes taken by [Name] on [Date]*
```
---

## Instructions

### 1. Header Information

- Use descriptive meeting title
- Include date, time with timezone
- Specify meeting type for context

### 2. Attendees

- List all attendees with roles
- Note the facilitator/lead
- Track absences for follow-up

### 3. Agenda

- List topics in order
- Include time allocations
- Assign topic owners

### 4. Discussion Notes

For each topic:

- **Context**: Why this topic matters
- **Discussion**: Key points raised
- **Outcome**: What was decided or next steps

### 5. Decisions

- Number decisions for reference
- Include rationale
- Assign ownership

### 6. Action Items

Use status indicators:

| Status      | Icon | Meaning              |
|-------------|------|----------------------|
| Open        | ⬜    | Not started          |
| In Progress | 🔄   | Being worked on      |
| Blocked     | 🚫   | Waiting on something |
| Complete    | ✅    | Done                 |

---

## Example

```markdown
# Meeting: Architecture Review

> **Date**: 2025-11-29
> **Time**: 14:00 - 15:30 (UTC+8)
> **Location**: Virtual - Teams
> **Type**: Review

---

## Attendees

### Present

- Alice Chen (Tech Lead) — Facilitator
- Bob Wang (Backend Dev)
- Carol Li (DevOps)

### Absent

- David Zhang (Frontend Dev) — On leave

---

## Agenda

1. Plugin System Design — 30 min — Alice
2. Timeout Hierarchy Review — 20 min — Bob
3. CI/CD Pipeline Updates — 20 min — Carol
4. Open Discussion — 15 min
5. Action Items Review — 5 min

---

## Discussion Notes

### Plugin System Design

**Context**: Need to finalize plugin architecture for v0.2.0

**Discussion**:

- Alice presented three options for plugin discovery
- Bob raised concerns about security sandboxing
- Carol suggested using entry points for external plugins

**Outcome**: Decided to use entry points + local directory scanning

### Timeout Hierarchy Review

**Context**: Current timeouts causing issues in production

**Discussion**:

- T3 timeout (2s) too short for large knowledge bases
- Suggested increasing to 3s with fallback mechanism

**Outcome**: Will increase T3 to 3s, add graceful degradation

---

## Decisions Made

| # | Decision | Rationale | Owner |
|---|----------|-----------|-------|
| D1 | Use entry points for plugins | Standard Python pattern, good ecosystem support | Alice |
| D2 | Increase T3 timeout to 3s | Production data shows 2s insufficient | Bob |

---

## Action Items

| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| A1 | Draft plugin system ADR | Alice | 2025-12-01 | ⬜ Open |
| A2 | Update timeout configuration | Bob | 2025-12-02 | ⬜ Open |
| A3 | Add plugin security checks to CI | Carol | 2025-12-05 | ⬜ Open |

---

## Next Meeting

- **Date**: 2025-12-06
- **Time**: 14:00 (UTC+8)
- **Proposed Agenda**:
    1. Plugin System ADR Review
    2. Timeout Changes Testing Results
    3. Action Items Review

---

*Notes taken by Alice Chen on 2025-11-29*
```
---

## Meeting Types

| Type              | Focus                     | Typical Duration |
|-------------------|---------------------------|------------------|
| **Standup**       | Daily sync, blockers      | 15 min           |
| **Planning**      | Sprint/iteration planning | 1-2 hours        |
| **Review**        | Design/code/architecture  | 1 hour           |
| **Decision**      | Make specific decisions   | 30-60 min        |
| **Brainstorm**    | Generate ideas            | 1 hour           |
| **1:1**           | Individual check-in       | 30 min           |
| **Retrospective** | Process improvement       | 1 hour           |

---

## Best Practices

1. **Prepare agenda** before meeting
2. **Start on time**, respect schedules
3. **Focus on outcomes**, not just discussion
4. **Assign owners** to all action items
5. **Share notes** within 24 hours
6. **Follow up** on action items

---

## Related

- `.knowledge/templates/CONVERSATION_RECORD.md` — AI collaboration records
- `.knowledge/templates/TASK_HANDOFF.md` — Task handoff documentation
- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Documentation standards

---

*Template from AI Collaboration Knowledge Base*
---

*AI Collaboration Knowledge Base*
