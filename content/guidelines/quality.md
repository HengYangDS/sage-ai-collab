# Quality Assurance Guidelines

> **Load Time**: On-demand (~150 tokens)  
> **Purpose**: Quality metrics, review processes, continuous improvement

---

## 8.1 Quality Dimensions

### The Quality Triangle

```
        Correctness
           /\
          /  \
         /    \
        /      \
       /________\
Maintainability  Performance
```

### Quality Metrics

| Dimension           | Metrics                            | Target                          |
|---------------------|------------------------------------|---------------------------------|
| **Correctness**     | Test coverage, bug rate            | >80% coverage, <1 bug/KLOC      |
| **Maintainability** | Cyclomatic complexity, duplication | <10 complexity, <3% duplication |
| **Performance**     | Response time, throughput          | <200ms P95, >1000 RPS           |
| **Security**        | Vulnerability count, audit score   | 0 critical, >90% score          |
| **Reliability**     | Uptime, MTTR                       | >99.9%, <15min MTTR             |

---

## 8.2 Code Review Standards

### Review Checklist

```markdown
## Code Review Checklist

### Correctness

- [ ] Logic is correct and complete
- [ ] Edge cases are handled
- [ ] Error handling is appropriate

### Code Quality

- [ ] Follows style guidelines
- [ ] No code duplication
- [ ] Names are clear and consistent

### Testing

- [ ] Tests cover new functionality
- [ ] Tests cover edge cases
- [ ] All tests pass

### Security

- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] No SQL injection risks

### Documentation

- [ ] Public APIs documented
- [ ] Complex logic explained
- [ ] README updated if needed
```

### Review Feedback Guidelines

| Type         | Prefix         | Example                   |
|--------------|----------------|---------------------------|
| Must fix     | `[REQUIRED]`   | Security vulnerability    |
| Should fix   | `[SUGGESTION]` | Better approach available |
| Nice to have | `[NIT]`        | Minor style preference    |
| Question     | `[QUESTION]`   | Seeking clarification     |
| Praise       | `[PRAISE]`     | Well-done aspect          |

---

## 8.3 Testing Strategy

### Test Coverage Goals

| Test Type   | Coverage Target | Focus                  |
|-------------|-----------------|------------------------|
| Unit        | >80%            | Business logic         |
| Integration | >60%            | Component interactions |
| E2E         | Critical paths  | User journeys          |

### Test Quality Criteria

```python
# GOOD: Clear, focused, maintainable test
def test_user_creation_with_valid_data_returns_user():
    # Arrange
    service = UserService(mock_repo)
    valid_data = {"name": "Alice", "email": "alice@example.com"}
    
    # Act
    result = service.create(valid_data)
    
    # Assert
    assert result.name == "Alice"
    assert result.email == "alice@example.com"
    assert mock_repo.save.called_once()

# BAD: Multiple concerns, unclear purpose
def test_user():
    # Tests creation, update, delete all in one
    # Hard to understand what's being tested
```

---

## 8.4 Quality Gates

### Pre-Commit Gates

- [ ] Linting passes (no errors)
- [ ] Formatting correct
- [ ] Type checking passes
- [ ] Unit tests pass

### Pre-Merge Gates

- [ ] All tests pass (unit, integration)
- [ ] Code review approved
- [ ] Coverage maintained or improved
- [ ] No security vulnerabilities
- [ ] Documentation updated

### Pre-Release Gates

- [ ] E2E tests pass
- [ ] Performance benchmarks met
- [ ] Security scan clean
- [ ] Changelog updated
- [ ] Version bumped

---

## 8.5 Continuous Improvement

### Retrospective Questions

1. What went well?
2. What could be improved?
3. What will we try differently?

### Quality Debt Tracking

| Category      | Example              | Priority |
|---------------|----------------------|----------|
| Technical     | Missing tests        | Medium   |
| Documentation | Outdated README      | Low      |
| Security      | Unpatched dependency | High     |
| Performance   | Slow query           | Medium   |

### Improvement Metrics

```
Track over time:
- Defect escape rate (bugs found in production)
- Mean time to resolution
- Code review turnaround time
- Test coverage trend
- Technical debt ratio
```

---

## 8.6 Quality Culture

### Principles

1. **Quality is everyone's responsibility**
2. **Prevention over detection**
3. **Continuous improvement**
4. **Measure what matters**
5. **Celebrate quality wins**

### Anti-Patterns to Avoid

| Anti-Pattern         | Problem                  | Better Approach              |
|----------------------|--------------------------|------------------------------|
| "Ship and fix"       | Quality debt accumulates | Build quality in from start  |
| "Not my code"        | Ownership gaps           | Collective ownership         |
| "Tests slow us down" | Short-term thinking      | Tests enable speed long-term |
| "Good enough"        | Gradual degradation      | Maintain standards           |

---

## 8.7 Quick Quality Reference

### Daily Quality Habits

- [ ] Run tests before committing
- [ ] Review own code before PR
- [ ] Update docs with code changes
- [ ] Address review feedback promptly

### Weekly Quality Habits

- [ ] Review test coverage reports
- [ ] Check for dependency updates
- [ ] Address technical debt items
- [ ] Share quality learnings

---

*Part of AI Collaboration Knowledge Base v2.0.0*
