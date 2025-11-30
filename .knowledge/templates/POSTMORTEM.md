# Incident Postmortem Template

> **Purpose**: Document incidents, root causes, and preventive measures
> **Use When**: After resolving any SEV1/SEV2 incident or significant outage

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Timeline](#timeline)
- [Impact Assessment](#impact-assessment)
- [Root Cause Analysis](#root-cause-analysis)
- [Detection & Response](#detection-response)
- [Action Items](#action-items)
- [Lessons Learned](#lessons-learned)
- [Appendix](#appendix)
- [Sign-off](#sign-off)
- [Instructions](#instructions)

## Template

```markdown
# Postmortem: [Incident Title]

> **Incident ID**: [INC-NNNN]
> **Date**: [YYYY-MM-DD]
> **Severity**: [SEV1 | SEV2 | SEV3]
> **Status**: [Draft | Review | Final]

---

## Executive Summary

**Duration**: [Start time] - [End time] ([X] hours [Y] minutes)

**Impact**:
- [X]% of users affected
- [Y] requests failed
- [Z] revenue impact (if applicable)

**Root Cause**: [One-sentence summary of root cause]

**Resolution**: [One-sentence summary of how it was fixed]

---

## Timeline

| Time (UTC) | Event |
|------------|-------|
| HH:MM | [First indicator of problem] |
| HH:MM | [Alert triggered] |
| HH:MM | [On-call engaged] |
| HH:MM | [Escalation to team lead] |
| HH:MM | [Root cause identified] |
| HH:MM | [Fix deployed] |
| HH:MM | [Service restored] |
| HH:MM | [All-clear declared] |

---

## Impact Assessment

### User Impact

| Metric | Value |
|--------|-------|
| Users affected | [Number or %] |
| Requests failed | [Number] |
| Error rate peak | [%] |
| Duration | [Time] |

### Business Impact

| Area | Impact |
|------|--------|
| Revenue | [$ amount or N/A] |
| SLA breach | [Yes/No, details] |
| Customer complaints | [Number] |
| Data loss | [Yes/No, details] |

### Systems Affected

- [System 1]
- [System 2]
- [Downstream dependency]

---

## Root Cause Analysis

### What Happened

[Detailed description of the technical failure]

### Why It Happened

**Direct Cause**:
[The immediate technical cause]

**Contributing Factors**:
1. [Factor 1: e.g., missing monitoring]
2. [Factor 2: e.g., inadequate testing]
3. [Factor 3: e.g., documentation gap]

### 5 Whys Analysis

1. **Why** did the service fail?
   → [Answer 1]

2. **Why** did [Answer 1] happen?
   → [Answer 2]

3. **Why** did [Answer 2] happen?
   → [Answer 3]

4. **Why** did [Answer 3] happen?
   → [Answer 4]

5. **Why** did [Answer 4] happen?
   → [Root cause]

---

## Detection & Response

### Detection

| Aspect | Assessment |
|--------|------------|
| How detected | [Alert / Customer report / Manual discovery] |
| Time to detect | [X minutes] |
| Detection gap | [What could have detected it earlier] |

### Response

| Aspect | Assessment |
|--------|------------|
| Time to respond | [X minutes] |
| Time to mitigate | [X minutes] |
| Time to resolve | [X hours] |
| Escalation path | [Who was involved] |

### What Went Well

- [Positive 1: e.g., fast escalation]
- [Positive 2: e.g., clear communication]
- [Positive 3: e.g., effective collaboration]

### What Could Be Improved

- [Improvement 1]
- [Improvement 2]
- [Improvement 3]

---

## Action Items

### Immediate (This Week)

| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| 1 | [Action item] | [Name] | [Date] | [ ] |
| 2 | [Action item] | [Name] | [Date] | [ ] |

### Short-term (This Month)

| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| 3 | [Action item] | [Name] | [Date] | [ ] |
| 4 | [Action item] | [Name] | [Date] | [ ] |

### Long-term (This Quarter)

| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| 5 | [Action item] | [Name] | [Date] | [ ] |
| 6 | [Action item] | [Name] | [Date] | [ ] |

---

## Lessons Learned

### Technical

- [Lesson 1]
- [Lesson 2]

### Process

- [Lesson 1]
- [Lesson 2]

### Communication

- [Lesson 1]
- [Lesson 2]

---

## Appendix

### Related Incidents

- [INC-XXXX]: [Brief description]
- [INC-YYYY]: [Brief description]

### Supporting Data

- [Link to dashboard during incident]
- [Link to relevant logs]
- [Link to Slack thread]

---

## Sign-off

| Role | Name | Date |
|------|------|------|
| Author | [Name] | [Date] |
| Reviewer | [Name] | [Date] |
| Approver | [Name] | [Date] |

---

*Postmortem from AI Collaboration Knowledge Base*
```
---

## Instructions

### 1. Postmortem Principles

| Principle      | Description                       |
|----------------|-----------------------------------|
| **Blameless**  | Focus on systems, not individuals |
| **Thorough**   | Document everything relevant      |
| **Actionable** | Every finding has an action item  |
| **Timely**     | Complete within 5 business days   |
| **Shared**     | Distribute learnings widely       |

### 2. When to Write

| Severity | Postmortem Required |
|----------|---------------------|
| SEV1     | Always              |
| SEV2     | Always              |
| SEV3     | If learning value   |
| SEV4     | Rarely              |

### 3. Timeline Best Practices

- Use UTC timestamps
- Be precise (HH:MM, not "around noon")
- Include all significant events
- Note communication points

### 4. Action Item Guidelines

| Quality  | Example                                                |
|----------|--------------------------------------------------------|
| **Good** | "Add alerting for database connection pool exhaustion" |
| **Bad**  | "Improve monitoring"                                   |
| **Good** | "Implement circuit breaker for payment service"        |
| **Bad**  | "Make service more reliable"                           |

### 5. Review Process

| Step                 | Timeline        |
|----------------------|-----------------|
| Draft                | Within 48 hours |
| Team review          | Within 72 hours |
| Final approval       | Within 5 days   |
| Action item tracking | Ongoing         |

---

## Related

- `.knowledge/templates/RUNBOOK.md` — Operational runbook template
- `.knowledge/practices/engineering/ERROR_HANDLING.md` — Error handling patterns
- `.knowledge/frameworks/resilience/TIMEOUT_PATTERNS.md` — Resilience patterns

---

*Template from AI Collaboration Knowledge Base*
---

*AI Collaboration Knowledge Base*
