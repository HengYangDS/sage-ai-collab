# AI Collaboration Patterns Framework

> **Load Time**: On-demand (~400 tokens)  
> **Purpose**: Patterns for effective human-AI collaboration  
> **Version**: 0.1.0

---

## Overview

This framework defines patterns for effective human-AI collaboration, including communication patterns, task handoff
protocols, and instruction engineering principles.

---

## 1. Communication Patterns

### 1.1 Instruction Types

| Type            | Description         | Example                         | Best Practice                 |
|-----------------|---------------------|---------------------------------|-------------------------------|
| **Direct**      | Explicit command    | "Create user API endpoint"      | Clear, specific, actionable   |
| **Contextual**  | Implied by context  | Fixing similar bugs             | Provide sufficient background |
| **Conditional** | With constraints    | "Refactor only if tests pass"   | State conditions clearly      |
| **Exploratory** | Open-ended research | "Investigate performance issue" | Define scope and criteria     |
| **Batch**       | Multiple tasks      | "Complete all TODO items"       | Group related tasks           |

### 1.2 Response Patterns

| Pattern           | When to Use          | Format                       |
|-------------------|----------------------|------------------------------|
| **Confirmation**  | Before risky actions | "I will do X. Proceed?"      |
| **Progress**      | Long operations      | "Step 2/5: Implementing..."  |
| **Completion**    | Task finished        | "Done. Summary: ..."         |
| **Clarification** | Ambiguous input      | "Did you mean A or B?"       |
| **Error**         | On failure           | "Error: X. Suggested fix: Y" |

### 1.3 Context Preservation

```markdown
## Session Context Template

### Project State

- Project: [name]
- Branch: [current branch]
- Recent changes: [summary]

### Current Task

- Objective: [what]
- Constraints: [limitations]
- Progress: [status]

### Relevant Files

-

[file1]: [purpose]
-

[file2]: [purpose]
```

---

## 2. Task Handoff Protocols

### 2.1 Simple Handoff

```
Human → AI: "Do X"
AI: [Confirms] → [Executes] → [Reports]
Human: [Reviews]
```

### 2.2 Detailed Handoff

```markdown
## Task: [Title]

### Requirements

- Requirement 1
- Requirement 2

### Constraints

- Constraint 1
- Constraint 2

### Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

### Autonomy Level

[L1-L6]
```

### 2.3 Batch Handoff

```markdown
## Batch Tasks

### Tasks (Autonomy: L4)

1. Task 1 - [priority]
2. Task 2 - [priority]
3. Task 3 - [priority]

### Execution Order

Sequential / Parallel / Priority-based

### Checkpoint

After [N] tasks / [time] / [milestone]
```

---

## 3. Instruction Engineering

### 3.1 CLEAR Framework

| Component        | Description                | Example                        |
|------------------|----------------------------|--------------------------------|
| **C**ontext      | Background information     | "In this FastAPI project..."   |
| **L**imitations  | Constraints and boundaries | "Don't modify database schema" |
| **E**xpectations | Success criteria           | "Tests should pass"            |
| **A**ction       | What to do                 | "Implement user auth"          |
| **R**eview       | Checkpoint requirements    | "Show plan before coding"      |

### 3.2 Instruction Quality Checklist

- [ ] **Specific**: Clear, unambiguous objective
- [ ] **Scoped**: Boundaries defined
- [ ] **Measurable**: Success criteria stated
- [ ] **Contextual**: Relevant background provided
- [ ] **Prioritized**: Importance indicated

### 3.3 Anti-Patterns to Avoid

| Anti-Pattern           | Problem               | Better Approach               |
|------------------------|-----------------------|-------------------------------|
| "Make it better"       | Vague, subjective     | Specific improvement criteria |
| "Do everything"        | Unbounded scope       | Prioritized task list         |
| "You know what I mean" | Assumes understanding | Explicit requirements         |
| "ASAP"                 | No real deadline      | Specific time constraint      |
| "Don't mess up"        | Negative framing      | Positive success criteria     |

---

## 4. Collaboration Modes

### 4.1 Mode Definitions

| Mode        | Description           | AI Behavior                   |
|-------------|-----------------------|-------------------------------|
| **Plan**    | Strategic planning    | Create plan, await approval   |
| **Execute** | Task execution        | Run with progress updates     |
| **Review**  | Code/design review    | Analyze without changes       |
| **Explain** | Teaching/learning     | Explain concepts clearly      |
| **Debug**   | Problem investigation | Diagnose with minimal changes |
| **Pair**    | Collaborative work    | Interactive back-and-forth    |

### 4.2 Mode Selection Guide

| Scenario              | Recommended Mode |
|-----------------------|------------------|
| Complex new feature   | Plan → Execute   |
| Bug fix (clear cause) | Execute          |
| Bug fix (unclear)     | Debug → Execute  |
| Code quality review   | Review           |
| Learning new tech     | Explain          |
| Refactoring           | Plan → Execute   |
| Quick changes         | Execute          |

---

## 5. Feedback Loops

### 5.1 Immediate Feedback

```
Action → Result → Adjustment
   ↑__________________|
```

- Correct misunderstandings immediately
- Provide specific feedback
- Acknowledge good work

### 5.2 Session Feedback

```markdown
## Session Feedback

### What Worked Well

- [positive pattern 1]
- [positive pattern 2]

### What Could Improve

- [improvement area 1]
- [improvement area 2]

### Autonomy Adjustment

Current: L[N] → Suggested: L[M]
Reason: [justification]
```

### 5.3 Calibration Signals

| Signal                   | Interpretation    | Action                 |
|--------------------------|-------------------|------------------------|
| "Let me see first"       | Decrease autonomy | Lower to L1-L2         |
| "You decide"             | Increase autonomy | Raise to L3-L4         |
| "Explain your reasoning" | Show more detail  | Verbose mode           |
| "Just do it"             | Less explanation  | Concise mode           |
| "Stop"                   | Pause execution   | Checkpoint immediately |

---

## 6. Error Recovery Patterns

### 6.1 Error Classification

| Type         | Severity | Recovery              |
|--------------|----------|-----------------------|
| **Syntax**   | Low      | Auto-fix              |
| **Logic**    | Medium   | Report + suggest      |
| **Data**     | High     | Stop + await guidance |
| **Security** | Critical | Stop immediately      |

### 6.2 Recovery Protocol

```
1. Detect error
2. Classify severity
3. Stop if High/Critical
4. Document error clearly
5. Analyze root cause
6. Propose solution(s)
7. Await approval if needed
8. Execute fix
9. Verify resolution
```

### 6.3 Error Report Template

```markdown
## Error Report

**Type**: [classification]
**Severity**: [Low/Medium/High/Critical]
**Location**: [file:line]

### Description

[What happened]

### Root Cause

[Why it happened]

### Impact

[What was affected]

### Proposed Fix

[Solution]

### Prevention

[How to avoid in future]
```

---

## 7. Integration with Autonomy Levels

| Level     | Communication    | Checkpoints       | Feedback  |
|-----------|------------------|-------------------|-----------|
| **L1-L2** | Every step       | After each action | Immediate |
| **L3-L4** | Major milestones | At decisions      | Periodic  |
| **L5-L6** | Completion only  | On issues         | Summary   |

---

## Quick Reference

### Starting a Collaboration

1. State context clearly
2. Define objective specifically
3. Set autonomy level
4. Specify constraints
5. Indicate priority/deadline

### During Collaboration

- Monitor progress updates
- Respond to questions promptly
- Provide feedback at checkpoints
- Adjust autonomy as needed

### Ending a Collaboration

- Review deliverables
- Provide session feedback
- Update autonomy calibration
- Document decisions made

---

*Version 0.1.0 | Part of AI Collaboration Knowledge Base*
