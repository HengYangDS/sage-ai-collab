# AI Collaboration Patterns

> Successful interaction patterns and project-specific optimizations for SAGE Knowledge Base

---

## Table of Contents

[1. Overview](#1-overview) · [2. Interaction Patterns](#2-interaction-patterns) · [3. Knowledge Capture Patterns](#3-knowledge-capture-patterns) · [4. Optimization Strategies](#4-optimization-strategies) · [5. Calibration Data](#5-calibration-data)

---

## 1. Overview

This document captures successful AI collaboration patterns discovered during SAGE development. These patterns help maintain consistency and efficiency in human-AI interactions.

### 1.1 Purpose

- Document proven interaction strategies
- Capture project-specific optimizations
- Track calibration data for autonomy levels
- Provide reference for future sessions

### 1.2 Pattern Categories

| Category | Description |
|----------|-------------|
| **Interaction** | Communication and workflow patterns |
| **Knowledge Capture** | When and how to document knowledge |
| **Optimization** | Efficiency improvements |
| **Calibration** | Autonomy level adjustments |

---

## 2. Interaction Patterns

### 2.1 Session Start Pattern

**Context**: Beginning a new collaboration session

**Pattern**:
1. Review `.junie/guidelines.md` for project context
2. Check `.history/current/` for active sessions
3. Review recent commits for context continuity
4. Establish task scope and autonomy level

**Benefits**: Faster context loading, consistent behavior

### 2.2 Progressive Disclosure Pattern

**Context**: Handling complex multi-step tasks

**Pattern**:
1. Start with high-level plan
2. Execute one step at a time
3. Report progress after each step
4. Adjust plan based on findings

**Benefits**: Maintains transparency, allows course correction

### 2.3 Clarification Request Pattern

**Context**: Ambiguous or incomplete requirements

**Pattern**:
1. State understanding of the requirement
2. List specific ambiguities
3. Propose default interpretation
4. Ask for confirmation or clarification

**Example**:
```
我理解您希望更新配置文件。有几点需要确认：
1. 是否包括所有子目录的配置？（默认：是）
2. 是否需要备份原文件？（默认：否）
请确认或调整。
```

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

**Where**: `.context/decisions/ADR-NNNN-*.md`

### 3.2 Convention Discovery Pattern

**When to capture**: New coding patterns or standards emerge

**What to capture**:
- Pattern description
- Usage examples
- When to apply
- Exceptions

**Where**: `.context/conventions/*.md`

### 3.3 Session Handoff Pattern

**When to capture**: End of significant work session

**What to capture**:
- Completed tasks
- Pending items
- Important findings
- Next steps

**Where**: `.history/handoffs/*.md`

### 3.4 Problem-Solution Pattern

**When to capture**: Solving non-trivial problems

**What to capture**:
- Problem description
- Investigation steps
- Root cause
- Solution applied

**Where**: Relevant documentation or `.history/conversations/`

---

## 4. Optimization Strategies

### 4.1 Context Window Optimization

**Strategy**: Minimize context while maximizing relevance

**Techniques**:
- Use targeted file searches over full directory scans
- Request specific line ranges when opening files
- Collapse completed plan items to save space
- Reference files by path instead of including content

### 4.2 Token Budget Management

**Strategy**: Stay within T4 (5s) timeout for most operations

**Techniques**:
- Load core knowledge first (highest priority)
- Use smart loading based on task type
- Implement graceful degradation for large requests
- Cache frequently accessed content

### 4.3 Parallel Task Execution

**Strategy**: Execute independent tasks concurrently

**Techniques**:
- Identify task dependencies
- Group independent operations
- Use batch commands where possible
- Verify results collectively

### 4.4 Error Recovery Strategy

**Strategy**: Graceful handling of failures

**Techniques**:
- Always have fallback approach
- Document partial progress
- Preserve work before risky operations
- Report issues with context

---

## 5. Calibration Data

### 5.1 Autonomy Level Calibration

Current calibration for SAGE project:

| Task Type | Recommended Level | Notes |
|-----------|-------------------|-------|
| Documentation updates | L5 (High) | Well-established patterns |
| Code formatting | L5 (High) | Ruff handles automatically |
| Bug fixes | L4 (Medium-High) | Verify with tests |
| New features | L3 (Medium) | Discuss design first |
| Architecture changes | L2 (Low) | Requires approval |
| Breaking changes | L1 (Minimal) | Full review required |

### 5.2 Response Time Expectations

| Operation | Expected Time | Timeout Level |
|-----------|---------------|---------------|
| Simple query | < 100ms | T1 |
| Single file read | < 500ms | T2 |
| Multi-file analysis | < 2s | T3 |
| Full KB load | < 5s | T4 |
| Complex analysis | < 10s | T5 |

### 5.3 Quality Thresholds

| Metric | Target | Action if Below |
|--------|--------|-----------------|
| Test coverage | > 80% | Add tests before merge |
| Type coverage | > 90% | Add type hints |
| Doc coverage | > 70% | Add docstrings |
| Complexity | < 10 | Refactor function |

---

## 6. Anti-Patterns

### 6.1 Avoid: Over-Engineering

**Problem**: Adding complexity for hypothetical future needs

**Instead**: Implement minimal solution, extend when needed

### 6.2 Avoid: Silent Assumptions

**Problem**: Proceeding without confirming ambiguous requirements

**Instead**: Use Clarification Request Pattern (2.3)

### 6.3 Avoid: Monolithic Changes

**Problem**: Large changes that are hard to review/revert

**Instead**: Use Batch Operation Pattern (2.4) with small commits

### 6.4 Avoid: Context Overload

**Problem**: Loading entire codebase into context

**Instead**: Use targeted searches and specific file sections

---

## Related

- `content/frameworks/autonomy/levels.md` — Autonomy level definitions
- `content/practices/ai_collaboration/` — AI collaboration best practices
- `.junie/guidelines.md` — Project collaboration guidelines
- `.history/` — Session history and handoffs

---

*Part of SAGE Knowledge Base - AI Intelligence Patterns*
