# Knowledge Extraction Patterns

> Methods for extracting reusable knowledge from experience

---

## Table of Contents

- [1. Extraction Types](#1-extraction-types)
- [2. Extraction Process](#2-extraction-process)
- [3. Pattern Extraction](#3-pattern-extraction)
- [4. Decision Extraction](#4-decision-extraction)
- [5. Learning Extraction](#5-learning-extraction)
- [6. Best Practices](#6-best-practices)

---

## 1. Extraction Types

| Type         | Source             | Output            |
|--------------|--------------------|-------------------|
| **Pattern**  | Repeated solutions | Reusable template |
| **Decision** | Choice made        | ADR document      |
| **Learning** | Mistake/success    | Best practice     |
| **Process**  | Workflow           | Procedure guide   |

---

## 2. Extraction Process

### 2.1 Steps

| Step | Action     | Output             |
|------|------------|--------------------|
| 1    | Identify   | What to extract    |
| 2    | Abstract   | Remove specifics   |
| 3    | Generalize | Make reusable      |
| 4    | Document   | Structured format  |
| 5    | Validate   | Test applicability |

### 2.2 Abstraction Levels

| Level      | Description        | Example                      |
|------------|--------------------|------------------------------|
| Specific   | Exact solution     | "Fix bug in auth.py line 42" |
| Contextual | Solution + context | "Handle null in auth flow"   |
| General    | Pattern            | "Null check pattern"         |
| Universal  | Principle          | "Defensive programming"      |

---

## 3. Pattern Extraction

### 3.1 Pattern Template

```markdown
## Pattern: [Name]

### Problem

[What problem it solves]

### Solution

[How to apply]

### Example

[Code or usage example]

### When to Use

[Applicability criteria]
```
### 3.2 Quality Criteria

| Criterion | Description               |
|-----------|---------------------------|
| Reusable  | Applies to multiple cases |
| Clear     | Easy to understand        |
| Complete  | Sufficient detail         |
| Tested    | Validated in practice     |

---

## 4. Decision Extraction

### 4.1 ADR Template

```markdown
## Decision: [Title]

### Status

[Proposed | Accepted | Deprecated]

### Context

[Why decision was needed]

### Decision

[What was decided]

### Consequences

[+] Benefits
[-] Drawbacks
```
### 4.2 Capture Triggers

| Trigger              | Action             |
|----------------------|--------------------|
| Architecture choice  | Record ADR         |
| Trade-off made       | Document reasoning |
| Alternative rejected | Note why           |

---

## 5. Learning Extraction

### 5.1 From Mistakes

| Step  | Question         |
|-------|------------------|
| What  | What went wrong? |
| Why   | Root cause?      |
| How   | How to prevent?  |
| Apply | Update practices |

### 5.2 From Success

| Step  | Question          |
|-------|-------------------|
| What  | What worked well? |
| Why   | Why did it work?  |
| How   | How to replicate? |
| Apply | Document pattern  |

---

## 6. Best Practices

| Practice               | Benefit                 |
|------------------------|-------------------------|
| Extract early          | Capture while fresh     |
| Abstract appropriately | Balance detail vs reuse |
| Validate               | Test before documenting |
| Update                 | Revise with experience  |
| Share                  | Make accessible         |

---

## Related

- `.knowledge/practices/ai_collaboration/CONTEXT_MANAGEMENT.md` — Managing context
- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Documentation standards

---

*AI Collaboration Knowledge Base*
