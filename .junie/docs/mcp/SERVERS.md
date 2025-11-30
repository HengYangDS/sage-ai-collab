
# MCP Servers Reference

> Detailed documentation for each MCP server (~20 min read)

---

## Table of Contents

1. [Server Priority Overview](#1-server-priority-overview)
2. [P0: Critical Servers](#2-p0-critical-servers)
3. [P1: Important Servers](#3-p1-important-servers)
4. [P2: Useful Servers](#4-p2-useful-servers)
5. [Server Selection Guide](#5-server-selection-guide)
6. [Related](#6-related)

---

## 1. Server Priority Overview

| Priority | Servers                                          | Recommendation           |
|:---------|:-------------------------------------------------|:-------------------------|
| **P0**   | filesystem, memory                               | Always enable            |
| **P1**   | fetch, github, sequential-thinking               | Enable for most projects |
| **P2**   | puppeteer, docker, everything, desktop-commander | Enable as needed         |

---

## 2. P0: Critical Servers

### Filesystem Server

**Purpose**: File system operations within project scope

**Package**: `@modelcontextprotocol/server-filesystem`

**Configuration**:

```json
{
  "filesystem": {
    "command": "npx.cmd",
    "args": [
      "-y",
      "@modelcontextprotocol/server-filesystem",
      ".",
      ".junie"
    ],
    "_meta": {
      "description": "File operations within project scope",
      "priority": "P0",
      "triggers": [
        "Need to read project file content",
        "Search for code patterns",
        "List directory contents",
        "Check if file exists"
      ],
      "fallback": "Use IDE built-in file reading"
    }
  }
}
```

**Tools Available**:

| Tool             | Description              | Example                           |
|:-----------------|:-------------------------|:----------------------------------|
| `read_file`      | Read file content        | `read_file("src/main.py")`        |
| `write_file`     | Write content to file    | `write_file("test.txt", "hello")` |
| `list_directory` | List directory contents  | `list_directory("src/")`          |
| `search_files`   | Search for text in files | `search_files("class User")`      |
| `get_file_info`  | Get file metadata        | `get_file_info("README.md")`      |

**Path Configuration**:

- Add directories as additional args
- Use relative paths from project root
- Example: `[".", ".junie", "docs", "src"]`

---

### Memory Server

**Purpose**: Cross-session knowledge persistence via knowledge graph

**Package**: `@modelcontextprotocol/server-memory`

**Configuration**:

```json
{
  "memory": {
    "command": "npx.cmd",
    "args": [
      "-y",
      "@modelcontextprotocol/server-memory"
    ],
    "_meta": {
      "description": "Cross-session knowledge persistence",
      "priority": "P0",
      "triggers": [
        "Store important decisions",
        "Remember user preferences",
        "Persist learned patterns",
        "Retrieve context from previous sessions"
      ],
      "fallback": "Document decisions in .history/ files"
    }
  }
}
```

**Tools Available**:

| Tool               | Description                 | Example                                    |
|:-------------------|:----------------------------|:-------------------------------------------|
| `create_entities`  | Store knowledge entities    | `create_entities([{name, type, content}])` |
| `search_nodes`     | Search knowledge graph      | `search_nodes("authentication")`           |
| `create_relations` | Create entity relationships | `create_relations([{from, to, type}])`     |
| `open_nodes`       | Retrieve specific entities  | `open_nodes(["entity_name"])`              |
| `delete_entities`  | Remove entities             | `delete_entities(["old_entity"])`          |

**Best Practices**: See [Memory Best Practices](memory.md) for detailed patterns.

---

## 3. P1: Important Servers

### Fetch Server

**Purpose**: HTTP requests to external URLs and APIs

**Package**: `mcp-server-fetch` (via uvx)

**Configuration**:

```json
{
  "fetch": {
    "command": "uvx",
    "args": [
      "mcp-server-fetch"
    ],
    "_meta": {
      "description": "HTTP requests to external URLs",
      "priority": "P1",
      "triggers": [
        "Access external documentation",
        "Fetch API responses",
        "Download remote resources"
      ],
      "fallback": "Ask user to provide content manually"
    }
  }
}
```

**Tools Available**:

| Tool    | Description       | Example                                 |
|:--------|:------------------|:----------------------------------------|
| `fetch` | Fetch URL content | `fetch("https://api.example.com/docs")` |

**Use Cases**:

- Fetching external documentation
- Accessing public APIs
- Downloading configuration templates

---

### GitHub Server

**Purpose**: GitHub API integration for issues, PRs, and repository data

**Package**: `@modelcontextprotocol/server-github`

**Configuration**:

```json
{
  "github": {
    "command": "npx.cmd",
    "args": [
      "-y",
      "@modelcontextprotocol/server-github"
    ],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
    },
    "_meta": {
      "description": "GitHub API integration",
      "priority": "P1",
      "triggers": [
        "Query GitHub issues",
        "Check pull requests",
        "Get repository metadata",
        "Search related issues"
      ],
      "fallback": "Use git CLI commands for local operations"
    }
  }
}
```

**Tools Available**:

| Tool               | Description            | Example                               |
|:-------------------|:-----------------------|:--------------------------------------|
| `list_issues`      | List repository issues | `list_issues("owner/repo", "open")`   |
| `get_pull_request` | Get PR details         | `get_pull_request("owner/repo", 123)` |
| `search_issues`    | Search issues          | `search_issues("bug label:critical")` |
| `get_repository`   | Get repo info          | `get_repository("owner/repo")`        |

**Setup Requirements**:

1. Create GitHub Personal Access Token at https://github.com/settings/tokens
2. Set environment variable `GITHUB_PERSONAL_ACCESS_TOKEN`

---

### Sequential Thinking Server

**Purpose**: Step-by-step problem decomposition for complex reasoning

**Package**: `@modelcontextprotocol/server-sequential-thinking`

**Configuration**:

```json
{
  "sequential-thinking": {
    "command": "npx.cmd",
    "args": [
      "-y",
      "@modelcontextprotocol/server-sequential-thinking"
    ],
    "_meta": {
      "description": "Step-by-step problem decomposition",
      "priority": "P1",
      "triggers": [
        "Complex problem requiring breakdown",
        "Multi-step reasoning needed",
        "Architecture decision analysis",
        "Planning complex refactoring"
      ],
      "fallback": "Use Expert Committee Pattern in guidelines.md"
    }
  }
}
```

**Use Cases**:

- Breaking down complex problems
- Planning multi-step implementations
- Analyzing architecture decisions
- Debugging complex issues

---

## 4. P2: Useful Servers

### Puppeteer Server

**Purpose**: Headless browser automation for web scraping and UI testing

**Package**: `@modelcontextprotocol/server-puppeteer`

**Configuration**:

```json
{
  "puppeteer": {
    "command": "npx.cmd",
    "args": [
      "-y",
      "@modelcontextprotocol/server-puppeteer"
    ],
    "_meta": {
      "description": "Headless browser automation",
      "priority": "P2",
      "triggers": [
        "Test web UI behavior",
        "Scrape dynamic web content",
        "Take screenshots",
        "Automate browser interactions"
      ],
      "fallback": "Use fetch for static content"
    }
  }
}
```

**Tools Available**:

| Tool         | Description        | Example                             |
|:-------------|:-------------------|:------------------------------------|
| `navigate`   | Navigate to URL    | `navigate("http://localhost:3000")` |
| `screenshot` | Take screenshot    | `screenshot()`                      |
| `click`      | Click element      | `click("button#submit")`            |
| `evaluate`   | Execute JavaScript | `evaluate("document.title")`        |

---

### Docker Server

**Purpose**: Docker container management

**Package**: `mcp-server-docker`

**Configuration**:

```json
{
  "docker": {
    "command": "npx.cmd",
    "args": [
      "-y",
      "mcp-server-docker"
    ],
    "_meta": {
      "description": "Docker container management",
      "priority": "P2",
      "triggers": [
        "Check container status",
        "Start/stop services",
        "View container logs",
        "Manage Docker images"
      ],
      "fallback": "Use docker CLI commands"
    }
  }
}
```

**Tools Available**:

| Tool              | Description        | Example                           |
|:------------------|:-------------------|:----------------------------------|
| `list_containers` | List containers    | `list_containers()`               |
| `container_logs`  | Get container logs | `container_logs("container_id")`  |
| `start_container` | Start container    | `start_container("container_id")` |
| `stop_container`  | Stop container     | `stop_container("container_id")`  |

---

### Everything Server (Windows)

**Purpose**: System-wide fast file search using Everything search engine

**Package**: `mcp-server-everything`

**Configuration**:

```json
{
  "everything": {
    "command": "npx.cmd",
    "args": [
      "-y",
      "mcp-server-everything"
    ],
    "_meta": {
      "description": "System-wide fast file search (Windows)",
      "priority": "P2",
      "triggers": [
        "Fast system-wide file search",
        "Find files by name pattern",
        "Locate files outside project"
      ],
      "fallback": "Use filesystem.search for project scope"
    }
  }
}
```

**Requirements**:

- Windows only
- Everything search engine installed

---

### Desktop Commander Server

**Purpose**: Desktop automation and system command execution

**Package**: `@wonderwhy-er/desktop-commander`

**Configuration**:

```json
{
  "desktop-commander": {
    "command": "npx.cmd",
    "args": [
      "-y",
      "@wonderwhy-er/desktop-commander@latest"
    ],
    "_meta": {
      "description": "Desktop automation and system commands",
      "priority": "P2",
      "triggers": [
        "Execute complex terminal commands",
        "System-level operations",
        "Run background processes"
      ],
      "fallback": "Use standard terminal commands"
    }
  }
}
```

---

## 5. Server Selection Guide

### By Project Type

| Project Type       | Recommended Servers                       |
|:-------------------|:------------------------------------------|
| **Python Backend** | filesystem, memory, github, fetch         |
| **Web Frontend**   | filesystem, memory, puppeteer, fetch      |
| **Full Stack**     | filesystem, memory, github, fetch, docker |
| **Documentation**  | filesystem, memory, fetch                 |

### By Task

| Task                 | Best Server         |
|:---------------------|:--------------------|
| Read/write files     | filesystem          |
| Remember decisions   | memory              |
| Access external APIs | fetch               |
| GitHub integration   | github              |
| Complex reasoning    | sequential-thinking |
| Browser automation   | puppeteer           |
| Container management | docker              |

---

## 6. Related

- [Overview](overview.md) — MCP architecture
- [Configuration](configuration.md) — Setup guide
- [Memory Best Practices](memory.md) — Knowledge persistence
- [Troubleshooting](troubleshooting.md) — Problem solving

---

*AI Collaboration Knowledge Base*
