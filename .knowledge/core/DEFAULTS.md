# Default Behaviors and Calibration

> Universal baseline behaviors and calibration parameters for AI collaboration

---

## Table of Contents

- [1. Loading Defaults](#1-loading-defaults)
- [2. Timeout Defaults](#2-timeout-defaults)
- [3. Autonomy Defaults](#3-autonomy-defaults)
- [4. Override Conditions](#4-override-conditions)
- [5. Response Structure](#5-response-structure)
- [6. Fallback Behavior](#6-fallback-behavior)

---

## 1. Loading Defaults

### 1.1 Recommended Parameters

| Parameter     | Typical Value                      | Purpose                |
|---------------|------------------------------------|------------------------|
| Max tokens    | 4000-8000                          | Context window budget  |
| Default layer | core                               | Always-load foundation |
| Preload files | index, principles, quick_reference | Essential context      |

### 1.2 Layer Budgets

| Layer      | Budget | Purpose       |
|------------|--------|---------------|
| core       | ~500   | Always loaded |
| guidelines | ~1200  | On-demand     |
| frameworks | ~2000  | On-demand     |
| practices  | ~1500  | On-demand     |
| scenarios  | ~500   | On-demand     |
| templates  | ~300   | On-demand     |

---

## 2. Timeout Defaults

### 2.1 Tiered Timeout Pattern

| Tier     | Typical Range | Operation Type                |
|----------|---------------|-------------------------------|
| Fast     | 50-200ms      | Cache lookup, memory access   |
| Standard | 200-1000ms    | Single file read, local I/O   |
| Extended | 1-5s          | Multi-file load, network call |
| Long     | 5-30s         | Full load, complex analysis   |

> **Note**: For project-specific timeout configurations, see your project's configuration files.

### 2.2 Circuit Breaker Defaults

| Parameter          | Typical Value   |
|--------------------|-----------------|
| Failure threshold  | 3-5 consecutive |
| Reset timeout      | 30-60s          |
| Half-open requests | 1-3             |

---

## 3. Autonomy Defaults

| Parameter        | Value                  |
|------------------|------------------------|
| Default level    | L4 (Medium-High)       |
| Initial level    | L3 (new collaboration) |
| Max auto-upgrade | L5                     |

### 3.1 Calibration Thresholds

| Success Rate | Action               |
|--------------|----------------------|
| > 95%        | Upgrade +1 (max L5)  |
| 85-95%       | Maintain             |
| 70-85%       | Downgrade -1         |
| < 70%        | Downgrade -2, review |

### 3.2 Reset Triggers

- Major errors
- New domain
- Team change
- Extended absence

---

## 4. Override Conditions

| Force Lower (L1-L2)    | Allow Higher (L5-L6)     |
|------------------------|--------------------------|
| Production deployments | Explicitly granted       |
| Database migrations    | Routine + tested         |
| Security-sensitive     | Sandbox/dev environments |
| Irreversible actions   | Pipelines with rollback  |
| Regulatory compliance  |                          |

---

## 5. Response Structure

```markdown
## Summary

[Brief outcome]

## Changes Made

[List of modifications]

## Verification

[How to verify]

## Next Steps

[Follow-up actions if applicable]
```

---

## 6. Fallback Behavior

| Situation      | Action               |
|----------------|----------------------|
| Timeout < 5s   | Return partial       |
| Timeout > 5s   | Return core only     |
| File not found | Return helpful error |
| Parse error    | Return raw content   |
| Network error  | Use cache            |

**Golden Rule**: Always return something useful, never hang or crash.

---

## Related

- `.knowledge/core/principles.md` — Core philosophy (Xin-Da-Ya)
- `.knowledge/core/quick_reference.md` — Quick reference card
- `.knowledge/frameworks/autonomy/levels.md` — Full autonomy framework
- `.knowledge/frameworks/resilience/timeout_patterns.md` — Timeout design patterns

---

*Part of SAGE Knowledge Base*
