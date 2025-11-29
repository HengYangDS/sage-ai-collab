# Quick Reference Card

> Instant lookup for common tasks and paths

<!-- TEMPLATE NOTES:
     📌 PROJECT-SPECIFIC: Commands, paths, and key files - update per project
     🔄 GENERIC: Autonomy levels, timeouts, session checklist
     Reference: project.yaml for centralized project variables -->

---

## 🚀 Commands

```bash
# Testing
pytest tests/ -v                    # Run all tests
pytest tests/unit/ -v               # Unit tests only
pytest tests/integration/ -v        # Integration tests only

# Services
sage serve                          # Start MCP server
sage get --layer core               # Get core layer content
sage search "timeout"               # Search knowledge base
sage info                           # System information

# Development
ruff check src/                     # Lint check
ruff format src/                    # Format code
mypy src/                           # Type check
```

---

## 📁 Key Paths

| Category | Path | Purpose |
|----------|------|---------|
| **Conventions** | `.context/conventions/` | Naming, patterns, structure |
| **Policies** | `.context/policies/` | Timeouts, loading, runtime |
| **ADRs** | `.context/decisions/` | Architecture decisions |
| **AI Patterns** | `.context/intelligence/` | Interaction patterns |
| **Config** | `config/sage.yaml` | Main configuration |
| **Core Code** | `src/sage/core/` | Core layer |
| **Services** | `src/sage/services/` | CLI, MCP, API |

---

## 🎯 Autonomy Levels

| Level | Action | Examples |
|-------|--------|----------|
| **L1-L2** | Ask first | Breaking changes, new deps |
| **L3-L4** ⭐ | Proceed, report | Bug fixes, refactoring |
| **L5-L6** | High autonomy | Docs, formatting |

**Default**: L4 (Medium-High)

---

## ⏱️ Timeouts

```
T1: 100ms  → Cache lookup
T2: 500ms  → Single file
T3: 2s     → Layer load
T4: 5s     → Full KB load
T5: 10s    → Complex analysis
```

---

## 📝 Session End Checklist

1. Create records in `.history/` if significant work done
2. Update relevant `index.md` file counts
3. Run tests before committing
4. Use `.outputs/` for temporary files

---

## 🔗 Quick Links

- **Full Guidelines**: `guidelines.md`
- **Project Context**: `.context/index.md`
- **Session History**: `.history/index.md`
- **Design Docs**: `docs/design/00-overview.md`

---

*Part of SAGE Knowledge Base - Quick Reference*
