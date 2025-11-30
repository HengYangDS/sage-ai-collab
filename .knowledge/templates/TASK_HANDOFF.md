# Task Handoff Template

> **Purpose**: Enable seamless task continuation between sessions or collaborators
> **Use When**: Ending a session with incomplete work, transferring tasks, or requesting async review

---

## Table of Contents

- [Overview](#overview)
- [Task Summary](#task-summary)
- [Context for Continuation](#context-for-continuation)
- [Technical Context](#technical-context)
- [Blockers & Risks](#blockers-risks)
- [Recommended Next Steps](#recommended-next-steps)
- [Resources & References](#resources-references)
- [Handoff Checklist](#handoff-checklist)
- [Notes for Recipient](#notes-for-recipient)
- [Instructions](#instructions)
- [Task Summary](#task-summary)
- [Context for Continuation](#context-for-continuation)
- [Recommended Next Steps](#recommended-next-steps)
- [Notes for Recipient](#notes-for-recipient)

## Overview

This template facilitates smooth task transitions between AI sessions or human collaborators. It captures everything
needed to continue work without context loss, ensuring efficient handoffs and maintaining task momentum.

---

## Template

```markdown
# Task Handoff: [TASK_NAME]

> **Handoff ID**: [YYYY-MM-DD]-[task]-handoff
> **From**: [Previous session/collaborator]
> **To**: [Next session/collaborator]
> **Created**: [YYYY-MM-DD HH:MM]
> **Priority**: [Critical/High/Medium/Low]

---

## Task Summary

### Original Objective

[What was the task trying to accomplish?]

### Current Status

| Aspect | Status |
|--------|--------|
| Overall Progress | [X]% complete |
| Blocking Issues | [Yes/No] |
| Tests Passing | [Yes/No/Partial/N/A] |
| Documentation | [Updated/Pending/N/A] |

### What's Done

- [x] [Completed item 1]
- [x] [Completed item 2]
- [x] [Completed item 3]

### What's Remaining

- [ ] [Remaining item 1]
- [ ] [Remaining item 2]
- [ ] [Remaining item 3]

---

## Context for Continuation

### Key Files

| File | Role | Current State |
|------|------|---------------|
| `[path/to/file1]` | [Purpose] | [State: Modified/Ready/Needs review] |
| `[path/to/file2]` | [Purpose] | [State: Modified/Ready/Needs review] |

### Important Decisions Already Made

| Decision | Rationale | Reference |
|----------|-----------|-----------|
| [Decision 1] | [Why] | [File/commit/doc] |
| [Decision 2] | [Why] | [File/commit/doc] |

### Decisions Pending

- [Decision needed 1]: [Options considered]
- [Decision needed 2]: [Options considered]

---

## Technical Context

### Architecture/Design Notes

[Key architectural considerations the next person should know]

### Code Patterns Used

```[language]
[Important code pattern or snippet to understand the approach]
```
### Dependencies

| Dependency | Version   | Notes                          |
|------------|-----------|--------------------------------|
| [Dep 1]    | [Version] | [Any issues or considerations] |

---

## Blockers & Risks

### Current Blockers

| Blocker     | Impact                   | Suggested Resolution |
|-------------|--------------------------|----------------------|
| [Blocker 1] | [How it blocks progress] | [Suggested approach] |

### Known Risks

| Risk     | Likelihood        | Mitigation      |
|----------|-------------------|-----------------|
| [Risk 1] | [High/Medium/Low] | [How to handle] |

---

## Recommended Next Steps

### Immediate Actions

1. **[Action 1]**: [Details and why this should be first]
2. **[Action 2]**: [Details]
3. **[Action 3]**: [Details]

### Verification Steps

- [ ] [How to verify the work so far]
- [ ] [How to test after completing remaining work]

---

## Resources & References

### Related Documents

- [Link to design doc]
- [Link to conversation record]
- [Link to session state]

### External References

- [Documentation links]
- [Issue tracker links]
- [Related PRs]

### Useful Commands

```bash
# [Description of command]
[command]

# [Description of command]
[command]
```
---

## Handoff Checklist

Before handoff, ensure:

- [ ] All changes committed (or stashed with note)
- [ ] Tests run and results documented
- [ ] Key decisions documented above
- [ ] Next steps are clear and actionable
- [ ] No uncommitted experimental code without notes

---

## Notes for Recipient

[Any additional context, warnings, or tips that don't fit above]

---

*Task handoff from AI Collaboration Knowledge Base*

```
---

## Instructions

1. **Naming**: Save as `YYYY-MM-DD-TASK-HANDOFF.md` (e.g., `2025-11-29-API-HANDOFF.md`)
2. **Location**: Store in `.history/handoffs/`
3. **Timing**: Create before ending a session with incomplete work
4. **Completeness**: Fill all relevant sections; mark N/A for non-applicable items

### When to Create

- Session ending with work in progress
- Passing task to different AI session
- Requesting human review or input
- Before extended breaks (days/weeks)
- When switching between related tasks

### Handoff Quality Checklist

A good handoff should enable the recipient to:

- [ ] Understand the task goal in <1 minute
- [ ] Know exactly where work stopped
- [ ] Find all relevant files immediately
- [ ] Understand key decisions without re-research
- [ ] Start productive work within 5 minutes

### After Handoff

- Archive to `.archive/` when task completes
- Reference in conversation records
- Update if circumstances change before pickup

---

## Example

```markdown
# Task Handoff: API Rate Limiting Implementation

> **Handoff ID**: 2025-11-29-rate-limit-handoff
> **From**: Morning session (Junie)
> **To**: Next session
> **Created**: 2025-11-29 12:30
> **Priority**: High

---

## Task Summary

### Original Objective

Implement rate limiting for the API service to prevent abuse and ensure fair usage.

### Current Status

| Aspect | Status |
|--------|--------|
| Overall Progress | 60% complete |
| Blocking Issues | No |
| Tests Passing | Partial (4/7) |
| Documentation | Pending |

### What's Done

- [x] Rate limiter core class with token bucket algorithm
- [x] Redis backend for distributed rate limiting
- [x] Configuration schema in `config/services/api.yaml`
- [x] Basic unit tests for core logic

### What's Remaining

- [ ] Integration with FastAPI middleware
- [ ] Remaining unit tests (edge cases)
- [ ] Integration tests
- [ ] API documentation update

---

## Context for Continuation

### Key Files

| File | Role | Current State |
|------|------|---------------|
| `src/app/services/rate_limiter.py` | Core implementation | Ready for review |
| `src/app/services/api.py` | Needs middleware integration | Pending changes |
| `tests/unit/services/test_rate_limiter.py` | Unit tests | 4/7 passing |

### Important Decisions Already Made

| Decision | Rationale | Reference |
|----------|-----------|-----------|
| Token bucket algorithm | Better burst handling than fixed window | `rate_limiter.py` L15-30 |
| Redis backend | Supports distributed deployment | `config/services/api.yaml` |

---

## Recommended Next Steps

### Immediate Actions

1. **Fix failing tests**: Check `test_concurrent_requests` - likely race condition in mock
2. **Add middleware**: Integrate `RateLimiter` into FastAPI app in `api.py`
3. **Add edge case tests**: Empty config, Redis connection failure

### Verification Steps

- [ ] Run `pytest tests/unit/services/test_rate_limiter.py -v`
- [ ] Start API and test with `curl` rapid requests
- [ ] Verify 429 responses include retry-after header

---

## Notes for Recipient

The Redis mock in tests occasionally fails due to timing. Consider using `freezegun` for time-dependent tests. See similar pattern in `test_timeout.py`.

---

*Task handoff from AI Collaboration Knowledge Base*
```
---

## Related

- `.history/INDEX.md` — Session history navigation
- `.knowledge/templates/CONVERSATION_RECORD.md` — Conversation record template
- `.knowledge/templates/SESSION_STATE.md` — Session state template

---

*Template from AI Collaboration Knowledge Base*
---

*AI Collaboration Knowledge Base*
