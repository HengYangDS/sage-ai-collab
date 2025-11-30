# AI Collaboration Patterns

> Successful interaction patterns for human-AI collaboration

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Interaction Patterns](#2-interaction-patterns)
- [3. Knowledge Capture Patterns](#3-knowledge-capture-patterns)
- [4. Optimization Strategies](#4-optimization-strategies)
- [5. Anti-Patterns](#5-anti-patterns)

---

## 1. Overview

This document captures successful AI collaboration patterns that help maintain consistency and efficiency in human-AI
interactions. These patterns are applicable across projects and AI tools.

### 1.1 Purpose

- Document proven interaction strategies
- Capture optimization techniques
- Provide reference for effective collaboration
- Avoid common anti-patterns

### 1.2 Pattern Categories

| Category              | Description                         |
|-----------------------|-------------------------------------|
| **Interaction**       | Communication and workflow patterns |
| **Knowledge Capture** | When and how to document knowledge  |
| **Optimization**      | Efficiency improvements             |
| **Anti-Patterns**     | What to avoid                       |

---

## 2. Interaction Patterns

### 2.1 Session Start Pattern

**Context**: Beginning a new collaboration session

**Pattern**:

1. Review project guidelines for context
2. Check for active sessions or pending work
3. Review recent changes for context continuity
4. Establish task scope and autonomy level

**Benefits**: Faster context loading, consistent behavior

---

### 2.2 Progressive Disclosure Pattern

**Context**: Handling complex multi-step tasks

**Pattern**:

1. Start with high-level plan
2. Execute one step at a time
3. Report progress after each step
4. Adjust plan based on findings

**Benefits**: Maintains transparency, allows course correction

---

### 2.3 Clarification Request Pattern

**Context**: Ambiguous or incomplete requirements

**Pattern**:

1. State understanding of the requirement
2. List specific ambiguities
3. Propose default interpretation
4. Ask for confirmation or clarification

**Example**:

```
I understand you wish to update the configuration files. A few points to confirm:
1. Does this include configuration in all subdirectories? (Default: Yes)
2. Should the original files be backed up? (Default: No)
Please confirm or adjust.
```
**Benefits**: Reduces misunderstandings, establishes shared expectations

---

### 2.4 Batch Operation Pattern

**Context**: Multiple similar changes across files

**Pattern**:

1. Identify all affected files first
2. Group by change type
3. Execute in batches with verification
4. Summarize changes at end

**Benefits**: Reduces errors, maintains consistency

---

## 3. Knowledge Capture Patterns

### 3.1 Decision Point Pattern

**When to capture**: Significant technical decisions made during development

**What to capture**:

- Context and constraints
- Options considered
- Decision rationale
- Expected consequences

**Where**: Project decision records (e.g., ADRs)

---

### 3.2 Convention Discovery Pattern

**When to capture**: New coding patterns or standards emerge

**What to capture**:

- Pattern description
- Usage examples
- When to apply
- Exceptions

**Where**: Project conventions documentation

---

### 3.3 Session Handoff Pattern

**When to capture**: End of significant work session

**What to capture**:

- Completed tasks
- Pending items
- Important findings
- Next steps

**Where**: Session history or handoff documents

---

### 3.4 Problem-Solution Pattern

**When to capture**: Solving non-trivial problems

**What to capture**:

- Problem description
- Investigation steps
- Root cause
- Solution applied

**Where**: Relevant documentation or conversation records

---

## 4. Optimization Strategies

### 4.1 Context Window Optimization

**Strategy**: Minimize context while maximizing relevance

**Techniques**:

- Use targeted file searches over full directory scans
- Request specific line ranges when opening files
- Collapse completed plan items to save space
- Reference files by path instead of including content

---

### 4.2 Token Budget Management

**Strategy**: Stay within reasonable limits for most operations

**Techniques**:

- Load core knowledge first (highest priority)
- Use smart loading based on task type
- Implement graceful degradation for large requests
- Cache frequently accessed content

---

### 4.3 Parallel Task Execution

**Strategy**: Execute independent tasks concurrently

**Techniques**:

- Identify task dependencies
- Group independent operations
- Use batch commands where possible
- Verify results collectively

---

### 4.4 Error Recovery Strategy

**Strategy**: Graceful handling of failures

**Techniques**:

- Always have fallback approach
- Document partial progress
- Preserve work before risky operations
- Report issues with context

---

## 5. Anti-Patterns

### 5.1 Avoid: Over-Engineering

**Problem**: Adding complexity for hypothetical future needs

**Instead**: Implement minimal solution, extend when needed

---

### 5.2 Avoid: Silent Assumptions

**Problem**: Proceeding without confirming ambiguous requirements

**Instead**: Use Clarification Request Pattern (2.3)

---

### 5.3 Avoid: Monolithic Changes

**Problem**: Large changes that are hard to review/revert

**Instead**: Use Batch Operation Pattern (2.4) with small commits

---

### 5.4 Avoid: Context Overload

**Problem**: Loading entire codebase into context

**Instead**: Use targeted searches and specific file sections

---

## Quick Reference

### Pattern Selection Guide

| Situation             | Recommended Pattern          |
|-----------------------|------------------------------|
| Starting work         | Session Start Pattern (2.1)  |
| Complex task          | Progressive Disclosure (2.2) |
| Unclear requirements  | Clarification Request (2.3)  |
| Multiple file changes | Batch Operation (2.4)        |
| Major decision        | Decision Point (3.1)         |
| New pattern found     | Convention Discovery (3.2)   |
| Ending session        | Session Handoff (3.3)        |
| Problem solved        | Problem-Solution (3.4)       |

---

## Related

- `.knowledge/frameworks/autonomy/LEVELS.md` — Autonomy level definitions
- `.knowledge/practices/ai_collaboration/WORKFLOW.md` — AI collaboration workflow
- `.knowledge/practices/ai_collaboration/CONTEXT_MANAGEMENT.md` — Context management
- `.knowledge/practices/ai_collaboration/SESSION_MANAGEMENT.md` — Session management

---

*AI Collaboration Knowledge Base*
