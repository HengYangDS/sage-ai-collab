# Engineering Practices Guidelines

> Configuration, testing, performance, change control, maintainability

---

## 1. Configuration Management

| Principle | Application |
|-----------|-------------|
| Environment separation | dev/staging/prod configs |
| Secrets management | Never in code, use env vars |
| Validation | Validate config at startup |
| Defaults | Sensible defaults, explicit overrides |

### 1.1 Config Priority

```
Environment vars > Config files > Defaults
```

---

## 2. Testing Strategy

### 2.1 Test Pyramid

| Level | Coverage | Speed | Focus |
|-------|----------|-------|-------|
| Unit | 80%+ | Fast | Logic |
| Integration | Key paths | Medium | Contracts |
| E2E | Critical flows | Slow | User journeys |

### 2.2 Test Principles

| Principle | Description |
|-----------|-------------|
| Isolation | Tests don't affect each other |
| Deterministic | Same input → same result |
| Fast | Quick feedback loop |
| Readable | Test as documentation |

---

## 3. Performance

### 3.1 Guidelines

| Area | Target |
|------|--------|
| Response time | < 200ms (p95) |
| Memory | Monitor growth |
| Caching | Cache expensive operations |
| Async | Use for I/O-bound tasks |

### 3.2 Optimization Process

```
Measure → Profile → Optimize → Verify
```

**Rule**: Never optimize without profiling first.

---

## 4. Change Control

### 4.1 Change Categories

| Category | Process |
|----------|---------|
| Trivial | Direct commit, self-review |
| Standard | PR, single reviewer |
| Significant | PR, multiple reviewers |
| Critical | PR, team review, staged rollout |

### 4.2 PR Checklist

- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or noted)
- [ ] Performance impact assessed

---

## 5. Maintainability

### 5.1 Technical Debt

| Priority | Action |
|----------|--------|
| High | Fix in current sprint |
| Medium | Schedule within month |
| Low | Track, address opportunistically |

### 5.2 Code Health

| Metric | Target |
|--------|--------|
| Test coverage | > 80% |
| Cyclomatic complexity | < 10 |
| File length | < 500 lines |
| Function length | < 50 lines |

---

## 6. Workflow Checklist

| Phase | Actions |
|-------|---------|
| **Start** | Understand requirements, identify risks |
| **During** | Tests alongside code, incremental changes |
| **Merge** | Tests pass, review approved, docs updated |

---

*Part of SAGE Knowledge Base*
