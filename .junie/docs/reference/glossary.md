---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---

# Glossary

> Unified terminology definitions for Junie configuration (~5 min reference)

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Design Philosophy](#2-design-philosophy)
3. [MCP Terminology](#3-mcp-terminology)
4. [Configuration Terms](#4-configuration-terms)
5. [Collaboration Terms](#5-collaboration-terms)
6. [Regex Terminology](#6-regex-terminology)
7. [File Paths](#7-file-paths)
8. [Related](#8-related)

---

## 1. Core Concepts

| Term                 | Definition                                                                     |
|:---------------------|:-------------------------------------------------------------------------------|
| **Junie**            | JetBrains AI Assistant integrated into JetBrains IDEs                          |
| **Action Allowlist** | Permission rules that control which operations Junie can execute automatically |
| **Terminal Rules**   | Regex patterns defining allowed terminal commands                              |
| **MCP**              | Model Context Protocol - standardized AI-to-tool integration protocol          |
| **Session**          | A continuous period of AI-human collaboration work                             |

---

## 2. Design Philosophy

### 信达雅 (Xin-Da-Ya)

The guiding design philosophy for this configuration system, derived from Chinese translation theory:

| Chinese | Pinyin | English      | Application in Configuration                   |
|:--------|:-------|:-------------|:-----------------------------------------------|
| **信**   | Xin    | Faithfulness | Accurate, reliable, testable configurations    |
| **达**   | Da     | Clarity      | Clear, maintainable, well-structured documents |
| **雅**   | Ya     | Elegance     | Refined, balanced, sustainable design          |

**Usage**: Always reference as "信达雅 (Xin-Da-Ya)" for consistency across documents.

---

## 3. MCP Terminology

| Term           | Definition                                                       |
|:---------------|:-----------------------------------------------------------------|
| **MCP Server** | A service that exposes tools to AI assistants via MCP protocol   |
| **MCP Client** | The component in Junie that connects to MCP servers              |
| **Tool**       | A specific function exposed by an MCP server (e.g., `read_file`) |
| **stdio**      | Standard input/output - the communication method for MCP servers |
| **JSON-RPC**   | The message format used in MCP communication                     |

### Priority Levels

| Priority | Name      | Description                          | Examples                           |
|:---------|:----------|:-------------------------------------|:-----------------------------------|
| **P0**   | Critical  | Essential for basic functionality    | filesystem, memory                 |
| **P1**   | Important | Significantly enhances workflow      | github, fetch, sequential-thinking |
| **P2**   | Useful    | Nice-to-have for specific scenarios  | puppeteer, docker, everything      |
| **P3**   | Optional  | Rarely needed, specialized use cases | Custom project-specific servers    |

---

## 4. Configuration Terms

| Term               | Definition                                                                       |
|:-------------------|:---------------------------------------------------------------------------------|
| **Schema Version** | Version identifier for configuration format compatibility                        |
| **Thin Layer**     | Architecture principle separating generic (🔄) and project-specific (📌) configs |
| **Hot Reload**     | Ability to apply configuration changes without full IDE restart                  |
| **Fallback**       | Alternative approach when primary method fails                                   |

### File Type Markers

| Marker | Meaning          | Description                                   |
|:-------|:-----------------|:----------------------------------------------|
| 🔄     | Generic          | Reusable across projects without modification |
| 📌     | Project-specific | Must be customized for each project           |

---

## 5. Collaboration Terms

### Autonomy Levels

| Level  | Name        | Autonomy Range | Behavior                                    |
|:-------|:------------|:---------------|:--------------------------------------------|
| **L1** | Minimal     | 0-20%          | Ask before any changes                      |
| **L2** | Low         | 20-40%         | Ask before significant changes              |
| **L3** | Medium      | 40-60%         | Proceed with routine tasks, ask for complex |
| **L4** | Medium-High | 60-80%         | Proceed, report after (default) ⭐           |
| **L5** | High        | 80-95%         | High autonomy for trusted patterns          |
| **L6** | Full        | 95-100%        | Full autonomy (documentation, formatting)   |

### Session Management

| Term              | Definition                                                         |
|:------------------|:-------------------------------------------------------------------|
| **Handoff**       | Document created when work is incomplete, for session continuation |
| **Conversation**  | Record of key decisions and outcomes from a session                |
| **Session State** | Active work tracking file in `.history/current/`                   |

### Timeout Tiers

| Tier | Duration | Use Case                           |
|:-----|:---------|:-----------------------------------|
| T1   | ~100ms   | Cache lookup, in-memory operations |
| T2   | ~500ms   | Single file read, simple queries   |
| T3   | ~2s      | Layer/module loading               |
| T4   | ~5s      | Full system initialization         |
| T5   | ~10s     | Complex analysis, external calls   |

---

## 6. Regex Terminology

| Term                | Definition                                         |
|:--------------------|:---------------------------------------------------|
| **Anchor**          | Pattern that matches position (`^` start, `$` end) |
| **Literal**         | Text matched exactly as written                    |
| **Quantifier**      | Specifies how many times to match (`*`, `+`, `?`)  |
| **Character Class** | Set of characters to match (`[abc]`, `[^abc]`)     |
| **Escape Sequence** | `\Q...\E` for literal matching in Java regex       |

---

## 7. File Paths

| Path        | Purpose                                    |
|:------------|:-------------------------------------------|
| `.junie/`   | Junie AI configuration directory           |
| `.context/` | Project-specific knowledge base            |
| `.history/` | AI session records                         |
| `.outputs/` | Temporary/intermediate files (git-ignored) |

---

## 8. Related

- [Quick Start](../guides/quick-start.md) — Get started guide
- [Action Allowlist](../guides/action-allowlist.md) — Terminal rules
- [MCP Overview](../mcp/overview.md) — MCP architecture
- [Regex Reference](regex.md) — Regex patterns

---

*Part of the Junie Configuration Template System*
