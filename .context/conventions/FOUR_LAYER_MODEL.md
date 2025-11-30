# Four Layer Model

> Architecture layers defining extension, capability, tool, and script boundaries

---

## 1. Layer Diagram

```
Abstract ▲
         │  ┌─────────────────────────────────────────┐
         │  │ plugins (Architecture Layer)            │
         │  │ · Extension mechanisms, lifecycle       │
         │  │ · src/sage/core/plugins/                │
         │  │ · docs/design/plugins/                  │
         │  └─────────────────────────────────────────┘
         │                    │
         │                    ▼
         │  ┌─────────────────────────────────────────┐
         │  │ capabilities (Interface Layer)          │
         │  │ · Capability family interfaces:         │
         │  │   analyzers, checkers, monitors,        │
         │  │   converters, generators                │
         │  │ · src/sage/capabilities/                │
         │  │ · docs/design/capabilities/             │
         │  └─────────────────────────────────────────┘
         │                    │
         │                    ▼
         │  ┌─────────────────────────────────────────┐
         │  │ tools (Implementation Layer)            │
         │  │ · Runtime tools, user-facing            │
         │  │ · tools/{analyzers,checkers,...}        │
         │  │ · docs/guides/TOOLS.md                  │
         │  └─────────────────────────────────────────┘
         │                    │
         ▼                    ▼
Concrete   ┌─────────────────────────────────────────┐
           │ scripts (Auxiliary Layer)               │
           │ · Development scripts, CI/CD            │
           │ · scripts/{dev,check,hooks,ci}          │
           │ · scripts/README.md                     │
           └─────────────────────────────────────────┘
```

---

## 2. Layer Definitions

| Layer | Definition | Key Question | Target User |
|-------|------------|--------------|-------------|
| **plugins** | Extension mechanisms | How to extend? | Framework developers |
| **capabilities** | Capability contracts | What can it do? | Capability developers |
| **tools** | Concrete implementations | How to use? | End users |
| **scripts** | Development utilities | How to develop? | Project developers |

---

## 3. Stability Levels

| Layer | Stability | Change Frequency |
|-------|-----------|------------------|
| plugins | ★★★★★ | Rarely changes |
| capabilities | ★★★★☆ | Infrequent changes |
| tools | ★★★☆☆ | Regular changes |
| scripts | ★★☆☆☆ | Frequent changes |

---

## 4. Dependency Rules

### 4.1 Allowed Dependencies

```
scripts → tools → capabilities → plugins
```

- Scripts may depend on tools
- Tools may depend on capabilities
- Capabilities may depend on plugins
- Each layer may depend on layers above it

### 4.2 Forbidden Dependencies

```
plugins ✗→ capabilities ✗→ tools ✗→ scripts
```

- Plugins must NOT depend on capabilities
- Capabilities must NOT depend on tools
- Tools must NOT depend on scripts
- No downward dependencies allowed

### 4.3 Dependency Matrix

| From ↓ / To → | plugins | capabilities | tools | scripts |
|---------------|---------|--------------|-------|---------|
| plugins       | ✅      | ❌           | ❌    | ❌      |
| capabilities  | ✅      | ✅           | ❌    | ❌      |
| tools         | ✅      | ✅           | ✅    | ❌      |
| scripts       | ✅      | ✅           | ✅    | ✅      |

---

## 5. Directory Mapping

| Layer | Source Code | Documentation |
|-------|-------------|---------------|
| plugins | `src/sage/core/plugins/` | `docs/design/plugins/` |
| capabilities | `src/sage/capabilities/` | `docs/design/capabilities/` |
| tools | `tools/{family}/` | `docs/guides/TOOLS.md` |
| scripts | `scripts/{category}/` | `scripts/README.md` |

---

## 6. Capability Families (tools layer)

| Family | Responsibility | Representative Tools |
|--------|---------------|---------------------|
| **analyzers** | Analysis, diagnosis, graph | knowledge_graph |
| **checkers** | Check, validate, verify | knowledge_validator |
| **monitors** | Monitor, observe, alert | timeout_manager |
| **converters** | Convert, migrate, adapt | migration_toolkit |
| **generators** | Generate, build, create | index_generator |

---

## 7. Script Categories (scripts layer)

| Category | Purpose | Examples |
|----------|---------|----------|
| **dev** | Development setup | setup_dev.py, new_file.py |
| **check** | Validation scripts | check_architecture.py |
| **hooks** | Git hooks | pre_commit.py, pre_push.py |
| **ci** | CI/CD pipelines | build.py, test.py, release.py |

---

## 8. Validation Checklist

- [ ] Each component belongs to exactly one layer
- [ ] No downward dependencies exist
- [ ] Tools are organized by capability family
- [ ] Scripts are organized by category
- [ ] Documentation follows layer structure

---

## Related

- `.knowledge/practices/engineering/MECE.md` — MECE categorization principle
- `.context/conventions/DIRECTORY_STRUCTURE.md` — Full directory layout
- `docs/design/architecture/INDEX.md` — Architecture documentation

---

*AI Collaboration Knowledge Base*
