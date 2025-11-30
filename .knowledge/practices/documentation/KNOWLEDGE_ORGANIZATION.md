# Knowledge Organization Patterns

> Hierarchical patterns for organizing AI-collaborative knowledge bases

---

## Table of Contents

- [1. Layer Architecture](#1-layer-architecture)
- [2. Layer Principles](#2-layer-principles)
- [3. Navigation Patterns](#3-navigation-patterns)
- [4. Content Distribution](#4-content-distribution)
- [5. Loading Strategy](#5-loading-strategy)

---

## 1. Layer Architecture

### 1.1 Standard Hierarchy

```text
.knowledge/
├── core/           # Foundational principles (always load)
├── guidelines/     # Standards and conventions (by role/task)
├── frameworks/     # Deep conceptual models (complex decisions)
├── practices/      # Actionable patterns (implementation)
├── references/     # Quick reference, glossary (on-demand)
├── scenarios/      # Context presets (specific workflows)
└── templates/      # Ready-to-use templates (direct use)
```
### 1.2 Layer Characteristics

| Layer          | Depth            | Load Timing       | Token Budget |
|----------------|------------------|-------------------|--------------|
| **Core**       | Minimal          | Always            | ~500         |
| **Guidelines** | Medium           | By role/task      | ~1,200       |
| **Frameworks** | Deep             | On-demand         | ~2,000       |
| **Practices**  | Actionable       | When implementing | ~1,500       |
| **References** | Quick lookup     | On-demand         | ~300         |
| **Scenarios**  | Context-specific | By trigger        | ~500         |
| **Templates**  | Ready-to-use     | Direct copy       | ~300         |

---

## 2. Layer Principles

### 2.1 Core Layer

| Principle         | Application                 |
|-------------------|-----------------------------|
| Essential only    | No nice-to-have content     |
| Always relevant   | Applies to all contexts     |
| Highly compressed | Maximum information density |
| Stable            | Rarely changes              |

**Contents**: Philosophy, critical questions, default behaviors

### 2.2 Guidelines Layer

| Principle        | Application                   |
|------------------|-------------------------------|
| Role-indexed     | Organized by audience         |
| Task-oriented    | "How to" focus                |
| Moderate detail  | Balanced depth                |
| Cross-referenced | Links to frameworks/practices |

**Contents**: Code style, engineering standards, collaboration patterns

### 2.3 Frameworks Layer

| Principle           | Application            |
|---------------------|------------------------|
| Theory-complete     | Full conceptual models |
| Deep understanding  | Why, not just how      |
| Reference material  | Look up when needed    |
| Standalone sections | Can load portions      |

**Contents**: Autonomy levels, expert committee, design axioms

### 2.4 Practices Layer

| Principle        | Application            |
|------------------|------------------------|
| Actionable       | Clear steps to follow  |
| Code examples    | Show, don't just tell  |
| Pattern-based    | Reusable solutions     |
| Problem-oriented | Organized by challenge |

**Contents**: Error handling, API design, testing strategies

### 2.5 Scenarios Layer

| Principle        | Application               |
|------------------|---------------------------|
| Context-specific | Tailored to workflows     |
| Pre-configured   | Ready-to-use settings     |
| Trigger-based    | Auto-load by keywords     |
| Composable       | Combine with other layers |

**Contents**: Python backend, frontend dev, data pipelines

### 2.6 Templates Layer

| Principle           | Application                |
|---------------------|----------------------------|
| Copy-paste ready    | Minimal modification       |
| Placeholder markers | Clear customization points |
| Self-contained      | No external dependencies   |
| Versioned           | Track template evolution   |

**Contents**: Project setup, decision records, review templates

---

## 3. Navigation Patterns

### 3.1 Path Structure

```text
[layer]/INDEX.md → [layer]/[topic].md → [layer]/[topic]/[detail].md
```
### 3.2 Index File Pattern

Each layer has an `INDEX.md` with:

| Section          | Purpose                          |
|------------------|----------------------------------|
| Contents table   | List all files with descriptions |
| By use case      | Alternative navigation by need   |
| Quick start path | Recommended reading order        |
| Related          | Links to adjacent layers         |

### 3.3 Cross-Reference Design

| Element         | Format             | Example                 |
|-----------------|--------------------|-------------------------|
| Related section | Unnumbered, at end | `## Related`            |
| Link format     | Path + description | `PATH.md` — Description |
| Link count      | 3-5 per document   | Balance coverage/noise  |
| Priority        | Same layer first   | Then adjacent layers    |

### 3.4 Anchor Conventions

| Element    | Format                | Example             |
|------------|-----------------------|---------------------|
| H2 anchor  | `#N-section-name`     | `#1-overview`       |
| H3 anchor  | `#NN-subsection-name` | `#11-core-concepts` |
| Multi-word | Lowercase, hyphens    | `#token-efficiency` |

---

## 4. Content Distribution

### 4.1 MECE Principle

| Aspect                  | Application               |
|-------------------------|---------------------------|
| Mutually Exclusive      | No overlapping content    |
| Collectively Exhaustive | Complete coverage         |
| Single location         | Each concept defined once |
| Cross-reference         | Link, don't duplicate     |

### 4.2 Distribution Guidelines

| Content Type | Primary Location | Reference From        |
|--------------|------------------|-----------------------|
| Philosophy   | `core/`          | All layers            |
| Standards    | `guidelines/`    | Practices             |
| Concepts     | `frameworks/`    | Guidelines, Practices |
| How-to       | `practices/`     | Scenarios             |
| Presets      | `scenarios/`     | Index only            |
| Boilerplate  | `templates/`     | Practices             |

### 4.3 Avoiding Duplication

| Instead Of          | Do This                   |
|---------------------|---------------------------|
| Copy content        | Add cross-reference       |
| Repeat examples     | Link to canonical example |
| Duplicate tables    | Reference source file     |
| Inline long content | Extract to separate file  |

---

## 5. Loading Strategy

### 5.1 Progressive Loading

| Phase            | Load                  | Purpose              |
|------------------|-----------------------|----------------------|
| Session start    | Core                  | Establish foundation |
| Task definition  | Guidelines (relevant) | Set standards        |
| Complex decision | Frameworks (specific) | Deep reference       |
| Implementation   | Practices (specific)  | Actionable guidance  |
| Specific context | Scenario (if matched) | Pre-configured setup |

### 5.2 Trigger-Based Loading

| Trigger Type      | Example                   | Action                  |
|-------------------|---------------------------|-------------------------|
| Keyword           | "python", "fastapi"       | Load Python scenario    |
| Task type         | "refactor", "review"      | Load relevant practices |
| Explicit request  | "load autonomy framework" | Load specific file      |
| Complexity signal | Multiple concerns         | Load expert committee   |

### 5.3 Token Budget Management

| Strategy         | Application              |
|------------------|--------------------------|
| Core always fits | Keep under 500 tokens    |
| Layer budgets    | Allocate by priority     |
| Partial loading  | Load sections, not files |
| Summary first    | Overview before details  |

---

## Related

- `.knowledge/practices/documentation/PROJECT_DIRECTORY_STRUCTURE.md` — Project directory organization patterns
- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Documentation format standards
- `.knowledge/practices/documentation/OPTIMIZATION_WORKFLOW.md` — Batch optimization process
- `.knowledge/frameworks/design/AXIOMS.md` — Design principles (MECE, SSOT)
- `.knowledge/core/INDEX.md` — Core layer example

---

*AI Collaboration Knowledge Base*
