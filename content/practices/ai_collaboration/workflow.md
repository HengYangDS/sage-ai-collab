# AI Collaboration Workflow Practices

> **Load Time**: On-demand (~180 tokens)  
> **Purpose**: Practical workflows for effective human-AI collaboration

---

## Daily Workflow Pattern

### Session Start

```
1. Context Setting (2 min)
   - State current project/task
   - Mention relevant recent changes
   - Set autonomy level for session

2. Goal Definition (1 min)
   - Clear objective statement
   - Success criteria
   - Time constraints

3. Begin Work
   - AI confirms understanding
   - Work proceeds per autonomy level
```

### Example Session Start

```markdown
## Session Context

Project: AI Collaboration KB
Recent: Completed guidelines chapters 01-09
Autonomy: L3 (autonomous execution)

## Today's Goal

Create framework documents for 03_frameworks/

- autonomy/levels.md
- cognitive/expert_committee.md
- timeout/hierarchy.md

Success: All three files created with comprehensive content
Time: 2 hours
```

---

## Task Handoff Patterns

### Simple Handoff

```
Human: "Create a user registration endpoint"
AI: [Confirms understanding, executes, reports]
```

### Detailed Handoff

```markdown
## Task: User Registration Endpoint

### Requirements

- POST /api/users/register
- Accept: email, password, name
- Validate email format and password strength
- Return JWT token on success

### Constraints

- Use existing auth middleware
- Follow project API patterns
- Add tests

### Autonomy: L2 (checkpoints at design and before merge)
```

### Batch Handoff

```markdown
## Task Batch: Code Quality Improvements

### Tasks (L4 autonomy)

1. Add type hints to services/*.py
2. Fix all linting errors in models/
3. Update docstrings in api/

### Completion Criteria

- All files pass mypy --strict
- Zero linting errors
- 100% public method documentation
```

---

## Progress Reporting

### Checkpoint Report

```markdown
## Checkpoint: Feature Implementation

**Progress**: 3/5 steps complete
**Status**: On track

### Completed

- [x] Database schema designed
- [x] Models implemented
- [x] Repository layer done

### Current

- [ ] Service layer (70% complete)

### Remaining

- [ ] API endpoints

### Issues

None currently

### Questions

Should pagination use cursor or offset?
```

### Completion Report

```markdown
## Task Complete: User Registration

### Summary

Implemented user registration endpoint with full validation
and JWT token generation.

### Changes Made

- Created `api/routes/register.py`
- Added `services/registration.py`
- Updated `models/user.py` with validation
- Added 12 unit tests (100% pass)

### Testing

- Unit tests: 12/12 passing
- Integration tests: 3/3 passing
- Manual testing: Verified with Postman

### Notes

- Used bcrypt for password hashing
- JWT expiry set to 24 hours (configurable)

### Next Steps (if any)

- Consider rate limiting for registration endpoint
```

---

## Error Handling Workflow

### When AI Encounters Error

```
1. Stop execution
2. Document error clearly
3. Analyze root cause
4. Propose solutions
5. Wait for guidance (unless L4+)
```

### Error Report Format

```markdown
## Error Encountered

**Type**: Test Failure
**Severity**: Medium (blocking PR)
**Location**: tests/test_user_service.py::test_create_user

### Error Details
```

AssertionError: Expected User object, got None

```

### Analysis
The `create_user` method returns None when email 
validation fails silently instead of raising exception.

### Root Cause
Missing validation in UserService.create_user()

### Proposed Solutions
1. **Quick fix**: Add email validation before save
2. **Better**: Create ValidationError exception class
3. **Best**: Implement pydantic model validation

### Recommendation
Option 3 - aligns with project patterns

### Action Needed
- [ ] Approve solution
- [ ] Provide alternative
- [ ] Escalate
```

---

## Context Preservation

### Session Summary (End of Day)

```markdown
## Session Summary: 2024-01-15

### Accomplished

- Completed 02_guidelines/ (9 chapters)
- Created 03_frameworks/autonomy/levels.md
- Fixed 3 bugs in loader.py

### In Progress

- 03_frameworks/cognitive/ (50%)

### Pending

- 04_practices/ directory
- Test coverage improvement

### Key Decisions

- Merged decorator patterns into Python chapter
- Adopted 5-level timeout hierarchy

### Tomorrow

- Complete 03_frameworks/
- Start 04_practices/

### Notes

- Consider adding mermaid diagrams
- User requested English documentation
```

### Context for New Session

```markdown
## Previous Context

### Project State

- AI Collaboration KB, version 0.1.0
- 85% complete on documentation
- Core Python modules functional

### Recent Changes

- Created 9 guideline chapters
- Implemented TimeoutLoader
- Added MCP server support

### Current Branch

feature/complete-documentation

### Known Issues

- CLI help text needs updating
- Missing tests for plugins
```

---

## Collaboration Anti-Patterns

### What to Avoid

| Pattern          | Problem               | Better Approach       |
|------------------|-----------------------|-----------------------|
| Vague requests   | "Make it better"      | Specific criteria     |
| No context       | Starting from scratch | Provide background    |
| Micro-managing   | Approving every line  | Trust autonomy levels |
| Ignoring updates | Missed important info | Review checkpoints    |
| Scope creep      | Endless expansion     | Define boundaries     |

### Warning Signs

- Frequent misunderstandings
- Repeated clarification requests
- Unexpected changes
- Slow progress

### Recovery Actions

1. Pause and align on goals
2. Adjust autonomy level
3. Provide more context
4. Simplify scope

---

## Quick Reference

### Session Checklist

- [ ] Context provided
- [ ] Goals defined
- [ ] Autonomy set
- [ ] Constraints stated

### Handoff Checklist

- [ ] Requirements clear
- [ ] Success criteria defined
- [ ] Time expectations set
- [ ] Questions answered

### Review Checklist

- [ ] Results match goals
- [ ] Quality acceptable
- [ ] Tests included
- [ ] Documentation updated

---

*Part of AI Collaboration Knowledge Base v2.0.0*
