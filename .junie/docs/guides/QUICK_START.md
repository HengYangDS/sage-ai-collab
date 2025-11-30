
# Quick Start Guide

> Get Junie configured in 10 minutes for maximum productivity

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Verify Junie Installation](#2-verify-junie-installation)
3. [Configure Terminal Rules](#3-configure-terminal-rules)
4. [Enable Allowed Actions](#4-enable-allowed-actions)
5. [Setup MCP Servers](#5-setup-mcp-servers-optional)
6. [Verify Setup](#6-verify-setup)
7. [Troubleshooting](#7-troubleshooting)
8. [Next Steps](#8-next-steps)
9. [Related](#9-related)

---

## 1. Prerequisites

Before starting, ensure you have:

- JetBrains IDE (2024.3+) with Junie plugin (2025.1+)
- Node.js v18+ (for MCP servers)
- Basic familiarity with your IDE's settings

---

## 2. Verify Junie Installation

1. Open your JetBrains IDE
2. Go to `Settings | Plugins`
3. Search for "Junie" and verify it's installed and enabled
4. Check version is 2025.1 or later (required for MCP support)

---

## 3. Configure Terminal Rules

Terminal rules allow Junie to execute common commands without manual approval.

### Method A: Auto-Configuration (Recommended)

If your project includes `.junie/` configuration:

1. **Restart IDE** after opening the project
2. **Verify Configuration**:
    - Open `Settings | Tools | Junie | Action Allowlist`
    - Confirm you see Terminal rules listed

3. **Test Execution**:
   ```bash
   git status  # Should execute without approval prompt
   ```

### Method B: Manual Configuration

1. Open `Settings | Tools | Junie | Action Allowlist`
2. Click "Add" to add Terminal rules
3. Copy rules from:
    - [Windows Rules](../reference/RULES_WINDOWS.md)
    - [macOS/Linux Rules](../reference/RULES_UNIX.md)

### Method C: Quick Copy-Paste

For immediate setup, copy the essential rules:

**Cross-Platform Essentials (works everywhere)**:

```
# Git commands
^\Qgit status\E$
^\Qgit diff\E.*$
^\Qgit log\E.*$
^\Qgit branch\E.*$
^\Qgit add\E [^\s;&|<>@$]*$
^\Qgit commit\E [^\s;&|<>@$]*$
^\Qgit push\E [^\s;&|<>@$]*$
^\Qgit pull\E [^\s;&|<>@$]*$

# Python commands
^\Qpython\E [^\s;&|<>@$]*$
^\Qpython -m pytest\E.*$
^\Qpip install\E [^\s;&|<>@$]*$
^\Qpip list\E$

# Node.js commands
^\Qnpm\E [^\s;&|<>@$]*$
^\Qnpx\E [^\s;&|<>@$]*$
```

---

## 4. Enable Allowed Actions

In `Settings | Tools | Junie | Action Allowlist`, enable:

| Action                  | Recommended | Purpose                 |
|:------------------------|:------------|:------------------------|
| **RunTest**             | ✅ Enable    | Run tests automatically |
| **Build**               | ✅ Enable    | Build project           |
| **ReadOutsideProject**  | ✅ Enable    | Read external files     |
| **WriteOutsideProject** | ⚠️ Optional | Modify external files   |

---

## 5. Setup MCP Servers (Optional)

MCP servers provide advanced capabilities like persistent memory and external tool access.

### Quick MCP Setup

1. Ensure `.junie/mcp/mcp.json` exists in your project
2. Go to `Settings | Tools | Junie | MCP Servers`
3. Click "Reload" to load server configurations
4. Verify servers show as "Connected"

### Essential MCP Servers

| Server         | Priority | Purpose                        |
|:---------------|:---------|:-------------------------------|
| **filesystem** | P0       | File operations within project |
| **memory**     | P0       | Cross-session knowledge        |
| **fetch**      | P1       | External URL access            |

For detailed MCP configuration, see [MCP Configuration](../mcp/configuration.md).

---

## 6. Verify Setup

### Test Terminal Rules

Run these commands — they should execute without approval:

```bash
git status
python --version
npm --version
```

### Test MCP Connection

In Junie chat, try:

- "Read the README.md file" (tests filesystem server)
- "Remember that we use pytest for testing" (tests memory server)

---

## 7. Troubleshooting

### Commands Still Require Approval

1. Check rule syntax in `Settings | Tools | Junie | Action Allowlist`
2. Verify regex patterns match your commands
3. See [Action Allowlist Guide](ACTION_ALLOWLIST.md) for detailed patterns

### MCP Servers Not Connecting

1. Verify Node.js is installed: `node --version`
2. Check server logs in IDE's MCP panel
3. See [MCP Troubleshooting](../mcp/troubleshooting.md)

---

## 8. Next Steps

| Goal                        | Document                                          |
|:----------------------------|:--------------------------------------------------|
| Configure all 87 rules      | [Action Allowlist](ACTION_ALLOWLIST.md)           |
| Setup advanced MCP features | [MCP Overview](../mcp/OVERVIEW.md)                |
| Track efficiency metrics    | [Metrics](../operations/METRICS.md)               |
| Learn about future features | [Future Protocols](../vision/FUTURE_PROTOCOLS.md) |

---

## 9. Related

- [Action Allowlist](ACTION_ALLOWLIST.md) — Complete Terminal rules guide
- [MCP Configuration](../mcp/CONFIGURATION.md) — MCP server setup
- [Glossary](../reference/GLOSSARY.md) — Terminology reference

---

*AI Collaboration Knowledge Base*
