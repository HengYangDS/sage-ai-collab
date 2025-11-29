# Default Behaviors and Calibration

> Baseline behaviors and calibration parameters

---

## Table of Contents

[1. Loading Defaults](#1-loading-defaults) · [2. Timeout Defaults](#2-timeout-defaults) · [3. Autonomy Defaults](#3-autonomy-defaults) · [4. Override Conditions](#4-override-conditions) · [5. Response Structure](#5-response-structure) · [6. Fallback Behavior](#6-fallback-behavior)

---

## 1. Loading Defaults

| Parameter     | Value                                       | Config Location       |
|---------------|---------------------------------------------|-----------------------|
| Max tokens    | 4000                                        | `config/loading.yaml` |
| Default layer | core                                        | `config/loading.yaml` |
| Preload       | index.md, principles.md, quick_reference.md | `config/loading.yaml` |

### 1.1 Layer Budgets

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

| Tier | Timeout | Operation        |
|------|---------|------------------|
| T1   | 100ms   | Cache lookup     |
| T2   | 500ms   | Single file read |
| T3   | 2s      | Layer load       |
| T4   | 5s      | Full KB load     |
| T5   | 10s     | Complex analysis |

### 2.1 Circuit Breaker

| Parameter          | Value         |
|--------------------|---------------|
| Failure threshold  | 3 consecutive |
| Reset timeout      | 30s           |
| Half-open requests | 1             |

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

- `sage.yaml` — Main configuration
- `config/timeout.yaml` — Timeout settings
- `config/loading.yaml` — Loading settings
- `config/autonomy.yaml` — Autonomy settings
- `frameworks/autonomy/levels.md` — Full autonomy framework

---

*Part of SAGE Knowledge Base*
