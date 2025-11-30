# Quarterly L5 Review Process

> Standard process for quarterly knowledge base expert committee review

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Schedule](#2-schedule)
- [3. Pre-Review Checklist](#3-pre-review-checklist)
- [4. Review Process](#4-review-process)
- [5. Post-Review Actions](#5-post-review-actions)

---

## 1. Overview

| Item | Description |
|:-----|:------------|
| **Frequency** | Quarterly (Q1: Jan, Q2: Apr, Q3: Jul, Q4: Oct) |
| **Level** | L5 Full Committee (24 Experts) |
| **Duration** | 1-2 sessions |
| **Output** | Review report + Action items |

---

## 2. Schedule

| Quarter | Review Month | Deadline |
|:--------|:-------------|:---------|
| Q1 | January | Jan 15 |
| Q2 | April | Apr 15 |
| Q3 | July | Jul 15 |
| Q4 | October | Oct 15 |

---

## 3. Pre-Review Checklist

### One Week Before

- [ ] Run `python scripts/validate_knowledge.py`
- [ ] Fix all errors (0 errors required)
- [ ] Review warning count trend
- [ ] Update VERSION.md changelog
- [ ] Prepare metrics summary

### Metrics to Gather

| Metric | Source |
|:-------|:-------|
| File count | Validation script |
| Error count | Validation script |
| Warning count | Validation script |
| New files since last review | Git log |
| Modified files | Git log |

---

## 4. Review Process

### Step 1: Invoke Expert Committee

```markdown
召集 Level 5 专家委员会，评审 .knowledge
要求评审前，先阅读文档写作及配置文件相关规范、标准等
```
### Step 2: Expert Groups

| Group | Focus Areas |
|:------|:------------|
| Architecture | Structure, scalability, consistency |
| Knowledge | Content, density, discoverability |
| AI Collaboration | Token efficiency, session management |
| Engineering | Code standards, testing, security |

### Step 3: Scoring

| Rating | Score | Action |
|:-------|:------|:-------|
| Excellent | 90-100 | Minor improvements |
| Good | 80-89 | Standard improvements |
| Acceptable | 70-79 | Priority improvements |
| Needs Work | <70 | Immediate action required |

---

## 5. Post-Review Actions

### Immediate (Week 1)

- [ ] Document review findings
- [ ] Create action items for P1 issues
- [ ] Update VERSION.md with review date

### Short-term (Month 1)

- [ ] Complete P1 improvements
- [ ] Plan P2 improvements
- [ ] Re-run validation

### Before Next Review

- [ ] Complete P2 improvements
- [ ] Address P3 as time permits
- [ ] Prepare next review metrics

---

## Related

- `.knowledge/templates/EXPERT_COMMITTEE.md` — Committee template
- `.knowledge/practices/documentation/KNOWLEDGE_MAINTENANCE_SOP.md` — Maintenance SOP
- `.knowledge/VERSION.md` — Version tracking

---

*AI Collaboration Knowledge Base*
