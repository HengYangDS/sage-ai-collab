# ADR-0001: Three-Layer Architecture

> Architecture Decision Record for SAGE Knowledge Base

---

## Status

**Accepted** | Date: 2025-11-28

---

## Context

SAGE Knowledge Base needs a modular, maintainable architecture that:

1. Separates concerns clearly between infrastructure, business logic, and interfaces
2. Supports multiple service interfaces (CLI, MCP, API)
3. Enables independent testing and deployment of components
4. Allows runtime extension through capabilities
5. Maintains clean dependency direction

### Constraints

- Must keep core minimal (<500 lines)
- Must support async operations throughout
- Must enable hot-pluggable capabilities
- Must isolate development tools from production code

---

## Decision

Adopt a **Core-Services-Capabilities** three-layer architecture with dev tools isolation.

### Layer Structure

```
┌─────────────────────────────────────────────────────────┐
│                    Core Engine Layer                    │
│                   (<500 lines minimal)                  │
│  • SAGE Protocol Interface                              │
│  • TimeoutManager                                       │
│  • EventBus                                             │
│  • DI Container                                         │
└─────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   CLI Service   │ │   MCP Service   │ │   API Service   │
│     (Typer)     │ │    (FastMCP)    │ │    (FastAPI)    │
└─────────────────┘ └─────────────────┘ └─────────────────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  Capabilities Layer                     │
│           (Analyzers, Checkers, Monitors)               │
└─────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Responsibility | Dependencies |
|-------|----------------|--------------|
| **Core** | Infrastructure, protocols, DI, events | None (standalone) |
| **Services** | User interfaces (CLI, MCP, API) | Core |
| **Capabilities** | Runtime features (analyzers, checkers) | Core |

### Dependency Rules

1. **Unidirectional**: Services → Core ← Capabilities
2. **No cross-layer**: Services cannot depend on Capabilities directly
3. **Protocol-based**: Layers communicate via protocols and EventBus
4. **Core isolation**: Core has zero external dependencies beyond stdlib

---

## Alternatives Considered

### Alternative 1: Monolithic Architecture

Single module with all functionality.

- **Pros**: Simple, no abstraction overhead
- **Cons**: Hard to test, maintain, extend; tight coupling
- **Rejected**: Does not scale with project growth

### Alternative 2: Hexagonal (Ports & Adapters)

Strict hexagonal architecture with ports and adapters.

- **Pros**: Very clean separation, highly testable
- **Cons**: Over-engineering for current scope; complexity overhead
- **Rejected**: Too complex for knowledge base domain

### Alternative 3: Plugin-Only Architecture

Everything as plugins, minimal core.

- **Pros**: Maximum flexibility
- **Cons**: Discovery complexity, performance overhead, harder debugging
- **Rejected**: Knowledge base needs stable core behaviors

---

## Consequences

### Positive

1. **Clear separation**: Each layer has single responsibility
2. **Testability**: Layers can be tested in isolation
3. **Flexibility**: Services and capabilities can be added independently
4. **Maintainability**: Changes localized to specific layers
5. **Scalability**: New services (e.g., gRPC) easily added

### Negative

1. **Indirection**: EventBus adds some complexity
2. **Learning curve**: New developers must understand layer boundaries
3. **Boilerplate**: Protocol definitions required for cross-layer communication

### Risks

1. **Layer leakage**: Developers might bypass layer boundaries
2. **Over-abstraction**: Risk of creating unnecessary protocols

### Mitigations

1. **Linting rules**: Enforce import restrictions
2. **Code review**: Check for layer violations
3. **Documentation**: Clear guidelines in `.context/conventions/`

---

## Implementation

### Directory Structure

```
src/sage/
├── core/           # Core layer
│   ├── config.py
│   ├── di/
│   ├── events/
│   ├── logging/
│   └── memory/
├── services/       # Services layer
│   ├── cli.py
│   ├── mcp.py
│   └── api.py
└── capabilities/   # Capabilities layer
    ├── analyzers/
    ├── checkers/
    └── monitors/
```

### Communication Patterns

```python
# Services → Core: Direct dependency
from sage.core.config import get_config
config = get_config()

# Core → Services: Via EventBus (decoupled)
bus.publish(Event(type="knowledge.loaded", data={...}))

# Services ↔ Capabilities: Via DI Container
analyzer = container.resolve(AnalyzerProtocol)
```

---

## Related

- `ADR-0004-dependency-injection.md` — DI container design
- `ADR-0005-event-bus.md` — Event communication
- `docs/design/01-architecture.md` — Full architecture documentation

---

*Part of SAGE Knowledge Base - Architecture Decisions*
