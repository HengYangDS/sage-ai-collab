# Conversation Record Template

> **Purpose**: Document AI collaboration sessions with key decisions and learnings
> **Use When**: Recording significant conversations, design discussions, or problem-solving sessions

---

## Table of Contents

- [Overview](#overview)
- [Context](#context)
- [Key Discussion Points](#key-discussion-points)
- [Decisions Made](#decisions-made)
- [Action Items](#action-items)
- [Learnings & Insights](#learnings-insights)
- [References](#references)
- [Follow-up](#follow-up)
- [Instructions](#instructions)
- [Context](#context)
- [Key Discussion Points](#key-discussion-points)
- [Decisions Made](#decisions-made)
- [Action Items](#action-items)
- [Learnings & Insights](#learnings-insights)

## Overview

This template helps capture the essential information from AI-human collaboration sessions. Use it to document important
conversations that contain decisions, insights, or learnings worth preserving for future reference.

---

## Template

```markdown
# [TOPIC]: [Brief Description]

> **Date**: [YYYY-MM-DD]
> **Participants**: [Human/AI roles involved]
> **Duration**: [Approximate session length]
> **Status**: [Completed/In Progress/Paused]

---

## Context

[What prompted this conversation? What problem or topic was being addressed?]

---

## Key Discussion Points

### [Topic 1]

[Summary of discussion]

### [Topic 2]

[Summary of discussion]

---

## Decisions Made

| Decision | Rationale | Impact |
|----------|-----------|--------|
| [Decision 1] | [Why this choice] | [What it affects] |
| [Decision 2] | [Why this choice] | [What it affects] |

---

## Action Items

- [ ] [Action 1] — [Owner] — [Due date if applicable]
- [ ] [Action 2] — [Owner] — [Due date if applicable]

---

## Learnings & Insights

### What Worked Well

- [Insight 1]
- [Insight 2]

### Challenges Encountered

- [Challenge 1]
- [Challenge 2]

### Future Considerations

- [Consideration 1]
- [Consideration 2]

---

## References

- [Related documents, code files, or external resources]

---

## Follow-up

- **Next Session**: [Planned follow-up if any]
- **Related Handoff**: [Link to handoff document if applicable]

---

*Conversation record from AI Collaboration Knowledge Base*
```
---

## Instructions

1. **Naming**: Save as `YYYY-MM-DD-TOPIC.md` (e.g., `2025-11-29-TIMEOUT-DESIGN.md`)
2. **Location**: Store in `.history/conversations/`
3. **Timing**: Create during or immediately after significant sessions
4. **Focus**: Capture decisions and learnings, not verbatim transcripts
5. **Links**: Reference related code, docs, or handoffs

### What to Include

- Significant design decisions
- Problem-solving approaches that worked
- Insights about the codebase or architecture
- Lessons learned from debugging sessions
- Cross-cutting concerns discovered

### What to Omit

- Routine queries with obvious answers
- Minor formatting or typo fixes
- Information already documented elsewhere

---

## Example

```markdown
# Timeout Architecture: Multi-tier Design Discussion

> **Date**: 2025-11-29
> **Participants**: Developer, Junie AI
> **Duration**: ~45 minutes
> **Status**: Completed

---

## Context

Designing the timeout hierarchy for MyProject to ensure responsive AI interactions while handling varying
content load times.

---

## Key Discussion Points

### Timeout Tier Structure

Discussed 5-tier approach from T1 (100ms cache) to T5 (10s complex analysis). Evaluated tradeoffs between responsiveness
and completeness.

### Fallback Strategies

Explored graceful degradation patterns when timeouts occur. Decided on partial content delivery over complete failure.

---

## Decisions Made

| Decision | Rationale | Impact |
|----------|-----------|--------|
| 5-tier timeout hierarchy | Balances speed vs completeness | Core architecture pattern |
| Partial content on T3/T4 timeout | Better UX than failure | Affects all loaders |

---

## Action Items

- [x] Document timeout hierarchy in `.context/policies/`
- [x] Implement TimeoutLoader base class
- [ ] Add timeout metrics to monitoring

---

## Learnings & Insights

### What Worked Well

- Breaking down by operation type clarified requirements
- Example scenarios helped validate tier boundaries

### Future Considerations

- May need T6 for batch operations
- Consider adaptive timeouts based on content size

---

*Conversation record from AI Collaboration Knowledge Base*
```
---

## Related

- `.history/INDEX.md` — Session history navigation
- `.knowledge/templates/TASK_HANDOFF.md` — Task handoff template
- `.knowledge/templates/SESSION_STATE.md` — Session state template

---

*Template from AI Collaboration Knowledge Base*
---

*AI Collaboration Knowledge Base*
