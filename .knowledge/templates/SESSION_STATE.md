# Session State Template

> **Purpose**: Capture current session context for continuity and recovery
> **Use When**: Starting complex tasks, before breaks, or when session may be interrupted

---

## Table of Contents

- [Overview](#overview)
- [Current Task](#current-task)
- [Progress](#progress)
- [Working Context](#working-context)
- [Blockers & Issues](#blockers-issues)
- [Quick Resume Guide](#quick-resume-guide)
- [Session Metadata](#session-metadata)
- [Instructions](#instructions)
- [Current Task](#current-task)
- [Progress](#progress)
- [Working Context](#working-context)
- [Quick Resume Guide](#quick-resume-guide)

## Overview

This template captures the current state of an AI collaboration session. It enables seamless continuation after
interruptions, provides context for session recovery, and helps maintain focus during complex multi-step tasks.

---

## Template

```markdown
# Session State: [TASK_NAME]

> **Session ID**: session-[YYYYMMDD]-[HHMM]
> **Started**: [YYYY-MM-DD HH:MM]
> **Last Updated**: [YYYY-MM-DD HH:MM]
> **Status**: [Active/Paused/Resuming]

---

## Current Task

### Objective

[What is the main goal of this session?]

### Scope

[What is included/excluded from this task?]

### Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

---

## Progress

### Completed Steps

1. [Step 1] ✓
2. [Step 2] ✓

### Current Step

**[Step N]**: [Brief description]

- Status: [In Progress/Blocked/Reviewing]
- Started: [HH:MM]
- Notes: [Any relevant observations]

### Remaining Steps

1. [Step N+1]
2. [Step N+2]

---

## Working Context

### Files Being Modified

| File | Purpose | Status |
|------|---------|--------|
| `[path/to/file1]` | [What's being done] | [Modified/Pending/Done] |
| `[path/to/file2]` | [What's being done] | [Modified/Pending/Done] |

### Key Decisions Made

- [Decision 1]: [Brief rationale]
- [Decision 2]: [Brief rationale]

### Dependencies

- [Dependency 1]: [Status]
- [Dependency 2]: [Status]

---

## Blockers & Issues

| Issue | Impact | Resolution |
|-------|--------|------------|
| [Issue 1] | [How it affects progress] | [Planned resolution] |

---

## Quick Resume Guide

### To Continue This Session

1. [First thing to do]
2. [Second thing to do]
3. [Where to pick up from]

### Key Context

- [Important context point 1]
- [Important context point 2]

### Commands/Code to Remember

```[language]
[Any important code snippets or commands]
```
---

## Session Metadata

- **Autonomy Level**: [L1-L6]
- **Related Issues**: [Links to issues/tickets]
- **Related Conversations**: [Links to conversation records]
- **Estimated Remaining**: [Time estimate]

---

*Session state from AI Collaboration Knowledge Base*

```
---

## Instructions

1. **Naming**: Save as `session-YYYYMMDD-HHMM.md` (e.g., `SESSION-20251129-2100.md`)
2. **Location**: Store in `.history/current/`
3. **Updates**: Update regularly during long sessions (every 30-60 min)
4. **Cleanup**: Move to `.archive/` or delete after session completion

### When to Create

- Starting a complex multi-step task
- Before taking a break during active work
- When session may be interrupted
- Beginning exploratory or research tasks

### When to Update

- Completing a significant step
- Making important decisions
- Encountering blockers
- Before any break or interruption

### When to Archive

- Task completed successfully
- Task handed off (create handoff document first)
- Session abandoned (note why in the document)

---

## Example

```markdown
# Session State: Implement Timeout Loader

> **Session ID**: session-20251129-1430
> **Started**: 2025-11-29 14:30
> **Last Updated**: 2025-11-29 16:45
> **Status**: Active

---

## Current Task

### Objective

Implement the TimeoutLoader base class with 5-tier timeout hierarchy.

### Scope

- Included: Base class, T1-T5 implementations, unit tests
- Excluded: Integration with existing loaders (separate task)

### Success Criteria

- [x] Base class with configurable timeouts
- [x] Fallback mechanisms for each tier
- [ ] Unit tests with >90% coverage
- [ ] Documentation updated

---

## Progress

### Completed Steps

1. Design timeout hierarchy ✓
2. Implement base TimeoutLoader class ✓
3. Add T1-T3 tier implementations ✓

### Current Step

**T4-T5 Implementation**: Adding complex operation timeout handling

- Status: In Progress
- Started: 16:30
- Notes: Need to handle partial content delivery

### Remaining Steps

1. Write unit tests
2. Update documentation
3. Code review

---

## Working Context

### Files Being Modified

| File | Purpose | Status |
|------|---------|--------|
| `src/app/core/loader.py` | Base TimeoutLoader | Done |
| `src/app/core/timeout.py` | Timeout utilities | Modified |
| `tests/unit/core/test_loader.py` | Unit tests | Pending |

### Key Decisions Made

- Use asyncio.timeout for Python 3.11+ compatibility
- Return partial content instead of raising on T3/T4

---

## Quick Resume Guide

### To Continue This Session

1. Open `src/app/core/timeout.py`
2. Continue implementing `handle_t4_timeout()` method
3. Reference T3 implementation for pattern

### Key Context

- Using asyncio patterns, not threading
- Partial content must include metadata about what's missing

---

*Session state from AI Collaboration Knowledge Base*
```
---

## Related

- `.history/INDEX.md` — Session history navigation
- `.knowledge/templates/CONVERSATION_RECORD.md` — Conversation record template
- `.knowledge/templates/TASK_HANDOFF.md` — Task handoff template

---

*Template from AI Collaboration Knowledge Base*
---

*AI Collaboration Knowledge Base*
