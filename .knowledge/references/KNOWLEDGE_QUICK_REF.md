# Knowledge Organization Quick Reference

> Essential patterns for organizing AI-collaborative knowledge bases

---

## Table of Contents

- [1. Layer Hierarchy](#1-layer-hierarchy)
- [2. Layer Token Budgets](#2-layer-token-budgets)
- [3. Navigation Pattern](#3-navigation-pattern)
- [4. MECE Principle](#4-mece-principle)
- [5. Loading Strategy](#5-loading-strategy)
- [6. Content Distribution](#6-content-distribution)

---

## 1. Layer Hierarchy

```text
.knowledge/
├── core/           # Always load (~500 tokens)
├── guidelines/     # By role/task (~1200 tokens)
├── frameworks/     # On-demand (~2000 tokens)
├── practices/      # When implementing (~1500 tokens)
├── scenarios/      # By trigger (~500 tokens)
└── templates/      # Direct copy (~300 tokens)
```
---

## 2. Layer Token Budgets

| Layer      | Budget | Load Timing    |
|------------|--------|----------------|
| Core       | ~500   | Always         |
| Guidelines | ~1200  | By role/task   |
| Frameworks | ~2000  | On-demand      |
| Practices  | ~1500  | Implementation |
| Scenarios  | ~500   | By trigger     |
| Templates  | ~300   | Direct use     |

---

## 3. Navigation Pattern

```text
[layer]/INDEX.md → [layer]/[topic].md → [layer]/[topic]/[detail].md
```
---

## 4. MECE Principle

| Aspect                  | Rule                      |
|-------------------------|---------------------------|
| Mutually Exclusive      | No overlapping content    |
| Collectively Exhaustive | Complete coverage         |
| Single location         | Each concept defined once |
| Cross-reference         | Link, don't duplicate     |

---

## 5. Loading Strategy

| Phase            | Load       | Purpose        |
|------------------|------------|----------------|
| Session start    | Core       | Foundation     |
| Task definition  | Guidelines | Standards      |
| Complex decision | Frameworks | Deep reference |
| Implementation   | Practices  | Actionable     |
| Specific context | Scenario   | Pre-configured |

---

## 6. Content Distribution

| Type       | Location      | Reference From |
|------------|---------------|----------------|
| Philosophy | `core/`       | All layers     |
| Standards  | `guidelines/` | Practices      |
| Concepts   | `frameworks/` | Guidelines     |
| How-to     | `practices/`  | Scenarios      |
| Presets    | `scenarios/`  | Index only     |

---

## Related

- `.knowledge/practices/documentation/KNOWLEDGE_ORGANIZATION.md` — Full organization guide
- `.knowledge/INDEX.md` — Knowledge base navigation
- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Documentation standards
- `.knowledge/references/GLOSSARY.md` — Terminology glossary

---

*AI Collaboration Knowledge Base*
