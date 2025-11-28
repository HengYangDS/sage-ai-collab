# AI Collaboration Guidelines

> **Load Time**: On-demand (~300 tokens)  
> **Purpose**: Human-AI interaction patterns, autonomy levels, execution modes

---

## 6.1 Instruction Types

### Classification Matrix

| Type            | Description         | Example                                     |
|-----------------|---------------------|---------------------------------------------|
| **Direct**      | Explicit command    | "Create a user registration endpoint"       |
| **Contextual**  | Implied by context  | Fixing similar bugs as previously discussed |
| **Conditional** | With constraints    | "Refactor only if tests pass"               |
| **Exploratory** | Open-ended research | "Investigate performance bottleneck"        |

### Instruction Quality Checklist

- [ ] Clear objective stated
- [ ] Scope boundaries defined
- [ ] Success criteria specified
- [ ] Constraints identified
- [ ] Priority indicated

---

## 6.2 Autonomy Levels

> **Reference**: See `content/frameworks/autonomy/levels.md` for full 6-level autonomy framework

### Level Definitions

```
L1: Minimal (0-20%)      ← Execute only explicit tasks, ask before every decision
L2: Low (20-40%)         ← Execute well-defined tasks, ask on implementation choices
L3: Medium (40-60%)      ← Complete tasks independently, ask for architectural changes
L4: Medium-High (60-80%) ← Proactive project partner, multi-task initiatives [DEFAULT]
L5: High (80-95%)        ← Strategic decisions, refactor architecture proactively
L6: Full (95-100%)       ← Autonomous agent, rarely recommended
```

### Level Selection Guide

| Scenario                    | Recommended Level |
|-----------------------------|-------------------|
| Critical production changes | L1-L2             |
| New feature development     | L2-L3             |
| Bug fixes (well-understood) | L3-L4             |
| Routine refactoring         | L3-L4             |
| Documentation updates       | L4-L5             |
| Formatting/style fixes      | L4-L5             |

### Autonomy Adjustment Signals

**Increase autonomy when:**

- Task is well-understood
- Similar tasks completed successfully
- Low risk of damage
- Clear rollback path exists

**Decrease autonomy when:**

- Task is novel or complex
- High-stakes changes
- Uncertainty about requirements
- Previous errors in similar tasks

---

## 6.3 Execution Modes

### Mode Descriptions

| Mode        | Behavior                    | Use Case        |
|-------------|-----------------------------|-----------------|
| **Plan**    | Create plan, await approval | Complex tasks   |
| **Execute** | Run with progress updates   | Standard tasks  |
| **Review**  | Analyze without changes     | Code review     |
| **Explain** | Teach/explain concepts      | Learning        |
| **Debug**   | Investigate issues          | Troubleshooting |

### Execution Flow

```
[Plan Mode]
1. Analyze requirements
2. Create step-by-step plan
3. Identify risks and dependencies
4. Present plan for approval
5. Wait for human confirmation

[Execute Mode]
1. Confirm understanding
2. Execute step by step
3. Report progress at checkpoints
4. Handle errors gracefully
5. Summarize results
```

---

## 6.4 Communication Patterns

### Status Updates

```markdown
## Progress Update

**Status**: In Progress (3/5 steps complete)

### Completed

- [x] Created database migration
- [x] Updated model schema
- [x] Added API endpoint

### In Progress

- [ ] Writing unit tests

### Remaining

- [ ] Update documentation

**Blockers**: None
**ETA**: 15 minutes
```

### Error Reporting

```markdown
## Error Report

**Type**: Test Failure
**Location**: tests/test_user.py::test_create_user
**Severity**: Medium

### Description

User creation test fails due to missing email validation.

### Root Cause

Email validator not imported in user model.

### Proposed Fix

Add `from validators import validate_email` to models/user.py

### Action Required

- [ ] Approve fix
- [ ] Request alternative approach
- [ ] Provide additional context
```

---

## 6.5 Default Behaviors

### Standard Defaults

| Behavior        | Default            | Rationale                      |
|-----------------|--------------------|--------------------------------|
| Autonomy Level  | L2 (Guided)        | Balance control and efficiency |
| Error Handling  | Stop and report    | Prevent cascading errors       |
| Scope Expansion | Ask first          | Avoid scope creep              |
| Assumptions     | State explicitly   | Ensure alignment               |
| Testing         | Run affected tests | Verify changes                 |

### Override Syntax

```
# Temporarily increase autonomy
[L4] Complete all formatting fixes in src/

# Set specific mode
[MODE:REVIEW] Check this PR for security issues

# Conditional execution
[IF tests pass] Merge to develop branch
```

---

## 6.6 Collaboration Anti-Patterns

### Patterns to Avoid

| Anti-Pattern        | Problem                  | Better Approach            |
|---------------------|--------------------------|----------------------------|
| Vague instructions  | Misaligned execution     | Be specific about goals    |
| No success criteria | Unknown completion       | Define "done" clearly      |
| Implicit scope      | Over/under delivery      | Explicit boundaries        |
| Ignoring warnings   | Cascading errors         | Address concerns           |
| Micro-management    | Inefficient, frustrating | Trust appropriate autonomy |

---

## 6.7 Calibration Signals

### Positive Signals (Working Well)

- Tasks completed as expected
- Few clarification questions needed
- Results match intent
- Efficient execution time

### Negative Signals (Adjustment Needed)

- Frequent misunderstandings
- Unexpected changes
- Missed requirements
- Excessive back-and-forth

### Calibration Actions

```
Signal: AI making too many assumptions
Action: Lower autonomy, increase checkpoints

Signal: AI asking too many questions
Action: Provide more context upfront, raise autonomy

Signal: Results consistently good
Action: Consider higher autonomy for similar tasks

Signal: Repeated similar errors
Action: Update guidelines, add specific rules
```

---

## 6.8 Quick Reference Card

### Starting a Task

1. State objective clearly
2. Define scope boundaries
3. Specify autonomy level (or use default L2)
4. Indicate priority and deadline
5. Mention any constraints

### During Execution

- Monitor progress updates
- Respond to questions promptly
- Approve/reject at checkpoints
- Provide feedback on approach

### After Completion

- Review results
- Provide feedback
- Update autonomy calibration
- Document learnings

---

*Part of AI Collaboration Knowledge Base v2.0.0*
