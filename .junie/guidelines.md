---
version: "1.3"
last_updated: "2025-11-30"
status: published
tokens: ~320
---

# Junie Guidelines

> Primary entry point for JetBrains Junie AI collaboration

---

## Table of Contents

- [1. About This File](#1-about-this-file)
- [2. AI Reading Order](#2-ai-reading-order)
- [3. AI Collaboration Rules](#3-ai-collaboration-rules)
- [4. Coding Standards](#4-coding-standards)
- [5. Token Efficiency](#5-token-efficiency)
- [6. Configuration Validation](#6-configuration-validation)
- [7. References](#7-references)
- [8. Template Information](#8-template-information)

---

## 1. About This File

This file contains **generic Junie AI collaboration rules**.
For project-specific rules, refer to `project/GUIDELINES.md`.

### Knowledge Sources (SSOT)

> All knowledge is maintained in `.knowledge/` as the Single Source of Truth.
> This section lists key references — see [7. References](#7-references) for the complete list.

| Topic | Authoritative Source |
|:------|:---------------------|
| Autonomy Levels (L1-L6) | `.knowledge/frameworks/autonomy/LEVELS.md` |
| Timeout Patterns | `.knowledge/frameworks/resilience/TIMEOUT_PATTERNS.md` |
| Code Style | `.knowledge/guidelines/CODE_STYLE.md` |
| AI Collaboration | `.knowledge/guidelines/AI_COLLABORATION.md` |

---

## 2. AI Reading Order

When starting a new session, load files in this priority order:

### Priority 1: Essential (Always Load)

| File | Purpose |
|:-----|:--------|
| `guidelines.md` | Core Junie rules (this file) |
| `project/config.yaml` | Project identity |
| `project/GUIDELINES.md` | Project-specific AI rules and patterns |

### Priority 2: Context (Load as Needed)

| File | Purpose | When |
|:-----|:--------|:-----|
| `generic/QUICKREF.md` | Quick lookup card | Reference needed |
| `mcp/mcp.json` | MCP configuration | MCP operations |
| `.knowledge/frameworks/autonomy/LEVELS.md` | Autonomy details | Autonomy decisions |

### Priority 3: Reference (On Demand)

| File | Purpose | When |
|:-----|:--------|:-----|
| `docs/README.md` | Documentation index | Finding docs |
| `docs/guides/*` | How-to guides | Specific guidance |
| `.knowledge/guidelines/*` | Detailed standards | Deep reference |

### Loading Strategy

```
Session Start
    │
    ├─► Load guidelines.md (this file)
    │
    ├─► Load project/config.yaml + project/GUIDELINES.md
    │
    ├─► Check task complexity
    │       │
    │       ├─► Simple task → Proceed
    │       │
    │       └─► Complex task → Load QUICKREF.md + relevant .knowledge/
    │
    └─► MCP needed? → Load mcp/mcp.json
```

---

## 3. AI Collaboration Rules

> **Project-specific rules**: See `project/GUIDELINES.md`

### Autonomy Levels

> **Full Definition**: `.knowledge/frameworks/autonomy/LEVELS.md`

| Level | Autonomy | Typical Use |
|:------|:---------|:------------|
| L1-L2 | 0-40% | Breaking changes, critical systems |
| L3-L4 | 40-80% | Bug fixes, routine development ⭐ |
| L5-L6 | 80-100% | Formatting, docs, trusted patterns |

**Default**: L4 (Medium-High) for mature collaboration.

### Generic Behaviors

| Behavior | Description |
|:---------|:------------|
| Follow patterns | Maintain consistency with existing codebase |
| Run tests | Verify changes before committing |
| Update docs | Keep documentation in sync with code |
| Use English | Default language for code and docs |

---

## 4. Coding Standards

> **Project-specific standards**: See `project/GUIDELINES.md`
> **Full Standards**: `.knowledge/guidelines/CODE_STYLE.md`

### General Principles

| Aspect | Guideline |
|:-------|:----------|
| Formatter | Use project's configured formatter |
| Type Hints | Required for statically-typed languages |
| Docstrings | Follow project's documentation style |
| Naming | Follow project's naming conventions |
| Architecture | Maintain layer separation |
| Error Handling | Implement proper error handling and logging |

---

## 5. Token Efficiency

Optimize token usage for better AI performance.

### Token Budget by Priority

| Priority | Files | Budget | Strategy |
|:---------|:------|:-------|:---------|
| P1 | `guidelines.md`, `project/*` | ~2000 | Always load |
| P2 | `QUICKREF.md` files | ~500 each | Load for complex |
| P3 | `docs/*`, `.knowledge/*` | ~1000 | On demand |

### Efficiency Patterns

| Pattern | Savings | Use Case |
|:--------|:--------|:---------|
| Tables instead of prose | ~40% | Structured comparisons |
| Cross-references | ~70% | Repeated content |
| Layered loading | ~50% | Large documentation |

### Anti-Patterns

- ❌ Loading entire directories at once
- ❌ Repeating content instead of cross-referencing
- ❌ Deep nesting (>3 levels)

---

## 6. Configuration Validation

### Validation Checklist

| Component | Method | Frequency |
|:----------|:-------|:----------|
| YAML syntax | `yamllint` or IDE | Every change |
| JSON syntax | `jsonlint` or IDE | Every change |
| Schema match | JSON Schema validation | Every change |
| MCP servers | Settings → Tools → Junie | After config |

### Quick Validation

```bash
# YAML
python -c "import yaml; yaml.safe_load(open('.junie/generic/config.yaml'))"

# JSON
python -c "import json; json.load(open('.junie/mcp/mcp.json'))"
```

### Common Issues

| Issue | Fix |
|:------|:----|
| Invalid YAML | Check indentation (2 spaces) |
| Invalid JSON | Check trailing commas, quotes |
| MCP won't start | Verify Node.js v18+ |

### Emergency Fallbacks

| Failure | Action |
|:--------|:-------|
| MCP servers down | Use IDE built-in operations |
| Memory server lost | Document in `.history/` |
| Config corrupted | Restore from `schema/` |

---

## 7. References

### Knowledge Sources (SSOT)

| Topic | Authoritative Source |
|:------|:---------------------|
| Autonomy Levels | `.knowledge/frameworks/autonomy/LEVELS.md` |
| Timeout Patterns | `.knowledge/frameworks/resilience/TIMEOUT_PATTERNS.md` |
| Documentation Standards | `.knowledge/guidelines/DOCUMENTATION.md` |
| Code Style | `.knowledge/guidelines/CODE_STYLE.md` |
| AI Collaboration | `.knowledge/guidelines/AI_COLLABORATION.md` |

### Configuration Files

| File | Purpose | Priority |
|:-----|:--------|:---------|
| `project/config.yaml` | Project identity | P1 |
| `project/GUIDELINES.md` | Project-specific rules | P1 |
| `mcp/mcp.json` | MCP configuration | P1 |
| `generic/config.yaml` | Generic settings | P2 |
| `generic/QUICKREF.md` | Quick lookup card | P2 |

### Key Documentation

| Document | Purpose |
|:---------|:--------|
| `docs/README.md` | Documentation index |
| `docs/guides/QUICK-START.md` | First-time setup |
| `docs/mcp/CONFIGURATION.md` | MCP setup |

### Version Compatibility

| Component | Minimum | Recommended |
|:----------|:--------|:------------|
| Junie Plugin | 2024.3 | 2025.1+ |
| JetBrains IDE | 2024.3 | 2025.1+ |
| Node.js | v18.0 | v20+ |

---

## 8. Template Information

This `.junie/` configuration follows the **Thin Layer** principle:

### Directory Structure

| Directory | Type | Purpose |
|:----------|:-----|:--------|
| `project/` | 📌 Customize | Project-specific files |
| `generic/` | 🔄 Generic | Settings, QUICKREF |
| `mcp/` | 🔄 Generic | MCP server config |
| `schema/` | 🔄 Generic | JSON Schema files |
| `docs/` | 🔄 Generic | Junie documentation |

### Customization

- **Customize**: Files in `project/` — edit freely
- **Override**: Copy generic files to `project/` to override
- **Extend**: Add new files in `project/` as needed

---

*Part of the Junie Configuration Template System*
