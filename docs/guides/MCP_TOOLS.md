
# MCP Tools Guide

> Complete reference for SAGE Knowledge Base MCP tools

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Tool Categories](#2-tool-categories)
- [3. Quick Reference](#3-quick-reference)
- [4. Best Practices](#4-best-practices)

---

## 1. Overview

### 1.1 Tool Categories

| Category        | Purpose                    | Tools   |
|-----------------|----------------------------|---------|
| **Knowledge**   | Content retrieval & search | 6 tools |
| **Capability**  | Analysis & health checks   | 3 tools |
| **Development** | Maintenance & debugging    | 6 tools |

### 1.2 Common Parameters

| Parameter     | Type   | Description                       |
|---------------|--------|-----------------------------------|
| `path`        | string | Root path for operations          |
| `timeout_ms`  | int    | Operation timeout in milliseconds |
| `layer`       | int    | Knowledge layer (0-3)             |
| `max_results` | int    | Maximum results to return         |

### 1.3 Detailed Documentation

| Document                           | Content                            |
|------------------------------------|------------------------------------|
| `docs/api/mcp_tools_ref.md`        | Knowledge tools detailed reference |
| `docs/api/mcp_resources.md`        | Resources, prompts, error handling |
| `docs/api/mcp_quick_ref.md`        | One-page quick reference           |

---

## 2. Tool Categories

### 2.1 Knowledge Tools

| Tool               | Purpose                    | Key Parameters              |
|--------------------|----------------------------|-----------------------------|
| `get_knowledge`    | Retrieve knowledge by layer| `layer`, `task`, `timeout_ms` |
| `search_knowledge` | Search knowledge base      | `query`, `max_results`      |
| `kb_info`          | Get KB information         | (none)                      |
| `get_guidelines`   | Get specific guidelines    | `section`                   |
| `get_framework`    | Get framework documentation| `name`, `timeout_ms`        |
| `get_best_practices`| Get best practices        | `topic`                     |

### 2.2 Capability Tools

| Tool               | Purpose                    | Key Parameters              |
|--------------------|----------------------------|-----------------------------|
| `analyze_quality`  | Analyze content quality    | `path`, `depth`             |
| `analyze_content`  | Content structure analysis | `path`, `format`            |
| `check_health`     | System health check        | (none)                      |

### 2.3 Development Tools

| Tool                  | Purpose                    | Key Parameters              |
|-----------------------|----------------------------|-----------------------------|
| `build_knowledge_graph`| Build knowledge graph     | `path`, `output_file`       |
| `check_links`         | Validate markdown links    | `path`, `check_external`    |
| `check_structure`     | Validate directory structure| `path`, `fix`              |
| `get_timeout_stats`   | Get timeout statistics     | (none)                      |
| `analyze_tokens`      | Token usage analysis       | `path`, `format`            |
| `export_knowledge`    | Export knowledge content   | `layers`, `format`          |

---

## 3. Quick Reference

### 3.1 Layer Mapping

| Layer | Name       | Tokens | Description              |
|-------|------------|--------|--------------------------|
| 0     | core       | ~500   | Core principles          |
| 1     | guidelines | ~1200  | Coding guidelines        |
| 2     | frameworks | ~2000  | Conceptual frameworks    |
| 3     | practices  | ~1500  | Best practices           |

### 3.2 Timeout Levels

| Level | Timeout | Use Case               |
|-------|---------|------------------------|
| T1    | 100ms   | Cache-only responses   |
| T2    | 500ms   | Single file operations |
| T3    | 2s      | Standard tool calls    |
| T4    | 5s      | Full knowledge load    |
| T5    | 10s     | Complex analysis       |

### 3.3 Common Workflows

**Starting a Task:**
```
1. kb_info() → Get available layers
2. get_knowledge(layer=0) → Load core principles
3. get_knowledge(layer=1, task="your task") → Load relevant guidelines
```

**Quality Check:**
```
1. analyze_quality(path="output/") → Check quality score
2. check_links(path="docs/") → Validate links
3. check_structure(path=".") → Validate structure
```

**Debugging:**
```
1. check_health() → Verify system status
2. get_timeout_stats() → Check timeout metrics
3. analyze_tokens(path=".knowledge/") → Check token usage
```

---

## 4. Best Practices

### 4.1 Tool Selection

| Task Type             | Primary Tool          | Secondary Tools          |
|-----------------------|-----------------------|--------------------------|
| New coding task       | `get_knowledge`       | `get_guidelines`         |
| Architecture decision | `get_framework`       | `get_best_practices`     |
| Code review           | `analyze_quality`     | `check_links`            |
| Documentation         | `get_guidelines`      | `analyze_content`        |
| Debugging             | `check_health`        | `get_timeout_stats`      |

### 4.2 Performance Tips

| Tip                    | Description                              |
|------------------------|------------------------------------------|
| Start with layer 0     | Core principles are smallest and fastest |
| Use task parameter     | Smart loading reduces token usage        |
| Cache results          | Avoid repeated tool calls                |
| Set appropriate timeout| Match timeout to operation complexity    |

### 4.3 Error Handling

| Error Code | Meaning              | Recovery Action           |
|------------|----------------------|---------------------------|
| TIMEOUT    | Operation timed out  | Use fallback content      |
| NOT_FOUND  | Resource not found   | Check path/layer          |
| INVALID    | Invalid parameters   | Verify input values       |

---

## Related

- `docs/api/mcp.md` — MCP protocol overview
- `docs/api/mcp_tools_ref.md` — Detailed tool schemas
- `docs/api/mcp_resources.md` — Resources and prompts
- `docs/api/mcp_quick_ref.md` — Quick reference card
- `docs/guides/quickstart.md` — Getting started guide

---

*AI Collaboration Knowledge Base*
