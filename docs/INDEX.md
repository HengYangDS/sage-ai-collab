---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---

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
| `design/00-OVERVIEW.md`          | Project overview and introduction     |
| `design/01-ARCHITECTURE.md`      | Three-layer architecture design       |
| `design/02-SAGE-PROTOCOL.md`     | SAGE protocol specification           |
| `design/03-SERVICES.md`          | Service layer design (CLI, MCP, API)  |
| `design/04-TIMEOUT-LOADING.md`   | Timeout hierarchy and smart loading   |
| `design/05-PLUGIN-MEMORY.md`     | Plugin system and memory persistence  |
| `design/06-CONTENT-STRUCTURE.md` | Knowledge content organization        |
| `design/07-ROADMAP.md`           | Implementation roadmap and milestones |
| `design/08-EVALUATION.md`        | Evaluation criteria and metrics       |
| `design/09-CONFIGURATION.md`     | Configuration management design       |

---

## 3. API Reference

API documentation for different interfaces:

| Document                  | Description                      |
|---------------------------|----------------------------------|
| `api/INDEX.md`            | API overview and quick reference |
| `api/CLI.md`              | Command-line interface reference |
| `api/MCP.md`              | MCP (Model Context Protocol) API |
| `api/MCP_QUICK_REF.md`    | MCP quick reference guide        |
| `api/PLUGIN_QUICK_REF.md` | Plugin API quick reference       |
| `api/PYTHON.md`           | Python SDK reference             |

---

## 4. User Guides

Tutorials and guides for users and developers:

| Document                       | Description                        |
|--------------------------------|------------------------------------|
| `guides/INDEX.md`              | Guides overview and navigation     |
| `guides/QUICKSTART.md`         | Quick start guide (5 minutes)      |
| `guides/CONFIGURATION.md`      | Configuration guide                |
| `guides/MCP_TOOLS.md`          | MCP tools usage guide              |
| `guides/PLUGIN_DEVELOPMENT.md` | Plugin development guide           |
| `guides/ADVANCED.md`           | Advanced usage and customization   |
| `guides/MIGRATION.md`          | Migration guide from other systems |
| `guides/TROUBLESHOOTING.md`    | Troubleshooting common issues      |
| `guides/FAQ.md`                | Frequently asked questions         |

---

## 5. Quick Access

### 5.1 Getting Started

1. Start with `guides/QUICKSTART.md` for a 5-minute introduction
2. Read `design/00-OVERVIEW.md` for project overview
3. Check `api/CLI.md` for command-line usage

### 5.2 For Developers

1. Review `design/01-ARCHITECTURE.md` for system design
2. See `guides/PLUGIN_DEVELOPMENT.md` for extending SAGE
3. Reference `api/PYTHON.md` for programmatic access

### 5.3 For Configuration

1. Check `guides/CONFIGURATION.md` for setup options
2. See `design/09-CONFIGURATION.md` for design details

---

## Related

- `.knowledge/` — Knowledge base content
- `.context/` — Project-specific context
- `config/` — Runtime configuration files
- `README.md` — Project overview

---

*Part of SAGE Knowledge Base*
