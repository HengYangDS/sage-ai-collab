---
title: SAGE Knowledge Base - Usage Patterns
version: "0.1.0"
last_updated: "2025-11-30"
status: production-ready
tokens: ~1200
---

# Usage Patterns

> **Bootstrap, quick start, exception handling, and AI scenarios**

---

## Table of Contents

- [1. Application Bootstrap](#1-application-bootstrap)
- [2. Quick Start](#2-quick-start)
- [3. Exception Handling](#3-exception-handling)
- [4. AI Usage Scenarios](#4-ai-usage-scenarios)

---

## 1. Application Bootstrap

### 1.1 Bootstrap Flow

```
┌───────────────────────────────────────────────┐
│              Application Start                │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│  1. Load Configuration (sage.yaml)            │
│     - Parse YAML, merge ENV overrides         │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│  2. Configure Logging                         │
│     - Set level, choose format                │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│  3. Initialize DI Container                   │
│     - Register services, set lifetimes        │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│  4. Start EventBus                            │
│     - Setup S.A.G.E. aligned pub/sub          │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│  5. Pre-cache Core Content                    │
│     - Load "always" content, warm cache       │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│  6. Start Requested Service                   │
│     - CLI / MCP Server / HTTP API             │
└───────────────────────────────────────────────┘
```

### 1.2 Bootstrap Code

```python
# src/sage/core/bootstrap.py
async def bootstrap(
    config_path: Path | None = None,
    config_override: dict | None = None
) -> DIContainer:
    """Bootstrap the application."""
    # 1. Load configuration
    config = SAGEConfig.load(config_path)
    if config_override:
        config = config.merge(config_override)

    # 2. Configure logging
    configure_logging(
        level=config.get("logging.level", "INFO"),
        format=config.get("logging.format", "console"),
    )

    # 3-4. Initialize DI Container with EventBus
    container = DIContainer()
    container.register_from_config(config.get("di.services", {}))

    # 5. Pre-cache core content
    loader = container.resolve(SourceProtocol)
    await loader.precache(config.get("loading.always", []))

    return container
```

---

## 2. Quick Start

### 2.1 Installation

```bash
# Install from PyPI
pip install sage-kb

# Or install with MCP support
pip install sage-kb[mcp]

# Or install for development
git clone https://github.com/your-org/sage-kb.git
cd sage-kb
pip install -e ".[dev]"
```

### 2.2 Basic Usage

```bash
# CLI usage
sage get --layer core       # Get core principles
sage search "autonomy"      # Search knowledge base
sage info                   # Get KB information

# Start MCP server (for AI Agents)
python -m sage serve
```

```python
# Python API
from sage.core.loader import KnowledgeLoader

loader = KnowledgeLoader()
result = await loader.load_core(timeout_ms=2000)
print(result.content)
```

### 2.3 Available MCP Tools

| Tool                   | Purpose                        |
|------------------------|--------------------------------|
| `get_knowledge`        | Load knowledge by layer/task   |
| `search_knowledge`     | Search the knowledge base      |
| `analyze_quality`      | Analyze content quality        |
| `check_health`         | System health verification     |

---

## 3. Exception Handling

> **Philosophy**: Graceful degradation over hard failures

### 3.1 Exception Hierarchy

```
SageException (Base)
├── ConfigurationError        # Configuration issues
│   ├── ConfigNotFoundError   # Config file missing
│   └── ConfigValidationError # Invalid config values
├── LoadingError              # Content loading issues
│   ├── TimeoutError          # Operation timed out
│   ├── FileNotFoundError     # Content file missing
│   └── ParseError            # Content parsing failed
├── ServiceError              # Service layer issues
│   ├── MCPError              # MCP protocol errors
│   └── APIError              # HTTP API errors
└── PluginError               # Plugin issues
    ├── PluginLoadError       # Plugin failed to load
    └── PluginExecutionError  # Plugin execution failed
```

### 3.2 Exception Propagation Rules

| Layer            | Catches           | Transforms To          | Action                 |
|------------------|-------------------|------------------------|------------------------|
| **Core**         | System exceptions | `LoadingError`         | Log + fallback content |
| **Capabilities** | Core exceptions   | Preserve or wrap       | Log + partial result   |
| **Services**     | All exceptions    | User-friendly response | Log + error response   |

### 3.3 Best Practices

```python
# ✅ CORRECT: Graceful handling with context
try:
    result = await loader.load(layer)
except LoadingError as e:
    logger.warning("load_failed", layer=layer, error=str(e))
    result = get_fallback(layer)

# ❌ WRONG: Silent failure
try:
    result = await loader.load(layer)
except Exception:
    pass  # Never do this!
```

---

## 4. AI Usage Scenarios

> **Purpose**: Guide AI Agents on when and how to use SAGE tools

### 4.1 Scenario: New Task Assessment

**When**: AI Agent receives a new task from user

```
1. get_knowledge(task="<user_task_description>")
   → Smart loading based on task keywords
   
2. If task involves code:
   get_guidelines(section="code_style")
   
3. If task involves architecture:
   get_framework(name="decision")
```

### 4.2 Scenario: Quality Check Before Delivery

**When**: AI Agent is about to deliver code/documentation

```
1. analyze_quality(path="<output_path>")
   → Get quality score (0-100)
   
2. If score < 80:
   Review issues and improve
   
3. check_links(path="<doc_path>")
   → Ensure no broken links
```

### 4.3 Tool Selection Guide

| Task Type             | Primary Tool                      | Secondary Tools                |
|-----------------------|-----------------------------------|--------------------------------|
| New coding task       | `get_knowledge(task=...)`         | `get_guidelines("code_style")` |
| Architecture decision | `get_framework("decision")`       | `get_guidelines("planning")`   |
| Code review           | `analyze_quality(path)`           | `check_links(path)`            |
| Documentation         | `get_guidelines("documentation")` | `analyze_content(path)`        |
| Debugging             | `get_knowledge(task="debug")`     | `check_health()`               |

### 4.4 Autonomy Level Mapping

| Autonomy Level           | Tool Usage Pattern                                      |
|--------------------------|---------------------------------------------------------|
| **L1-L2** (0-40%)        | Use `search_knowledge()`, ask user for confirmation     |
| **L3-L4** (40-80%) ⭐     | Use `get_knowledge()` directly, report actions after    |
| **L5-L6** (80-100%)      | Use tools autonomously, only report on completion       |

**Default**: L4 (Medium-High) for mature collaboration.

---

## Related

- `docs/design/01-architecture.md` — Main architecture design
- `docs/design/01a-infrastructure.md` — Infrastructure design
- `docs/design/01b-configuration.md` — Configuration design
- `docs/guides/quickstart.md` — User quick start guide
- `.knowledge/frameworks/autonomy/levels.md` — Autonomy framework

---

*Part of SAGE Knowledge Base*
