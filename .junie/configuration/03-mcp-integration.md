# MCP Integration Guide

> Achieve 60-75% token efficiency improvement with intelligent context management (~1-2 hours)

---

## Table of Contents

- [1. MCP Overview](#1-mcp-overview)
- [2. MCP Tools for Junie](#2-mcp-tools-for-junie)
- [3. MCP Configuration Methods](#3-mcp-configuration-methods)
- [4. Integration Roadmap](#4-integration-roadmap)
- [5. Tool Invocation Patterns](#5-tool-invocation-patterns)
- [6. Best Practices](#6-best-practices)
- [7. Troubleshooting](#7-troubleshooting)
- [8. FAQ](#8-faq)
- [9. Summary](#9-summary)

---

## 1. MCP Overview

**Model Context Protocol (MCP)** is an open protocol developed by Anthropic to establish standardized connections
between AI applications and external data sources and tools.

**Official Resources**:

- 📘 **MCP Specification**: https://modelcontextprotocol.io/specification
- 🌐 **MCP Official Site**: https://modelcontextprotocol.io/
- 💻 **MCP GitHub**: https://github.com/modelcontextprotocol
- 📖 **Junie MCP Docs**: https://www.jetbrains.com/help/junie/model-context-protocol-mcp.html

#### MCP Architecture Overview

The following diagram illustrates how Junie integrates with MCP servers to access external resources:

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
|  |   Filesystem   |  |     Memory     |  |      Git       |      |
|  |    Server      |  |     Server     |  |    Server      |      |
|  |  +-----------+ |  |  +-----------+ |  |  +-----------+ |      |
|  |  | read_file | |  |  | store     | |  |  | log       | |      |
|  |  | search    | |  |  | retrieve  | |  |  | diff      | |      |
|  |  | list_dir  | |  |  | query     | |  |  | status    | |      |
|  |  +-----------+ |  |  +-----------+ |  |  +-----------+ |      |
|  +-------+--------+  +-------+--------+  +-------+--------+      |
|          |                   |                   |               |
+----------|-------------------|-------------------|---------------+
           |                   |                   |
           v                   v                   v
+------------------------------------------------------------------+
|                     External Resources                           |
|                                                                  |
|  +----------------+  +----------------+  +----------------+      |
|  |   .junie/      |  |  Knowledge     |  |  Git           |      |
|  |   Config Files |  |  Graph Store   |  |  Repository    |      |
|  +----------------+  +----------------+  +----------------+      |
|                                                                  |
+------------------------------------------------------------------+
```

**Architecture Components**:

| Layer              | Component          | Function                                                  |
|:-------------------|:-------------------|:----------------------------------------------------------|
| **IDE Layer**      | Junie AI Assistant | Code generation, context management, user interaction     |
| **Protocol Layer** | MCP Client         | Protocol handling, server management, tool routing        |
| **Server Layer**   | MCP Servers        | Filesystem, Memory, Git operations via standardized tools |
| **Resource Layer** | External Resources | Config files, knowledge storage, version control          |

**Data Flow**:

1. **Request**: Junie sends tool request via MCP Client
2. **Route**: MCP Client routes to appropriate server via stdio
3. **Execute**: Server performs operation on external resource
4. **Response**: Result returns through the same path to Junie

#### MCP Integration Goals

**🚀 Core Goal**: Achieve intelligent context management, 60-75% token efficiency improvement

| MCP Server     | Priority  | Core Value                          | Implementation Status |
|:---------------|:----------|:------------------------------------|:----------------------|
| **Filesystem** | P0 🔥🔥🔥 | Intelligent config file access      | 📋 To Configure       |
| **Memory**     | P0 🔥🔥🔥 | Cross-session knowledge persistence | 📋 To Configure       |
| **Git**        | P0 🔥🔥🔥 | Configuration history tracing       | 📋 To Configure       |
| **GitHub**     | P1 🔥🔥   | Decision background tracing         | ⏸️ Optional           |
| **SQLite**     | P1 🔥🔥   | Configuration metadata management   | ⏸️ Optional           |

**Key Values**:

- 🧠 **Intelligence**: Load configuration on-demand, replace full loading
- ⚡ **Efficiency**: 60-75% reduction in token consumption
- 📚 **Knowledge Persistence**: Auto-convert project experience to configuration rules
- 🔍 **Traceability**: Understand evolution history and decision background of each configuration

#### MCP Configuration Statistics

- **Recommended P0 Tools**: 3 (Filesystem, Memory, Git)
- **Recommended P1 Tools**: 3 (GitHub, SQLite, Puppeteer)
- **Recommended P2 Tools**: 3 (Slack, Fetch, Google Drive)
- **Integration Phases**: Phase 1-3 (progressive implementation)

#### Why Junie Needs MCP

**Core Values**:

- 🚀 **Intelligent Configuration Access**: Dynamically read and search `.junie/` configuration repository
- 🧠 **Long-term Memory**: Maintain cross-session context and knowledge graph
- 📊 **Knowledge Persistence**: Auto-convert project experience to configuration rules
- ⚡ **Token Efficiency**: Load configuration on-demand, save 60-75% token consumption
- 🔍 **Configuration Tracing**: Understand evolution history and decision background of configurations

#### MCP Requirements for Junie Configuration Repository

Based on the project's `.junie` configuration repository architecture (three-tier configuration, intelligent layered
loading, dynamic knowledge persistence), core requirements include:

1. **Configuration Document Management**: Read and search configuration files in `.junie/` directory
2. **Intelligent Context Selection**: Dynamically load relevant configuration modules based on task type
3. **Knowledge Persistence**: Dynamically persist project experience to configuration repository
4. **Code Development Guidance**: Access project code, run tests, execute builds
5. **Version Control Integration**: Git operations, commit history queries, configuration evolution tracing
6. **Long-term Memory**: Cross-session context maintenance and project knowledge graph

#### Prerequisites

Before configuring MCP for Junie, ensure the following:

**Required**:

| Component     | Requirement               | Verification Command                                   |
|:--------------|:--------------------------|:-------------------------------------------------------|
| JetBrains IDE | With Junie plugin enabled | `Settings                                              | Plugins | Junie` |
| Node.js       | v18 or higher             | `node --version`                                       |
| npm/npx       | Included with Node.js     | `npx --version` (Unix) / `npx.cmd --version` (Windows) |

**Not Required**:

- ❌ Claude Desktop or Claude Code (Junie has native MCP support)
- ❌ Anthropic API key (Junie uses JetBrains AI backend)

> **Note**: MCP is an open protocol. Junie's MCP implementation is independent of Claude's implementation.

---

## 2. MCP Tools for Junie

Here are the recommended MCP tools prioritized for implementation.

#### 🏆 Priority P0: Core Tools (Immediate Integration)

##### 1. Filesystem Server ⭐⭐⭐⭐⭐

**Official Repository**: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

**Why Suitable for Junie**:

- ✅ Core requirement: Read and search `.junie/` configuration files
- ✅ Supports file search, content reading, directory traversal
- ✅ Secure sandbox mechanism with access scope restrictions
- ✅ Implements intelligent configuration file access

**Typical Use Cases**:

- Find configuration for specific topics (e.g., "Python coding standards")
- Read decision frameworks from `guidelines.md`
- Traverse `practices/` directory for best practices
- Search for relevant configuration modules

**Configuration Example**:

**Windows Configuration**:

```json
{
  "mcpServers": {
    "junie-config": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\\\path\\\\to\\\\project\\\\.junie"
      ]
    }
  }
}
```

**macOS/Linux Configuration**:

```json
{
  "mcpServers": {
    "junie-config": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/project/.junie"
      ]
    }
  }
}
```

> **⚠️ Cross-Platform Notes**:
> - **Windows**: Must use `npx.cmd`, paths use double backslashes `\\\\`
> - **macOS/Linux**: Use `npx`, paths use forward slashes `/`
> - **Verification**: Run `npx.cmd --version` (Windows) or `npx --version` (Unix) to confirm installation

---

##### 2. Memory Server ⭐⭐⭐⭐⭐

**Official Repository**: https://github.com/modelcontextprotocol/servers/tree/main/src/memory

**Why Suitable for Junie**:

- ✅ Core requirement: Implement "dynamic knowledge persistence mechanism"
- ✅ Supports knowledge graph storage and retrieval
- ✅ Cross-session long-term memory
- ✅ Entity-relationship modeling (configuration module → use case → effect evaluation)

**Typical Use Cases**:

- Store project-specific decision history
- Remember user's coding preferences and conventions
- Build project knowledge graph (module → function → best practice)
- Implement "experience to rules" automatic persistence
- Maintain cross-session configuration usage statistics

**Configuration Example**:

**Windows Configuration**:

```json
{
  "mcpServers": {
    "junie-memory": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    }
  }
}
```

**macOS/Linux Configuration**:

```json
{
  "mcpServers": {
    "junie-memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    }
  }
}
```

> **💡 Tip**: Windows users use `npx.cmd`, macOS/Linux users use `npx`

---

##### 3. Git Server ⭐⭐⭐⭐⭐

**Official Repository**: https://github.com/modelcontextprotocol/servers/tree/main/src/git

**Why Suitable for Junie**:

- ✅ Core requirement: Understand project and configuration evolution history
- ✅ Read commit history, branches, diffs
- ✅ Help Junie understand "why designed this way"
- ✅ Trace introduction background of configuration rules

**Typical Use Cases**:

- Query "why was this rule introduced" (via git blame)
- Understand configuration file evolution history
- Learn project's architectural decision-making process
- Trace modification history of specific rules

**Configuration Example**:

**Windows Configuration**:

```json
{
  "mcpServers": {
    "project-git": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "@modelcontextprotocol/server-git",
        "C:\\\\path\\\\to\\\\project"
      ]
    }
  }
}
```

**macOS/Linux Configuration**:

```json
{
  "mcpServers": {
    "project-git": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-git",
        "/path/to/project"
      ]
    }
  }
}
```

> **💡 Tip**: Windows users use `npx.cmd` and `\\\\` path separators, macOS/Linux users use `npx` and `/` path separators

---

#### 🥈 Priority P1/P2: Enhancement Tools (Optional)

**P1 Tools** (Near-term Integration):

- **GitHub Server** ⭐⭐⭐⭐: Access GitHub Issues and PRs for decision background
- **SQLite Server** ⭐⭐⭐⭐: Configuration metadata and usage statistics management
- **Puppeteer Server** ⭐⭐⭐: Automatically fetch external best practices

**P2 Tools** (Long-term Consideration):

- **Slack Server** ⭐⭐⭐: Team collaboration and configuration discussion integration
- **Fetch Server** ⭐⭐⭐: HTTP API calls for external data integration
- **Google Drive Server** ⭐⭐: Sync team shared configuration templates

**Complete Tool Comparison Matrix**:

| MCP Tool            | Suitability | Implementation Difficulty | Token Efficiency | Maintenance Cost | Priority |
|:--------------------|:------------|:--------------------------|:-----------------|:-----------------|:---------|
| Filesystem Server   | ⭐⭐⭐⭐⭐       | Low                       | High             | Low              | P0       |
| Memory Server       | ⭐⭐⭐⭐⭐       | Medium                    | Extremely High   | Medium           | P0       |
| Git Server          | ⭐⭐⭐⭐⭐       | Low                       | High             | Low              | P0       |
| GitHub Server       | ⭐⭐⭐⭐        | Medium                    | Medium           | Medium           | P1       |
| SQLite Server       | ⭐⭐⭐⭐        | Medium                    | High             | Medium           | P1       |
| Puppeteer Server    | ⭐⭐⭐         | High                      | Medium           | High             | P1       |
| Slack Server        | ⭐⭐⭐         | Medium                    | Low              | Medium           | P2       |
| Fetch Server        | ⭐⭐⭐         | Low                       | Medium           | Low              | P2       |
| Google Drive Server | ⭐⭐          | Medium                    | Low              | Medium           | P2       |

---

## 3. MCP Configuration Methods

> **⚠️ Important: Cross-Platform Configuration Differences**
>
> **All configuration examples in this section must be adjusted according to operating system**:
>
> | Platform | NPX Command | Path Separator | Example Path |
> |----------|-------------|----------------|--------------|
> | **Windows** | `npx.cmd` | `\\\\` (double backslash) | `C:\\\\path\\\\to\\\\project` |
> | **macOS/Linux** | `npx` | `/` (forward slash) | `/path/to/project` |
>
> **Verification Method**:
> - Windows: `npx.cmd --version`
> - macOS/Linux: `npx --version`
>
> **Common Issues**: If `npx.cmd` doesn't work on Windows, check:
> 1. Node.js is properly installed
> 2. `npm` and `npx` are in PATH environment variable
> 3. Try using full path: `C:\Program Files\nodejs\npx.cmd`

#### Current Status (November 2025)

**✅ JetBrains Junie Officially Supports MCP Integration**

JetBrains has released official Junie MCP documentation, indicating MCP functionality is officially supported. Please
refer to the following official documentation for the latest configuration methods:

- **Official MCP Documentation
  **: [Model Context Protocol (MCP)](https://www.jetbrains.com/help/junie/model-context-protocol-mcp.html)
- **MCP Settings Guide**: [MCP Settings](https://www.jetbrains.com/help/junie/mcp-settings.html)

The following provides generic configuration methods based on MCP standard protocol. **It's recommended to prioritize
the official documentation above for the most accurate configuration steps**.

---

#### Method 1: Settings UI Configuration (Official Recommendation)

**Path**: `Settings | Tools | Junie | MCP Settings`

**Configuration Steps**:

1. Open Settings (`Ctrl + Alt + S`)
2. Navigate to `Tools | Junie`
3. Look for "MCP Settings" or "Model Context Protocol" option
4. Click toolbar button to edit `mcp.json` file
5. Add MCP server configuration (JSON format)

**Important**: Specific configuration interface and options may vary by Junie version, please refer to official
documentation: https://www.jetbrains.com/help/junie/mcp-settings.html

---

#### Method 2: Configuration File Method (Advanced Users)

**Configuration File Locations**:

**Global Configuration** (available for all projects):

- **Windows**: `%USERPROFILE%\\.junie\\mcp.json`
- **macOS/Linux**: `~/.junie/mcp.json`

**Project-Level Configuration** (current project only):

- `<project-root>/.junie/mcp/mcp.json`

**Standard mcp.json Configuration Format**:

**Windows Example**:

```json
{
  "mcpServers": {
    "junie-config": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\\\path\\\\to\\\\project\\\\.junie"
      ]
    },
    "junie-memory": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    },
    "project-git": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "@modelcontextprotocol/server-git",
        "C:\\\\path\\\\to\\\\project"
      ]
    }
  }
}
```

**macOS/Linux Example**:

```json
{
  "mcpServers": {
    "junie-config": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/project/.junie"
      ]
    },
    "junie-memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    },
    "project-git": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-git",
        "/path/to/project"
      ]
    }
  }
}
```

**Supported Transport Types**:

- ✅ **stdio** (Standard Input/Output) - Currently supported
- ⏸️ Other transport types (may be supported in future)

**Important Notes**:

- ⚠️ Directly modifying configuration files has risks, Settings UI (Method 1) is recommended
- ⚠️ Backup configuration file before modification
- ⚠️ Refer to official documentation for specific configuration
  format: https://www.jetbrains.com/help/junie/mcp-settings.html
- ✅ Settings UI is recommended for configuration
- 📁 Global configuration for personal common tools, project-level configuration for team sharing

---

## 4. Integration Roadmap

#### Phase 1: Basic Integration (1-2 weeks)

**Goal**: Implement intelligent configuration file access

**Integration Tools**:

- ✅ Filesystem Server
- ✅ Memory Server
- ✅ Git Server

**Verification Criteria**:

- ✅ AI can search and reference rules from `.junie/guidelines.md`
- ✅ Knowledge persistence functionality works (Memory Server)
- ✅ Git history queries successful
- ✅ Token consumption reduced by 40-50%

**Expected Benefits**:

- Intelligent configuration queries replace full loading
- Cross-session memory and context persistence
- Configuration evolution history tracing

---

## 5. Tool Invocation Patterns

This section provides guidance on when and how AI agents should automatically invoke MCP tools. Tool metadata is defined
in `mcp.json` with `_meta` fields containing triggers, examples, and fallbacks.

#### 5.1 Tool Priority Levels

| Priority | Level    | Description                                    | Tools                                            |
|:---------|:---------|:-----------------------------------------------|:-------------------------------------------------|
| **P0**   | Core     | Essential tools for basic functionality        | filesystem, memory                               |
| **P1**   | Enhanced | Tools that improve efficiency and capabilities | fetch, github, sequential-thinking               |
| **P2**   | Optional | Specialized tools for specific use cases       | puppeteer, docker, everything, desktop-commander |

**Recommendation**: Start with P0 tools, add P1 tools after validating benefits, use P2 tools only when specific needs
arise.

---

#### 5.2 Automatic Trigger Rules

The following table maps common task scenarios to appropriate MCP tools:

| Trigger Condition                        | Tool                  | Action                                                                |
|:-----------------------------------------|:----------------------|:----------------------------------------------------------------------|
| Need to read project file content        | `filesystem`          | `filesystem.read_file('.junie/guidelines.md')`                        |
| Search for code patterns or text         | `filesystem`          | `filesystem.search_files('class UserService')`                        |
| List directory contents                  | `filesystem`          | `filesystem.list_directory('src/')`                                   |
| Store important decisions for future     | `memory`              | `memory.create_entities([{name: 'decision', ...}])`                   |
| Retrieve context from previous sessions  | `memory`              | `memory.search_nodes('authentication approach')`                      |
| Build project knowledge graph            | `memory`              | `memory.create_relations([{from: 'A', to: 'B', type: 'depends_on'}])` |
| Access external documentation or URLs    | `fetch`               | `fetch.get('https://api.example.com/docs')`                           |
| Query GitHub issues or PRs               | `github`              | `github.list_issues(repo='owner/repo', state='open')`                 |
| Complex problem requiring step breakdown | `sequential-thinking` | `sequential_thinking.analyze(problem='...')`                          |
| Test web UI behavior                     | `puppeteer`           | `puppeteer.navigate('http://localhost:3000')`                         |
| Check container status                   | `docker`              | `docker.list_containers()`                                            |
| Fast file search across system           | `everything`          | `everything.search('*.config.js')`                                    |
| Execute complex terminal commands        | `desktop-commander`   | `desktop_commander.execute('npm run build')`                          |

---

#### 5.3 Tool Chain Combinations

For complex workflows, combine multiple tools in sequence:

**Pattern 1: Intelligent Configuration Loading**

```
1. filesystem.search_files('authentication')     # Find relevant config
2. filesystem.read_file('found_file.md')         # Read content
3. memory.create_entities([...])                 # Persist to knowledge graph
```

**Pattern 2: Decision Documentation**

```
1. sequential_thinking.analyze(problem='...')    # Analyze problem
2. memory.create_entities([{type: 'decision'}])  # Store decision
3. filesystem.write_file('.history/...')         # Create history record
```

**Pattern 3: External Knowledge Integration**

```
1. fetch.get('https://docs.example.com/api')     # Fetch external docs
2. memory.create_entities([...])                 # Store relevant info
3. filesystem.search_files('related_code')       # Find related code
```

**Pattern 4: GitHub Issue Investigation**

```
1. github.get_issue(repo='...', issue_number=N)  # Get issue details
2. filesystem.search_files('error_message')      # Search codebase
3. sequential_thinking.decompose(task='fix')     # Plan fix approach
```

---

#### 5.4 Fallback Strategies

When a tool is unavailable or fails, use these fallback approaches:

| Tool                  | Primary Function      | Fallback Strategy                                              |
|:----------------------|:----------------------|:---------------------------------------------------------------|
| `filesystem`          | File operations       | Use IDE built-in file reading                                  |
| `memory`              | Knowledge persistence | Document in `.history/` files                                  |
| `fetch`               | HTTP requests         | Ask user to provide content manually                           |
| `github`              | GitHub API            | Use git CLI commands for local operations                      |
| `sequential-thinking` | Complex reasoning     | Use Expert Committee Pattern in guidelines.md                  |
| `puppeteer`           | Browser automation    | Use fetch for static content, manual testing for UI            |
| `docker`              | Container management  | Use docker CLI commands directly                               |
| `everything`          | System-wide search    | Use filesystem.search for project scope, or terminal find/grep |
| `desktop-commander`   | System commands       | Use standard terminal commands via bash tool                   |

---

#### 5.5 Usage Examples

##### Filesystem Operations

```javascript
// Read a configuration file
filesystem.read_file('.junie/guidelines.md')

// Search for patterns in code
filesystem.search_files('class UserService')

// List directory contents
filesystem.list_directory('src/')
```

##### Memory Operations

```javascript
// Store a decision
memory.create_entities([{
    name: 'auth_decision',
    type: 'decision',
    content: 'Using JWT for API authentication'
}])

// Search for previous context
memory.search_nodes('authentication approach')

// Create relationships
memory.create_relations([{
    from: 'UserService',
    to: 'AuthModule',
    type: 'depends_on'
}])
```

##### External Data Access

```javascript
// Fetch external documentation
fetch.get('https://api.example.com/docs')

// Query GitHub issues
github.list_issues(repo = 'owner/repo', state = 'open')
github.get_pull_request(repo = 'owner/repo', pr_number = 123)
```

##### Complex Problem Solving

```javascript
// Step-by-step problem analysis
sequential_thinking.analyze(problem = 'How to migrate from REST to GraphQL')

// Task decomposition
sequential_thinking.decompose(task = 'Implement authentication system')
```

---

#### 5.6 Best Practices for Tool Invocation

1. **Check tool availability** before attempting complex tool chains
2. **Use P0 tools first** - filesystem and memory cover most common needs
3. **Persist important findings** - use memory to store discoveries for future sessions
4. **Document fallback usage** - when fallbacks are used, note why the primary tool failed
5. **Minimize external calls** - batch fetch/github requests when possible
6. **Validate before storing** - ensure data quality before persisting to memory

---

## 6. Best Practices

#### 1. Security First

**Access Control**:

- Limit Filesystem Server to `.junie/` directory only
- Do not grant write permissions to sensitive directories
- Regular security audits of MCP tool access scope

#### 2. Performance Optimization

**Configuration Strategies**:

- Start with P0 tools (Filesystem + Memory + Git)
- Monitor token efficiency improvement
- Add P1/P2 tools only after confirming benefits

#### 3. Maintenance Strategy

**Regular Tasks**:

- Review MCP tool usage logs
- Update MCP server versions monthly
- Monitor token consumption and efficiency metrics

#### 4. Progressive Integration

**Recommended Flow**:

1. ✅ Start with P0 tools
2. ✅ Verify in JetBrains IDE (`Settings | Tools | Junie | MCP Settings`)
3. ✅ Record token consumption comparison
4. ✅ Evaluate before adding P1/P2 tools
5. ✅ Avoid integrating too many services at once (affects performance)

---

## 7. Troubleshooting

#### Problem 1: MCP Server Cannot Start

**Symptoms**: MCP server doesn't respond after configuration

**Possible Causes**:

- Node.js not installed or version too low
- npx command not available
- Network issues causing package download failure

**Solutions**:

1. Confirm Node.js is installed: `node --version` (requires v18+)
2. Confirm npx is available: `npx --version`
3. Manually install MCP servers:
   ```bash
   npm install -g @modelcontextprotocol/server-filesystem
   npm install -g @modelcontextprotocol/server-memory
   ```
4. Check firewall settings

---

#### Problem 1A: Windows Platform npx Command Not Working ⚠️

**Symptoms**: Windows system reports error after MCP configuration, indicating `npx` command not found or execution
failed

**Typical Error Messages**:

- `'npx' is not recognized as an internal or external command`
- `npx: command not found`
- MCP server startup fails, no response

**Root Cause**:

Windows PowerShell requires explicit `.cmd` extension to correctly execute npm scripts. Using `npx` directly on Windows
will fail.

**Solution 1: Use npx.cmd (Recommended)**

Change all `"command": "npx"` in configuration to `"command": "npx.cmd"`:

```json
{
  "mcpServers": {
    "junie-config": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\\\path\\\\to\\\\project\\\\.junie"
      ]
    }
  }
}
```

> **✅ Key Point**: Windows must use `npx.cmd` instead of `npx`

**Solution 2: Use Node.js Full Path**

If `npx.cmd` still doesn't work, use Node.js absolute path:

```json
{
  "mcpServers": {
    "junie-config": {
      "command": "node",
      "args": [
        "C:\\\\Program Files\\\\nodejs\\\\node_modules\\\\npm\\\\bin\\\\npx-cli.js",
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\\\path\\\\to\\\\project\\\\.junie"
      ]
    }
  }
}
```

**Solution 3: Check Environment Variable Configuration**

1. Open PowerShell, verify Node.js installation:
   ```powershell
   node --version
   npm --version
   npx.cmd --version
   ```

2. Check PATH environment variable:
   ```powershell
   C:\Users\Administrator\.conda\envs\star;C:\Users\Administrator\.conda\envs\star\Library\mingw-w64\bin;C:\Users\Administrator\.conda\envs\star\Library\usr\bin;C:\Users\Administrator\.conda\envs\star\Library\bin;C:\Users\Administrator\.conda\envs\star\Scripts;C:\Users\Administrator\.conda\envs\star\bin;D:\ProgramData\miniconda3\condabin;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0;C:\WINDOWS\System32\OpenSSH;C:\Program Files\NVIDIA Corporation\NVIDIA App\NvDLISR;C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;C:\Program Files\nodejs;D:\Program Files\Git\cmd;C:\Program Files\Docker\Docker\resources\bin;C:\Users\Administrator\scoop\apps\openjdk\current\bin;C:\Users\Administrator\scoop\apps\openjdk21\current\bin;C:\Users\Administrator\scoop\shims;C:\Users\Administrator\.local\bin;C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps;C:\Users\Administrator\AppData\Local\JetBrains\Toolbox\scripts;C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps;C:\Users\Administrator\AppData\Roaming\npm -split ';' | Select-String -Pattern 'nodejs'
   ```

3. If Node.js not in PATH, add the following paths to system environment variables:
    - `C:\Program Files\nodejs\`
    - `%APPDATA%\npm`

4. Restart IDE for environment variables to take effect

**Solution 4: Reinstall Node.js**

If above methods don't work:

1. Completely uninstall Node.js
2. Download latest LTS version from official site: https://nodejs.org/
3. During installation, ensure "Add to PATH" is checked
4. Restart computer after installation
5. Verify installation:
   ```powershell
   node --version
   npx.cmd --version
   ```

**Verify Fix is Successful**:

```powershell
# Test if npx.cmd is available
npx.cmd --version

# Test if MCP server can start
npx.cmd -y @modelcontextprotocol/server-filesystem --help
```

**Common Pitfalls**:

- ❌ Using `npx` instead of `npx.cmd`
- ❌ Using single backslash `\` instead of double backslash `\\\\`
- ❌ Not restarting IDE after environment variable configuration
- ❌ Testing in Git Bash or WSL (should test in PowerShell)

**Platform Comparison**:

| Platform | Correct Command | Incorrect Command |
|----------|-----------------|-------------------|
| Windows  | `npx.cmd`       | `npx` ❌           |
| macOS    | `npx`           | `npx.cmd` ❌       |
| Linux    | `npx`           | `npx.cmd` ❌       |

---

#### Problem 2: Filesystem Server Access Denied

**Symptoms**: Cannot read `.junie/` directory files

**Possible Causes**:

- Path configuration error
- Insufficient permissions
- Path contains special characters

**Solutions**:

1. **Verify Path Format**:
    - Windows: Use double backslashes `C:\\\\path\\\\to\\\\.junie`
    - Unix: Use forward slashes `/path/to/.junie`

2. **Check Permissions**:
   ```bash
   # Unix
   chmod -R 755 .junie/
   
   # Windows (PowerShell, run as admin if needed)
   icacls .junie /grant Everyone:(OI)(CI)F
   ```

3. **Use Absolute Paths**:
    - Avoid relative paths
    - Use full absolute paths for reliability

---

## 8. FAQ

> **Scope**: This FAQ covers MCP integration questions. For Action Allowlist questions,
> see [Action Allowlist FAQ](#action-allowlist-faq) in Part 2.

#### Q1: How do I verify MCP is working after configuration?

**A**:

1. Open `Settings | Tools | Junie | MCP Settings`
2. Check that configured servers show "Connected" status
3. In a Junie session, ask it to read a file from `.junie/` directory
4. If it can access the file without manual approval, MCP is working

#### Q2: MCP server starts but Junie can't use it. Why?

**A**: Common causes:

1. **Path issues**: Verify paths use correct format (Windows: `\\`, Unix: `/`)
2. **Permission denied**: Check file/directory permissions
3. **Server timeout**: Some servers take time to initialize; wait 10-15 seconds
4. **Version mismatch**: Ensure Node.js is v18+ (`node --version`)

#### Q3: Do I need Claude Desktop for MCP?

**A**: **No**. Junie has native MCP support. Claude Desktop is only needed for Claude-specific workflows, not for Junie.

#### Q4: What's the expected token efficiency improvement with MCP?

**A**: With P0 tools (Filesystem, Memory, Git) properly configured:

- **40-50% improvement** in Phase 1 (basic integration)
- **60-75% improvement** after optimization and knowledge persistence

---

## 9. Summary

### 9.1 Configuration Achievements

**Basic Configuration (Action Allowlist)**:

- ✅ 87 Terminal rules
- ✅ 3 Allowed Actions (RunTest, Build, ReadOutsideProject)
- ✅ Level 5 autonomy
- ✅ 90%+ reduction in manual approvals

**Advanced Integration (MCP)**:

- 🚀 9 recommended MCP tools (P0: 3, P1: 3, P2: 3)
- 🚀 2 configuration methods (Settings UI / Configuration file)
- 🚀 3-phase integration roadmap (Phase 1-3, progressive implementation)
- 🚀 Complete best practices and troubleshooting guides

---

### 9.2 Core Values

**Basic Configuration Values**:

- 🔒 **Security**: Precise control, dangerous operations excluded, 87 rules comprehensive coverage
- 🚀 **Autonomy**: Batch execution enabled, 90%+ interaction reduction, Level 5 high autonomy
- 🎯 **Flexibility**: Progressive trust building, rules adjustable anytime
- 📊 **Controllability**: Global management, thorough verification, configuration recoverable

**MCP Integration Values**:

- 🧠 **Intelligence**: Dynamic configuration loading, intelligent context selection
- ⚡ **Efficiency**: 60-75% token consumption reduction, on-demand module loading
- 📚 **Knowledge Persistence**: Auto-convert project experience to configuration rules
- 🔍 **Traceability**: Understand configuration evolution history and decision background
- 🌐 **Extensibility**: 9 MCP tools covering files, memory, version control, team collaboration, etc.

---

### 9.3 Expected Results

**After Action Allowlist Configuration**:

- ✅ Common commands require no approval (90%+ auto-execution)
- ✅ Code quality checks automated (6 tools)
- ✅ Phase-level continuous execution (batch mode)
- ✅ 5-10x collaboration efficiency improvement

**After MCP Integration**:

- 🚀 60-75% token efficiency improvement (intelligent loading vs. full loading)
- 🚀 Enhanced configuration query accuracy (Filesystem Server)
- 🚀 Cross-session memory persistence (Memory Server)
- 🚀 Configuration evolution tracing (Git Server)
- 🚀 Self-evolving configuration library (dynamic knowledge persistence)
- 🚀 Enhanced team collaboration (GitHub/Slack integration)

**Overall Impact**:

- 🎯 10-15x development efficiency improvement
- 🎯 70% configuration maintenance time reduction
- 🎯 50% onboarding time reduction
- 🎯 Configuration library becomes team knowledge hub

---

## Related

- `README.md` — Configuration guide index
- `01-introduction.md` — Document overview
- `02-action-allowlist.md` — Terminal rules configuration (previous)
- `04-future-vision.md` — Protocol roadmap (next)
- `05-appendix.md` — References and resources

---

*Part of the Junie Configuration Guide*
