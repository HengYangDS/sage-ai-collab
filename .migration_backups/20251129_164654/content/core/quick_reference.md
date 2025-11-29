# Quick Reference Card

> **Load Priority**: Always Load (~150 tokens)  
> **Purpose**: Critical questions and autonomy levels at a glance

---

## 🧠 5 Critical Questions

Before any significant decision or action, ask:

| # | Question                                  | Purpose                       |
|---|-------------------------------------------|-------------------------------|
| 1 | **What am I assuming?**                   | Surface hidden assumptions    |
| 2 | **What could go wrong?**                  | Identify risks and edge cases |
| 3 | **Is there a simpler way?**               | Avoid over-engineering        |
| 4 | **What will future maintainers need?**    | Ensure sustainability         |
| 5 | **How does this fit the bigger picture?** | Maintain coherence            |

---

## 🎚️ Autonomy Levels (1-6)

> **Reference**: See `content/frameworks/autonomy/levels.md` for full framework

| Level  | Name          | Authority | When to Use                             |
|--------|---------------|-----------|-----------------------------------------|
| **L1** | Minimal       | 0-20%     | Critical/unfamiliar tasks, onboarding   |
| **L2** | Low           | 20-40%    | New project phases, learning codebase   |
| **L3** | Medium        | 40-60%    | Routine development, clear guidelines   |
| **L4** | Medium-High ⭐ | 60-80%    | Mature collaboration, proactive partner |
| **L5** | High          | 80-95%    | Strategic partnership, trusted systems  |
| **L6** | Full          | 95-100%   | Autonomous agent (rarely recommended)   |

### Autonomy Selection Guide

```
Risk Level    Familiarity    → Recommended Level
───────────────────────────────────────────────
High          Low            → L1-L2
High          High           → L2-L3
Medium        Low            → L2-L3
Medium        High           → L3-L4
Low           Low            → L3-L4
Low           High           → L4-L5
```

---

## ⚡ Calibration Signals

### Increase Autonomy When:

- ✅ Consistent successful outcomes
- ✅ Clear, well-defined patterns
- ✅ Low-risk, reversible changes
- ✅ Strong test coverage exists

### Decrease Autonomy When:

- ⚠️ Errors or misunderstandings occur
- ⚠️ Entering unfamiliar territory
- ⚠️ High-impact or irreversible changes
- ⚠️ Ambiguous requirements

---

## 🎯 Decision Quick Check

```
┌─────────────────────────────────────┐
│ Is the requirement clear?           │
│   No  → Clarify first (L1-L2)       │
│   Yes ↓                             │
├─────────────────────────────────────┤
│ Is it reversible?                   │
│   No  → Extra caution (L1-L3)       │
│   Yes ↓                             │
├─────────────────────────────────────┤
│ Have we done this before?           │
│   No  → Learn mode (L2-L3)          │
│   Yes → Execute mode (L4-L5)        │
└─────────────────────────────────────┘
```

---

## 📋 Instruction Types

| Type           | Format          | Example                   |
|----------------|-----------------|---------------------------|
| **Directive**  | Do X            | "Implement feature Y"     |
| **Constraint** | Don't do X      | "Don't modify config"     |
| **Guideline**  | Prefer X over Y | "Prefer composition"      |
| **Context**    | Background info | "This is a legacy system" |
| **Goal**       | Outcome wanted  | "Improve performance"     |

---

## ⏱️ Timeout Quick Reference

| Operation | Default | Max   |
|-----------|---------|-------|
| Cache     | 100ms   | 200ms |
| File      | 500ms   | 1s    |
| Layer     | 2s      | 3s    |
| Full      | 5s      | 10s   |

**Rule**: Always return something, never hang.

---

*Keep this reference accessible during all collaboration sessions.*
