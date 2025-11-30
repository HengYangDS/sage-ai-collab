# Context Management Practices

> Strategies for building and managing shared context in AI collaboration

---

## Table of Contents

- [1. Context Types](#1-context-types)
- [2. Context Building](#2-context-building)
- [3. Context Efficiency](#3-context-efficiency)
- [4. Context Maintenance](#4-context-maintenance)
- [5. Context Templates](#5-context-templates)
- [6. Best Practices](#6-best-practices)

---

## 1. Context Types

| Type        | Purpose            | Example                   |
|-------------|--------------------|---------------------------|
| **Task**    | Current work       | "Refactor auth module"    |
| **Project** | Broader scope      | Architecture, conventions |
| **Domain**  | Subject knowledge  | Business rules            |
| **Session** | Conversation state | Previous decisions        |

---

## 2. Context Building

### 2.1 Essential Elements

| Element     | When to Include      |
|-------------|----------------------|
| Goal        | Always               |
| Constraints | When applicable      |
| Background  | Complex tasks        |
| Examples    | Unclear requirements |
| References  | Related files        |

### 2.2 Progressive Loading

| Phase   | Context Level                |
|---------|------------------------------|
| Start   | Minimal (goal + constraints) |
| Working | Add as needed                |
| Complex | Full context                 |
| Handoff | Summary + key decisions      |

---

## 3. Context Efficiency

### 3.1 Compression Techniques

| Technique         | Savings | Use Case        |
|-------------------|---------|-----------------|
| Summarize history | ~50%    | Long sessions   |
| Reference files   | ~70%    | Code context    |
| Use tables        | ~40%    | Structured info |
| Abbreviate        | ~20%    | Common terms    |

### 3.2 Anti-Patterns

| Pattern              | Problem     | Solution            |
|----------------------|-------------|---------------------|
| Dump everything      | Token waste | Progressive loading |
| Repeat info          | Redundancy  | Reference previous  |
| Verbose explanations | Inefficient | Use tables          |
| Include irrelevant   | Noise       | Filter context      |

---

## 4. Context Maintenance

### 4.1 During Session

| Action     | When                  |
|------------|-----------------------|
| Summarize  | Every 5-10 exchanges  |
| Prune      | When context grows    |
| Checkpoint | Before major changes  |
| Reset      | When switching topics |

### 4.2 Across Sessions

| Strategy            | Purpose            |
|---------------------|--------------------|
| Handoff summary     | Transfer knowledge |
| Decision log        | Track choices      |
| Progress checkpoint | Resume work        |

---

## 5. Context Templates

### 5.1 Task Start

```markdown
## Context

- **Goal**: [What to achieve]
- **Constraints**: [Limits to respect]
- **Files**: [Relevant files]

## Background

[Brief context if needed]
```
### 5.2 Session Summary

```markdown
## Session Summary

- **Completed**: [What was done]
- **Decisions**: [Key choices made]
- **Next**: [What's pending]
```
---

## 6. Best Practices

| Practice                | Benefit            |
|-------------------------|--------------------|
| Start minimal           | Reduce noise       |
| Add progressively       | Efficient tokens   |
| Summarize regularly     | Maintain clarity   |
| Reference, don't repeat | Save tokens        |
| Checkpoint decisions    | Preserve knowledge |

---

## Related

- `.knowledge/practices/ai_collaboration/TOKEN_OPTIMIZATION.md` — Token efficiency
- `.knowledge/practices/ai_collaboration/WORKFLOW.md` — Collaboration workflows

---

*AI Collaboration Knowledge Base*
