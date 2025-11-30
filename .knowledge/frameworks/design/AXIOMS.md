# Design Axioms Framework

> 8 foundational design principles (信达雅 applied to software design)

---

## Table of Contents

- [1. Core Axioms](#1-core-axioms)
- [2. Axiom Details](#2-axiom-details)
- [3. Architecture Application](#3-architecture-application)
- [4. Timeout Axiom](#4-timeout-axiom)
- [5. Extensibility Axiom](#5-extensibility-axiom)
- [6. Philosophy Mapping](#6-philosophy-mapping)

---

## 1. Core Axioms

| # | Axiom                  | Description                                 |
|---|------------------------|---------------------------------------------|
| 1 | MECE                   | Mutually Exclusive, Collectively Exhaustive |
| 2 | SSOT                   | Single Source of Truth                      |
| 3 | Progressive Disclosure | Overview → detail                           |
| 4 | Separation of Concerns | Content, code, config separated             |
| 5 | Fail-Fast              | No operation hangs indefinitely             |
| 6 | Plugin Extensibility   | Extension points for customization          |
| 7 | Zero Cross-Import      | Layers communicate via EventBus             |
| 8 | On-Demand Loading      | Minimal core, features loaded as needed     |

---

## 2. Axiom Details

### 2.1 MECE Principle

| Aspect           | Application                        |
|------------------|------------------------------------|
| Categories       | Non-overlapping, complete coverage |
| Responsibilities | Clear boundaries                   |
| Testing          | No gaps, no duplicates             |

### 2.2 Single Source of Truth

| Aspect        | Application              |
|---------------|--------------------------|
| Configuration | One place per setting    |
| Data          | Canonical source defined |
| Documentation | No duplication           |

### 2.3 Progressive Disclosure

| Level | Content        |
|-------|----------------|
| L1    | Quick summary  |
| L2    | Key details    |
| L3    | Full reference |
| L4    | Deep dive      |

### 2.4 Separation of Concerns

| Layer   | Responsibility           |
|---------|--------------------------|
| Content | Knowledge, documentation |
| Code    | Logic, processing        |
| Config  | Settings, parameters     |

---

## 3. Architecture Application

### 3.1 Layer Rules

| Layer    | Depends On | Never Depends On  |
|----------|------------|-------------------|
| Core     | Nothing    | Services, Plugins |
| Services | Core       | Other Services    |
| Plugins  | Core       | Services          |

### 3.2 Communication

```
Components → EventBus → Components
(No direct imports between layers)
```
---

## 4. Timeout Axiom

| Principle            | Implementation              |
|----------------------|-----------------------------|
| Fail-fast            | Every operation has timeout |
| Graceful degradation | Return partial over nothing |
| User feedback        | Always inform of status     |

---

## 5. Extensibility Axiom

| Hook Point  | Purpose                |
|-------------|------------------------|
| pre_load    | Before content loading |
| post_load   | After content loading  |
| on_timeout  | Timeout handling       |
| pre_search  | Before search          |
| post_search | After search           |

---

## 6. Philosophy Mapping

| Axiom                  | 信达雅 Alignment                     |
|------------------------|-----------------------------------|
| MECE                   | 信 (Faithful) — Complete, accurate |
| SSOT                   | 信 (Faithful) — Single truth       |
| Progressive Disclosure | 达 (Clear) — Accessible            |
| Separation of Concerns | 达 (Clear) — Organized             |
| Fail-Fast              | 雅 (Elegant) — Robust              |
| Plugin Extensibility   | 雅 (Elegant) — Flexible            |
| Zero Cross-Import      | 雅 (Elegant) — Clean               |
| On-Demand Loading      | 雅 (Elegant) — Efficient           |

---

## Related

- `.knowledge/core/PRINCIPLES.md` — 信达雅 philosophy
- `docs/design/01-architecture.md` — Architecture design

---

*AI Collaboration Knowledge Base*
