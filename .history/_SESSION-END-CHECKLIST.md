---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---
# Session End Checklist - SAGE Project

> Quick reference for SAGE session management

---

## Generic Checklist Reference

For the comprehensive session management checklist, see:

**→ `.knowledge/practices/ai_collaboration/SESSION_CHECKLIST.md`**

This includes:

- Session Start checklist
- During Session checklist
- Pre-Completion checks (work verification, quality, code review)
- Session End checklist (documentation, cleanup, handoff)
- Decision Guide (when to create which records)

---

## SAGE-Specific Additions

### Quality Checks (SAGE-specific)

- [ ] Code follows `.context/conventions/` patterns
- [ ] Timeout limits respected (T1:100ms → T5:10s)
- [ ] EventBus events properly published
- [ ] DI Container registrations correct

### Project Paths

| Record Type   | Location                    |
|---------------|-----------------------------|
| Conversation  | `.history/conversations/`   |
| Handoff       | `.history/handoffs/`        |
| Session State | `.history/current/`         |
| Temp Files    | `.outputs/` (delete on end) |

### SAGE Templates

| Template      | Location                                      |
|---------------|-----------------------------------------------|
| Conversation  | `.knowledge/templates/CONVERSATION_RECORD.md` |
| Handoff       | `.knowledge/templates/TASK_HANDOFF.md`        |
| Session State | `.knowledge/templates/SESSION_STATE.md`       |

---

## Quick Decision Guide

| Situation                        | Action                     |
|----------------------------------|----------------------------|
| Significant decisions made       | Create conversation record |
| Work incomplete, will continue   | Create handoff document    |
| Pausing mid-task                 | Create session state       |
| Routine completion, no decisions | No record needed           |
| Bug fix or minor change          | Commit message sufficient  |

---

## Related

- `.knowledge/practices/ai_collaboration/SESSION_CHECKLIST.md` — Generic checklist
- `.knowledge/practices/ai_collaboration/SESSION_MANAGEMENT.md` — Full session practices
- `.history/INDEX.md` — Session history navigation
- `.junie/GUIDELINES.md` — Project guidelines

---

*Part of SAGE Knowledge Base - Session Management*
