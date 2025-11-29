# Autonomy Decision Cases

> **Load Time**: On-demand (~200 tokens)  
> **Purpose**: Concrete examples for autonomy level decisions  
> **Reference**: See [Autonomy Levels Framework](../../frameworks/autonomy/levels.md) for theory

---

## Overview

This document provides real-world examples of autonomy level decisions across different scenarios. Use these cases to calibrate AI autonomy in your projects.

---

## Case Categories

1. [Code Changes](#1-code-changes)
2. [Configuration & Infrastructure](#2-configuration--infrastructure)
3. [Documentation](#3-documentation)
4. [Testing](#4-testing)
5. [Security & Sensitive Operations](#5-security--sensitive-operations)
6. [Architecture & Design](#6-architecture--design)

---

## 1. Code Changes

### L5-L6: High Autonomy (Proceed Independently)

| Scenario | Autonomy | Rationale |
|----------|----------|-----------|
| Fix typo in variable name | L6 | Trivial, no semantic change |
| Add missing type hints | L5 | Improves quality, no behavior change |
| Format code with configured linter | L6 | Automated, reversible |
| Add docstring to undocumented function | L5 | Documentation only |
| Remove unused imports | L5 | Safe cleanup, tools verify |
| Rename local variable for clarity | L5 | Scope limited, improves readability |

### L3-L4: Medium Autonomy (Proceed, Report After)

| Scenario | Autonomy | Rationale |
|----------|----------|-----------|
| Refactor function to reduce complexity | L4 | Behavior preserved, tests verify |
| Add error handling to existing function | L4 | Improves robustness |
| Extract method from long function | L4 | Standard refactoring pattern |
| Update deprecated API usage | L3 | May affect behavior, needs verification |
| Add logging statements | L4 | Observability improvement |
| Optimize loop performance | L3 | Behavior should be same, verify with tests |

### L1-L2: Low Autonomy (Ask Before Changes)

| Scenario | Autonomy | Rationale |
|----------|----------|-----------|
| Change public API signature | L1 | Breaking change, affects consumers |
| Modify business logic | L2 | Core functionality, needs validation |
| Add new dependency | L2 | Project-wide impact |
| Change database schema | L1 | Data migration required |
| Modify authentication flow | L1 | Security critical |
| Remove existing feature | L1 | User-facing impact |

---

## 2. Configuration & Infrastructure

### L5-L6: High Autonomy

| Scenario | Autonomy | Rationale |
|----------|----------|-----------|
| Update .gitignore patterns | L5 | Low risk, reversible |
| Add editor config settings | L6 | Developer tooling only |
| Update linter rules (non-breaking) | L5 | Quality improvement |
| Add pre-commit hook | L4-L5 | Improves workflow |

### L3-L4: Medium Autonomy

| Scenario | Autonomy | Rationale |
|----------|----------|-----------|
| Update CI pipeline steps | L3 | May affect deployment |
| Modify Docker configuration | L3 | Environment impact |
| Change logging configuration | L4 | Observability change |
| Update dependency versions (minor) | L4 | Usually safe, verify tests |

### L1-L2: Low Autonomy

| Scenario | Autonomy | Rationale |
|----------|----------|-----------|
| Change production environment config | L1 | Live system impact |
| Modify secrets management | L1 | Security critical |
| Update major dependency version | L2 | Breaking changes possible |
| Change deployment strategy | L1 | Operational risk |

---

## 3. Documentation

### L5-L6: High Autonomy

| Scenario | Autonomy | Rationale |
|----------|----------|-----------|
| Fix typos in documentation | L6 | No semantic change |
| Update code examples to match code | L5 | Accuracy improvement |
| Add missing README sections | L5 | Completeness |
| Format markdown consistently | L6 | Style only |
| Add inline code comments | L5 | Clarity improvement |

### L3-L4: Medium Autonomy

| Scenario | Autonomy | Rationale |
|----------|----------|-----------|
| Rewrite unclear documentation | L4 | May change meaning |
| Add architecture diagrams | L4 | New content, review helpful |
| Update API documentation | L3 | Must match implementation |
| Create new guide or tutorial | L3 | New content, needs review |

### L1-L2: Low Autonomy

| Scenario | Autonomy | Rationale |
|----------|----------|-----------|
| Change license information | L1 | Legal implications |
| Modify contributing guidelines | L2 | Community impact |
| Update security documentation | L1 | Critical information |
| Change project vision/goals | L1 | Strategic decision |

---

## 4. Testing

### L5-L6: High Autonomy

| Scenario | Autonomy | Rationale |
|----------|----------|-----------|
| Add test for uncovered code path | L5 | Improves coverage |
| Fix flaky test | L5 | Reliability improvement |
| Add assertion to existing test | L5 | Strengthens validation |
| Improve test naming | L6 | Clarity only |

### L3-L4: Medium Autonomy

| Scenario | Autonomy | Rationale |
|----------|----------|-----------|
| Refactor test structure | L4 | May affect coverage |
| Add integration test | L4 | New validation |
| Update test fixtures | L3 | May affect multiple tests |
| Add performance test | L3 | New test category |

### L1-L2: Low Autonomy

| Scenario | Autonomy | Rationale |
|----------|----------|-----------|
| Remove existing test | L1 | Reduces coverage |
| Change test assertions (weaker) | L1 | May hide bugs |
| Skip/disable test | L2 | Technical debt |
| Modify test data with PII | L1 | Privacy implications |

---

## 5. Security & Sensitive Operations

### Always L1: Requires Explicit Approval

| Scenario | Rationale |
|----------|-----------|
| Modify authentication logic | Security critical |
| Change authorization rules | Access control |
| Update encryption methods | Data protection |
| Modify input validation | Vulnerability prevention |
| Change password policies | User security |
| Update CORS settings | Security boundary |
| Modify rate limiting | Abuse prevention |
| Change audit logging | Compliance |

---

## 6. Architecture & Design

### L3-L4: Medium Autonomy

| Scenario | Autonomy | Rationale |
|----------|----------|-----------|
| Add new utility module | L4 | Isolated addition |
| Create helper function | L4 | Reusability improvement |
| Implement design pattern | L3 | Structural change |
| Add new internal service | L3 | Component addition |

### L1-L2: Low Autonomy

| Scenario | Autonomy | Rationale |
|----------|----------|-----------|
| Change system architecture | L1 | Fundamental design |
| Add new external dependency | L2 | Long-term maintenance |
| Create new public API | L1 | Contract commitment |
| Change data model | L1 | Schema migration |
| Introduce new technology | L1 | Team expertise needed |

---

## Decision Flowchart

```
Is it security-related?
├── Yes → L1 (Always ask)
└── No ↓

Is it a breaking change?
├── Yes → L1-L2 (Ask before)
└── No ↓

Does it change behavior?
├── Yes ↓
│   Can tests verify correctness?
│   ├── Yes → L3-L4 (Proceed, report)
│   └── No → L2 (Ask before)
└── No ↓

Is it easily reversible?
├── Yes → L5-L6 (High autonomy)
└── No → L3-L4 (Medium autonomy)
```

---

## Calibration Tips

1. **Start Conservative**: Begin with lower autonomy, increase as trust builds
2. **Document Decisions**: Record why specific autonomy levels were chosen
3. **Review Periodically**: Adjust levels based on outcomes
4. **Context Matters**: Same action may need different levels in different projects
5. **When in Doubt**: Choose lower autonomy level

---

## Project-Specific Overrides

Add your project-specific autonomy overrides here:

```yaml
# Example: .junie/autonomy_overrides.yaml
overrides:
  # Elevate for trusted patterns
  - pattern: "tests/**/*.py"
    operation: "add_test"
    level: L5
    reason: "Well-tested test patterns"
  
  # Lower for sensitive areas
  - pattern: "src/auth/**"
    operation: "*"
    level: L1
    reason: "Security-critical module"
```

---

**See Also**:
- [Autonomy Levels Framework](../../frameworks/autonomy/levels.md) - Full 6-level spectrum
- [AI Collaboration Guidelines](../../guidelines/ai_collaboration.md) - Collaboration patterns
- [Expert Committee Templates](../../templates/expert_committee.md) - Decision prompts
