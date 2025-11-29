# Memory Server Best Practices

> Knowledge graph persistence patterns and usage guidelines (~15 min read)

---

## Table of Contents

- [1. Memory Server Overview](#1-memory-server-overview)
- [2. Entity Design Patterns](#2-entity-design-patterns)
- [3. Relationship Modeling](#3-relationship-modeling)
- [4. Query Strategies](#4-query-strategies)
- [5. Session Workflow](#5-session-workflow)
- [6. Best Practices](#6-best-practices)
- [7. Troubleshooting](#7-troubleshooting)

---

## 1. Memory Server Overview

The **Memory MCP Server** provides cross-session knowledge persistence through a knowledge graph structure. It enables
Junie to remember decisions, patterns, and context across multiple sessions.

### Core Capabilities

| Capability                    | Description                           | Use Case                         |
|:------------------------------|:--------------------------------------|:---------------------------------|
| **Entity Storage**            | Store named knowledge units           | Decisions, patterns, conventions |
| **Relationship Mapping**      | Connect entities with typed relations | Dependencies, hierarchies        |
| **Semantic Search**           | Query by meaning, not just keywords   | Find related concepts            |
| **Cross-Session Persistence** | Data survives session boundaries      | Long-term project memory         |

### When to Use Memory Server

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
  "content": "Human-readable description and details",
  "metadata": {
    "created": "YYYY-MM-DD",
    "confidence": "high",
    "source": "user_decision"
  }
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

```
<category>_<subject>_<qualifier>

Examples:
- decision_auth_jwt
- convention_naming_files
- pattern_error_retry
- preference_format_ruff
```

### Entity Examples

**Decision Entity**:

```javascript
memory.create_entities([{
    name: "decision_auth_jwt",
    type: "decision",
    content: "Using JWT for API authentication. Reasons: stateless, scalable, industry standard. Access tokens expire in 15 minutes, refresh tokens in 7 days."
}])
```

**Convention Entity**:

```javascript
memory.create_entities([{
    name: "convention_file_naming",
    type: "convention",
    content: "Python files use snake_case. Classes use PascalCase. Constants use UPPER_SNAKE_CASE. Test files prefix with test_."
}])
```

**Pattern Entity**:

```javascript
memory.create_entities([{
    name: "pattern_timeout_hierarchy",
    type: "pattern",
    content: "5-tier timeout system: T1(100ms) cache, T2(500ms) file, T3(2s) layer, T4(5s) init, T5(10s) complex. Always implement fallback strategies."
}])
```

---

## 3. Relationship Modeling

### Relationship Types

| Relation Type | Description         | Example                                    |
|:--------------|:--------------------|:-------------------------------------------|
| `depends_on`  | A requires B        | `UserService depends_on AuthModule`        |
| `implements`  | A realizes B        | `JWTAuth implements AuthStrategy`          |
| `part_of`     | A is component of B | `Loader part_of CoreLayer`                 |
| `related_to`  | General association | `TimeoutPolicy related_to ErrorHandling`   |
| `supersedes`  | A replaces B        | `NewPattern supersedes OldPattern`         |
| `influences`  | A affects B         | `PerformanceGoal influences CacheStrategy` |

### Creating Relationships

```javascript
memory.create_relations([
    {
        from: "decision_auth_jwt",
        to: "component_api_gateway",
        type: "influences"
    },
    {
        from: "component_user_service",
        to: "component_auth_module",
        type: "depends_on"
    }
])
```

### Relationship Graph Example

```
                    ┌─────────────────┐
                    │  Architecture   │
                    │   Decisions     │
                    └────────┬────────┘
                             │ influences
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
      ┌───────────┐  ┌───────────┐  ┌───────────┐
      │   Auth    │  │  Timeout  │  │   Error   │
      │  Strategy │  │  Policy   │  │ Handling  │
      └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
            │              │              │
            │ implements   │ applies_to   │ implements
            ▼              ▼              ▼
      ┌───────────┐  ┌───────────┐  ┌───────────┐
      │  JWT Auth │  │   Core    │  │   Retry   │
      │  Module   │  │   Layer   │  │  Pattern  │
      └───────────┘  └───────────┘  └───────────┘
```

---

## 4. Query Strategies

### Search Patterns

**Semantic Search** (recommended for discovery):

```javascript
memory.search_nodes("authentication approach")
// Returns entities related to authentication
```

**Exact Lookup** (for known entities):

```javascript
memory.get_entity("decision_auth_jwt")
// Returns specific entity
```

**Relationship Traversal**:

```javascript
memory.get_relations("component_user_service")
// Returns all relationships for entity
```

### Query Best Practices

| Scenario                    | Strategy              | Example                              |
|:----------------------------|:----------------------|:-------------------------------------|
| **Find related decisions**  | Semantic search       | `search_nodes("database choice")`    |
| **Check specific decision** | Exact lookup          | `get_entity("decision_db_postgres")` |
| **Understand dependencies** | Relation query        | `get_relations("component_api")`     |
| **Explore a topic**         | Broad search + filter | `search_nodes("security")`           |

---

## 5. Session Workflow

### Session Start

```javascript
// 1. Check for existing project knowledge
memory.search_nodes("project conventions")
memory.search_nodes("recent decisions")

// 2. Load relevant context
memory.get_entity("convention_file_naming")
memory.get_entity("pattern_error_handling")
```

### During Session

```javascript
// Record important decisions as they're made
memory.create_entities([{
    name: "decision_cache_redis",
    type: "decision",
    content: "Chose Redis for caching. Reasons: performance, pub/sub support, team familiarity."
}])

// Link to related entities
memory.create_relations([{
    from: "decision_cache_redis",
    to: "component_data_layer",
    type: "influences"
}])
```

### Session End

```javascript
// 1. Summarize session learnings
memory.create_entities([{
    name: "session_YYYYMMDD_summary",
    type: "session",
    content: "Implemented caching layer with Redis. Key decisions: TTL strategy, cache invalidation patterns."
}])

// 2. Update any changed conventions
memory.update_entity("convention_caching", {
    content: "Updated caching conventions with Redis patterns..."
})
```

---

## 6. Best Practices

### Do's ✅

| Practice                          | Benefit                         |
|:----------------------------------|:--------------------------------|
| Use consistent naming conventions | Easy retrieval and organization |
| Include reasoning in content      | Future context for decisions    |
| Create relationships proactively  | Rich knowledge graph            |
| Review and prune periodically     | Maintain relevance              |
| Use semantic search for discovery | Find unexpected connections     |

### Don'ts ❌

| Anti-Pattern                | Problem                          |
|:----------------------------|:---------------------------------|
| Store large code blocks     | Memory is for concepts, not code |
| Use vague entity names      | Hard to find and maintain        |
| Skip relationship creation  | Isolated knowledge silos         |
| Store temporary information | Clutters long-term memory        |
| Duplicate existing entities | Inconsistent knowledge base      |

### Content Guidelines

**Good Content**:

```
"Using pytest with pytest-asyncio for testing. Convention: test files in tests/ 
mirror src/ structure. Fixtures in conftest.py. Integration tests require 
TEST_DB environment variable."
```

**Poor Content**:

```
"pytest"  // Too brief, no context
```

---

## 7. Troubleshooting

### Common Issues

| Issue                 | Cause                        | Solution                         |
|:----------------------|:-----------------------------|:---------------------------------|
| Entity not found      | Name mismatch or not created | Use `search_nodes` with keywords |
| Duplicate entities    | Inconsistent naming          | Establish naming conventions     |
| Stale information     | No update workflow           | Regular review and updates       |
| Missing relationships | Not created during session   | Add relationships retroactively  |

### Recovery Patterns

**When Memory Server is Unavailable**:

1. Document decisions in `.history/` files
2. Use session handoff notes
3. Sync to memory server when available

**Rebuilding Knowledge Graph**:

1. Export existing entities
2. Review and consolidate
3. Re-import with consistent naming
4. Rebuild relationships

---

## Related

- `03-mcp-integration.md` — MCP server setup including Memory server
- `../mcp/mcp.json` — Memory server configuration
- `../generic/config.yaml` — Session history settings
- `06-migration-guide.md` — Version migration strategies

---

*Part of the Junie Configuration Guide*
