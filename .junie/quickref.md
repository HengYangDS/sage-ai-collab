# Quick Reference Card

> Instant lookup for AI collaboration essentials

**Type**: 🔄 Generic (reusable across projects)

---

## 🎯 Autonomy Levels

| Level | Action | Examples |
|-------|--------|----------|
| **L1-L2** | Ask first | Breaking changes, new deps |
| **L3-L4** ⭐ | Proceed, report | Bug fixes, refactoring |
| **L5-L6** | High autonomy | Docs, formatting |

**Default**: L4 (Medium-High)

---

## ⏱️ Timeout Tiers

| Tier | Duration | Use Case |
|------|----------|----------|
| T1 | ~100ms | Cache lookup |
| T2 | ~500ms | Single file |
| T3 | ~2s | Layer load |
| T4 | ~5s | Full init |
| T5 | ~10s | Complex analysis |

---

## 📝 Session End Checklist

1. ☐ Create records in `.history/` if significant work done
2. ☐ Update relevant `index.md` file counts
3. ☐ Run tests before committing
4. ☐ Use `.outputs/` for temporary files
5. ☐ Document key decisions made

---

## 📁 Standard Paths

| Category | Typical Path | Purpose |
|----------|--------------|---------|
| **AI Config** | `.junie/` | Junie configuration |
| **Context** | `.context/` | Project knowledge |
| **History** | `.history/` | Session records |
| **Outputs** | `.outputs/` | Temporary files |
| **Docs** | `docs/` | Documentation |
| **Source** | `src/` | Source code |
| **Tests** | `tests/` | Test suite |

---

## 🔗 Quick Links

| Document | Purpose |
|----------|---------|
| `guidelines.md` | Full AI collaboration rules |
| `config.yaml` | Junie settings |
| `project.yaml` | Project variables |
| `project-guidelines.md` | Project-specific info |
| `mcp/mcp.json` | MCP server config |

---

## 📋 Naming Conventions

### Session History Files

| Type | Format | Example |
|------|--------|---------|
| Conversation | `YYYY-MM-DD-topic.md` | `2025-01-15-api-design.md` |
| Handoff | `YYYY-MM-DD-task-handoff.md` | `2025-01-15-refactor-handoff.md` |
| Session | `session-YYYYMMDD-HHMM.md` | `session-20250115-1430.md` |

---

## 🚀 Project-Specific Commands

See `project-guidelines.md` for:
- Build commands
- Test commands
- Service commands
- Development scripts

See `project.yaml` for:
- Project identity
- Tech stack
- Directory structure
- Key files

---

*Part of the Junie Configuration Template System*
