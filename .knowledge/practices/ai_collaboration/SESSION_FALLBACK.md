# Session Management Manual Fallback

> Manual procedures when automated session tools are unavailable

---

## Table of Contents

- [1. When to Use](#1-when-to-use)
- [2. Session Start Fallback](#2-session-start-fallback)
- [3. Session Checkpoint Fallback](#3-session-checkpoint-fallback)
- [4. Session End Fallback](#4-session-end-fallback)
- [5. Recovery Procedures](#5-recovery-procedures)

---

## 1. When to Use

| Scenario | Action |
|:---------|:-------|
| MCP tools unavailable | Use manual templates below |
| Tool timeout/error | Retry once, then fallback |
| Partial tool failure | Complete manually |
| New environment setup | Use until tools configured |

---

## 2. Session Start Fallback

### Manual Checklist

```markdown
## Session Start: [DATE TIME]

### Context Loaded
- [ ] Core principles reviewed
- [ ] Project config checked
- [ ] Recent changes noted

### Task Definition
- **Objective**: [What to accomplish]
- **Scope**: [Boundaries]
- **Constraints**: [Limitations]

### Environment
- Project: [name]
- Branch: [current branch]
- Key files: [list]
```
### Quick Start Command

```bash
# Gather context manually
git status
git log --oneline -5
ls -la .knowledge/
```
---

## 3. Session Checkpoint Fallback

### When to Checkpoint

| Trigger | Action |
|:--------|:-------|
| Every 5-10 exchanges | Quick summary |
| Before risky operation | Full state capture |
| Context growing large | Summarize and trim |

### Checkpoint Template

```markdown
## Checkpoint: [TIME]

### Progress
- Completed: [list]
- Current: [task]
- Remaining: [list]

### Key Decisions
- [Decision 1]: [rationale]

### Modified Files
- [file1]: [change summary]
```
---

## 4. Session End Fallback

### Handoff Template

```markdown
## Session Handoff: [DATE]

### Summary
[1-2 sentence overview]

### Completed
- [x] [Task 1]
- [x] [Task 2]

### Pending
- [ ] [Remaining task]

### For Next Session
1. [First priority]
2. [Second priority]

### Context Files
- `.history/sessions/[date].md`
```
---

## 5. Recovery Procedures

### Lost Context Recovery

1. Check `.history/` for recent sessions
2. Review git log for changes
3. Scan modified files for TODO/FIXME
4. Rebuild context incrementally

### Partial Failure Recovery

| Issue | Recovery |
|:------|:---------|
| Tool timeout | Retry with shorter scope |
| Data loss | Check git stash, recent commits |
| State corruption | Reset to last checkpoint |

---

## Related

- `.knowledge/templates/SESSION_STATE.md` — Session state template
- `.knowledge/templates/TASK_HANDOFF.md` — Task handoff template
- `.knowledge/practices/ai_collaboration/SESSION_MANAGEMENT.md` — Full session guide

---

*AI Collaboration Knowledge Base*
