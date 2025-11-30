# Incremental Improvement Practices

> Systematic approach to continuous, low-risk enhancement

---

## Table of Contents

- [1. Principles](#1-principles)
- [2. Improvement Cycle](#2-improvement-cycle)
- [3. Risk Management](#3-risk-management)
- [4. Validation](#4-validation)
- [5. Patterns](#5-patterns)
- [6. Anti-Patterns](#6-anti-patterns)

---

## 1. Principles

| Principle             | Description              | Anti-Pattern        |
|-----------------------|--------------------------|---------------------|
| Small steps           | Each change minimal      | Big bang releases   |
| Continuous validation | Test after every step    | Test only at end    |
| Always shippable      | Main branch deployable   | Long-lived branches |
| Learn and adapt       | Adjust based on feedback | Rigid adherence     |

### 1.1 Step Size Guidelines

| Change Type  | Size          | Validation     |
|--------------|---------------|----------------|
| Bug fix      | Single issue  | Unit test      |
| Refactor     | One pattern   | Existing tests |
| Feature      | Minimal slice | Feature test   |
| Optimization | One metric    | Benchmark      |

---

## 2. Improvement Cycle

### 2.1 PDCA Loop

```
Plan → Do → Check → Adjust → (repeat)
```
| Step   | Duration | Output          |
|--------|----------|-----------------|
| Plan   | 10-20%   | Scope, criteria |
| Do     | 40-50%   | Implementation  |
| Check  | 20-30%   | Validation      |
| Adjust | 10-20%   | Lessons learned |

### 2.2 Cycle Frequency

| Context         | Duration      | Batch Size   |
|-----------------|---------------|--------------|
| Rapid iteration | Minutes-Hours | 1-2 changes  |
| Standard dev    | Hours-Days    | 3-5 changes  |
| Migration       | Days-Weeks    | 5-10 changes |

---

## 3. Risk Management

### 3.1 Risk Matrix

| Impact / Likelihood | Low     | Medium | High     |
|---------------------|---------|--------|----------|
| High                | Medium  | High   | Critical |
| Medium              | Low     | Medium | High     |
| Low                 | Minimal | Low    | Medium   |

### 3.2 Mitigation by Level

| Risk     | Step Size | Validation   | Rollback |
|----------|-----------|--------------|----------|
| Minimal  | Normal    | Automated    | Standard |
| Low      | Normal    | +Spot check  | Standard |
| Medium   | Smaller   | +Peer review | Prepared |
| High     | Minimal   | +Staging     | Ready    |
| Critical | Atomic    | +Manual QA   | Instant  |

---

## 4. Validation

### 4.1 Continuous Validation

| After       | Type        | Scope            |
|-------------|-------------|------------------|
| Each edit   | Lint        | Changed files    |
| Each commit | Unit tests  | Affected modules |
| Each PR     | Integration | Full suite       |
| Each deploy | Smoke tests | Critical paths   |

### 4.2 Quality Gates

```
Edit → Lint ✓ → Commit → Tests ✓ → PR → Review ✓ → Merge
```
| Gate        | Criteria    | Block   |
|-------------|-------------|---------|
| Lint        | No errors   | Yes     |
| Unit tests  | 100% pass   | Yes     |
| Integration | 100% pass   | Yes     |
| Coverage    | > threshold | Warning |

---

## 5. Patterns

### 5.1 Feature Toggles

```python
if feature_enabled("new_algorithm"):
    return new_algorithm(data)
return old_algorithm(data)
```
**Benefits**: Deploy without releasing, gradual rollout, instant rollback.

### 5.2 Strangler Fig

| Phase | Action                      |
|-------|-----------------------------|
| 1     | Build new alongside old     |
| 2     | Route traffic incrementally |
| 3     | Remove old when complete    |

### 5.3 Branch by Abstraction

| Phase | Action                           |
|-------|----------------------------------|
| 1     | Create abstraction layer         |
| 2     | Implement new behind abstraction |
| 3     | Switch implementations           |
| 4     | Remove old implementation        |

---

## 6. Anti-Patterns

| Anti-Pattern  | Problem         | Solution              |
|---------------|-----------------|-----------------------|
| Big bang      | High risk       | Small increments      |
| Long branches | Merge conflicts | Trunk-based           |
| No validation | Hidden bugs     | Continuous testing    |
| Scope creep   | Never done      | Fixed scope per cycle |

---

## Related

- `.knowledge/practices/engineering/BATCH_OPTIMIZATION.md` — Batch processing
- `.knowledge/frameworks/patterns/COLLABORATION.md` — Collaboration patterns

---

*AI Collaboration Knowledge Base*
