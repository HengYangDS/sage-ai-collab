---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---

# Quick Reference Card

> Instant lookup for AI collaboration essentials

---

## Table of Contents

- [1. Autonomy Levels](#1-autonomy-levels)
- [2. Timeout Tiers](#2-timeout-tiers)
- [3. Session End Checklist](#3-session-end-checklist)
- [4. Standard Paths](#4-standard-paths)
- [5. Quick Links](#5-quick-links)
- [6. Naming Conventions](#6-naming-conventions)
- [7. Project Commands](#7-project-commands)

---

## 1. Autonomy Levels

| Level       | Action          | Examples                   |
|-------------|-----------------|----------------------------|
| **L1-L2**   | Ask first       | Breaking changes, new deps |
| **L3-L4** ⭐ | Proceed, report | Bug fixes, refactoring     |
| **L5-L6**   | High autonomy   | Docs, formatting           |

**Default**: L4 (Medium-High)

---

## 2. Timeout Tiers

| Tier | Duration | Use Case         |
|------|----------|------------------|
| T1   | ~100ms   | Cache lookup     |
| T2   | ~500ms   | Single file      |
| T3   | ~2s      | Layer load       |
| T4   | ~5s      | Full init        |
| T5   | ~10s     | Complex analysis |

---

## 3. Session End Checklist

1. ☐ Create records in `.history/` if significant work done
2. ☐ Update relevant `INDEX.md` file counts
3. ☐ Run tests before committing
4. ☐ Use `.outputs/` for temporary files
5. ☐ Document key decisions made

---

## 4. Standard Paths

| Category      | Typical Path | Purpose             |
|---------------|--------------|---------------------|
| **AI Config** | `.junie/`    | Junie configuration |
| **Context**   | `.context/`  | Project knowledge   |
| **History**   | `.history/`  | Session records     |
| **Outputs**   | `.outputs/`  | Temporary files     |
| **Docs**      | `docs/`      | Documentation       |
| **Source**    | `src/`       | Source code         |
| **Tests**     | `tests/`     | Test suite          |

---

## 5. Quick Links

| Document                 | Purpose                     |
|--------------------------|-----------------------------|
| `../guidelines.md`       | Full AI collaboration rules |
| `config.yaml`            | Junie settings              |
| `../project/config.yaml` | Project variables           |
| `../project/GUIDELINES.md` | Project-specific guidelines |
| `../mcp/mcp.json`        | MCP server config           |

---

## 6. Naming Conventions

### Session History Files

| Type         | Format                       | Example                          |
|--------------|------------------------------|----------------------------------|
| Conversation | `YYYY-MM-DD-TOPIC.md`        | `2025-01-15-API-DESIGN.md`       |
| Handoff      | `YYYY-MM-DD-TASK-HANDOFF.md` | `2025-01-15-REFACTOR-HANDOFF.md` |
| Session      | `session-YYYYMMDD-HHMM.md`   | `SESSION-20250115-1430.md`       |

---

## 7. Project Commands

See `../project/GUIDELINES.md` for:

- Build commands
- Test commands
- Service commands
- Development scripts

See `../project/config.yaml` for:

- Project identity
- Tech stack
- Directory structure
- Key files

---

*Part of the Junie Configuration Template System*
