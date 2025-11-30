# AI Collaboration Effectiveness Metrics

> Measuring and improving human-AI collaboration quality

---

## Table of Contents

- [1. Key Metrics](#1-key-metrics)
- [2. Measurement Methods](#2-measurement-methods)
- [3. Benchmarks](#3-benchmarks)
- [4. Improvement Actions](#4-improvement-actions)

---

## 1. Key Metrics

### Efficiency Metrics

| Metric | Formula | Target |
|:-------|:--------|:-------|
| Token Efficiency | Output value / Tokens used | High |
| Task Completion Rate | Completed / Attempted | >90% |
| Iteration Count | Rounds to completion | <5 |
| Time to First Value | Minutes to useful output | <10 |

### Quality Metrics

| Metric | Measure | Target |
|:-------|:--------|:-------|
| First-time Accuracy | Correct without revision | >80% |
| Code Quality | Lint/test pass rate | >95% |
| Documentation Coverage | Docs per feature | 100% |

---

## 2. Measurement Methods

### Session Tracking

```markdown
## Session Log: [DATE]
- Tokens used: [estimate]
- Tasks completed: [count]
- Iterations needed: [count]
- Blockers hit: [list]
```
### Weekly Review

| Question | Answer |
|:---------|:-------|
| Most efficient task type? | [type] |
| Biggest token waste? | [cause] |
| Improvement opportunity? | [action] |

---

## 3. Benchmarks

| Task Type | Token Budget | Iterations | Time |
|:----------|:-------------|:-----------|:-----|
| Bug fix | 500-1000 | 1-2 | 5-10min |
| New feature | 2000-5000 | 3-5 | 30-60min |
| Refactoring | 1500-3000 | 2-4 | 20-40min |
| Documentation | 500-1500 | 1-3 | 10-20min |

---

## 4. Improvement Actions

| Issue | Action |
|:------|:-------|
| High token usage | Use tiered loading |
| Many iterations | Clearer initial spec |
| Low accuracy | Add context/examples |
| Slow start | Use scenario presets |

---

## Related

- `.knowledge/practices/ai_collaboration/TOKEN_OPTIMIZATION.md` — Token optimization
- `.knowledge/practices/ai_collaboration/INTERACTION_PATTERNS.md` — Interaction patterns

---

*AI Collaboration Knowledge Base*
