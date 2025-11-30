---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---

# MCP Overview

> Model Context Protocol architecture and concepts (~15 min read)

---

## Table of Contents

1. [What is MCP?](#1-what-is-mcp)
2. [Architecture Overview](#2-architecture-overview)
3. [Integration Goals](#3-integration-goals)
4. [MCP Servers](#4-mcp-servers)
5. [Key Concepts](#5-key-concepts)
6. [Benefits for Junie](#6-benefits-for-junie)
7. [Getting Started](#7-getting-started)
8. [Related](#8-related)

---

## 1. What is MCP?

**Model Context Protocol (MCP)** is an open protocol developed by Anthropic that establishes standardized connections
between AI applications and external data sources and tools.

### Official Resources

- 📘 **MCP Specification**: https://modelcontextprotocol.io/specification
- 🌐 **MCP Official Site**: https://modelcontextprotocol.io/
- 💻 **MCP GitHub**: https://github.com/modelcontextprotocol
- 📖 **Junie MCP Docs**: https://www.jetbrains.com/help/junie/model-context-protocol-mcp.html

---

## 2. Architecture Overview

```
+------------------------------------------------------------------+
|                        JetBrains IDE                             |
|  +------------------------------------------------------------+  |
|  |                     Junie AI Assistant                     |  |
|  |  +-------------------------+  +-------------------------+  |  |
|  |  |    Code Generation      |  |    Context Management   |  |  |
|  |  +-------------------------+  +-------------------------+  |  |
|  +---------------------------+--------------------------------+  |
|                              |                                   |
|                              v                                   |
|  +---------------------------+--------------------------------+  |
|  |                    MCP Client (Built-in)                   |  |
|  |  - Protocol Handler    - Server Manager    - Tool Router   |  |
|  +---------------------------+--------------------------------+  |
+------------------------------|-----------------------------------+
                               | stdio/JSON-RPC
                               v
+------------------------------------------------------------------+
|                      MCP Server Layer                            |
|                                                                  |
|  +----------------+  +----------------+  +----------------+      |
|  |   Filesystem   |  |     Memory     |  |     Fetch      |      |
|  |    Server      |  |     Server     |  |    Server      |      |
|  |  +-----------+ |  |  +-----------+ |  |  +-----------+ |      |
|  |  | read_file | |  |  | store     | |  |  | get       | |      |
|  |  | search    | |  |  | retrieve  | |  |  | post      | |      |
|  |  | list_dir  | |  |  | query     | |  |  | fetch     | |      |
|  |  +-----------+ |  |  +-----------+ |  |  +-----------+ |      |
|  +-------+--------+  +-------+--------+  +-------+--------+      |
+----------|-------------------|-------------------|---------------+
           v                   v                   v
+------------------------------------------------------------------+
|                     External Resources                           |
|  +----------------+  +----------------+  +----------------+      |
|  |   Project      |  |  Knowledge     |  |   External     |      |
|  |   Files        |  |  Graph Store   |  |   APIs         |      |
|  +----------------+  +----------------+  +----------------+      |
+------------------------------------------------------------------+
```

### Architecture Components

| Layer              | Component          | Function                                              |
|:-------------------|:-------------------|:------------------------------------------------------|
| **IDE Layer**      | Junie AI Assistant | Code generation, context management, user interaction |
| **Protocol Layer** | MCP Client         | Protocol handling, server management, tool routing    |
| **Server Layer**   | MCP Servers        | Filesystem, Memory, Fetch operations via tools        |
| **Resource Layer** | External Resources | Project files, knowledge storage, external APIs       |

### Data Flow

1. **Request**: Junie sends tool request via MCP Client
2. **Route**: MCP Client routes to appropriate server via stdio
3. **Execute**: Server performs operation on external resource
4. **Response**: Result returns through the same path to Junie

---

## 3. Integration Goals

**🚀 Core Goal**: Achieve intelligent context management with 60-75% token efficiency improvement

| Benefit                  | Impact     | Description                            |
|:-------------------------|:-----------|:---------------------------------------|
| **Token Efficiency**     | 60-75%     | Reduced context by intelligent caching |
| **Cross-Session Memory** | Persistent | Knowledge survives session boundaries  |
| **External Access**      | Expanded   | Access APIs, files, and services       |
| **Automation**           | Enhanced   | Complex workflows via tool chaining    |

---

## 4. MCP Servers

### Priority Levels

| Priority | Name      | Description                          | Examples                           |
|:---------|:----------|:-------------------------------------|:-----------------------------------|
| **P0**   | Critical  | Essential for basic functionality    | filesystem, memory                 |
| **P1**   | Important | Significantly enhances workflow      | github, fetch, sequential-thinking |
| **P2**   | Useful    | Nice-to-have for specific scenarios  | puppeteer, docker, everything      |
| **P3**   | Optional  | Rarely needed, specialized use cases | Custom project-specific servers    |

### Server Overview

| Server                  | Priority  | Core Value                           |
|:------------------------|:----------|:-------------------------------------|
| **filesystem**          | P0 🔥🔥🔥 | File operations within project scope |
| **memory**              | P0 🔥🔥🔥 | Cross-session knowledge persistence  |
| **fetch**               | P1 🔥🔥   | HTTP requests to external URLs/APIs  |
| **github**              | P1 🔥🔥   | GitHub API integration               |
| **sequential-thinking** | P1 🔥🔥   | Step-by-step problem decomposition   |
| **puppeteer**           | P2 🔥     | Headless browser automation          |
| **docker**              | P2 🔥     | Docker container management          |
| **everything**          | P2 🔥     | System-wide file search (Windows)    |
| **desktop-commander**   | P2 🔥     | Desktop automation                   |

For detailed server configuration, see [Servers Reference](SERVERS.md).

---

## 5. Key Concepts

### Tools

**Tools** are specific functions exposed by MCP servers that Junie can invoke:

```
filesystem.read_file(path)     → Read file content
memory.create_entities([...])  → Store knowledge
fetch.get(url)                 → HTTP GET request
```

### Communication Protocol

MCP uses **stdio** (standard input/output) with **JSON-RPC** messages:

- **Transport**: Process stdio streams
- **Format**: JSON-RPC 2.0
- **Direction**: Bidirectional (request/response)

### Server Lifecycle

```
1. IDE starts → MCP Client initializes
2. Client spawns server processes
3. Servers register available tools
4. Junie invokes tools as needed
5. IDE closes → Servers terminate
```

---

## 6. Benefits for Junie

### 6.1. Intelligent Context Loading

Instead of loading entire files, Junie can:

- Read specific sections via filesystem server
- Query relevant knowledge via memory server
- Fetch external documentation on demand

### 6.2. Persistent Knowledge

Memory server enables:

- Architecture decisions that persist across sessions
- Learned patterns from codebase analysis
- User preferences and conventions

### 6.3. Extended Capabilities

MCP servers provide:

- File system operations
- External API access
- Browser automation
- Container management

---

## 7. Getting Started

### Quick Setup

1. **Verify prerequisites**: Node.js v18+, Junie 2025.1+
2. **Configure servers**: Edit `.junie/mcp/mcp.json`
3. **Enable in IDE**: `Settings | Tools | Junie | MCP Servers`
4. **Test connection**: Use Junie to read a file

### Next Steps

| Goal                   | Document                              |
|:-----------------------|:--------------------------------------|
| Configure MCP servers  | [Configuration](CONFIGURATION.md)     |
| Learn server details   | [Servers Reference](SERVERS.md)       |
| Use Memory effectively | [Memory Best Practices](MEMORY.md)    |
| Fix connection issues  | [Troubleshooting](TROUBLESHOOTING.md) |

---

## 8. Related

- [Configuration](CONFIGURATION.md) — Setup MCP servers
- [Servers Reference](SERVERS.md) — Detailed server documentation
- [Memory Best Practices](MEMORY.md) — Knowledge persistence patterns
- [Troubleshooting](TROUBLESHOOTING.md) — Problem solving

---

*Part of the Junie Configuration Template System*
