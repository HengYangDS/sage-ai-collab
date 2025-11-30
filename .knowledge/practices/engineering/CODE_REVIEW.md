# Code Review Practices

> Effective code review patterns for quality and knowledge sharing

---

## Table of Contents

- [1. Review Goals](#1-review-goals)
- [2. Review Checklist](#2-review-checklist)
- [3. Review Process](#3-review-process)
- [4. Feedback Guidelines](#4-feedback-guidelines)
- [5. Author Responsibilities](#5-author-responsibilities)
- [6. Reviewer Responsibilities](#6-reviewer-responsibilities)
- [7. Review Size Guidelines](#7-review-size-guidelines)

---

## 1. Review Goals

| Goal        | Focus                            |
|-------------|----------------------------------|
| Correctness | Logic, edge cases, bugs          |
| Quality     | Style, patterns, maintainability |
| Security    | Vulnerabilities, data handling   |
| Learning    | Knowledge transfer, mentoring    |

---

## 2. Review Checklist

### 2.1 Functionality

- [ ] Logic is correct
- [ ] Edge cases handled
- [ ] Error cases covered
- [ ] Requirements met

### 2.2 Code Quality

- [ ] Names are clear
- [ ] Functions are focused
- [ ] No duplication
- [ ] Appropriate abstraction

### 2.3 Testing

- [ ] Tests exist
- [ ] Tests are meaningful
- [ ] Edge cases tested
- [ ] Coverage adequate

### 2.4 Documentation

- [ ] Public API documented
- [ ] Complex logic explained
- [ ] README updated if needed

---

## 3. Review Process

| Step | Action                              |
|------|-------------------------------------|
| 1    | Understand context (PR description) |
| 2    | Review high-level design            |
| 3    | Check implementation details        |
| 4    | Run/test if needed                  |
| 5    | Provide constructive feedback       |

---

## 4. Feedback Guidelines

### 4.1 Effective Feedback

| ✓ Do                 | ❌ Don't          |
|----------------------|------------------|
| Be specific          | Be vague         |
| Explain why          | Just say "wrong" |
| Suggest alternatives | Only criticize   |
| Ask questions        | Assume intent    |
| Be respectful        | Be dismissive    |

### 4.2 Comment Types

| Prefix        | Meaning            |
|---------------|--------------------|
| `nit:`        | Minor, optional    |
| `suggestion:` | Consider this      |
| `question:`   | Need clarification |
| `issue:`      | Must address       |
| `praise:`     | Good work          |

---

## 5. Author Responsibilities

| Before Review          | During Review           |
|------------------------|-------------------------|
| Self-review first      | Respond to all comments |
| Clear PR description   | Explain decisions       |
| Small, focused changes | Be open to feedback     |
| Tests included         | Update as needed        |

---

## 6. Reviewer Responsibilities

| Responsibility  | Action            |
|-----------------|-------------------|
| Timely review   | Within 24 hours   |
| Thorough review | Check all aspects |
| Constructive    | Help improve      |
| Available       | Answer follow-ups |

---

## 7. Review Size Guidelines

| Size      | Lines   | Review Time |
|-----------|---------|-------------|
| Small     | < 100   | 15 min      |
| Medium    | 100-300 | 30 min      |
| Large     | 300-500 | 1 hour      |
| Too Large | > 500   | Split PR    |

---

## Related

- `.knowledge/guidelines/quality.md` — Quality standards
- `.knowledge/guidelines/code_style.md` — Code style

---

*AI Collaboration Knowledge Base*
