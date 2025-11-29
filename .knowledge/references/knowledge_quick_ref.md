# Knowledge Organization Quick Reference

> Essential patterns for organizing AI-collaborative knowledge bases

---

## Layer Hierarchy

```
.knowledge/
├── core/           # Always load (~500 tokens)
├── guidelines/     # By role/task (~1200 tokens)
├── frameworks/     # On-demand (~2000 tokens)
├── practices/      # When implementing (~1500 tokens)
├── scenarios/      # By trigger (~500 tokens)
└── templates/      # Direct copy (~300 tokens)
```

---

## Layer Token Budgets

| Layer      | Budget | Load Timing    |
|------------|--------|----------------|
| Core       | ~500   | Always         |
| Guidelines | ~1200  | By role/task   |
| Frameworks | ~2000  | On-demand      |
| Practices  | ~1500  | Implementation |
| Scenarios  | ~500   | By trigger     |
| Templates  | ~300   | Direct use     |

---

## Navigation Pattern

```
[layer]/index.md → [layer]/[topic].md → [layer]/[topic]/[detail].md
```

---

## MECE Principle

| Aspect                  | Rule                      |
|-------------------------|---------------------------|
| Mutually Exclusive      | No overlapping content    |
| Collectively Exhaustive | Complete coverage         |
| Single location         | Each concept defined once |
| Cross-reference         | Link, don't duplicate     |

---

## Loading Strategy

| Phase            | Load       | Purpose        |
|------------------|------------|----------------|
| Session start    | Core       | Foundation     |
| Task definition  | Guidelines | Standards      |
| Complex decision | Frameworks | Deep reference |
| Implementation   | Practices  | Actionable     |
| Specific context | Scenario   | Pre-configured |

---

## Content Distribution

| Type       | Location      | Reference From |
|------------|---------------|----------------|
| Philosophy | `core/`       | All layers     |
| Standards  | `guidelines/` | Practices      |
| Concepts   | `frameworks/` | Guidelines     |
| How-to     | `practices/`  | Scenarios      |
| Presets    | `scenarios/`  | Index only     |

---

**Full Guide**: `practices/documentation/knowledge_organization.md`
