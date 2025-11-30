# AI Autonomy Levels Framework

> 6-level autonomy spectrum for human-AI collaboration

---

## Table of Contents

- [1. Level Spectrum](#1-level-spectrum)
- [2. Level Details](#2-level-details)
- [3. Level Selection](#3-level-selection)
- [4. Calibration](#4-calibration)
- [5. Override Conditions](#5-override-conditions)
- [6. Implementation](#6-implementation)

---

## 1. Level Spectrum

| Level  | Name        | Range   | Behavior                       |
|--------|-------------|---------|--------------------------------|
| **L1** | Minimal     | 0-20%   | Ask before all changes         |
| **L2** | Low         | 20-40%  | Ask before significant changes |
| **L3** | Medium      | 40-60%  | Proceed routine, ask novel     |
| **L4** | Medium-High | 60-80%  | Proceed, report after          |
| **L5** | High        | 80-95%  | High autonomy, minimal checks  |
| **L6** | Full        | 95-100% | Full autonomy                  |

---

## 2. Level Details

### 2.1 L1-L2: Low Autonomy

| Aspect   | L1                | L2              |
|----------|-------------------|-----------------|
| Changes  | Ask all           | Ask significant |
| Scope    | Minimal           | Small           |
| Use case | New collaboration | Sensitive tasks |

### 2.2 L3-L4: Medium Autonomy

| Aspect    | L3                       | L4              |
|-----------|--------------------------|-----------------|
| Changes   | Routine proceed          | Most proceed    |
| Reporting | Ask novel                | Report after    |
| Use case  | Established relationship | Trusted routine |

### 2.3 L5-L6: High Autonomy

| Aspect   | L5              | L6               |
|----------|-----------------|------------------|
| Changes  | Most autonomous | Fully autonomous |
| Checks   | Minimal         | None             |
| Use case | Expert tasks    | Full delegation  |

---

## 3. Level Selection

| Context              | Recommended Level |
|----------------------|-------------------|
| New collaboration    | L2-L3             |
| Established trust    | L4-L5             |
| Production/sensitive | L1-L2             |
| Routine tasks        | L4-L5             |
| Sandbox/dev          | L5-L6             |
| Critical systems     | L1-L2             |

---

## 4. Calibration

### 4.1 Adjustment Rules

| Success Rate | Action               |
|--------------|----------------------|
| > 95%        | Upgrade +1 (max L5)  |
| 85-95%       | Maintain current     |
| 70-85%       | Downgrade -1         |
| < 70%        | Downgrade -2, review |

### 4.2 Reset Triggers

- Major errors or failures
- New problem domain
- Team composition change
- Extended absence (> 2 weeks)

---

## 5. Override Conditions

| Force Lower (L1-L2)    | Allow Higher (L5-L6)    |
|------------------------|-------------------------|
| Production deployments | Explicitly granted      |
| Database migrations    | Routine + well-tested   |
| Security-sensitive ops | Sandbox environments    |
| Irreversible actions   | Pipelines with rollback |
| Regulatory compliance  |                         |

---

## 6. Implementation

### 6.1 Setting Level

```yaml
# In task context
autonomy:
  level: L4
  reason: "Established trust, routine refactoring"
```
### 6.2 Reporting Format

| Level | Report Style            |
|-------|-------------------------|
| L1-L2 | Detailed, before action |
| L3-L4 | Summary, after action   |
| L5-L6 | Minimal, on completion  |

---

**Golden Rule**: Start conservative (L2-L3), increase gradually based on demonstrated success.

---

## Related

- `.knowledge/core/QUICK_REFERENCE.md` — Quick autonomy reference
- `.knowledge/practices/decisions/AUTONOMY_CASES.md` — Concrete examples
- `.knowledge/guidelines/AI_COLLABORATION.md` — Collaboration guidelines

---

*AI Collaboration Knowledge Base*
