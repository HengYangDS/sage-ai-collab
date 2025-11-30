# Scenario Presets

> Context-specific knowledge presets for common development scenarios

---

## Table of Contents

- [1. Available Scenarios](#1-available-scenarios)
- [2. Scenario Structure](#2-scenario-structure)
- [3. Creating New Scenarios](#3-creating-new-scenarios)

---

## 1. Available Scenarios

| Scenario                 | Path                      | Purpose                           |
|--------------------------|---------------------------|-----------------------------------|
| **Data Pipeline**        | `data_pipeline/`          | ETL and data processing workflows |
| **DevOps**               | `devops/`                 | CI/CD and infrastructure          |
| **Documentation**        | `documentation/`          | Technical writing projects        |
| **Knowledge Management** | `knowledge_management/`   | Knowledge base system development |
| **Legacy Modernization** | `legacy_modernization/`   | Legacy system updates             |
| **MCP Integration**      | `mcp_integration/`        | Model Context Protocol services   |
| **Microservices**        | `microservices/`          | Microservices architecture        |
| **Monorepo**             | `monorepo/`               | Monorepo management               |
| **Plugin Development**   | `plugin_development/`     | Plugin development                |
| **Python Backend**       | `python_backend/`         | Python web service development    |
| **TypeScript Frontend**  | `typescript_frontend/`    | React/Vue frontend development    |

Each scenario contains:
- `INDEX.md` — Scenario navigation
- `CONTEXT.md` — Main scenario context
- `CHECKLIST.md` — Task checklist

---

## 2. Scenario Structure

```text
scenarios/[name]/
├── INDEX.md        # Scenario navigation
├── CONTEXT.md      # Main scenario context
└── CHECKLIST.md    # Task checklist
```

### Context File Format

```markdown
# [Scenario Name] Context

> [Brief description]

## Quick Setup

[Essential setup steps]

## Key Guidelines

[Scenario-specific guidelines]

## Common Tasks

[Frequent operations]

## Pitfalls

[Common mistakes to avoid]
```

---

## 3. Creating New Scenarios

1. Create directory: `.knowledge/scenarios/[name]/`
2. Add `INDEX.md` with scenario navigation
3. Add `CONTEXT.md` with scenario context
4. Add `CHECKLIST.md` with task checklist
5. Define auto-load triggers in `config/knowledge/triggers.yaml`
6. Update this index

---

## Related

- `.knowledge/guidelines/INDEX.md` — General guidelines
- `.knowledge/practices/INDEX.md` — Implementation practices
- `.knowledge/templates/INDEX.md` — Document templates
- `config/knowledge/triggers.yaml` — Trigger configuration

---

*AI Collaboration Knowledge Base*
