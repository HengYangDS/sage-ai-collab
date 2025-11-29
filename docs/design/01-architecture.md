---
title: SAGE Knowledge Base - Architecture Design
version: 0.1.0
date: 2025-11-28
status: production-ready
---

# Architecture Design

> **Core-Services-Capabilities Modular Architecture with Dev Tools Isolation**

> ⚠️ **Document Type: Design Specification (Target Architecture)**
>
> This document describes the **target architecture** and **design goals** for the SAGE Knowledge Base system.
> It serves as a blueprint for implementation, not documentation of the current state.
>
> **Current Implementation Status (2025-11-29):**
>
> | Aspect | Design Target | Current State | Status |
> |--------|---------------|---------------|--------|
> | Package name | `sage-kb` | `sage-kb` in pyproject.toml | ✅ Complete |
> | Source location | `src/sage/` | `src/sage/` | ✅ Complete |
> | Config file | `sage.yaml` | Created at project root | ✅ Complete |
> | Directory structure | Core/Services/Capabilities | core/, services/, capabilities/ | ✅ Complete |
> | Capabilities layer | analyzers, checkers, monitors | Implemented | ✅ Complete |
> | Core infrastructure | DI, EventBus, Protocols | core/di/, core/events/, core/protocols.py | ✅ Complete |
> | Structured logging | structlog integration | core/logging/ | ✅ Complete |
> | Memory persistence | MemoryStore, TokenBudget | core/memory/ | ✅ Complete |
> | SAGE Protocol | models, protocols, exceptions | core/models.py, core/protocols.py, core/exceptions.py | ✅ Complete |
> | Configuration | SAGEConfig, env overrides | core/config.py | ✅ Complete |
> | Domain models | KnowledgeAsset, Session | domain/knowledge.py, domain/session.py | ✅ Complete |
> | Interfaces | Protocol re-exports | interfaces/__init__.py | ✅ Complete |
> | Entry point | python -m sage | __main__.py | ✅ Complete |
>
> **Status**: M3 complete. 841+ tests passing, 89% coverage.
>
> For detailed implementation status and roadmap, see `07-roadmap.md`.

## Architecture Overview

```
                              [Config File sage.yaml]
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           Core Engine Layer                             │
│                        (<500 lines minimal core)                        │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ SAGE Protocol Interface (Source-Analyze-Generate-Evolve)          │  │
│  │ +-- SourceProtocol    (S) - Knowledge sourcing                    │  │
│  │ +-- AnalyzeProtocol   (A) - Processing & analysis                 │  │
│  │ +-- GenerateProtocol  (G) - Multi-channel output                  │  │
│  │ +-- EvolveProtocol    (E) - Metrics & optimization                │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ TimeoutManager (Core infrastructure for timeout handling)         │  │
│  │ +-- TimeoutConfig     - Timeout level configuration (T1-T5)       │  │
│  │ +-- CircuitBreaker    - Circuit breaker pattern implementation    │  │
│  │ +-- execute_with_timeout() - Async timeout execution              │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ EventBus (Async pub/sub message broker)                           │  │
│  │ +-- source.*    (S) - Knowledge sourcing events                   │  │
│  │ +-- analyze.*   (A) - Processing & analysis events                │  │
│  │ +-- generate.*  (G) - Multi-channel output events                 │  │
│  │ +-- evolve.*    (E) - Metrics & optimization events               │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ DI Container (Dependency Injection)                               │  │
│  │ +-- Lifetime: singleton | transient | scoped                      │  │
│  │ +-- Auto-wiring from type hints                                   │  │
│  │ +-- YAML-driven service registration                              │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           │                            │                            │
           ▼                            ▼                            ▼
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│    CLI Service      │      │    MCP Service      │      │    API Service      │
│      (Typer)        │      │     (FastMCP)       │      │     (FastAPI)       │
├─────────────────────┤      ├─────────────────────┤      ├─────────────────────┤
│ • get               │      │ • get_knowledge     │      │ GET /knowledge      │
│ • search            │      │ • search_knowledge  │      │ GET /search         │
│ • info              │      │ • kb_info           │      │ GET /info           │
│ • serve             │      │ • get_framework     │      │ GET /frameworks     │
│ • analyze           │      │ • analyze_*         │      │ GET /analyze/*      │
│ • check             │      │ • check_*           │      │ GET /check/*        │
│ • health            │      │ • check_health      │      │ GET /health         │
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
           │                            │                            │
           └────────────────────────────┼────────────────────────────┘
                                        │
                                        ▼
                       ┌──────────────────────────────────────────────┐
                       │            Capabilities Layer                │  ← Runtime Capabilities
                       │      (Analyzers, Checkers, Monitors)         │
                       ├──────────────────────────────────────────────┤
                       │ • analyzers/   Quality, Content              │
                       │ • checkers/    Links                         │
                       │ • monitors/    Health                        │
                       └──────────────────────────────────────────────┘

                             ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
                             │              Tools Layer                  │  ← Dev-Only (Isolated)
                             │            (Dev Utilities)                │
                             ├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤
                             │ • monitors/         TimeoutMonitor (perf) │
                             │ • dev_scripts/      Development setup     │
                             └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘

Layer Separation:
  - Interfaces: Protocol definitions (shared contracts for all layers)
  - Domain: Business models (KnowledgeAsset, CollaborationSession, etc.)
  - Core: Minimal engine, protocols, TimeoutManager, EventBus, DI Container
  - Services: CLI, MCP, API interfaces (call Capabilities)
  - Capabilities: Runtime abilities exposed via Services (HealthMonitor, etc.)
  - Tools: Dev-only utilities, NOT imported at runtime (TimeoutMonitor, etc.)
  - Plugins: Extension mechanism (base + bundled implementations)

Key Distinctions:
  - TimeoutManager (Core): Infrastructure for timeout execution, used by loader
  - TimeoutMonitor (Tools): Dev tool for timeout statistics and performance analysis
  - HealthMonitor (Capabilities): Runtime health checks exposed via MCP

Zero Cross Import: Services communicate via EventBus; Services directly use Capabilities
Pluggable: Every feature is an independent plugin
On-Demand: Config file controls loading
Dev Tools Isolation: Tools exposed via MCP are dynamically imported only when called
```

---

## Dependency Rules

| Rule                      | Description                                 | Example                                       |
|---------------------------|---------------------------------------------|-----------------------------------------------|
| ✅ Services → Core         | Services can import from Core               | `from sage.core.loader import TimeoutLoader`  |
| ✅ Services → Capabilities | Services can import from Capabilities       | `from sage.capabilities.analyzers import ...` |
| ✅ Capabilities → Core     | Capabilities can import from Core           | `from sage.core.config import SageSettings`   |
| ❌ Core → Services         | Core cannot import from Services            | Forbidden: circular dependency                |
| ❌ Core → Capabilities     | Core cannot import from Capabilities        | Forbidden: core should be independent         |
| ❌ Services ↔ Services     | Services cannot import each other           | Use EventBus for communication                |
| ❌ Capabilities ↔ Services | Capabilities cannot import from Services    | Forbidden: reverse dependency                 |
| ⚠️ tools/ (isolated)      | tools/ is dev-only, not imported at runtime | Monitors, dev utilities                       |

### Key Design Principles

1. **Zero Cross-Import**: Layers communicate via EventBus, no direct dependencies
2. **Capabilities Layer**: Runtime abilities (analyzers, checkers) exposed via Services
3. **Pluggable**: Every module is an independent plugin, can be enabled/disabled
4. **On-Demand Loading**: Minimal core engine, features loaded as needed
5. **Unidirectional Dependency**: Lower layers don't depend on upper layers
6. **Interface-First**: All interactions through explicit Protocol interfaces
7. **Dev Tools Isolation**: tools/ directory is for development only, never imported at runtime

---

## Directory Structure

> **Design Document**: Production-Ready Directory Structure
> **Key Features**: MECE 8-directory organization, modular architecture, unified logging

```
sage/                                  # 📁 Project root directory
│
├── README.md                          # 🔹 Project documentation
├── LICENSE                            # 🔹 Open source license
├── CHANGELOG.md                       # 🔹 Change log
├── pyproject.toml                     # 🔹 Python project configuration
├── Makefile                           # 🔹 Make development commands
├── justfile                           # 🔹 Just commands (cross-platform, modern)
├── .pre-commit-config.yaml            # 🔹 Pre-commit hook configuration
├── .env.example                       # 🔹 Environment variables template
├── .gitignore                         # 🔹 Git ignore rules
│
├── sage.yaml                          # 🔹 Smart loading configuration
├── index.md                           # 🔹 Navigation entry (~100 tokens, Always Load)
├── features.yaml                      # 🆕 Feature flags configuration
│
├── .junie/                            # 🔒 JetBrains Junie AI configuration (hidden)
│   ├── guidelines.md                  #    AI collaboration guidelines (Knowledge Index)
│   ├── loading_rules.yaml             #    Smart loading configuration
│   └── mcp/                           #    MCP server configuration
│
├── .context/                          # 🔒 Project-specific knowledge base (hidden)
│   ├── index.md                       #    Context navigation entry
│   ├── conventions/                   #    Project conventions
│   ├── decisions/                     #    Architecture Decision Records (ADRs)
│   └── intelligence/                  # 🆕 AI intelligence patterns
│
├── .history/                          # 🔒 AI session history and handoffs (hidden)
│   ├── current/                       #    Current session state
│   ├── conversations/                 #    Conversation records
│   └── handoffs/                      #    Task handoff documents
│
├── .archive/                          # 🔒 Historical archives (hidden)
│   └── 202511/                        # 🆕 Monthly organization (YYYYMM format)
│
├── .logs/                             # 🔒 Runtime log files (hidden, git-ignored)
│   └── .gitkeep                       #    Placeholder for empty directory
│
├── .outputs/                          # 🔒 Intermediate process files (hidden, git-ignored)
│   └── .gitkeep                       #    Placeholder for empty directory
│
├── docs/                              # 📖 Project documentation (separate from content)
│   ├── design/                        #    Design documents
│   │   ├── 00-overview.md             #    Project overview
│   │   ├── 01-architecture.md         #    Architecture design (this file)
│   │   ├── 02-sage-protocol.md        #    SAGE protocol design
│   │   ├── 03-services.md             #    Services layer design
│   │   ├── 04-timeout-loading.md      #    Timeout & smart loading
│   │   ├── 05-plugin-memory.md        #    Plugin system & memory
│   │   ├── 06-content-structure.md    #    Content organization
│   │   ├── 07-roadmap.md              #    Implementation roadmap
│   │   └── 08-evaluation.md           #    Expert committee evaluation
│   ├── api/                           #    API documentation
│   │   ├── http_api.md                #    HTTP REST API reference
│   │   ├── mcp_protocol.md            #    MCP protocol specification
│   │   └── cli_reference.md           #    CLI command reference
│   ├── guides/                        #    Development guides
│   │   ├── quickstart.md              #    Quick start guide
│   │   └── contributing.md            #    Contributing guide
│   └── standards/                     # 🆕 Standards documentation
│       └── navigation_standards.md    #    Navigation hierarchy (L0-L4)
│
├── content/                           # 📚 Knowledge content directory
│   │
│   ├── core/                          # 🔸 Core principles (~500 tokens, Always Load)
│   │   ├── principles.md              #    Xin-Da-Ya philosophy, core values
│   │   ├── quick_reference.md         #    5 critical questions, autonomy quick ref
│   │   └── defaults.md                #    Default behaviors, calibration standards
│   │
│   ├── guidelines/                    # 🔸 Engineering guidelines (~1,200 tokens, On-Demand)
│   │   ├── guidelines_index.yaml      # 🆕 Semantic ordering configuration
│   │   ├── quick_start.md             #    3-minute quick start (~60 lines)
│   │   ├── planning_design.md         #    Planning and architecture (~80 lines)
│   │   ├── code_style.md              #    Code style standards (~150 lines)
│   │   ├── engineering.md             #    Config/test/perf/change/maintain (~120 lines)
│   │   ├── documentation.md           #    Documentation standards (~100 lines)
│   │   ├── python.md                  #    Python best practices (~130 lines)
│   │   ├── ai_collaboration.md        #    AI collaboration and autonomy (~200 lines)
│   │   ├── cognitive.md               #    Cognitive enhancement core (~100 lines)
│   │   ├── quality.md                 #    Quality framework (~80 lines)
│   │   └── success.md                 #    Xin-Da-Ya mapping, success criteria (~80 lines)
│   │
│   ├── frameworks/                    # 🔸 Deep frameworks (~2,000 tokens, On-Demand)
│   │   ├── autonomy/                  #    Autonomy framework
│   │   │   └── levels.md              #    6-level autonomy spectrum definition
│   │   ├── cognitive/                 #    Cognitive framework
│   │   │   └── expert_committee.md    #    Expert committee, chain-of-thought, iteration
│   │   ├── collaboration/             #    Collaboration framework
│   │   │   └── patterns.md            #    Collaboration patterns, instruction engineering
│   │   ├── decision/                  #    Decision framework
│   │   │   └── quality_angles.md      #    Quality angles, expert roles
│   │   └── timeout/                   #    Timeout framework
│   │       └── hierarchy.md           #    Timeout principles, strategies, recovery
│   │
│   ├── practices/                     # 🔸 Best practices (~1,500 tokens, On-Demand)
│   │   ├── ai_collaboration/          #    AI collaboration practices
│   │   │   └── workflow.md            #    Workflow, interaction patterns
│   │   ├── decisions/                 # 🆕 Dynamic framework cases
│   │   │   └── autonomy_cases.md      #    Concrete autonomy decision examples
│   │   ├── documentation/             #    Documentation practices
│   │   │   └── DOCUMENTATION_STANDARDS.md  #    Documentation standards (SSOT)
│   │   └── engineering/               #    Engineering practices
│   │       └── patterns.md            #    Design patterns, best practices
│   │
│   ├── scenarios/                     # 🔸 Scenario presets (~500 tokens, On-Demand)
│   │   └── python_backend/            #    Python backend scenario
│   │       └── context.md             #    Context configuration, specific guidelines
│   │
│   └── templates/                     # 🔸 Reusable templates (~300 tokens, On-Demand)
│       ├── project_setup.md           #    Project initialization template
│       └── expert_committee.md        # 🆕 Standardized decision prompts template
│
├── src/                               # 💻 Source code directory (modular architecture)
│   └── sage/                          #    Main package
│       ├── __init__.py                #    Package entry, version info
│       ├── __main__.py                # 🆕 Unified entry point (python -m sage)
│       ├── py.typed                   # 🆕 PEP 561 type marker
│       │
│       ├── interfaces/                # 🆕 Protocol definitions (centralized)
│       │   ├── __init__.py            #    Interface exports
│       │   └── protocols.py           #    All Protocol definitions
│       │
│       ├── domain/                    # 🆕 Business domain models
│       │   ├── __init__.py            #    Domain exports
│       │   ├── knowledge.py           #    KnowledgeAsset, KnowledgeCycle
│       │   └── session.py             #    CollaborationSession models
│       │
│       ├── core/                      # 🔷 Layer 1: Core layer (<500 lines)
│       │   ├── __init__.py            #    Core layer exports
│       │   ├── config.py              #    Config management (YAML+ENV+defaults)
│       │   ├── loader.py              #    Knowledge loader (with timeout protection)
│       │   ├── timeout.py             # 🆕 Timeout management (moved from tools)
│       │   ├── models.py              # 🆕 Data model definitions
│       │   ├── protocols.py           # 🆕 SAGE protocol interfaces
│       │   ├── eventbus.py            # 🆕 Async pub/sub message broker
│       │   ├── container.py           # 🆕 DI container
│       │   ├── exceptions.py          #    Exception hierarchy
│       │   └── logging/               # 🆕 Unified logging subpackage
│       │       ├── __init__.py        #    Logging exports (get_logger, bind_context)
│       │       ├── config.py          #    Logging config (structlog + stdlib)
│       │       ├── processors.py      #    structlog processors
│       │       └── context.py         #    Context management (request_id, etc.)
│       │
│       ├── services/                  # 🔶 Layer 2: Services layer
│       │   ├── __init__.py            #    Services layer exports
│       │   ├── cli.py                 #    Rich CLI command-line interface
│       │   ├── mcp_server.py          #    MCP service implementation (calls capabilities)
│       │   └── http_server.py         # 🆕 HTTP REST API (optional)
│       │
│       ├── capabilities/              # 🆕 Runtime Capabilities (used by Services, exposed via MCP/API)
│       │   ├── __init__.py            #    Capabilities package exports
│       │   ├── analyzers/             #    Analysis capabilities
│       │   │   ├── __init__.py        #    Analyzers exports
│       │   │   ├── quality.py         #    Quality analyzer (MCP: analyze_quality)
│       │   │   └── content.py         #    Content analyzer (MCP: analyze_content)
│       │   ├── checkers/              #    Checking capabilities
│       │   │   ├── __init__.py        #    Checkers exports
│       │   │   └── links.py           #    Link checker (MCP: check_links)
│       │   └── monitors/              #    Monitoring capabilities
│       │       ├── __init__.py        #    Monitors exports
│       │       └── health.py          #    Health monitor (MCP: check_health)
│       │
│       └── plugins/                   # 🔌 Plugin infrastructure (interfaces + registry)
│           ├── __init__.py            #    Plugin package exports
│           ├── base.py                #    Plugin base classes (7 hook points)
│           ├── registry.py            #    Plugin registry with hot-reload
│           └── bundled/               # 🆕 Bundled plugin implementations (moved from tools/)
│               ├── __init__.py        #    Bundled plugins exports
│               ├── cache_plugin.py    #    Content caching plugin
│               └── semantic_search.py #    Semantic search plugin
│
├── tools/                             # 🔧 Tools directory (Dev-Only, NOT imported at runtime)
│   ├── __init__.py                    #    Tools package init
│   │
│   ├── monitors/                      # 📊 Monitoring tools (dev-only)
│   │   ├── __init__.py                #    Monitors exports
│   │   └── timeout_monitor.py         #    Timeout statistics (MCP: get_timeout_stats)
│   │
│   └── dev_scripts/                   # 🆕 Development scripts (dev-only)
│       ├── __init__.py                #    Scripts exports
│       └── setup_dev.py               #    Development environment setup
│
├── tests/                             # 🧪 Test directory (mirrors source structure)
│   ├── __init__.py                    #    Test package init
│   ├── conftest.py                    # 🆕 Global pytest fixtures
│   │
│   ├── fixtures/                      # 🆕 Test data
│   │   ├── __init__.py
│   │   ├── sample_content/            #    Sample knowledge content
│   │   │   ├── index.md
│   │   │   └── core/
│   │   ├── mock_responses/            #    Mock response data
│   │   │   ├── mcp_success.json
│   │   │   └── mcp_error.json
│   │   └── configs/                   #    Test configurations
│   │       └── sage_test.yaml
│   │
│   ├── unit/                          # 🆕 Unit tests
│   │   ├── __init__.py
│   │   ├── core/                      #    Tests for src/sage/core/
│   │   │   ├── __init__.py
│   │   │   ├── test_config.py
│   │   │   ├── test_loader.py
│   │   │   ├── test_timeout.py
│   │   │   └── test_logging.py
│   │   └── services/                  #    Tests for src/sage/services/
│   │       ├── __init__.py
│   │       ├── test_cli.py
│   │       └── test_mcp_server.py
│   │
│   ├── integration/                   # 🆕 Integration tests
│   │   ├── __init__.py
│   │   ├── test_end_to_end.py
│   │   └── test_mcp_workflow.py
│   │
│   ├── tools/                         # 🆕 Tool tests
│   │   ├── __init__.py
│   │   └── test_timeout_monitor.py    #    Tests for tools/monitors/
│   │
│   └── performance/                   # Performance tests
│       ├── __init__.py
│       ├── test_performance.py
│       └── benchmarks/                # 🆕 Benchmark tests
│           ├── __init__.py
│           └── bench_loader.py
│
├── examples/                          # 📝 Usage examples
│   ├── basic_usage.py                 #    Basic usage example
│   ├── custom_loader.py               #    Custom loader example
│   ├── plugin_development.py          #    Plugin development guide
│   ├── structured_logging.py          # 🆕 Structured logging example
│   └── cli_automation.sh              #    CLI automation script
│
└── scripts/                           # 🛠️ Development scripts
    ├── setup_dev.sh                   #    Dev environment setup
    ├── run_tests.sh                   #    Run tests
    └── build_docs.sh                  #    Build documentation
```

---

## Directory Statistics

> **Design Target**: Production-ready directory structure statistics

| Directory                        | Files    | Subdirs | Primary Function                                      |
|----------------------------------|----------|---------|-------------------------------------------------------|
| Root                             | 12       | 12      | Project entry, config, dev toolchain (+features.yaml) |
| .junie/                          | 2        | 1       | JetBrains Junie AI configuration (hidden)             |
| .context/                        | 1        | 3       | Project-specific KB (+intelligence/)                  |
| .history/                        | 0        | 3       | AI session history (current/conversations/handoffs)   |
| .archive/                        | 0        | 1       | Historical archives (monthly: 202511/)                |
| docs/                            | 7        | 4       | Project documentation (+standards/)                   |
| content/core/                    | 3        | 0       | Core principles (~500 tokens, Always Load)            |
| content/guidelines/              | 11       | 0       | Engineering guidelines (+guidelines_index.yaml)       |
| content/frameworks/              | 5        | 5       | Deep frameworks (~2,000 tokens)                       |
| content/practices/               | 4        | 4       | Best practices (+decisions/)                          |
| content/scenarios/               | 1        | 1       | Scenario presets (~500 tokens)                        |
| content/templates/               | 2        | 0       | Templates (+expert_committee.md)                      |
| src/sage/interfaces/             | 2        | 0       | Protocol definitions (centralized)                    |
| src/sage/domain/                 | 3        | 0       | Business domain models                                |
| src/sage/core/                   | 9        | 1       | Core layer (Layer 1, <500 lines)                      |
| src/sage/core/logging/           | 4        | 0       | Unified logging (structlog + stdlib)                  |
| src/sage/services/               | 4        | 0       | Services layer (Layer 2)                              |
| src/sage/capabilities/           | 1        | 3       | 🆕 Runtime capabilities (exposed via MCP/API)         |
| src/sage/capabilities/analyzers/ | 2        | 0       | 🆕 Analyzers (quality, content)                       |
| src/sage/capabilities/checkers/  | 2        | 0       | 🆕 Checkers (links)                                   |
| src/sage/capabilities/monitors/  | 2        | 0       | 🆕 Monitors (health)                                  |
| src/sage/plugins/                | 3        | 1       | Plugin infrastructure (interfaces + registry)         |
| src/sage/plugins/bundled/        | 3        | 0       | 🆕 Bundled plugin implementations (moved from tools/) |
| tools/                           | 1        | 2       | 🔄 Dev-only tools (NOT imported at runtime)           |
| tools/monitors/                  | 2        | 0       | 🆕 Timeout statistics and performance (dev-only)      |
| tools/dev_scripts/               | 2        | 0       | 🆕 Development scripts (dev-only)                     |
| tests/fixtures/                  | 4        | 3       | Test data (sample content, mocks, configs)            |
| tests/unit/                      | 7        | 2       | Unit tests (mirrors src/ structure)                   |
| tests/integration/               | 3        | 0       | Integration tests                                     |
| tests/tools/                     | 2        | 0       | Tool tests                                            |
| tests/performance/               | 3        | 1       | Performance tests + benchmarks                        |
| examples/                        | 5        | 0       | Usage examples                                        |
| scripts/                         | 3        | 0       | Development scripts                                   |
| **Total**                        | **~105** | **~40** | Production-ready structure (streamlined)              |

---

## Generated Directories (Git Ignored)

> **Note**: These directories are created during development/testing and should be in `.gitignore`

| Directory         | Purpose                  | Generated By         | Clean Command            |
|-------------------|--------------------------|----------------------|--------------------------|
| `allure-results/` | Raw test results (JSON)  | `pytest --alluredir` | `rm -rf allure-results/` |
| `allure-report/`  | Static HTML test reports | `allure generate`    | `rm -rf allure-report/`  |
| `htmlcov/`        | Coverage HTML reports    | `pytest-cov`         | `rm -rf htmlcov/`        |
| `.coverage`       | Coverage data file       | `pytest-cov`         | `rm .coverage`           |
| `.pytest_cache/`  | pytest cache             | `pytest`             | `rm -rf .pytest_cache/`  |
| `.mypy_cache/`    | Type check cache         | `mypy`               | `rm -rf .mypy_cache/`    |
| `.ruff_cache/`    | Linter cache             | `ruff`               | `rm -rf .ruff_cache/`    |
| `build/`          | Build artifacts          | `hatchling`          | `rm -rf build/`          |
| `dist/`           | Distribution packages    | `hatchling`          | `rm -rf dist/`           |
| `*.egg-info/`     | Package metadata         | `pip install -e`     | `rm -rf *.egg-info/`     |

### Recommended .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
build/
dist/
*.egg-info/

# Testing & Coverage
.pytest_cache/
.coverage
.coverage.*
htmlcov/
.tox/

# Allure Reports
allure-results/
allure-report/

# Linting & Type Checking
.mypy_cache/
.ruff_cache/

# Virtual environments
.venv/
venv/
.env

# IDE
.idea/
.vscode/
```

---

## Unified Logging

### Technology Selection

| Component       | Choice                      | Rationale                                |
|-----------------|-----------------------------|------------------------------------------|
| **Core**        | structlog                   | Structured logging, context binding      |
| **Integration** | stdlib logging              | Compatibility with third-party libraries |
| **Output**      | JSON (prod) / Console (dev) | Machine-readable in production           |

### Logging Configuration

```python
# src/sage/core/logging/config.py
import structlog
import logging
import sys


def configure_logging(
    level: str = "INFO",
    format: str = "console",  # "console" or "json"
    log_file: str | None = None
) -> None:
    """Configure unified logging for the application."""

    # Shared processors
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if format == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=shared_processors + [
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure stdlib logging for third-party libraries
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
```

### Usage Example

```python
from sage.core.logging import get_logger, bind_context

logger = get_logger(__name__)

# Basic logging
logger.info("loading layer", layer="core", tokens=500)
logger.debug("cache hit", key="principles.md")

# Context binding
with bind_context(request_id="req-123", user="ai-client"):
    logger.info("processing request")
    # All logs in this context will include request_id and user

# Error logging with stack trace
try:
    risky_operation()
except Exception as e:
    logger.exception("operation failed", error=str(e))
```

### Output Formats

**Development (console format):**

```
2025-11-28T14:30:00+08:00 [info     ] loading layer              layer=core request_id=req-123 tokens=500
```

**Production (JSON format):**

```json
{
  "timestamp": "2025-11-28T14:30:00+08:00",
  "level": "info",
  "event": "loading layer",
  "layer": "core",
  "tokens": 500,
  "request_id": "req-123"
}
```

---

## Development Toolchain

### Makefile Commands

```makefile
.PHONY: help install dev test lint format serve clean

help:           ## Show all commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:        ## Install production dependencies
	pip install -e .

dev:            ## Install dev dependencies + pre-commit
	pip install -e ".[dev]"
	pre-commit install

test:           ## Run all tests with coverage
	pytest tests/ -v --cov=sage --cov-report=term-missing --alluredir=allure-results

test-parallel:  ## Run tests in parallel
	pytest tests/ -v -n auto --alluredir=allure-results

lint:           ## Run ruff + mypy
	ruff check src/ tests/
	mypy src/

format:         ## Format code with ruff
	ruff format src/ tests/

serve:          ## Start MCP server
	python -m sage serve

clean:          ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .ruff_cache
```

### justfile (Cross-Platform)

```just
# justfile - Cross-platform task runner
# Install: cargo install just OR pip install just

default:
    @just --list

install:
    pip install -e .

dev:
    pip install -e ".[dev]"
    pre-commit install

test:
    pytest tests/ -v --cov=sage --alluredir=allure-results

test-parallel:
    pytest tests/ -v -n auto

lint:
    ruff check src/ tests/
    mypy src/

format:
    ruff format src/ tests/

serve:
    python -m sage serve
```

### Pre-commit Hooks

> **Note**: The `.pre-commit-config.yaml` file below is a recommended configuration for future implementation. It has
> not been created in the project yet.

```yaml
# .pre-commit-config.yaml (recommended)
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [ --fix ]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.0
    hooks:
      - id: mypy
        additional_dependencies: [ pydantic>=2.0 ]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

---

## Package Distribution

### Why No MANIFEST.in?

This project uses `hatchling` as the build backend (PEP 517/518/621 compliant). With hatchling, `MANIFEST.in` is **not
needed**.

| Approach       | Era                 | Configuration                              |
|----------------|---------------------|--------------------------------------------|
| MANIFEST.in    | Legacy (setuptools) | Separate file with glob patterns           |
| pyproject.toml | Modern (hatchling)  | `[tool.hatch.build.targets.sdist]` section |

### pyproject.toml Configuration

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "sage-kb"
version = "0.1.0"
description = "Production-grade knowledge management for AI collaboration"
readme = "README.md"
license = "MIT"
requires-python = ">=3.12"
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Typing :: Typed",
]

dependencies = [
    "pyyaml>=6.0.2",
    "pydantic>=2.8",
    "pydantic-settings>=2.3",
    "structlog>=24.4",
    "platformdirs>=4.2",
    "anyio>=4.4",
    "typer>=0.12",
    "rich>=13.8",
    "fastapi>=0.115",
    "uvicorn>=0.30",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3",
    "pytest-asyncio>=0.24",
    "pytest-cov>=5.0",
    "pytest-xdist>=3.5",
    "allure-pytest>=2.13",
    "hypothesis>=6.108",
    "ruff>=0.6",
    "mypy>=1.11",
    "pre-commit>=3.8",
]
mcp = [
    "fastmcp>=2.0",
]

[project.scripts]
sage = "sage.services.cli:app"

[tool.hatch.build.targets.sdist]
include = [
    "/src",
    "/content",
    "/tools",
    "/index.md",
    "/sage.yaml",
    "/README.md",
    "/LICENSE",
]

[tool.hatch.build.targets.wheel]
packages = ["src/sage"]
only-include = ["src/sage"]

[tool.ruff]
line-length = 88
target-version = "py312"
select = ["E", "F", "W", "I", "UP", "B", "C4", "PTH"]

[tool.ruff.format]
quote-style = "double"

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --tb=short"
```

---

## Python Version Features

> **Source**: Level 5 Expert Committee Comprehensive Modernization Enhancement (8.11.2)

This project requires Python 3.12+ and adopts modern Python features progressively.

### Python 3.12 Features (Required)

| Feature               | PEP     | Application       | Code Example                       |
|-----------------------|---------|-------------------|------------------------------------|
| Type parameter syntax | PEP 695 | Generic classes   | `class Loader[T]:`                 |
| Type aliases          | PEP 695 | Type definitions  | `type LoadResult = dict[str, Any]` |
| Union syntax          | -       | Optional types    | `value: str \| None`               |
| @override decorator   | PEP 698 | Method overrides  | `@override def load():`            |
| Improved f-strings    | PEP 701 | String formatting | Nested quotes, multiline           |
| Faster isinstance()   | -       | Protocol checks   | 2-20x speedup                      |

### Python 3.13 Features (Optional/Forward-Compatible)

| Feature                 | PEP     | Application      | Code Example                    |
|-------------------------|---------|------------------|---------------------------------|
| Type parameter defaults | PEP 696 | Generic defaults | `class Cache[K = str]:`         |
| @deprecated decorator   | PEP 702 | API deprecation  | `@deprecated("Use v2")`         |
| typing.ReadOnly         | PEP 705 | Immutable fields | `ReadOnly[str]`                 |
| typing.TypeIs           | PEP 742 | Type narrowing   | `def is_str(x) -> TypeIs[str]:` |

### Python 3.14 Features (Future-Ready)

| Feature                 | PEP         | Application      | Notes                    |
|-------------------------|-------------|------------------|--------------------------|
| Template strings        | PEP 750     | Safe templating  | t-string literals        |
| Deferred annotations    | PEP 649/749 | Lazy evaluation  | No `__future__` import   |
| concurrent.interpreters | PEP 734     | True parallelism | Multi-interpreter stdlib |

### Modern Python Code Patterns

```python
# ============ Before (Old Style) ============
from typing import TypeVar, Generic, Optional, List

T = TypeVar("T")


class Container(Generic[T]):
    def __init__(self, value: Optional[T] = None) -> None:
        self.value = value

    def get_items(self) -> List[T]:
        return []


# ============ After (Python 3.12+ Style) ============
from typing import override


# PEP 695: Type parameter syntax
class Container[T]:
    def __init__(self, value: T | None = None) -> None:
        self.value = value

    def get_items(self) -> list[T]:
        return []


# PEP 695: Type aliases
type LoadResult = dict[str, str | int | list[str]]
type EventHandler[T] = Callable[[T], Awaitable[None]]


# PEP 698: Override decorator
class CustomLoader(BaseLoader):
    @override
    async def load(self, layers: list[str]) -> LoadResult:
        ...
```

### Migration Guidelines

1. **New code**: Always use Python 3.12+ syntax
2. **Existing code**: Migrate during refactoring (not urgently)
3. **Type hints**: Prefer `list[T]` over `List[T]`, `dict[K, V]` over `Dict[K, V]`
4. **Optionals**: Use `T | None` instead of `Optional[T]`
5. **Generics**: Use `class Foo[T]:` instead of `class Foo(Generic[T]):`

---

## Cross-Platform Support

### Platform-Specific Paths

Using `platformdirs` for cross-platform directory handling:

```python
from platformdirs import user_config_dir, user_cache_dir, user_data_dir
from pathlib import Path


def get_platform_paths() -> dict[str, Path]:
    """Get platform-specific paths for SAGE."""
    app_name = "sage"

    return {
        # Config: ~/.config/sage (Linux), ~/Library/Application Support/sage (macOS)
        "config": Path(user_config_dir(app_name)),

        # Cache: ~/.cache/sage (Linux), ~/Library/Caches/sage (macOS)
        "cache" : Path(user_cache_dir(app_name)),

        # Data: ~/.local/share/sage (Linux), ~/Library/Application Support/sage (macOS)
        "data"  : Path(user_data_dir(app_name)),
    }
```

### Platform Paths Table

| Platform    | Config                                | Cache                                       | Data                                  |
|-------------|---------------------------------------|---------------------------------------------|---------------------------------------|
| **Linux**   | `~/.config/sage/`                     | `~/.cache/sage/`                            | `~/.local/share/sage/`                |
| **macOS**   | `~/Library/Application Support/sage/` | `~/Library/Caches/sage/`                    | `~/Library/Application Support/sage/` |
| **Windows** | `C:\Users\<user>\AppData\Local\sage\` | `C:\Users\<user>\AppData\Local\sage\Cache\` | `C:\Users\<user>\AppData\Local\sage\` |

### Path Handling Best Practices

```python
from pathlib import Path

# ✅ CORRECT: Use pathlib (cross-platform, explicit, readable)
config_file = Path("content") / "core" / "principles.md"

# ⚠️ AVOID: Hardcoded string paths (works but not recommended)
config_file = "content/core/principles.md"  # Works in Python, but not explicit
config_file = "content\\core\\principles.md"  # Windows-only, fails on Unix

# Note: Python's pathlib and open() handle forward slashes on all platforms.
# However, pathlib is preferred for:
# 1. Explicit cross-platform intent
# 2. Path manipulation (parent, stem, suffix)
# 3. Readable path construction with / operator
# 4. Consistency when passing paths to external tools/shell commands
```

---

## Configuration Hierarchy

### Priority Order (Highest to Lowest)

```
┌───────────────────────────────────────────────────┐
│ 1. Environment Variables (SAGE_*)                 │ ← Highest
├───────────────────────────────────────────────────┤
│ 2. User Config (~/.config/sage/config.yaml)       │
├───────────────────────────────────────────────────┤
│ 3. Project Config (./sage.yaml)                   │
├───────────────────────────────────────────────────┤
│ 4. Package Defaults (built-in)                    │ ← Lowest
└───────────────────────────────────────────────────┘
```

### Environment Variable Examples

```bash
# Override timeout settings
export SAGE_TIMEOUT_GLOBAL_MAX_MS=15000
export SAGE_TIMEOUT_DEFAULT_MS=8000

# Override logging
export SAGE_LOG_LEVEL=DEBUG
export SAGE_LOG_FORMAT=json

# Override loading behavior
export SAGE_LOADING_MAX_TOKENS=8000
export SAGE_LOADING_CACHE_ENABLED=false
```

---

## Timeout & Reliability

> **Detailed Design**: See `04-timeout-loading.md`
> **Philosophy**: "No operation should block indefinitely"

### Five-Level Timeout Hierarchy

| Level  | Timeout | Scope            | Action on Timeout      | Use Case                   |
|--------|---------|------------------|------------------------|----------------------------|
| **T1** | 100ms   | Cache lookup     | Return cached/fallback | Memory cache, index lookup |
| **T2** | 500ms   | Single file read | Use partial/fallback   | Individual markdown file   |
| **T3** | 2s      | Layer load       | Load partial + warning | `content/core/` directory  |
| **T4** | 5s      | Full KB load     | Emergency core only    | All layers requested       |
| **T5** | 10s     | Complex analysis | Abort + summary        | Search, graph building     |

### Graceful Degradation Strategy

```
Priority Order: Always return something (never empty response)

┌────────────────────────────────────────────────────┐
│ Level 1: Full Load (all requested layers)          │ ← Ideal
├────────────────────────────────────────────────────┤
│ Level 2: Partial Load (core + some requested)      │ ← Acceptable
├────────────────────────────────────────────────────┤
│ Level 3: Minimal Load (core only)                  │ ← Fallback
├────────────────────────────────────────────────────┤
│ Level 4: Emergency (hardcoded principles)          │ ← Last resort
└────────────────────────────────────────────────────┘

Key Principles:
1. Core principles ALWAYS available (pre-cached)
2. Partial results preferred over timeout error
3. Clear indication of incomplete load in response
```

### Circuit Breaker Pattern

```yaml
# sage.yaml - Circuit Breaker Configuration
timeout:
  circuit_breaker:
    enabled: true
    failure_threshold: 3      # Open after 3 consecutive failures
    reset_timeout: 30s        # Try again after 30 seconds
    half_open_requests: 1     # Test requests in half-open state
```

**Circuit Breaker States:**

```
State Transitions:

    ┌──────────────────┐
    │      CLOSED      │  ← Normal operation
    │    (healthy)     │
    └────────┬─────────┘
             │
             │ failure_threshold exceeded
             ▼
    ┌──────────────────┐
    │       OPEN       │  ← Reject all requests
    │    (failing)     │
    └────────┬─────────┘
             │
             │ reset_timeout elapsed
             ▼
    ┌──────────────────┐
    │    HALF-OPEN     │  ← Test with limited requests
    │    (testing)     │
    └────────┬─────────┘
             │
       ┌─────┴─────┐
       │           │
       ▼           ▼
   success      failure
       │           │
       ▼           ▼
   CLOSED        OPEN
```

**State Transition Table:**

| Current State | Event             | Next State | Action                   |
|---------------|-------------------|------------|--------------------------|
| CLOSED        | failure_threshold | OPEN       | Start rejecting requests |
| OPEN          | reset_timeout     | HALF-OPEN  | Allow test request       |
| HALF-OPEN     | test_success      | CLOSED     | Resume normal operation  |
| HALF-OPEN     | test_failure      | OPEN       | Continue rejecting       |

---

## YAML Configuration DSL

> **Central Configuration**: All behavior controlled via `sage.yaml`

### Smart Loading Triggers

```yaml
# sage.yaml - Smart Loading with Keyword Triggers
loading:
  always: # Always loaded (pre-cached)
    - index.md
    - content/core/principles.md
    - content/core/quick_reference.md

triggers:
  code:
    keywords:
      # English
      - code
      - implement
      - fix
      - refactor
      - debug
      # Chinese (中文)
      - 代码
      - 实现
      - 修复
      - 重构
      - 调试
    load:
      - content/guidelines/code_style.md
      - content/guidelines/python.md
    timeout_ms: 2000
    priority: 1                        # Lower = higher priority

  architecture:
    keywords:
      # English
      - architecture
      - design
      - system
      - pattern
      # Chinese (中文)
      - 架构
      - 设计
      - 系统
      - 模式
    load:
      - content/guidelines/planning_design.md
      - content/frameworks/decision/
    timeout_ms: 3000
    priority: 2

  testing:
    keywords:
      # English
      - test
      - coverage
      - unit
      - integration
      # Chinese (中文)
      - 测试
      - 覆盖率
      - 单元
      - 集成
    load:
      - content/guidelines/engineering.md
    timeout_ms: 2000
    priority: 3

  ai_collaboration:
    keywords:
      # English
      - autonomy
      - collaboration
      - ai
      - level
      # Chinese (中文)
      - 自主
      - 协作
      - 人工智能
      - 级别
    load:
      - content/guidelines/ai_collaboration.md
      - content/frameworks/autonomy/
    timeout_ms: 2000
    priority: 4
```

### DI Container Configuration

```yaml
# sage.yaml - Dependency Injection Configuration
di:
  auto_wire: true                      # Auto-resolve from type hints

  services:
    EventBus: # S.A.G.E. aligned event bus
      lifetime: singleton              # One instance for entire app
      implementation: AsyncEventBus    # source.*/analyze.*/generate.*/evolve.* channels

    SourceProtocol: # S.A.G.E. - Source (knowledge sourcing)
      lifetime: singleton
      implementation: TimeoutLoader
      config_key: plugins.loader       # Additional config location

    AnalyzeProtocol: # S.A.G.E. - Analyze (processing & analysis)
      lifetime: transient              # New instance per request
      implementation: KnowledgeService

    GenerateProtocol: # S.A.G.E. - Generate (multi-channel output)
      lifetime: scoped                 # One instance per scope/request
      implementation: MultiChannelOutput
```

**Lifetime Types:**

| Lifetime    | Description                         | Use Case                           |
|-------------|-------------------------------------|------------------------------------|
| `singleton` | One instance for entire application | EventBus, Config, Cache            |
| `transient` | New instance per resolution         | Request handlers, DTOs             |
| `scoped`    | One instance per scope (request)    | Database sessions, request context |

### Timeout Configuration

```yaml
# sage.yaml - Timeout Configuration
timeout:
  global_max: 10s                      # Absolute maximum
  default: 5s                          # Default if not specified

  operations:
    cache_lookup: 100ms                # T1
    file_read: 500ms                   # T2
    layer_load: 2s                     # T3
    full_load: 5s                      # T4
    analysis: 10s                      # T5
    mcp_call: 10s
    search: 3s

  strategies:
    on_timeout:
      - return_partial                 # Return what we have
      - use_fallback                   # Use cached/default content
      - log_warning                    # Log for monitoring
      - never_hang                     # Guarantee response
```

---

## Application Bootstrap

> **Purpose**: Declarative application initialization from YAML configuration

### Bootstrap Flow

```
┌───────────────────────────────────────────────┐
│              Application Start                │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│  1. Load Configuration (sage.yaml)            │
│     - Parse YAML                              │
│     - Merge with ENV overrides                │
│     - Validate schema                         │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│  2. Configure Logging                         │
│     - Set log level from config               │
│     - Choose format (console/json)            │
│     - Bind context processors                 │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│  3. Initialize DI Container                   │
│     - Register services from config           │
│     - Set up lifetimes                        │
│     - Enable auto-wiring                      │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│  4. Start EventBus                            │
│     - Initialize S.A.G.E. aligned pub/sub     │
│     - Register source/analyze/generate/evolve │
│     - Setup default handlers per channel      │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│  5. Pre-cache Core Content                    │
│     - Load "always" content                   │
│     - Warm up fallback cache                  │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│  6. Start Requested Service                   │
│     - CLI / MCP Server / HTTP API             │
└───────────────────────────────────────────────┘
```

### Bootstrap Code Example

```python
# src/sage/core/bootstrap.py
from pathlib import Path
from typing import Optional, Dict, Any


async def bootstrap(
    config_path: Optional[Path] = None,
    config_override: Optional[Dict[str, Any]] = None
) -> DIContainer:
    """
    Bootstrap the application.
    
    Args:
        config_path: Path to sage.yaml (default: ./sage.yaml)
        config_override: Optional config overrides
    
    Returns:
        Configured DI container ready for use
    
    Example:
        container = await bootstrap()
        loader = container.resolve(SourceProtocol)
        result = await loader.load(["core"])
    """
    # 1. Load configuration
    config = load_config(config_path or Path("sage.yaml"))

    # 2. Apply overrides (ENV vars, explicit overrides)
    config = merge_config(config, config_override)

    # 3. Configure logging
    configure_logging(
        level=config.get("logging.level", "INFO"),
        format=config.get("logging.format", "console")
    )

    # 4. Initialize DI container
    container = DIContainer.get_instance()
    register_services(container, config.get("di.services", {}))

    # 5. Start EventBus (S.A.G.E. aligned: source/analyze/generate/evolve channels)
    event_bus = container.resolve(EventBus)
    await event_bus.start()

    # 6. Pre-cache core content (S.A.G.E. - Source)
    loader = container.resolve(SourceProtocol)
    await loader.precache(config.get("loading.always", []))

    return container
```

---

## Quick Start

> **Purpose**: Get started with SAGE Knowledge Base in 5 minutes

### Installation

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

### Basic Usage

```bash
# 1. Using the CLI
sage get --layer core       # Get core principles
sage search "autonomy"      # Search knowledge base
sage info                   # Get KB information

# 2. Start MCP server (for AI Agents)
python -m sage serve
```

```python
# 3. Using Python API
from sage.core.loader import KnowledgeLoader

loader = KnowledgeLoader()
result = await loader.load_core(timeout_ms=2000)
print(result.content)
```

**Available MCP tools:**

- `get_knowledge(layer, task, timeout_ms)`
- `search_knowledge(query, max_results)`
- `analyze_quality(path)`
- `check_health()`

### Configuration

```yaml
# sage.yaml - Minimal configuration
loading:
  always:
    - index.md
    - content/core/principles.md

timeout:
  default: 5s
  operations:
    cache_lookup: 100ms
    file_read: 500ms
```

---

## Exception Handling

> **Philosophy**: Graceful degradation over hard failures

### Exception Hierarchy

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

### Exception Propagation Rules

| Layer            | Catches           | Transforms To          | Action                 |
|------------------|-------------------|------------------------|------------------------|
| **Core**         | System exceptions | `LoadingError`         | Log + fallback content |
| **Capabilities** | Core exceptions   | Preserve or wrap       | Log + partial result   |
| **Services**     | All exceptions    | User-friendly response | Log + error response   |

### Timeout Exception Handling

```python
from sage.core.exceptions import TimeoutError
from sage.core.timeout import TimeoutManager


async def load_with_fallback(path: str, timeout_ms: int) -> str:
    """Load content with graceful timeout handling."""
    try:
        return await timeout_manager.execute(
            load_file(path),
            timeout_ms=timeout_ms
        )
    except TimeoutError:
        # Graceful degradation: return cached or fallback
        logger.warning("timeout_fallback", path=path, timeout_ms=timeout_ms)
        return get_fallback_content(path)
```

### Best Practices

1. **Never swallow exceptions silently** - Always log with context
2. **Prefer fallback over failure** - Return partial/cached content
3. **Include operation context** - Log what was being attempted
4. **Use structured logging** - Include relevant metadata

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

## AI Usage Scenarios

> **Purpose**: Guide AI Agents on when and how to use SAGE tools

### Scenario 1: New Task Assessment

**When**: AI Agent receives a new task from user

**Recommended Flow**:

```
1. get_knowledge(task="<user_task_description>")
   → Smart loading based on task keywords
   
2. If task involves code:
   get_guidelines(section="code_style")
   
3. If task involves architecture:
   get_framework(name="decision")
```

**Example**:

```python
# User: "Help me implement authentication for our API"
result = await get_knowledge(task="implement authentication API")
# Returns: code_style.md, python.md, engineering.md (auto-selected)
```

### Scenario 2: Quality Check Before Delivery

**When**: AI Agent is about to deliver code/documentation

**Recommended Flow**:

```
1. analyze_quality(path="<output_path>")
   → Get quality score (0-100)
   
2. If score < 80:
   Review issues and improve
   
3. check_links(path="<doc_path>")
   → Ensure no broken links
```

### Scenario 3: System Health Verification

**When**: Before starting complex operations

**Recommended Flow**:

```
1. check_health()
   → Verify system is operational
   
2. If status != "HEALTHY":
   Report to user, proceed with caution
```

### Scenario 4: Knowledge Search

**When**: AI Agent needs specific information

**Recommended Flow**:

```
1. search_knowledge(query="<topic>", max_results=5)
   → Find relevant content
   
2. get_knowledge(layer=<relevant_layer>)
   → Load full content
```

### Tool Selection Guide

| Task Type             | Primary Tool                      | Secondary Tools                |
|-----------------------|-----------------------------------|--------------------------------|
| New coding task       | `get_knowledge(task=...)`         | `get_guidelines("code_style")` |
| Architecture decision | `get_framework("decision")`       | `get_guidelines("planning")`   |
| Code review           | `analyze_quality(path)`           | `check_links(path)`            |
| Documentation         | `get_guidelines("documentation")` | `analyze_content(path)`        |
| Debugging             | `get_knowledge(task="debug")`     | `check_health()`               |
| Performance issue     | `get_timeout_stats()`             | `check_health()`               |

### Autonomy Level Mapping

> **Reference**: See `content/frameworks/autonomy/levels.md` for full 6-level autonomy framework

| Autonomy Level                           | Tool Usage Pattern                                                   |
|------------------------------------------|----------------------------------------------------------------------|
| **L1-L2** (Minimal/Low, 0-40%)           | Use `search_knowledge()` to find guidance, ask user for confirmation |
| **L3-L4** (Medium/Medium-High, 40-80%) ⭐ | Use `get_knowledge()` directly, report actions after                 |
| **L5-L6** (High/Full, 80-100%)           | Use tools autonomously, only report on completion                    |

**Default**: L4 (Medium-High) for mature collaboration.

### Autonomy Decision Tree

```
                        ┌─────────────────────┐
                        │   Assess Task Type  │
                        └──────────┬──────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
     ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
     │  High Risk?    │   │  Reversible?   │   │  Precedent?    │
     │  (breaking     │   │  (can undo     │   │  (done before  │
     │   changes)     │   │   easily)      │   │   successfully)│
     └───────┬────────┘   └───────┬────────┘   └───────┬────────┘
             │                    │                    │
        Yes  │  No           No   │  Yes          No   │  Yes
             │                    │                    │
             ▼                    ▼                    ▼
        ┌────────┐           ┌────────┐           ┌────────┐
        │ L1-L2  │           │ L3-L4  │           │ L5-L6  │
        │  Ask   │           │Proceed │           │  Auto  │
        │ First  │           │& Report│           │        │
        └────────┘           └────────┘           └────────┘

Decision Factors:
  • Impact Scope: Single file (↑) vs Multiple systems (↓)
  • Reversibility: Easy rollback (↑) vs Permanent (↓)
  • Precedent: Established pattern (↑) vs Novel approach (↓)
  • User Trust: Mature collaboration (↑) vs New relationship (↓)
```

> **Calibration Examples**: For practical scenarios demonstrating autonomy level selection
> (database migrations, unit tests, refactoring, production config), see Section 10 of
> `content/frameworks/autonomy/levels.md`.

---

## References

### Design Documents

- **Protocol Design**: See `02-sage-protocol.md`
- **Services**: See `03-services.md`
- **Timeout Details**: See `04-timeout-loading.md`
- **Plugin System**: See `05-plugin-memory.md`
- **Content Structure**: See `06-content-structure.md`
- **Implementation**: See `07-roadmap.md`
- **Expert Evaluation**: See `08-evaluation.md`

### Architecture Decision Records

- **ADR-0001**: `.context/decisions/ADR-0001-architecture.md` — Architecture design decisions
- **ADR-0004**: `.context/decisions/ADR-0004-dependency-injection.md` — DI container design
- **ADR-0005**: `.context/decisions/ADR-0005-event-bus.md` — EventBus design
- **ADR-0006**: `.context/decisions/ADR-0006-protocol-first.md` — Protocol-first design

