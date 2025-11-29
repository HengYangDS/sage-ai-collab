# MCP Tools Guide

> Complete reference for SAGE Knowledge Base MCP tools

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Knowledge Tools](#2-knowledge-tools)
- [3. Capability Tools](#3-capability-tools)
- [4. Development Tools](#4-development-tools)
- [5. Tool Combinations](#5-tool-combinations)
- [6. Best Practices](#6-best-practices)

---

## 1. Overview

### 1.1 Tool Categories

| Category        | Purpose                    | Tools   |
|-----------------|----------------------------|---------|
| **Knowledge**   | Content retrieval & search | 6 tools |
| **Capability**  | Analysis & health checks   | 3 tools |
| **Development** | Maintenance & debugging    | 6 tools |

### 1.2 Quick Reference

```python
# List all available tools
result = await list_tools()
print(result["knowledge_tools"])
print(result["capabilities"])
print(result["dev_tools"])
```

### 1.3 Common Parameters

| Parameter     | Type   | Description                       |
|---------------|--------|-----------------------------------|
| `path`        | string | Root path for operations          |
| `timeout_ms`  | int    | Operation timeout in milliseconds |
| `layer`       | int    | Knowledge layer (0-3)             |
| `max_results` | int    | Maximum results to return         |

---

## 2. Knowledge Tools

### 2.1 get_knowledge

Retrieve knowledge by layer with smart loading.

**Parameters**:
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `layer` | int | 0 | Layer to load (0=core, 1=guidelines, etc.) |
| `task` | string | "" | Task description for smart filtering |
| `timeout_ms` | int | 5000 | Operation timeout |

**Examples**:

```python
# Get core knowledge
result = await get_knowledge(layer=0)

# Get knowledge filtered by task
result = await get_knowledge(
    layer=1,
    task="implement authentication",
    timeout_ms=3000
)

# Response
{
    "status"      : "success",
    "duration_ms" : 245,
    "content"     : {...},
    "layer"       : 0,
    "files_loaded": 5
}
```

**Use Cases**:

- Load context at session start
- Get relevant guidelines for a task
- Refresh knowledge periodically

---

### 2.2 search_knowledge

Search across knowledge base content.

**Parameters**:
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `query` | string | required | Search query |
| `max_results` | int | 10 | Maximum results |
| `layer` | int | None | Limit to specific layer |

**Examples**:

```python
# Basic search
result = await search_knowledge(query="timeout patterns")

# Search with limits
result = await search_knowledge(
    query="authentication",
    max_results=5,
    layer=2  # frameworks only
)

# Response
{
    "status"       : "success",
    "query"        : "timeout patterns",
    "results"      : [
        {
            "path"   : ".knowledge/frameworks/resilience/timeout_patterns.md",
            "title"  : "Timeout Patterns",
            "score"  : 0.95,
            "snippet": "..."
        }
    ],
    "total_results": 3
}
```

**Use Cases**:

- Find specific documentation
- Discover related content
- Verify knowledge exists

---

### 2.3 kb_info

Get knowledge base information and statistics.

**Parameters**: None

**Examples**:

```python
result = await kb_info()

# Response
{
    "version"     : "0.1.0",
    "status"      : "healthy",
    "statistics"  : {
        "total_files" : 150,
        "total_tokens": 45000,
        "layers"      : {
            "core"      : 10,
            "guidelines": 25,
            "frameworks": 40,
            "practices" : 75
        }
    },
    "last_updated": "2025-11-29T22:00:00"
}
```

**Use Cases**:

- Check KB status
- Monitor KB health
- Verify available content

---

### 2.4 get_guidelines

Retrieve specific guideline sections.

**Parameters**:
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `section` | string | required | Section name |

**Examples**:

```python
# Get coding guidelines
result = await get_guidelines(section="code_style")

# Get documentation guidelines
result = await get_guidelines(section="documentation")

# Available sections
sections = [
    "overview", "code_style", "documentation",
    "engineering", "ai_collaboration", "quality"
]

# Response
{
    "status" : "success",
    "section": "code_style",
    "content": "...",
    "path"   : ".knowledge/guidelines/code_style.md"
}
```

**Use Cases**:

- Load specific style guides
- Get project conventions
- Reference best practices

---

### 2.5 get_framework

Retrieve framework documentation.

**Parameters**:
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `name` | string | required | Framework name |

**Examples**:

```python
# Get autonomy framework
result = await get_framework(name="autonomy")

# Get design patterns
result = await get_framework(name="patterns")

# Available frameworks
frameworks = [
    "autonomy", "cognitive", "design",
    "patterns", "resilience"
]

# Response
{
    "status"   : "success",
    "framework": "autonomy",
    "content"  : "...",
    "files"    : ["levels.md"]
}
```

**Use Cases**:

- Reference decision frameworks
- Load pattern libraries
- Get architectural guidance

---

### 2.6 get_template

Retrieve document templates.

**Parameters**:
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `name` | string | required | Template name |

**Examples**:

```python
# Get ADR template
result = await get_template(name="adr")

# Get API spec template
result = await get_template(name="api_spec")

# Available templates
templates = [
    "adr", "api_spec", "conversation_record",
    "expert_committee", "postmortem", "project_setup",
    "runbook", "session_state", "task_handoff", "case_study"
]

# Response
{
    "status"  : "success",
    "template": "adr",
    "content" : "...",
    "path"    : ".knowledge/templates/adr.md"
}
```

**Use Cases**:

- Create new documents
- Follow standard formats
- Ensure consistency

---

## 3. Capability Tools

### 3.1 analyze_quality

Analyze code/content quality metrics.

**Parameters**:
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `path` | string | "." | Path to analyze |
| `extensions` | string | ".py,.md" | File extensions |

**Examples**:

```python
# Analyze Python files
result = await analyze_quality(path="src/", extensions=".py")

# Analyze documentation
result = await analyze_quality(path="docs/", extensions=".md")

# Response
{
    "success": true,
    "result" : {
        "files_analyzed": 25,
        "avg_complexity": 5.2,
        "issues"        : [
            {"file": "...", "type": "...", "message": "..."}
        ],
        "summary"       : {
            "high_complexity"   : 2,
            "missing_docstrings": 5
        }
    }
}
```

**Use Cases**:

- Code review preparation
- Quality monitoring
- Technical debt tracking

---

### 3.2 analyze_content

Analyze content structure and metrics.

**Parameters**:
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `path` | string | "." | Path to analyze |
| `extensions` | string | ".md" | File extensions |

**Examples**:

```python
# Analyze markdown content
result = await analyze_content(path=".knowledge/")

# Response
{
    "success": true,
    "result" : {
        "files_analyzed"     : 80,
        "total_tokens"       : 45000,
        "avg_tokens_per_file": 562,
        "structure"          : {
            "with_frontmatter": 75,
            "with_toc"        : 60,
            "avg_headings"    : 8
        }
    }
}
```

**Use Cases**:

- Content inventory
- Token budget planning
- Structure validation

---

### 3.3 check_health

Comprehensive health check.

**Parameters**:
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `path` | string | "." | Path to check |

**Examples**:

```python
result = await check_health(path=".")

# Response
{
    "success": true,
    "result" : {
        "overall" : "healthy",
        "checks"  : {
            "config"   : "pass",
            "content"  : "pass",
            "links"    : "warning",
            "structure": "pass"
        },
        "warnings": [
            "3 broken links found"
        ],
        "errors"  : []
    }
}
```

**Use Cases**:

- Regular health monitoring
- Pre-deployment validation
- Issue detection

---

## 4. Development Tools

### 4.1 build_knowledge_graph

Build knowledge graph for analysis.

**Parameters**:
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `path` | string | "." | Root path |
| `include_content` | bool | false | Include file content |
| `output_file` | string | "" | Export filename (saved to .outputs/) |

**Examples**:

```python
# Build graph
result = await build_knowledge_graph(path="content")

# Build and export
result = await build_knowledge_graph(
    path="content",
    include_content=False,
    output_file="kb_graph.json"  # Saved to .outputs/kb_graph.json
)

# Response
{
    "success": true,
    "result" : {
        "total_nodes"  : 150,
        "total_edges"  : 320,
        "total_tokens" : 45000,
        "nodes_by_type": {"file": 80, "concept": 50, "tag": 20},
        "edges_by_type": {"links_to": 200, "references": 100}
    }
}
```

**Use Cases**:

- Content relationship analysis
- Navigation optimization
- Knowledge gap detection

---

### 4.2 check_links

Validate links in markdown files.

**Parameters**:
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `path` | string | "." | Root path |
| `check_external` | bool | false | Check external URLs |
| `pattern` | string | "**/*.md" | File pattern |

**Examples**:

```python
# Check internal links
result = await check_links(path="content")

# Include external links
result = await check_links(
    path="docs",
    check_external=True,
    pattern="**/*.md"
)

# Response
{
    "success": true,
    "result" : {
        "total_links" : 250,
        "valid_links" : 247,
        "broken_links": [
            {
                "source": "docs/guide.md",
                "target": "missing.md",
                "line"  : 45
            }
        ],
        "broken_rate" : 0.012
    }
}
```

**Use Cases**:

- Documentation validation
- Link maintenance
- Quality assurance

---

### 4.3 check_structure

Validate directory structure.

**Parameters**:
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `path` | string | "." | Root path |
| `fix` | bool | false | Attempt fixes |
| `dry_run` | bool | true | Preview only |

**Examples**:

```python
# Check structure
result = await check_structure(path=".")

# Preview fixes
result = await check_structure(
    path=".",
    fix=True,
    dry_run=True
)

# Response
{
    "success": true,
    "result" : {
        "issues"         : [
            {"type": "missing_index", "path": ".knowledge/new_folder/"}
        ],
        "error_count"    : 0,
        "warning_count"  : 1,
        "fixes_available": 1
    }
}
```

**Use Cases**:

- Structure validation
- Convention enforcement
- Automated fixes

---

### 4.4 get_timeout_stats

Get timeout performance statistics.

**Parameters**:
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `minutes` | int | 60 | Time window |

**Examples**:

```python
# Get stats for last hour
result = await get_timeout_stats(minutes=60)

# Get stats for last 30 minutes
result = await get_timeout_stats(minutes=30)

# Response
{
    "success": true,
    "result" : {
        "total_operations" : 150,
        "timeout_count"    : 3,
        "timeout_rate"     : 0.02,
        "near_timeout_rate": 0.08,
        "avg_duration_ms"  : 245,
        "by_level"         : {
            "T1": {"count": 50, "avg_ms": 45},
            "T2": {"count": 40, "avg_ms": 180}
        },
        "recommendations"  : [
            "Consider increasing T2 timeout for large files"
        ]
    }
}
```

**Use Cases**:

- Performance monitoring
- Timeout tuning
- Issue detection

---

### 4.5 create_backup

Create knowledge base backup.

**Parameters**:
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `path` | string | "." | Path to backup |
| `name` | string | "" | Backup name |

**Examples**:

```python
# Create named backup
result = await create_backup(
    path=".",
    name="pre_migration"
)

# Create auto-named backup
result = await create_backup(path=".")

# Response
{
    "success": true,
    "result" : {
        "backup_path": ".backups/pre_migration_20251129_220000",
        "name"       : "pre_migration",
        "size_mb"    : 15.5,
        "files_count": 200
    }
}
```

**Use Cases**:

- Pre-migration backup
- Version snapshots
- Disaster recovery

---

### 4.6 list_backups

List available backups.

**Parameters**:
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `path` | string | ".backups" | Backup directory |

**Examples**:

```python
result = await list_backups(path=".backups")

# Response
{
    "success": true,
    "result" : {
        "backups"      : [
            {
                "name"   : "pre_migration",
                "path"   : ".backups/pre_migration_20251129",
                "created": "2025-11-29T22:00:00",
                "size_mb": 15.5
            }
        ],
        "total_count"  : 3,
        "total_size_mb": 45.2
    }
}
```

**Use Cases**:

- Backup inventory
- Storage management
- Recovery preparation

---

## 5. Tool Combinations

### 5.1 Session Startup

```python
# Recommended startup sequence
async def initialize_session():
    # 1. Check health
    health = await check_health(path=".")
    if health["result"]["overall"] != "healthy":
        print("Warning: KB health issues detected")

    # 2. Load core knowledge
    core = await get_knowledge(layer=0)

    # 3. Get KB info
    info = await kb_info()

    return {"health": health, "core": core, "info": info}
```

### 5.2 Task-Based Loading

```python
# Load context for specific task
async def load_task_context(task_description: str):
    # 1. Get relevant knowledge
    knowledge = await get_knowledge(
        layer=1,
        task=task_description
    )

    # 2. Search for specific content
    search_results = await search_knowledge(
        query=task_description,
        max_results=5
    )

    return {"knowledge": knowledge, "related": search_results}
```

### 5.3 Quality Check Workflow

```python
# Comprehensive quality check
async def full_quality_check():
    results = {}

    # 1. Check health
    results["health"] = await check_health(path=".")

    # 2. Check links
    results["links"] = await check_links(path="content")

    # 3. Check structure
    results["structure"] = await check_structure(path=".")

    # 4. Analyze quality
    results["quality"] = await analyze_quality(path="src/")

    # 5. Build graph for analysis
    results["graph"] = await build_knowledge_graph(
        path="content",
        output_file="quality_check_graph.json"
    )

    return results
```

### 5.4 Maintenance Workflow

```python
# Regular maintenance routine
async def maintenance_routine():
    # 1. Create backup
    backup = await create_backup(name="maintenance")

    # 2. Check and fix structure
    structure = await check_structure(
        path=".",
        fix=True,
        dry_run=True  # Preview first
    )

    # 3. Check links
    links = await check_links(path="content")

    # 4. Get timeout stats
    stats = await get_timeout_stats(minutes=1440)  # 24 hours

    return {
        "backup"     : backup,
        "structure"  : structure,
        "links"      : links,
        "performance": stats
    }
```

---

## 6. Best Practices

### 6.1 Error Handling

```python
async def safe_tool_call(tool_func, **kwargs):
    try:
        result = await tool_func(**kwargs)
        if result.get("success") == False:
            print(f"Tool error: {result.get('error')}")
        return result
    except Exception as e:
        print(f"Exception: {e}")
        return {"success": False, "error": str(e)}
```

### 6.2 Timeout Management

| Tool                     | Recommended Timeout |
|--------------------------|---------------------|
| `get_knowledge`          | 3000-5000ms         |
| `search_knowledge`       | 2000-3000ms         |
| `build_knowledge_graph`  | 10000-30000ms       |
| `check_links` (external) | 30000-60000ms       |

### 6.3 Result Caching

```python
# Cache frequently used results
knowledge_cache = {}


async def get_cached_knowledge(layer: int, ttl_seconds: int = 300):
    cache_key = f"knowledge_{layer}"
    now = time.time()

    if cache_key in knowledge_cache:
        cached, timestamp = knowledge_cache[cache_key]
        if now - timestamp < ttl_seconds:
            return cached

    result = await get_knowledge(layer=layer)
    knowledge_cache[cache_key] = (result, now)
    return result
```

### 6.4 Tool Selection Guide

| Need                    | Tool                    |
|-------------------------|-------------------------|
| Load session context    | `get_knowledge`         |
| Find specific content   | `search_knowledge`      |
| Check KB status         | `kb_info`               |
| Get coding standards    | `get_guidelines`        |
| Reference patterns      | `get_framework`         |
| Create document         | `get_template`          |
| Analyze code            | `analyze_quality`       |
| Analyze content         | `analyze_content`       |
| Full health check       | `check_health`          |
| Visualize relationships | `build_knowledge_graph` |
| Validate links          | `check_links`           |
| Validate structure      | `check_structure`       |
| Monitor performance     | `get_timeout_stats`     |
| Backup data             | `create_backup`         |
| List backups            | `list_backups`          |

---

## Quick Reference

### All Tools

| Tool                    | Category   | Primary Use           |
|-------------------------|------------|-----------------------|
| `get_knowledge`         | Knowledge  | Load content by layer |
| `search_knowledge`      | Knowledge  | Search content        |
| `kb_info`               | Knowledge  | Get KB status         |
| `get_guidelines`        | Knowledge  | Get guidelines        |
| `get_framework`         | Knowledge  | Get frameworks        |
| `get_template`          | Knowledge  | Get templates         |
| `list_tools`            | Knowledge  | List all tools        |
| `analyze_quality`       | Capability | Code analysis         |
| `analyze_content`       | Capability | Content analysis      |
| `check_health`          | Capability | Health check          |
| `build_knowledge_graph` | Dev        | Build graph           |
| `check_links`           | Dev        | Validate links        |
| `check_structure`       | Dev        | Validate structure    |
| `get_timeout_stats`     | Dev        | Performance stats     |
| `create_backup`         | Dev        | Create backup         |
| `list_backups`          | Dev        | List backups          |

---

## Related

- `docs/api/mcp.md` — MCP API reference
- `.knowledge/frameworks/patterns/integration.md` — Integration patterns
- `.knowledge/practices/engineering/knowledge_graph.md` — Graph guide
- `docs/guides/configuration.md` — Configuration guide

---

*Part of SAGE Knowledge Base — 信达雅 (Xin-Da-Ya)*
