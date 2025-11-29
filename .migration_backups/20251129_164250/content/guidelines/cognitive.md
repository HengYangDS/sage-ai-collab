# Cognitive Enhancement Guidelines

> **Load Time**: On-demand (~300 tokens)  
> **Purpose**: Enhanced metacognitive capabilities for AI collaboration  
> **Principle**: Make AI thinking visible, iterative, and collaborative

---

## Overview

This chapter covers 9 cognitive dimensions for enhanced AI collaboration:

1. [Chain-of-Thought Reasoning](#71-chain-of-thought-reasoning)
2. [Iterative Feedback Loop](#72-iterative-feedback-loop)
3. [Multi-Perspective Critique](#73-multi-perspective-critique)
4. [Critical Thinking Habits](#74-critical-thinking-habits)
5. [External Systems Mastery](#75-external-systems-mastery)
6. [Long-Term Memory](#76-long-term-memory)
7. [Multi-Agent Collaboration](#77-multi-agent-collaboration)
8. [Task Decomposition](#78-task-decomposition)
9. [Learning & Adaptation](#79-learning--adaptation)

**Complete Framework**: See [Cognitive Enhancement Framework](../03_frameworks/cognitive/expert_committee.md) for full
details.

---

## 7.1 Chain-of-Thought Reasoning

**Principle**: Show reasoning process, not just final answer.

### When to Use

- Architecture decisions
- Breaking changes
- Trade-off decisions
- Novel problems without precedent

### Structure

```markdown
## Problem Analysis

- What: [Problem description]
- Why: [Root cause]
- Impact: [Consequences if unaddressed]

## Approach Exploration

| Option | Pros | Cons | Risk |
|--------|------|------|------|
| A | ... | ... | Low |
| B | ... | ... | Medium |
| C | ... | ... | High |

## Decision Rationale

- Selected: [Option]
- Why: [Reasoning]
- Trade-offs: [What we're accepting]
- Risks: [Mitigation plan]

## Implementation Steps

1. Step 1 → Expected outcome
2. Step 2 → Validation criteria
3. Step 3 → Success metrics
```

### Integration with Autonomy

| Level | Chain-of-Thought Display     |
|-------|------------------------------|
| L2-L3 | Show all reasoning           |
| L4    | Show key decisions only      |
| L5-L6 | Show only for novel problems |

---

## 7.2 Iterative Feedback Loop

**Principle**: Think → Decide → Observe → Iterate

### Cycle Structure

```
┌─────────────────────────────────────┐
│ 1. THINK                            │
│    └─ Analyze situation, options    │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 2. DECIDE                           │
│    └─ Choose approach, commit       │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 3. ACT                              │
│    └─ Implement, execute            │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 4. OBSERVE                          │
│    └─ Measure results, gather data  │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 5. LEARN                            │
│    └─ Extract insights, adjust      │
└─────────────────┬───────────────────┘
                  ▼
            [Next Cycle]
```

### Documentation Template

```markdown
## Iteration [N]

### Thinking

[Analysis and reasoning]

### Decision

[What was decided and why]

### Action

[What was implemented]

### Observation

[Results and measurements]

### Learning

[Insights for next iteration]
```

### Integration with Autonomy

| Level | Iteration Reporting       |
|-------|---------------------------|
| L2-L3 | Report each cycle         |
| L4    | Report milestones         |
| L5-L6 | Report completion summary |

---

## 7.3 Multi-Perspective Critique

**Principle**: Evaluate from multiple quality angles.

### Core 10 Quality Angles

#### Functional Quality (4)

| Angle             | Definition                | Key Questions                         |
|-------------------|---------------------------|---------------------------------------|
| **Correctness**   | Solves problem accurately | Edge cases handled? Production-ready? |
| **Completeness**  | All requirements met      | Docs complete? Tests sufficient?      |
| **Safety**        | Secure and protected      | Input validated? Vulnerabilities?     |
| **Effectiveness** | Delivers business value   | Goal achieved? User problem solved?   |

#### Architectural Quality (3)

| Angle           | Definition          | Key Questions                         |
|-----------------|---------------------|---------------------------------------|
| **Clarity**     | Understandable code | Readable? Well-named? Maintainable?   |
| **Efficiency**  | Good performance    | Fast enough? Resources reasonable?    |
| **Reliability** | Stable operation    | Fault-tolerant? Graceful degradation? |

#### Evolutionary Quality (3)

| Angle             | Definition      | Key Questions                          |
|-------------------|-----------------|----------------------------------------|
| **Testability**   | Easy to test    | Mockable? Isolated? Coverage possible? |
| **Observability** | Easy to monitor | Logging? Metrics? Debuggable?          |
| **Adaptability**  | Easy to change  | Extensible? Configurable? Migratable?  |

### Extended Angles (15+)

Activate for specific scenarios:

- **User Experience**: Usability, Accessibility, Responsiveness, Aesthetics
- **Technical Depth**: Scalability, Performance, Portability, Interoperability, Resilience
- **Maintenance**: Maintainability, Reproducibility, Upgradability
- **Compliance**: Auditability, Compliance, Privacy

### Quick Critique Template

```markdown
## Quality Critique: [Feature/Component]

### Core Angles Assessment

| Angle | Status | Notes |
|-------|--------|-------|
| Correctness | ✅/⚠️/❌ | ... |
| Completeness | ✅/⚠️/❌ | ... |
| Safety | ✅/⚠️/❌ | ... |
| ... | ... | ... |

### Issues Found

1. [Issue] - Priority: P0/P1/P2/P3

### Recommendations

1. [Action] - Effort: Low/Medium/High
```

---

## 7.4 Critical Thinking Habits

**Principle**: Continuous questioning before delivering.

### The 5 Critical Questions

| # | Question                                  | Purpose                    | Action              |
|---|-------------------------------------------|----------------------------|---------------------|
| 1 | **What am I assuming?**                   | Surface hidden assumptions | Challenge, validate |
| 2 | **What could go wrong?**                  | Identify failure modes     | Plan mitigation     |
| 3 | **Is there a simpler way?**               | Avoid over-engineering     | Apply KISS          |
| 4 | **What will future maintainers need?**    | Ensure sustainability      | Document decisions  |
| 5 | **How does this fit the bigger picture?** | System coherence           | Align with 信达雅      |

### Application Example

```
Task: Add caching to user API

Q1: Assuming cache invalidation is straightforward
    → Reality: Complex with related entities
    → Action: Design proper invalidation strategy

Q2: Could go wrong: stale data, memory exhaustion, race conditions
    → Action: Add TTL, memory limits, locking

Q3: Simpler way: HTTP caching headers vs custom cache
    → Action: Start with HTTP caching first

Q4: Future maintainers need: clear cache strategy docs
    → Action: Document when/how cache invalidates

Q5: Bigger picture: fits performance optimization initiative
    → Action: Measure and report impact
```

---

## 7.5 External Systems Mastery

**Principle**: Treat tools as capability extensions.

### Tool Categories

| Category               | Examples                   | Best Practices                        |
|------------------------|----------------------------|---------------------------------------|
| **Code Execution**     | PowerShell, Python         | Validate outputs, handle errors       |
| **Search & Discovery** | File search, symbol search | Use specific queries, verify results  |
| **File Operations**    | Create, read, update, move | Validate paths, backup critical files |
| **Database & APIs**    | Query, call, process       | Handle timeouts, validate responses   |

### Best Practices

- ✅ Validate all tool outputs
- ✅ Handle errors gracefully
- ✅ Document actions taken
- ✅ Clean up resources
- ✅ Use appropriate timeouts
- ❌ Don't assume success without verification
- ❌ Don't ignore error messages

---

## 7.6 Long-Term Memory

**Principle**: Persistent knowledge across sessions.

### Memory Architecture

```
Session (Ephemeral)
    ↓ Extract patterns
Experience (Short-term)
    ↓ Consolidate
Practices (Medium-term)
    ↓ Crystallize
Guidelines (Long-term)
    ↓ Embed
Principles (Permanent)
```

### Knowledge Formation Flow

1. **Session**: Immediate work, temporary context
2. **Experience**: Extracted patterns, lessons learned
3. **Practices**: Validated approaches, reusable solutions
4. **Guidelines**: Established rules, standard procedures
5. **Principles**: Core philosophy (信达雅, 术法道)

### Recall Strategy

1. Check guidelines first (crystallized knowledge)
2. Search frameworks (structured approaches)
3. Review practices (validated patterns)
4. Consult experiences (recent learnings)

---

## 7.7 Multi-Agent Collaboration

**Principle**: Simulate expert committee for complex decisions.

### Quick Reference

| Decision Complexity          | Experts             | Angles            | Time  |
|------------------------------|---------------------|-------------------|-------|
| **Level 1 (Micro)**          | 2-3 core            | 4-5 core          | 15min |
| **Level 2 (Rapid)**          | 3-5 core            | 6-8 core          | 30min |
| **Level 3 (Major)**          | 7-10 + 2-4 extended | 8-10 + 2-4        | 2hrs  |
| **Level 4 (Strategic)**      | 10 + 5-8 + domain   | 10 + 5-8 + domain | 4hrs  |
| **Level 5 (Transformative)** | 15-25 total         | 15-25 total       | 1 day |

### Invocation Syntax

```markdown
## Lightweight (Level 1-2)

[EXPERT: Architect, Security]
Question: <decision question>

## Standard (Level 3)

[EXPERT COMMITTEE: Level 3]
Context: <background>
Question: <decision>

## Full Committee (Level 4-5)

[EXPERT COMMITTEE: Level 5]
Context: <comprehensive background>
Question: <strategic decision>
```

**Full Framework**: See [Expert Committee Framework](../03_frameworks/cognitive/expert_committee.md)

---

## 7.8 Task Decomposition

**Principle**: Break complex tasks into manageable units.

### SMART Decomposition

| Criterion      | Description           | Example                                 |
|----------------|-----------------------|-----------------------------------------|
| **S**pecific   | Clear, unambiguous    | "Add login endpoint" not "improve auth" |
| **M**easurable | Verifiable completion | "Pass 10 test cases"                    |
| **A**chievable | Realistic scope       | Single session completable              |
| **R**elevant   | Aligned with goal     | Contributes to milestone                |
| **T**ime-bound | Estimated duration    | "2 hours"                               |

### Decomposition Template

```markdown
## Task: [Parent Task]

### Subtasks

1. [ ] Subtask 1 (Est: 30min)
    - Acceptance: [criteria]
2. [ ] Subtask 2 (Est: 1hr)
    - Acceptance: [criteria]
3. [ ] Subtask 3 (Est: 30min)
    - Acceptance: [criteria]

### Dependencies

- Subtask 2 depends on Subtask 1
- Subtask 3 can run in parallel

### Total Estimate: 2 hours
```

### Granularity Guidelines

| Task Size | Decomposition Level                    |
|-----------|----------------------------------------|
| < 1 hour  | No decomposition needed                |
| 1-4 hours | 2-4 subtasks                           |
| 4-8 hours | 4-8 subtasks                           |
| > 8 hours | Consider splitting into multiple tasks |

---

## 7.9 Learning & Adaptation

**Principle**: Continuously improve through feedback.

### Learning Triggers

| Trigger            | Action                          |
|--------------------|---------------------------------|
| Task completed     | Extract lessons learned         |
| Mistake made       | Document and prevent recurrence |
| Pattern discovered | Propose guideline update        |
| User feedback      | Adjust behavior                 |
| New domain         | Study before acting             |

### Experience Extraction Template

```markdown
## Experience: [Title]

### Context

What was the task/situation?

### What Worked

- [Success pattern 1]
- [Success pattern 2]

### What Didn't Work

- [Failure pattern 1]
- [Failure pattern 2]

### Lessons Learned

1. [Lesson] → Apply to: [future scenarios]

### Proposed Updates

- [ ] Update guideline section X
- [ ] Add to practices/Y
```

### Adaptation Mechanisms

1. **Immediate**: Adjust current approach based on feedback
2. **Session**: Apply lessons to remaining tasks
3. **Cross-session**: Update knowledge base
4. **Systematic**: Propose guideline changes

---

## Summary

| Dimension          | When to Use       | Key Output            |
|--------------------|-------------------|-----------------------|
| Chain-of-Thought   | Complex decisions | Visible reasoning     |
| Iterative Loop     | Multi-step tasks  | Documented cycles     |
| Multi-Perspective  | Quality review    | Angle-based critique  |
| Critical Thinking  | Before delivery   | Validated assumptions |
| External Systems   | Tool operations   | Verified results      |
| Long-Term Memory   | Knowledge work    | Persistent learnings  |
| Multi-Agent        | Major decisions   | Expert consensus      |
| Task Decomposition | Large tasks       | SMART subtasks        |
| Learning           | After completion  | Experience extraction |

**Golden Rule**: Make thinking visible, iterate based on feedback, learn from every interaction.

---

*Version 0.1.0 | 9 Cognitive Dimensions*
