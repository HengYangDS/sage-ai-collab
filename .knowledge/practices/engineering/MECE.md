# MECE Principle

> Mutually Exclusive, Collectively Exhaustive — the foundation of clear categorization

---

## Table of Contents

- [1. Definition](#1-definition)
- [2. Application in SAGE](#2-application-in-sage)
- [3. Benefits](#3-benefits)
- [4. Anti-Patterns](#4-anti-patterns)
- [5. Validation Checklist](#5-validation-checklist)

## 1. Definition

**MECE** (Mutually Exclusive, Collectively Exhaustive) is a grouping principle that ensures:

| Property | Meaning | Validation |
|----------|---------|------------|
| **Mutually Exclusive** | No overlap between categories | Each item belongs to exactly one category |
| **Collectively Exhaustive** | Complete coverage | All possible items have a category |

---

## 2. Application in SAGE

### 2.1 Capability Families (5 Families)

| Family | Responsibility | Key Question |
|--------|---------------|--------------|
| **analyzers** | Analysis, diagnosis, graph | What is it? |
| **checkers** | Check, validate, verify | Is it correct? |
| **monitors** | Monitor, observe, alert | What's happening? |
| **converters** | Convert, migrate, adapt | How to transform? |
| **generators** | Generate, build, create | How to produce? |

### 2.2 Classification Decision Tree

```
New tool/capability arrives
    │
    ├── Does it analyze/diagnose? ──────────► analyzers/
    │
    ├── Does it validate/check? ────────────► checkers/
    │
    ├── Does it monitor/observe? ───────────► monitors/
    │
    ├── Does it convert/transform? ─────────► converters/
    │
    └── Does it generate/create? ───────────► generators/
```
### 2.3 Boundary Rules

| Rule | Description | Example |
|------|-------------|---------|
| **Single Responsibility** | One tool, one family | `link_checker.py` → checkers only |
| **Primary Function** | Classify by main purpose | Tool that checks then reports → checkers |
| **No Hybrids** | Split if dual purpose | analyzer+generator → 2 separate tools |

---

## 3. Benefits

1. **Predictable Location** — Know where to find things
2. **Clear Ownership** — Know who maintains what
3. **Reduced Confusion** — No "where should this go?" debates
4. **Scalable Structure** — Easy to add new items

---

## 4. Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `utils/` catch-all | Becomes dumping ground | Use specific families |
| `misc/` folder | Violates CE property | Classify properly |
| Overlapping categories | Violates ME property | Redefine boundaries |
| Missing category | Violates CE property | Add new family |

---

## 5. Validation Checklist

- [ ] Each item belongs to exactly one category (ME)
- [ ] All items have a home (CE)
- [ ] Categories have clear, non-overlapping definitions
- [ ] Decision tree has no ambiguous paths
- [ ] No `utils/`, `misc/`, `common/` escape hatches

---

## Related

- `.context/conventions/DIRECTORY_STRUCTURE.md` — Directory layout using MECE
- `.context/conventions/FOUR_LAYER_MODEL.md` — Architecture layers
- `docs/design/capabilities/INDEX.md` — Capability families

---

*AI Collaboration Knowledge Base*
