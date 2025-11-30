# Session Checklist

> Quick reference checklist for AI collaboration session management

---

## Table of Contents

- [1. Session Start](#1-session-start)
- [2. During Session](#2-during-session)
- [3. Pre-Completion](#3-pre-completion)
- [4. Session End](#4-session-end)
- [5. Decision Guide](#5-decision-guide)

---

## 1. Session Start

### 1.1 Context Loading

- [ ] Review project guidelines (`.junie/GUIDELINES.md` or equivalent)
- [ ] Check for active sessions (`.history/current/`)
- [ ] Review recent commits for context continuity
- [ ] Identify task scope and success criteria
- [ ] Establish autonomy level for the session

### 1.2 Environment Check

- [ ] Confirm working directory
- [ ] Verify access to required files
- [ ] Note any dependencies or blockers

---

## 2. During Session

### 2.1 Progress Tracking

- [ ] Update task status as work progresses
- [ ] Document decisions with rationale
- [ ] Note any blockers or issues encountered
- [ ] Commit changes at logical checkpoints

### 2.2 State Preservation

- [ ] Save session state before breaks
- [ ] Document current position for easy resume
- [ ] Note open files and active context

---

## 3. Pre-Completion

### 3.1 Work Verification

- [ ] All planned tasks completed or documented as pending
- [ ] Code changes tested (if applicable)
- [ ] No broken functionality introduced
- [ ] Documentation updated for changed features

### 3.2 Quality Checks

- [ ] Code follows project conventions
- [ ] No temporary debug code left in place
- [ ] Error handling implemented appropriately
- [ ] Performance constraints respected (timeouts, limits)

### 3.3 Code Review Points

- [ ] Variable/function names are clear
- [ ] Comments explain "why", not "what"
- [ ] No hardcoded values that should be configurable
- [ ] Edge cases handled

---

## 4. Session End

### 4.1 Documentation

| Record Type   | When to Create                         | Location                  |
|---------------|----------------------------------------|---------------------------|
| Conversation  | Important decisions, notable learnings | `.history/conversations/` |
| Handoff       | Work incomplete, will continue         | `.history/handoffs/`      |
| Session State | Pausing mid-task                       | `.history/current/`       |

### 4.2 Cleanup Actions

- [ ] Move completed session files from `.history/current/`
- [ ] Archive old records per retention policy
- [ ] Delete temporary working files from output directories
- [ ] Commit changes if significant milestone reached

### 4.3 Handoff Preparation

- [ ] Summarize completed work
- [ ] Document pending items clearly
- [ ] Provide context for continuation
- [ ] List recommended next steps

---

## 5. Decision Guide

### 5.1 When to Create Records

| Situation                        | Action                     |
|----------------------------------|----------------------------|
| Significant decisions made       | Create conversation record |
| Work incomplete, will continue   | Create handoff document    |
| Pausing mid-task                 | Create session state       |
| Routine completion, no decisions | No record needed           |
| Bug fix or minor change          | Commit message sufficient  |

### 5.2 Record Depth Guide

| Session Type | Duration    | Documentation Level     |
|--------------|-------------|-------------------------|
| Quick        | < 30 min    | Commit message only     |
| Standard     | 30min - 2hr | Session state if paused |
| Extended     | > 2 hr      | Full documentation      |
| Multi-day    | Days+       | Handoff required        |

### 5.3 Autonomy Level Reminders

| Level | Before Acting                       |
|-------|-------------------------------------|
| L1-L2 | Ask for approval                    |
| L3-L4 | Proceed, report after (default)     |
| L5-L6 | Act independently, summarize at end |

---

## Quick Reference Card

```
SESSION START
  □ Load context  □ Check active sessions  □ Set scope

DURING WORK
  □ Track progress  □ Document decisions  □ Commit often

BEFORE END
  □ Verify work  □ Quality check  □ Update docs

SESSION END
  □ Create records  □ Cleanup  □ Prepare handoff
```
---

## Related

- `.knowledge/practices/ai_collaboration/SESSION_MANAGEMENT.md` — Full session management practices
- `.knowledge/practices/ai_collaboration/CONTEXT_MANAGEMENT.md` — Context preservation strategies
- `.knowledge/templates/CONVERSATION_RECORD.md` — Conversation template
- `.knowledge/templates/TASK_HANDOFF.md` — Handoff template
- `.knowledge/templates/SESSION_STATE.md` — Session state template

---

*AI Collaboration Knowledge Base*
