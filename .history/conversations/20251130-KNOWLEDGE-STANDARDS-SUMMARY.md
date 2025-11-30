# Knowledge Standards Summary

> Session record: Documentation and Configuration Standards extracted from .knowledge/

---

## Date: 2025-11-30

## Purpose

This file stores key knowledge about documentation writing standards and configuration file standards extracted from the
`.knowledge/` directory (now renamed to `.knowledge/`).

---

## 1. Documentation Writing Standards

### 1.1 Document Format

| Element    | Standard                                  |
|------------|-------------------------------------------|
| Title      | H1, no emoji in production                |
| Purpose    | Single-line blockquote after title        |
| TOC        | Required if >60 lines or >3 H2 headings   |
| TOC Format | Vertical list with `- [Section](#anchor)` |
| H2         | `## N. Section` (numbered 1., 2., 3.)     |
| H3         | `### N.N Subsection` (decimal 1.1, 1.2)   |
| H4         | `#### N.N.N Detail` (use sparingly)       |
| Footer     | `*Part of SAGE Knowledge Base*`           |

### 1.2 Content Types

| Type      | Structure                              | Use For            |
|-----------|----------------------------------------|--------------------|
| Index     | Navigation table + descriptions        | Layer entry points |
| Guide     | Numbered steps + examples              | How-to content     |
| Reference | Tables + code blocks                   | API, config docs   |
| Framework | Concepts + patterns + examples         | Conceptual models  |
| Practice  | Patterns + anti-patterns + checklist   | Best practices     |
| Template  | Placeholders `[MARKER]` + instructions | Reusable documents |

### 1.3 Token Efficiency Patterns

| Pattern              | Savings | Application            |
|----------------------|---------|------------------------|
| Tables vs paragraphs | ~40%    | Structured comparisons |
| Lists vs paragraphs  | ~30%    | Enumerations, steps    |
| Vertical TOC         | ~50%    | Document navigation    |
| Cross-references     | ~70%    | Repeated content       |

### 1.4 Target Metrics

| Metric               | Target |
|----------------------|--------|
| Tokens per section   | <500   |
| Lines per file       | <300   |
| H2 headings per file | 5-15   |
| Nesting depth        | ≤3     |
| Related links        | 3-5    |

### 1.5 Writing Style

| Rule          | Avoid                    | Prefer                         |
|---------------|--------------------------|--------------------------------|
| Active voice  | "File is read by loader" | "Loader reads file"            |
| Present tense | "This will create"       | "This creates"                 |
| Specific      | "Configure system"       | "Set `MAX=100` in config.yaml" |
| Concise       | "In order to"            | "To"                           |

### 1.6 File Naming

| Type     | Convention              | Example                      |
|----------|-------------------------|------------------------------|
| Markdown | `SNAKE_CASE.md`         | `DOCUMENTATION_STANDARDS.md` |
| ADR      | `ADR-NNNN-TITLE.md`     | `ADR-0001-FASTMCP-CHOICE.md` |
| Session  | `YYYY-MM-DD-TOPIC.md`   | `2025-11-29-TIMEOUT.md`      |
| Handoff  | `YYYY-MM-DD-HANDOFF.md` | `2025-11-29-API-HANDOFF.md`  |

---

## 2. Knowledge Organization

### 2.1 Layer Architecture

```text
.knowledge/
├── core/           # Foundational principles (always load, ~500 tokens)
├── guidelines/     # Standards and conventions (by role/task, ~1200 tokens)
├── frameworks/     # Deep conceptual models (on-demand, ~2000 tokens)
├── practices/      # Actionable patterns (implementation, ~1500 tokens)
├── scenarios/      # Context presets (by trigger, ~500 tokens)
└── templates/      # Ready-to-use templates (direct use, ~300 tokens)
```

### 2.2 Layer Principles

| Layer      | Key Principle                                              |
|------------|------------------------------------------------------------|
| Core       | Essential only, always relevant, highly compressed, stable |
| Guidelines | Role-indexed, task-oriented, moderate detail               |
| Frameworks | Theory-complete, deep understanding, reference material    |
| Practices  | Actionable, code examples, pattern-based                   |
| Scenarios  | Context-specific, pre-configured, trigger-based            |
| Templates  | Copy-paste ready, placeholder markers, self-contained      |

### 2.3 MECE Principle

| Aspect                  | Application               |
|-------------------------|---------------------------|
| Mutually Exclusive      | No overlapping content    |
| Collectively Exhaustive | Complete coverage         |
| Single location         | Each concept defined once |
| Cross-reference         | Link, don't duplicate     |

---

## 3. Directory Structure Conventions

### 3.1 Hidden Directories

| Directory     | Purpose                    | Git Policy |
|---------------|----------------------------|------------|
| `.context/`   | Project-specific knowledge | Tracked    |
| `.history/`   | Session history, handoffs  | Tracked    |
| `.archive/`   | Historical/deprecated      | Tracked    |
| `.backups/`   | Pre-change snapshots       | Tracked    |
| `.logs/`      | Runtime logs               | Ignored    |
| `.outputs/`   | Intermediate files         | Ignored    |
| `.knowledge/` | Generic reusable knowledge | Tracked    |

### 3.2 Visible Directories

| Directory | Purpose                   |
|-----------|---------------------------|
| `docs/`   | User-facing documentation |
| `src/`    | Source code               |
| `tests/`  | Test suite                |

---

## 4. YAML Configuration Standards

### 4.1 Naming Conventions

| Type     | Format               | Example                          |
|----------|----------------------|----------------------------------|
| General  | `snake_case`         | `max_connections`, `retry_count` |
| Boolean  | `is_*` / `*_enabled` | `is_active`, `cache_enabled`     |
| Duration | `*_ms` / `*_seconds` | `timeout_ms: 5000`               |
| Size     | `*_bytes` / `*_mb`   | `max_size_mb: 50`                |
| Count    | `max_*` / `min_*`    | `max_retries: 3`                 |

### 4.2 Structure Rules

| Rule          | Standard                 |
|---------------|--------------------------|
| Indentation   | 2 spaces (never tabs)    |
| Nesting depth | ≤3 levels recommended    |
| File size     | 50-150 lines recommended |
| File naming   | `[domain].yaml`          |

### 4.3 Section Format

```yaml
# [Component/Module] Configuration
#
# [Description]
# Version: x.y.z

# =============================================================================
# [Section Name]
# =============================================================================

key: value              # Inline comment (aligned)
```

### 4.4 Quick Checklist

| ✓ Do                   | ✗ Don't                  |
|------------------------|--------------------------|
| 2-space indent         | Tab or 4-space           |
| snake_case keys        | camelCase                |
| Numbers without quotes | `port: "8080"`           |
| Align inline comments  | Random comment placement |
| Include units          | No unit indication       |
| Keep nesting ≤3 levels | Deep nesting             |

---

## 5. Junie Configuration Template

### 5.1 Two-Category Architecture

| Category | Symbol | Description                    |
|----------|--------|--------------------------------|
| Generic  | 🔄     | Reusable across projects       |
| Project  | 📌     | Must be customized per project |

### 5.2 Delegation Pattern

| Target        | Content Type                                   |
|---------------|------------------------------------------------|
| `.context/`   | Project-specific knowledge (ADRs, conventions) |
| `.knowledge/` | Generic, reusable knowledge                    |
| `docs/`       | User-facing documentation                      |

### 5.3 Best Practices

| Do                        | Don't                         |
|---------------------------|-------------------------------|
| Reference detailed docs   | Duplicate detailed content    |
| Use short summaries       | Include full specifications   |
| Link to `.context/`       | Copy from `.context/`         |
| Keep files ~100-250 lines | Create large monolithic files |

---

## Related

- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Full documentation standards
- `.knowledge/practices/documentation/KNOWLEDGE_ORGANIZATION.md` — Layer architecture details
- `.knowledge/practices/engineering/YAML_CONVENTIONS.md` — YAML configuration standards
- `.knowledge/practices/ai_collaboration/JUNIE_CONFIGURATION_TEMPLATE.md` — Junie template system

---

*AI Collaboration Knowledge Base*
