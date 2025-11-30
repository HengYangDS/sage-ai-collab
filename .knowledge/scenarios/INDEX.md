# Scenario Presets

> Context-specific knowledge presets for common development scenarios

---

## Table of Contents

- [1. Available Scenarios](#1-available-scenarios)

- [2. Python Backend Scenario](#2-python-backend-scenario)

- [3. Scenario Structure](#3-scenario-structure)

- [4. Creating New Scenarios](#4-creating-new-scenarios)

---

## 1. Available Scenarios

| Scenario                 | Path                    | Tokens | Context                           |

|--------------------------|-------------------------|--------|-----------------------------------|

| **Python Backend**       | `python_backend/`       | ~200   | Python web service development    |

| **TypeScript Frontend**  | `typescript_frontend/`  | ~300   | React/Vue frontend development    |

| **Data Pipeline**        | `data_pipeline/`        | ~400   | ETL and data processing workflows |

| **DevOps**               | `devops/`               | ~400   | CI/CD and infrastructure          |

| **Documentation**        | `documentation/`        | ~300   | Technical writing projects        |

| **Knowledge Management** | `knowledge_management/` | ~300   | Knowledge base system development |

| **MCP Integration**      | `mcp_integration/`      | ~400   | Model Context Protocol services   |

| **Plugin Development**   | `plugin_development/`   | ~400   | plugin development           |

---

## 2. Python Backend Scenario

**Path**: `python_backend/CONTEXT.md`

### When to Load

- Building Python web services

- FastAPI/Flask development

- REST API implementation

- Python testing with pytest

### Includes

- Python code style guidelines

- Testing strategies for Python

- API design patterns

- Configuration management

### Auto-Load Triggers

| Keywords                    | Action        |

|-----------------------------|---------------|

| fastapi, flask, django      | Load scenario |

| python backend, web service | Load scenario |

| pytest, python test         | Load scenario |

---

## 3. Scenario Structure

Each scenario contains:

```text
scenarios/[name]/
├── CONTEXT.md      # Main scenario context
├── CHECKLIST.md    # Optional: task checklist
└── templates/      # Optional: scenario-specific templates
```
### Context File Format

```markdown

# [Scenario Name] Context

> **Purpose**: [brief description]

> **Stack**: [technologies]

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

## 4. Creating New Scenarios

1. Create directory: `.knowledge/scenarios/[name]/`

2. Add `CONTEXT.md` with scenario context

3. Define auto-load triggers in `config/knowledge/triggers.yaml`

4. Update this index

---

## Related

- `.knowledge/guidelines/INDEX.md` — General guidelines

- `.knowledge/practices/INDEX.md` — Implementation practices

- `.knowledge/templates/INDEX.md` — Document templates

- `.config/knowledge/triggers.yaml` — Trigger configuration

---

*AI Collaboration Knowledge Base*

