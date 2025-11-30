# Planning and Design Guidelines

> Architecture and design principles for sustainable systems

---

## Table of Contents

- [1. Execution Principles](#1-execution-principles)
- [2. Architecture Principles](#2-architecture-principles)
- [3. Decision Framework](#3-decision-framework)
- [4. Complexity Management](#4-complexity-management)
- [5. Anti-Patterns](#5-anti-patterns)

---

## 1. Execution Principles

| Principle   | Description                                 |
|-------------|---------------------------------------------|
| Incremental | Small, verified steps over big-bang changes |
| Reversible  | Prefer changes that can be undone           |
| Observable  | Make system state visible                   |
| Testable    | Design for verification                     |

---

## 2. Architecture Principles

### 2.1 SOLID

| Principle                 | Meaning                                     |
|---------------------------|---------------------------------------------|
| **S**ingle Responsibility | One reason to change                        |
| **O**pen/Closed           | Open for extension, closed for modification |
| **L**iskov Substitution   | Subtypes substitutable for base types       |
| **I**nterface Segregation | Small, focused interfaces                   |
| **D**ependency Inversion  | Depend on abstractions                      |

### 2.2 Design Axioms

| Axiom                  | Application                                 |
|------------------------|---------------------------------------------|
| MECE                   | Mutually exclusive, collectively exhaustive |
| SSOT                   | Single source of truth                      |
| Separation of concerns | Content, code, config separated             |
| Progressive disclosure | Overview → detail                           |
| Fail-fast              | No operation hangs indefinitely             |

---

## 3. Decision Framework

### 3.1 Before Deciding

| Question                      | Purpose            |
|-------------------------------|--------------------|
| What problem does this solve? | Validate need      |
| What are the alternatives?    | Ensure best choice |
| What are the trade-offs?      | Understand costs   |
| Is this reversible?           | Assess risk        |

### 3.2 Decision Record

```markdown
## Context

[Why decision needed]

## Decision

[What was decided]

## Consequences

[+] Benefits
[-] Drawbacks
[~] Trade-offs
```
---

## 4. Complexity Management

| Strategy    | Application                     |
|-------------|---------------------------------|
| Decompose   | Break into smaller parts        |
| Abstract    | Hide implementation details     |
| Standardize | Use consistent patterns         |
| Document    | Capture decisions and rationale |

---

## 5. Anti-Patterns

| Anti-Pattern           | Problem                 | Solution               |
|------------------------|-------------------------|------------------------|
| God Object             | Does everything         | Split responsibilities |
| Premature Optimization | Complexity without need | Profile first          |
| Copy-Paste             | Duplication             | Extract to shared      |
| Magic Numbers          | Unclear intent          | Named constants        |

---

## Related

- `.knowledge/frameworks/design/AXIOMS.md` — Design axioms and principles
- `.knowledge/guidelines/ENGINEERING.md` — Engineering practices
- `.knowledge/practices/engineering/API_DESIGN.md` — API design patterns
- `.knowledge/frameworks/patterns/DECISION.md` — Decision quality framework

---

*AI Collaboration Knowledge Base*
