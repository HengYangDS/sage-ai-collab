# Quick Reference Card

> Critical questions and autonomy levels at a glance

---

## Table of Contents

- [1. Five Critical Questions](#1-five-critical-questions)
- [2. Autonomy Levels](#2-autonomy-levels)
- [3. Response Structure](#3-response-structure)
- [4. Timeout Tiers](#4-timeout-tiers)
- [5. Philosophy Quick Check](#5-philosophy-quick-check)

---

## 1. Five Critical Questions

Ask before every task:

| # | Question                           | Purpose                |
|---|------------------------------------|------------------------|
| 1 | What assumptions am I making?      | Validate premises      |
| 2 | What could go wrong?               | Risk assessment        |
| 3 | Is there a simpler approach?       | Avoid over-engineering |
| 4 | Will this be maintainable?         | Long-term thinking     |
| 5 | How does this fit the big picture? | Context alignment      |

---

## 2. Autonomy Levels

| Level  | Name        | Range   | Behavior                       |
|--------|-------------|---------|--------------------------------|
| **L1** | Minimal     | 0-20%   | Ask before all changes         |
| **L2** | Low         | 20-40%  | Ask before significant changes |
| **L3** | Medium      | 40-60%  | Proceed routine, ask novel     |
| **L4** | Medium-High | 60-80%  | Proceed, report after          |
| **L5** | High        | 80-95%  | High autonomy, minimal checks  |
| **L6** | Full        | 95-100% | Full autonomy                  |

### 2.1 Level Selection

| Context              | Recommended |
|----------------------|-------------|
| New collaboration    | L2-L3       |
| Established trust    | L4-L5       |
| Production/sensitive | L1-L2       |
| Routine tasks        | L4-L5       |

### 2.2 Calibration

| Success Rate | Action               |
|--------------|----------------------|
| > 95%        | Upgrade +1 level     |
| 85-95%       | Maintain             |
| 70-85%       | Downgrade -1         |
| < 70%        | Downgrade -2, review |

---

## 3. Response Structure

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

## 4. Timeout Tiers

| Tier     | Typical Range | Use For                |
|----------|---------------|------------------------|
| Fast     | 50-200ms      | Cache, memory access   |
| Standard | 200-1000ms    | Single file, local I/O |
| Extended | 1-5s          | Multi-file, network    |
| Long     | 5-30s         | Full load, analysis    |

**Rule**: Always return something, never hang.

> See project configuration for specific timeout values.

---

## 5. Philosophy Quick Check

| Principle    | Question                       |
|--------------|--------------------------------|
| 信 (Faithful) | Is this correct?               |
| 达 (Clear)    | Is this understandable?        |
| 雅 (Elegant)  | Is this the simplest solution? |

---

## Related

- `.knowledge/core/PRINCIPLES.md` — Full philosophy
- `.knowledge/core/DEFAULTS.md` — Default behaviors
- `.knowledge/frameworks/autonomy/LEVELS.md` — Autonomy framework

---

*AI Collaboration Knowledge Base*
