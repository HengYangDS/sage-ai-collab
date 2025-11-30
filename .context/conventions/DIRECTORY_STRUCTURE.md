# Directory Structure

> Canonical directory layout for SAGE Knowledge Base

---

## 1. Project Root

```
sage-kb/
├── .knowledge/              # Universal knowledge (cross-project)
├── .context/                # Project knowledge (this project)
├── .junie/                  # AI assistant configuration
├── docs/                    # User documentation
│   ├── design/              # Design documents (this refactor target)
│   └── guides/              # User guides
├── src/sage/                # Source code
├── tools/                   # Runtime tools (5 capability families)
├── scripts/                 # Development scripts (4 categories)
├── tests/                   # Test suite
├── config/                  # Configuration files
├── README.md
├── CHANGELOG.md
└── CONTRIBUTING.md
```

---

## 2. docs/design/ Structure

```
docs/design/                        # 12 subdirectories + 57 files
├── INDEX.md
├── OVERVIEW.md
├── philosophy/                     # ★★★★★
│   ├── INDEX.md
│   ├── XIN_DA_YA.md
│   └── DESIGN_AXIOMS.md
├── protocols/                      # ★★★★★
│   ├── INDEX.md
│   ├── SAGE_PROTOCOL.md
│   ├── SOURCE_PROTOCOL.md
│   ├── ANALYZE_PROTOCOL.md
│   ├── GENERATE_PROTOCOL.md
│   └── EVOLVE_PROTOCOL.md
├── architecture/                   # ★★★★★
│   ├── INDEX.md
│   ├── THREE_LAYER.md
│   ├── DEPENDENCIES.md
│   ├── DIRECTORY_LAYOUT.md
│   └── INFRASTRUCTURE.md
├── core_engine/                    # ★★★★☆
│   ├── INDEX.md
│   ├── DI_CONTAINER.md
│   ├── EVENT_BUS.md
│   ├── DATA_MODELS.md
│   ├── EXCEPTIONS.md
│   └── BOOTSTRAP.md
├── timeout_resilience/             # ★★★★☆
│   ├── INDEX.md
│   ├── TIMEOUT_HIERARCHY.md
│   ├── CIRCUIT_BREAKER.md
│   ├── GRACEFUL_DEGRADATION.md
│   └── SMART_LOADING.md
├── services/                       # ★★★☆☆
│   ├── INDEX.md
│   ├── SERVICE_LAYER.md
│   ├── CLI_SERVICE.md
│   ├── MCP_SERVICE.md
│   └── API_SERVICE.md
├── capabilities/                   # ★★★☆☆
│   ├── INDEX.md
│   ├── CAPABILITY_MODEL.md
│   ├── ANALYZERS.md
│   ├── CHECKERS.md
│   ├── MONITORS.md
│   ├── CONVERTERS.md
│   ├── GENERATORS.md
│   └── EXTENDING.md
├── plugins/                        # ★★★☆☆
│   ├── INDEX.md
│   ├── PLUGIN_ARCHITECTURE.md
│   ├── EXTENSION_POINTS.md
│   ├── PLUGIN_LIFECYCLE.md
│   └── BUNDLED_PLUGINS.md
├── knowledge_system/               # ★★★☆☆
│   ├── INDEX.md
│   ├── LAYER_HIERARCHY.md
│   ├── CONTENT_TAXONOMY.md
│   ├── LOADING_STRATEGY.md
│   └── TOKEN_BUDGET.md
├── memory_state/                   # ★★★☆☆
│   ├── INDEX.md
│   ├── PERSISTENCE.md
│   ├── SESSION_MANAGEMENT.md
│   └── CROSS_TASK_MEMORY.md
├── configuration/                  # ★★★☆☆
│   ├── INDEX.md
│   ├── CONFIG_HIERARCHY.md
│   ├── YAML_DSL.md
│   └── CONFIG_REFERENCE.md
└── evolution/                      # ★★☆☆☆
    ├── INDEX.md
    ├── ROADMAP.md
    ├── MILESTONES.md
    ├── EVALUATION_CRITERIA.md
    └── CHANGELOG.md
```

---

## 3. tools/ Structure

```
tools/
├── INDEX.md
├── __init__.py
├── analyzers/
│   ├── __init__.py
│   ├── INDEX.md
│   └── knowledge_graph/
├── checkers/
│   ├── __init__.py
│   ├── INDEX.md
│   ├── knowledge_validator.py
│   ├── link_checker.py
│   └── format_checker.py
├── monitors/
│   ├── __init__.py
│   ├── INDEX.md
│   ├── timeout_manager.py
│   └── health_monitor.py
├── converters/
│   ├── __init__.py
│   ├── INDEX.md
│   ├── migration_toolkit.py
│   └── format_converter.py
└── generators/
    ├── __init__.py
    ├── INDEX.md
    ├── index_generator.py
    └── template_generator.py
```

**Rules:**
- ❌ No top-level `.py` files (except `__init__.py`)
- ✅ All tools organized by capability family
- ✅ Each family has `INDEX.md` and `__init__.py`

---

## 4. scripts/ Structure

```
scripts/
├── README.md
├── dev/
│   ├── setup_dev.py
│   ├── new_file.py
│   └── generate_index.py
├── check/
│   ├── check_architecture.py
│   ├── check_docs.py
│   ├── check_links.py
│   ├── check_naming.py
│   └── validate_format.py
├── hooks/
│   ├── pre_commit.py
│   ├── post_commit.py
│   └── pre_push.py
└── ci/
    ├── build.py
    ├── test.py
    └── release.py
```

**Rules:**
- ✅ 4 categories: dev, check, hooks, ci
- ✅ Each category is a subdirectory
- ❌ No top-level scripts (except README.md)

---

## 5. Naming Rules Summary

| Element | Convention | Example |
|---------|------------|---------|
| Markdown files | `UPPER_SNAKE_CASE.md` | `SAGE_PROTOCOL.md` |
| Markdown extension | lowercase `.md` | `.md` not `.MD` |
| Directories | `lower_snake_case/` | `core_engine/` |
| Python files | `lower_snake_case.py` | `timeout_manager.py` |
| Index files | `INDEX.md` | Always uppercase |

**Forbidden:**
- ❌ Numeric prefixes (`01-`, `02-`)
- ❌ Kebab-case for Markdown (`timeout-hierarchy.md`)
- ❌ Uppercase directories (`Core_Engine/`)

---

## 6. Validation Checklist

- [ ] docs/design/ has 12 subdirectories
- [ ] Each subdirectory has INDEX.md
- [ ] tools/ has 5 capability family subdirectories
- [ ] tools/ has no top-level .py (except __init__.py)
- [ ] scripts/ has 4 category subdirectories
- [ ] All Markdown: UPPER_SNAKE_CASE.md
- [ ] All directories: lower_snake_case/
- [ ] No numeric prefixes
- [ ] No Frontmatter in Markdown

---

## Related

- `.context/conventions/NAMING.md` — Detailed naming rules
- `.context/conventions/FOUR_LAYER_MODEL.md` — Layer architecture
- `.knowledge/practices/engineering/MECE.md` — MECE principle

---

*AI Collaboration Knowledge Base*
