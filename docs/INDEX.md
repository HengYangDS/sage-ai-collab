
# Documentation Navigation

> User-facing documentation for SAGE Knowledge Base

---

## Table of Contents

- [1. Directory Structure](#1-directory-structure)
- [2. Design Documents](#2-design-documents)
- [3. API Reference](#3-api-reference)
- [4. User Guides](#4-user-guides)
- [5. Quick Access](#5-quick-access)

---

## 1. Directory Structure

| Directory | Purpose                               | Files |
|-----------|---------------------------------------|-------|
| `design/` | Architecture and design documentation | 10    |
| `api/`    | API reference documentation           | 6     |
| `guides/` | User guides and tutorials             | 9     |

---

## 2. Design Documents

Comprehensive design documentation for SAGE architecture and implementation:

| Document                         | Description                           |
|----------------------------------|---------------------------------------|
| `design/00-overview.md`          | Project overview and introduction     |
| `design/01-architecture.md`      | Three-layer architecture design       |
| `design/02-sage-protocol.md`     | SAGE protocol specification           |
| `design/03-services.md`          | Service layer design (CLI, MCP, API)  |
| `design/04-timeout-loading.md`   | Timeout hierarchy and smart loading   |
| `design/05-plugin-memory.md`     | Plugin system and memory persistence  |
| `design/06-content-structure.md` | Knowledge content organization        |
| `design/07-roadmap.md`           | Implementation roadmap and milestones |
| `design/08-evaluation.md`        | Evaluation criteria and metrics       |
| `design/09-configuration.md`     | Configuration management design       |

---

## 3. API Reference

API documentation for different interfaces:

| Document                  | Description                      |
|---------------------------|----------------------------------|
| `api/index.md`            | API overview and quick reference |
| `api/cli.md`              | Command-line interface reference |
| `api/mcp.md`              | MCP (Model Context Protocol) API |
| `api/mcp_quick_ref.md`    | MCP quick reference guide        |
| `api/plugin_quick_ref.md` | Plugin API quick reference       |
| `api/python.md`           | Python SDK reference             |

---

## 4. User Guides

Tutorials and guides for users and developers:

| Document                       | Description                        |
|--------------------------------|------------------------------------|
| `guides/index.md`              | Guides overview and navigation     |
| `guides/quickstart.md`         | Quick start guide (5 minutes)      |
| `guides/configuration.md`      | Configuration guide                |
| `guides/mcp_tools.md`          | MCP tools usage guide              |
| `guides/plugin_development.md` | Plugin development guide           |
| `guides/advanced.md`           | Advanced usage and customization   |
| `guides/migration.md`          | Migration guide from other systems |
| `guides/troubleshooting.md`    | Troubleshooting common issues      |
| `guides/faq.md`                | Frequently asked questions         |

---

## 5. Quick Access

### 5.1 Getting Started

1. Start with `guides/quickstart.md` for a 5-minute introduction
2. Read `design/00-overview.md` for project overview
3. Check `api/cli.md` for command-line usage

### 5.2 For Developers

1. Review `design/01-architecture.md` for system design
2. See `guides/plugin_development.md` for extending SAGE
3. Reference `api/python.md` for programmatic access

### 5.3 For Configuration

1. Check `guides/configuration.md` for setup options
2. See `design/09-configuration.md` for design details

---

## Related

- `.knowledge/` — Knowledge base content
- `.context/` — Project-specific context
- `config/` — Runtime configuration files
- `README.md` — Project overview

---

*AI Collaboration Knowledge Base*
