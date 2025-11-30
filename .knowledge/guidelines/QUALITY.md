# Quality Assurance Guidelines

> Quality metrics, review processes, continuous improvement

---

## Table of Contents

- [1. Quality Dimensions](#1-quality-dimensions)
- [2. Code Quality Metrics](#2-code-quality-metrics)
- [3. Review Process](#3-review-process)
- [4. Testing Strategy](#4-testing-strategy)
- [5. Continuous Improvement](#5-continuous-improvement)
- [6. Quality Checklist](#6-quality-checklist)

---

## 1. Quality Dimensions

| Dimension       | Description          | Measure            |
|-----------------|----------------------|--------------------|
| Correctness     | Works as intended    | Tests pass         |
| Completeness    | All requirements met | Coverage           |
| Clarity         | Understandable       | Review feedback    |
| Efficiency      | Optimal performance  | Benchmarks         |
| Maintainability | Easy to modify       | Complexity metrics |

---

## 2. Code Quality Metrics

| Metric                | Target      | Tool       |
|-----------------------|-------------|------------|
| Test coverage         | > 80%       | pytest-cov |
| Cyclomatic complexity | < 10        | radon      |
| Function length       | < 50 lines  | pylint     |
| File length           | < 500 lines | wc         |
| Type hint coverage    | > 80%       | mypy       |

---

## 3. Review Process

### 3.1 Self-Review Checklist

- [ ] Code compiles/runs without errors
- [ ] Tests pass
- [ ] No obvious bugs
- [ ] Names are clear
- [ ] Logic is understandable
- [ ] Edge cases handled

### 3.2 Peer Review Focus

| Reviewer Checks   | Author Prepares       |
|-------------------|-----------------------|
| Logic correctness | Clear PR description  |
| Edge cases        | Test coverage         |
| Code style        | Self-review completed |
| Performance       | Context for decisions |

---

## 4. Testing Strategy

### 4.1 Test Pyramid

| Level       | Coverage       | Focus                 |
|-------------|----------------|-----------------------|
| Unit        | 80%+           | Individual functions  |
| Integration | Key paths      | Component interaction |
| E2E         | Critical flows | User journeys         |

### 4.2 Test Quality

```python
# ✓ Good: Arrange-Act-Assert
def test_user_creation():
    # Arrange
    data = {"name": "Alice"}

    # Act
    result = service.create(data)

    # Assert
    assert result.name == "Alice"
```
---

## 5. Continuous Improvement

### 5.1 Feedback Loops

| Loop           | Frequency    | Action                   |
|----------------|--------------|--------------------------|
| Tests          | Every commit | Fix failures immediately |
| Reviews        | Every PR     | Address feedback         |
| Retrospectives | Weekly       | Process improvements     |
| Metrics        | Monthly      | Trend analysis           |

### 5.2 Technical Debt

| Priority | Timeline     | Action          |
|----------|--------------|-----------------|
| Critical | This sprint  | Fix immediately |
| High     | This month   | Schedule fix    |
| Medium   | This quarter | Plan fix        |
| Low      | Backlog      | Track           |

---

## 6. Quality Checklist

| Phase       | Actions                                                  |
|-------------|----------------------------------------------------------|
| **Daily**   | Tests before commit, self-review, update docs            |
| **Weekly**  | Coverage reports, dependency updates, share learnings    |
| **Monthly** | Complexity analysis, performance review, debt assessment |

---

## Related

- `.knowledge/practices/engineering/CODE_REVIEW.md` — Code review practices
- `.knowledge/practices/engineering/TESTING_STRATEGY.md` — Testing strategies
- `.knowledge/guidelines/ENGINEERING.md` — Engineering practices
- `.knowledge/frameworks/patterns/DECISION.md` — Decision quality framework

---

*AI Collaboration Knowledge Base*
