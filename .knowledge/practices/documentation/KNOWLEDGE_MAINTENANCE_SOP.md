# Knowledge Base Maintenance SOP

> Standard operating procedures for maintaining .knowledge directory

---

## Table of Contents

- [1. Daily Tasks](#1-daily-tasks)
- [2. Weekly Tasks](#2-weekly-tasks)
- [3. Monthly Tasks](#3-monthly-tasks)
- [4. Quarterly Review](#4-quarterly-review)
- [5. Issue Resolution](#5-issue-resolution)

---

## 1. Daily Tasks

| Task | Action | Tool |
|:-----|:-------|:-----|
| Check validation | Run `python scripts/validate_knowledge.py` | Script |
| Review changes | `git diff .knowledge/` | Git |
| Fix broken links | Update paths immediately | Manual |

---

## 2. Weekly Tasks

| Task | Action |
|:-----|:-------|
| Content audit | Review 5-10 random documents for accuracy |
| Token check | Verify files stay under limits |
| Index sync | Ensure INDEX.md files match actual content |

---

## 3. Monthly Tasks

| Task | Action |
|:-----|:-------|
| Full validation | Run complete validation suite |
| Stale content | Archive outdated documents |
| Gap analysis | Identify missing documentation |
| Cross-reference | Verify Related links work |

---

## 4. Quarterly Review

### Review Checklist

- [ ] Run L5 Expert Committee review
- [ ] Update version numbers
- [ ] Archive deprecated content
- [ ] Update file counts in indexes
- [ ] Review and update Token budgets
- [ ] Check for redundant content

---

## 5. Issue Resolution

### Common Issues

| Issue | Resolution |
|:------|:-----------|
| Broken link | Update path or remove reference |
| Oversized file | Split into multiple documents |
| Stale content | Update or archive |
| Duplicate content | Merge and redirect |

### Escalation Path

1. Self-fix if < 5 minutes
2. Create issue if complex
3. Discuss in quarterly review if systemic

---

## Related

- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Writing standards
- `.knowledge/practices/documentation/KNOWLEDGE_ORGANIZATION.md` — Organization guide
- `scripts/validate_knowledge.py` — Validation script

---

*AI Collaboration Knowledge Base*
