
# Memory Server Best Practices

> Knowledge graph persistence patterns and usage guidelines (~15 min read)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Entity Design Patterns](#2-entity-design-patterns)
3. [Entity Examples](#3-entity-examples)
4. [Relationship Modeling](#4-relationship-modeling)
5. [Query Strategies](#5-query-strategies)
6. [Session Workflow](#6-session-workflow)
7. [Best Practices](#7-best-practices)
8. [Common Patterns](#8-common-patterns)
9. [Troubleshooting](#9-troubleshooting)
10. [Fallback Approach](#10-fallback-approach)
11. [Related](#11-related)

---

## 1. Overview

The **Memory MCP Server** provides cross-session knowledge persistence through a knowledge graph structure. It enables
Junie to remember decisions, patterns, and context across multiple sessions.

### Core Capabilities

| Capability                    | Description                           | Use Case                         |
|:------------------------------|:--------------------------------------|:---------------------------------|
| **Entity Storage**            | Store named knowledge units           | Decisions, patterns, conventions |
| **Relationship Mapping**      | Connect entities with typed relations | Dependencies, hierarchies        |
| **Semantic Search**           | Query by meaning, not just keywords   | Find related concepts            |
| **Cross-Session Persistence** | Data survives session boundaries      | Long-term project memory         |

### When to Use

✅ **Recommended**:

- Architecture decisions that affect future development
- User preferences and coding conventions
- Learned patterns from codebase analysis
- Project-specific terminology and concepts

❌ **Not Recommended**:

- Temporary debugging information
- Session-specific context (use `.history/` instead)
- Large binary data or file contents
- Frequently changing operational data

---

## 2. Entity Design Patterns

### Entity Structure

```json
{
  "name": "unique_identifier",
  "type": "entity_type",
  "content": "Human-readable description and details"
}
```

### Recommended Entity Types

| Type         | Purpose                       | Example Name                 |
|:-------------|:------------------------------|:-----------------------------|
| `decision`   | Architecture/design decisions | `auth_strategy_jwt`          |
| `convention` | Coding conventions            | `naming_convention_services` |
| `pattern`    | Recognized code patterns      | `error_handling_pattern`     |
| `preference` | User preferences              | `test_framework_pytest`      |
| `concept`    | Domain concepts               | `timeout_hierarchy`          |
| `component`  | System components             | `core_layer_loader`          |

### Naming Conventions

```text
<category>_<subject>_<qualifier>

Examples:
- decision_auth_jwt
- convention_naming_files
- pattern_error_retry
- preference_format_ruff
```

---

## 3. Entity Examples

### Decision Entity

Store architecture or design decisions:

```javascript
memory.create_entities([{
    name: "decision_auth_jwt",
    type: "decision",
    content: "Using JWT for API authentication. Reasons: stateless, scalable, industry standard. Access tokens expire in 15 minutes, refresh tokens in 7 days."
}])
```

### Convention Entity

Store coding conventions:

```javascript
memory.create_entities([{
    name: "convention_file_naming",
    type: "convention",
    content: "Python files use snake_case. Classes use PascalCase. Constants use UPPER_SNAKE_CASE. Test files prefix with test_."
}])
```

### Pattern Entity

Store recognized code patterns:

```javascript
memory.create_entities([{
    name: "pattern_error_handling",
    type: "pattern",
    content: "Use custom exception classes. Log errors with context. Return structured error responses. Never expose internal errors to users."
}])
```

### Preference Entity

Store user preferences:

```javascript
memory.create_entities([{
    name: "preference_testing",
    type: "preference",
    content: "User prefers pytest with pytest-asyncio. Tests should be in tests/ directory. Use fixtures for common setup. Target 80% coverage."
}])
```

---

## 4. Relationship Modeling

### Creating Relationships

```javascript
memory.create_relations([{
    from: "UserService",
    to: "AuthModule",
    type: "depends_on"
}])
```

### Relationship Types

| Type         | Description                 | Example                   |
|:-------------|:----------------------------|:--------------------------|
| `depends_on` | Dependency relationship     | Service → Module          |
| `implements` | Implementation relationship | Class → Interface         |
| `contains`   | Containment relationship    | Module → Functions        |
| `related_to` | General relationship        | Concept → Concept         |
| `supersedes` | Replacement relationship    | NewDecision → OldDecision |

### Relationship Example

```javascript
// Create component entities
memory.create_entities([
    {name: "core_layer", type: "component", content: "Core layer with loader, config, timeout"},
    {name: "service_layer", type: "component", content: "Service layer with CLI, MCP, API"}
])

// Create relationships
memory.create_relations([
    {from: "service_layer", to: "core_layer", type: "depends_on"}
])
```

---

## 5. Query Strategies

### Semantic Search

Search by meaning:

```javascript
memory.search_nodes("authentication approach")
// Returns entities related to authentication
```

### Direct Retrieval

Get specific entities:

```javascript
memory.open_nodes(["decision_auth_jwt", "convention_file_naming"])
// Returns exact entities by name
```

### Search Tips

| Goal                  | Approach                             |
|:----------------------|:-------------------------------------|
| Find related concepts | Use semantic search with keywords    |
| Get specific entity   | Use `open_nodes` with exact name     |
| Explore area          | Search with broad terms first        |
| Verify existence      | Search before creating to avoid dups |

---

## 6. Session Workflow

### Start of Session

```javascript
// 1. Check for relevant existing knowledge
memory.search_nodes("project architecture")
memory.search_nodes("recent decisions")

// 2. Load specific entities if known
memory.open_nodes(["project_overview", "current_sprint"])
```

### During Session

```javascript
// Store important decisions as they're made
memory.create_entities([{
    name: "decision_api_versioning",
    type: "decision",
    content: "Using URL path versioning (v1, v2). Decided during API design discussion."
}])
```

### End of Session

```javascript
// 1. Store key outcomes
memory.create_entities([{
    name: "session_outcome_20251130",
    type: "session",
    content: "Completed authentication module. Next: implement refresh tokens."
}])

// 2. Update relationships if needed
memory.create_relations([{
    from: "auth_module",
    to: "user_service",
    type: "depends_on"
}])
```

---

## 7. Best Practices

### Naming

| Practice                | Example                                |
|:------------------------|:---------------------------------------|
| Use descriptive names   | `decision_auth_jwt` not `auth1`        |
| Include category prefix | `pattern_`, `decision_`, `convention_` |
| Use snake_case          | `error_handling_pattern`               |
| Be specific             | `test_framework_pytest` not `testing`  |

### Content

| Practice                    | Description                        |
|:----------------------------|:-----------------------------------|
| Include context             | Why the decision was made          |
| Be concise but complete     | Key information in few sentences   |
| Use structured format       | Lists, categories when appropriate |
| Include dates when relevant | For time-sensitive decisions       |

### Organization

| Practice                     | Description              |
|:-----------------------------|:-------------------------|
| Check before creating        | Avoid duplicate entities |
| Update rather than duplicate | Modify existing entities |
| Create relationships         | Connect related concepts |
| Clean up obsolete data       | Remove outdated entities |

---

## 8. Common Patterns

### Project Onboarding

```javascript
// Store project overview
memory.create_entities([{
    name: "project_overview",
    type: "concept",
    content: "SAGE Knowledge Base - Production-grade knowledge management system. Python 3.12+, FastAPI, pytest. 3-layer architecture: Core → Services → Capabilities."
}])
```

### Decision Recording

```javascript
// Record architecture decision
memory.create_entities([{
    name: "decision_database_sqlite",
    type: "decision",
    content: "Using SQLite for metadata storage. Reasons: simple deployment, sufficient for expected scale, file-based backup."
}])
```

### Convention Documentation

```javascript
// Document coding convention
memory.create_entities([{
    name: "convention_imports",
    type: "convention",
    content: "Import order: stdlib, third-party, local. Use absolute imports. Group with blank lines. Sort alphabetically within groups."
}])
```

---

## 9. Troubleshooting

### Entity Not Found

**Symptom**: `search_nodes` returns empty

**Solutions**:

1. Check entity name spelling
2. Try broader search terms
3. Verify entity was created successfully

### Duplicate Entities

**Symptom**: Multiple similar entities exist

**Solutions**:

1. Search before creating
2. Delete duplicates: `memory.delete_entities(["duplicate_name"])`
3. Establish naming conventions

### Stale Information

**Symptom**: Entity contains outdated information

**Solutions**:

1. Delete old entity
2. Create new entity with updated content
3. Use `supersedes` relationship if needed

---

## 10. Fallback Approach

If Memory server is unavailable, use file-based persistence:

```text
.history/
├── conversations/
│   └── YYYY-MM-DD-topic.md      # Key decisions
├── handoffs/
│   └── YYYY-MM-DD-task.md       # Continuation context
└── current/
    └── session-state.md         # Active work state
```

---

## 11. Related

- [Overview](overview.md) — MCP architecture
- [Configuration](configuration.md) — Setup guide
- [Servers Reference](servers.md) — All MCP servers
- [Troubleshooting](troubleshooting.md) — Problem solving

---

*AI Collaboration Knowledge Base*
