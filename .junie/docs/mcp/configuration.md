# MCP Configuration

> Setup and configure MCP servers for Junie (~30 min)

---

## Prerequisites

Before configuring MCP:

- **Node.js v18+**: Required for running MCP servers
- **Junie 2025.1+**: MCP support requires this version
- **npx**: Comes with Node.js, used to run server packages

Verify installation:

```bash
node --version   # Should show v18.x or higher
npx --version    # Should show version number
```

---

## Configuration Methods

### Method 1: Project Configuration (Recommended)

Place `mcp.json` in your project's `.junie/mcp/` directory:

```
your-project/
└── .junie/
    └── mcp/
        └── mcp.json    # MCP server configuration
```

**Advantages**:

- Version controlled with project
- Shared across team
- Project-specific servers

### Method 2: IDE Settings

Configure via `Settings | Tools | Junie | MCP Servers`:

1. Open Settings
2. Navigate to `Tools | Junie | MCP Servers`
3. Add servers manually

**Advantages**:

- Global configuration
- No project setup required

---

## Configuration File Structure

### Basic Structure

```json
{
  "$schema": "./mcp.schema.json",
  "mcpServers": {
    "server-name": {
      "command": "npx.cmd",
      "args": ["-y", "@package/server-name"],
      "env": {},
      "_meta": {}
    }
  }
}
```

### Field Reference

| Field     | Required | Description                            |
|:----------|:---------|:---------------------------------------|
| `command` | Yes      | Executable to run (`npx.cmd` or `npx`) |
| `args`    | Yes      | Command arguments array                |
| `env`     | No       | Environment variables                  |
| `_meta`   | No       | Metadata for documentation             |

### Platform Commands

| Platform        | Command   |
|:----------------|:----------|
| **Windows**     | `npx.cmd` |
| **macOS/Linux** | `npx`     |

---

## Essential Server Configurations

### Filesystem Server (P0)

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
      "priority": "P0"
    }
  }
}
```

**Path Arguments**:

- `.` — Project root (current directory)
- `.junie` — Configuration directory
- Add more paths as needed

### Memory Server (P0)

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
      "priority": "P0"
    }
  }
}
```

### Fetch Server (P1)

```json
{
  "fetch": {
    "command": "uvx",
    "args": ["mcp-server-fetch"],
    "_meta": {
      "description": "HTTP requests to external URLs",
      "priority": "P1"
    }
  }
}
```

### GitHub Server (P1)

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
      "priority": "P1"
    }
  }
}
```

**Setup**:

1. Create GitHub Personal Access Token
2. Set environment variable: `GITHUB_PERSONAL_ACCESS_TOKEN`

---

## Complete Configuration Example

```json
{
  "$schema": "./mcp.schema.json",
  "$comment": "MCP Server Configuration for Junie",
  "mcpServers": {
    "filesystem": {
      "command": "npx.cmd",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", ".", ".junie"],
      "_meta": {
        "description": "File system operations",
        "priority": "P0",
        "triggers": ["Read file", "Search code", "List directory"],
        "fallback": "Use IDE built-in file reading"
      }
    },
    "memory": {
      "command": "npx.cmd",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "_meta": {
        "description": "Knowledge persistence",
        "priority": "P0",
        "triggers": ["Store decision", "Remember pattern", "Retrieve context"],
        "fallback": "Document in .history/ files"
      }
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "_meta": {
        "description": "HTTP requests",
        "priority": "P1",
        "triggers": ["Access external docs", "Fetch API responses"],
        "fallback": "Ask user to provide content"
      }
    },
    "github": {
      "command": "npx.cmd",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      },
      "_meta": {
        "description": "GitHub API",
        "priority": "P1",
        "triggers": ["Query issues", "Check PRs", "Repository info"],
        "fallback": "Use git CLI commands"
      }
    },
    "sequential-thinking": {
      "command": "npx.cmd",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "_meta": {
        "description": "Step-by-step reasoning",
        "priority": "P1",
        "triggers": ["Complex problem", "Multi-step analysis"],
        "fallback": "Use Expert Committee Pattern"
      }
    }
  }
}
```

---

## Server Profiles

Configure different server sets for different scenarios:

### Minimal Profile

Essential servers only:

```json
{
  "mcpServers": {
    "filesystem": { "..." },
    "memory": { "..." }
  }
}
```

**Use case**: Basic development, limited resources

### Standard Profile

Common workflow servers:

```json
{
  "mcpServers": {
    "filesystem": { "..." },
    "memory": { "..." },
    "fetch": { "..." },
    "github": { "..." }
  }
}
```

**Use case**: Regular development workflow

### Full Profile

All available servers:

```json
{
  "mcpServers": {
    "filesystem": { "..." },
    "memory": { "..." },
    "fetch": { "..." },
    "github": { "..." },
    "sequential-thinking": { "..." },
    "puppeteer": { "..." },
    "docker": { "..." }
  }
}
```

**Use case**: Advanced workflows, automation

---

## Path Configuration

### Relative Paths (Recommended)

Use `.` for project root — resolves to current working directory:

```json
"args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
```

### Multiple Paths

Allow access to multiple directories:

```json
"args": ["-y", "@modelcontextprotocol/server-filesystem", ".", ".junie", "docs"]
```

### Important Notes

- ✅ Use relative paths (`.`, `./src`, `.junie`)
- ✅ Paths resolve when server starts
- ❌ Avoid `${PROJECT_ROOT}` — not supported
- ❌ Avoid absolute paths — not portable

---

## Environment Variables

### Setting Tokens

For servers requiring authentication:

**Windows PowerShell**:

```powershell
$env:GITHUB_PERSONAL_ACCESS_TOKEN = "your-token-here"
```

**macOS/Linux**:

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="your-token-here"
```

### Persistent Configuration

Add to shell profile (`.bashrc`, `.zshrc`, PowerShell profile):

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_xxxxxxxxxxxx"
```

---

## Enabling in IDE

### Step 1: Load Configuration

1. Open `Settings | Tools | Junie | MCP Servers`
2. Click "Reload" to load from `mcp.json`
3. Verify servers appear in list

### Step 2: Start Servers

1. Select servers to enable
2. Click "Start" or "Start All"
3. Wait for "Connected" status

### Step 3: Verify Connection

Test with Junie:

- "Read the README.md file" (filesystem)
- "Remember that we use pytest" (memory)

---

## Cross-Platform Configuration

### Windows to Unix Conversion

```bash
# macOS/Linux
sed -i 's/npx\.cmd/npx/g' .junie/mcp/mcp.json
```

### Unix to Windows Conversion

```powershell
# Windows PowerShell
(Get-Content .junie/mcp/mcp.json) -replace '"npx"', '"npx.cmd"' | Set-Content .junie/mcp/mcp.json
```

### Platform-Specific Files

Alternative approach with separate configs:

```
.junie/mcp/
├── mcp.json              # Active config (symlink or copy)
├── mcp.windows.json      # Windows template
└── mcp.unix.json         # macOS/Linux template
```

---

## Validation

### Schema Validation

Use JSON schema for validation:

```json
{
  "$schema": "./mcp.schema.json",
  "mcpServers": { }
}
```

### Manual Verification

1. Check JSON syntax is valid
2. Verify all required fields present
3. Test each server individually

---

## Related

- [Overview](overview.md) — MCP architecture
- [Servers Reference](servers.md) — Detailed server documentation
- [Memory Best Practices](memory.md) — Knowledge persistence
- [Troubleshooting](troubleshooting.md) — Problem solving

---

*Part of the Junie Documentation*
