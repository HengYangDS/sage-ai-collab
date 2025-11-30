---
version: "1.1"
last_updated: "2025-11-30"
status: published
tokens: ~400
---

# Project Guidelines

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

This file contains **Junie-specific AI collaboration rules**.
For detailed knowledge, refer to the appropriate knowledge sources:

| Topic | Location |
|:------|:---------|
| Autonomy Levels (L1-L6) | `.knowledge/frameworks/autonomy/LEVELS.md` |
| Timeout Hierarchy (T1-T5) | `.context/policies/TIMEOUT_HIERARCHY.md` |
| Documentation Standards | `.knowledge/guidelines/DOCUMENTATION.md` |
| AI Collaboration Patterns | `.knowledge/guidelines/AI_COLLABORATION.md` |
| Project Calibration Data | `.context/intelligence/calibration/CALIBRATION.md` |

**Project-specific configuration**:

- **Project Config**: `project/config.yaml` — Project identity, tech stack, commands
- **Project Quick Reference**: `project/QUICKREF.md` — Project-specific documentation

**Generic configuration**:

- **Settings**: `generic/config.yaml` — Junie settings
- **Quick Reference**: `generic/QUICKREF.md` — Quick lookup card
- **MCP Config**: `mcp/mcp.json` — MCP server configuration
- **Documentation**: `docs/` — Junie documentation

---

## 2. AI Reading Order

When starting a new session, load files in this priority order:

### Priority 1: Essential (Always Load)

| File | Purpose | When |
|:-----|:--------|:-----|
| `guidelines.md` | Core Junie rules | Every session |
| `project/config.yaml` | Project identity, tech stack | Every session |

### Priority 2: Context (Load as Needed)

| File | Purpose | When |
|:-----|:--------|:-----|
| `project/QUICKREF.md` | Project-specific patterns | Complex tasks |
| `generic/QUICKREF.md` | Quick lookup card | Reference needed |
| `mcp/mcp.json` | MCP server configuration | MCP operations |
| `.knowledge/frameworks/autonomy/LEVELS.md` | Autonomy level details | Autonomy decisions |
| `.context/policies/TIMEOUT_HIERARCHY.md` | Timeout configuration | Timeout-sensitive ops |

### Priority 3: Reference (On Demand)

| File | Purpose | When |
|:-----|:--------|:-----|
| `docs/README.md` | Documentation index | Finding docs |
| `docs/guides/*` | How-to guides | Specific guidance |
| `docs/mcp/*` | MCP documentation | MCP troubleshooting |
| `.knowledge/guidelines/*` | Detailed standards | Deep reference |

### Loading Strategy

```
Session Start
    │
    ├─► Load guidelines.md (this file)
    │
    ├─► Load project/config.yaml
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

### Autonomy Levels (Quick Reference)

> **Full Definition**: `.knowledge/frameworks/autonomy/LEVELS.md`

| Level | Name | Autonomy | Typical Use |
|:------|:-----|:---------|:------------|
| L1-L2 | Minimal/Low | 0-40% | Breaking changes, critical systems |
| L3-L4 | Medium | 40-80% | Bug fixes, routine development ⭐ |
| L5-L6 | High/Full | 80-100% | Formatting, docs, trusted patterns |

**Default**: L4 (Medium-High) for mature collaboration.

### Key Behaviors

1. **Follow existing patterns** in the codebase
2. **Run tests** before committing changes
3. **Update relevant documentation** when modifying features
4. **Output files to designated temp directory** (typically `.outputs/`)
5. **Create session records** for significant work sessions
6. **Use English** for code and documentation (unless project specifies otherwise)
7. **Respect timeout limits** — See `.context/policies/TIMEOUT_HIERARCHY.md`

### Session History Management

At session end, create records in `.history/`:

| Directory | Purpose |
|:----------|:--------|
| `conversations/` | Key decisions and outcomes |
| `handoffs/` | Task continuation context |
| `current/` | Active work state |

**Naming**: `YYYYMMDD-TOPIC.md`, `YYYYMMDD-TASK-HANDOFF.md`

### Session Automation (MCP Tools)

| Tool | When | Purpose |
|:-----|:-----|:--------|
| `session_start` | Beginning of significant work | Creates session state |
| `session_end` | Work completed/ending | Creates record |
| `session_status` | Start of new session | Check state |

### Expert Committee Pattern

For complex decisions, simulate **Level 5 Expert Committee** review:

- **Architecture** — System design, scalability
- **Engineering Practice** — Code quality, testing
- **Domain Knowledge** — Business logic alignment
- **AI Collaboration** — Human-AI interaction

---

## 4. Coding Standards

> **Full Standards**: `.knowledge/guidelines/CODE_STYLE.md`, `.knowledge/guidelines/PYTHON.md`

### General Principles

- **Formatter**: Use project's configured formatter
- **Type Hints**: Required for statically-typed languages
- **Docstrings**: Follow project's documentation style
- **Naming**: Follow project's naming conventions

### Architecture Patterns

- Follow project's established patterns
- Maintain layer separation
- Use dependency injection where applicable
- Implement proper error handling and logging

---

## 5. Token Efficiency

Optimize token usage for better AI performance.

### Token Budget by Priority

| Priority | Files | Budget | Strategy |
|:---------|:------|:-------|:---------|
| P1 | `guidelines.md`, `project/config` | ~2000 | Always load |
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
| Timeout Config (T1-T5) | `.context/policies/TIMEOUT_HIERARCHY.md` |
| Documentation Standards | `.knowledge/guidelines/DOCUMENTATION.md` |
| Code Style | `.knowledge/guidelines/CODE_STYLE.md` |
| AI Collaboration | `.knowledge/guidelines/AI_COLLABORATION.md` |
| Project Calibration | `.context/intelligence/calibration/CALIBRATION.md` |

### Configuration Files

| File | Purpose | Priority |
|:-----|:--------|:---------|
| `project/config.yaml` | Project identity | P1 |
| `mcp/mcp.json` | MCP configuration | P1 |
| `generic/config.yaml` | Generic settings | P2 |
| `project/QUICKREF.md` | Project patterns | P2 |

### Key Documentation

| Document | Purpose |
|:---------|:--------|
| `docs/README.md` | Documentation index |
| `docs/guides/QUICK-START.md` | First-time setup |
| `docs/mcp/CONFIGURATION.md` | MCP setup |
| `docs/mcp/TROUBLESHOOTING.md` | Problem solving |

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
| `generic/` | 🔄 Generic | Settings, QUICKREF |
| `mcp/` | 🔄 Generic | MCP server config |
| `schema/` | 🔄 Generic | JSON Schema files |
| `docs/` | 🔄 Generic | Junie documentation |
| `project/` | 📌 Customize | Project-specific files |

### Reusability

- 🔄 **Generic**: Copy to new projects without modification
- 📌 **Project**: Must customize for each project

---

## Related

- `.knowledge/INDEX.md` — Generic knowledge navigation
- `.context/INDEX.md` — Project-specific context
- `docs/README.md` — Junie documentation index

---

*Part of the Junie Configuration Template System*
