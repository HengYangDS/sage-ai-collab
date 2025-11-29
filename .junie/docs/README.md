# Junie Documentation

> Comprehensive documentation for JetBrains Junie AI Assistant configuration

---

## Overview

This documentation covers everything you need to configure and optimize Junie AI Assistant for maximum productivity:

- **Action Allowlist**: Configure 87 Terminal rules for 90%+ automatic command approval
- **MCP Integration**: Achieve 60-75% token efficiency with intelligent context management
- **Operations**: Maintenance, migration, metrics, and error recovery
- **Future Vision**: Prepare for A2A multi-agent collaboration (2026+)

### Quality Principles — 信达雅 (Xin-Da-Ya)

| Principle        | Description           | Application                             |
|:-----------------|:----------------------|:----------------------------------------|
| **Faithfulness** | Technical correctness | All configurations tested and verified  |
| **Clarity**      | Easy understanding    | Step-by-step instructions with examples |
| **Elegance**     | Professional quality  | Clean formatting, consistent style      |

---

## Documentation Structure

```
docs/
├── README.md                 # This file - main index
├── guides/                   # 📘 User Guides
│   ├── quick-start.md        # First-time setup (~10 min)
│   └── action-allowlist.md   # Terminal rules configuration (~30 min)
├── mcp/                      # 🔌 MCP Integration
│   ├── overview.md           # Architecture and concepts (~15 min)
│   ├── configuration.md      # Setup and configuration (~30 min)
│   ├── servers.md            # Server reference (~20 min)
│   ├── memory.md             # Memory best practices (~15 min)
│   └── troubleshooting.md    # Problem solving (~10 min)
├── operations/               # 🔧 Operations Guide
│   ├── maintenance.md        # Daily operations (~10 min)
│   ├── migration.md          # Version migration (~10 min)
│   ├── metrics.md            # Efficiency tracking (~10 min)
│   └── recovery.md           # Error recovery (~10 min)
├── reference/                # 📚 Reference Materials
│   ├── glossary.md           # Terminology (~5 min)
│   ├── regex.md              # Regex patterns (~10 min)
│   ├── rules-windows.md      # Windows rules (copy-paste)
│   └── rules-unix.md         # macOS/Linux rules (copy-paste)
└── vision/                   # 🔮 Future Vision
    └── future-protocols.md   # Protocol roadmap (~30 min)
```

---

## Quick Navigation

### By Goal

| Your Goal                       | Go To                                                                   | Time      |
|:--------------------------------|:------------------------------------------------------------------------|:----------|
| 🚀 **First-time setup**         | [Quick Start](guides/quick-start.md)                                    | 10 min    |
| 📘 **Configure Terminal rules** | [Action Allowlist](guides/action-allowlist.md)                          | 30 min    |
| 🔌 **Setup MCP servers**        | [MCP Configuration](mcp/configuration.md)                               | 30 min    |
| 📋 **Copy all rules**           | [Windows](reference/rules-windows.md) / [Unix](reference/rules-unix.md) | 5 min     |
| 🐛 **Fix issues**               | [MCP Troubleshooting](mcp/troubleshooting.md)                           | 10-20 min |
| 🔮 **Learn future protocols**   | [Future Protocols](vision/future-protocols.md)                          | 30 min    |

### By Role

| Role              | Recommended Path                              |
|:------------------|:----------------------------------------------|
| **New User**      | Quick Start → Action Allowlist → MCP Overview |
| **Administrator** | Operations (all) → Migration → Metrics        |
| **Advanced User** | MCP Configuration → Memory → Future Protocols |

---

## Key Metrics

| Metric                 | Target    | Description                           |
|:-----------------------|:----------|:--------------------------------------|
| **Terminal Rules**     | 87 rules  | Cross-platform command automation     |
| **Auto-Approval Rate** | 90%+      | Commands auto-approved after setup    |
| **Token Efficiency**   | 60-75%    | Improvement with MCP integration      |
| **Security**           | Zero risk | Dangerous character exclusion pattern |

---

## Platform Reference

| Platform           | Terminal Rules | Key Commands             |
|:-------------------|:---------------|:-------------------------|
| **Windows**        | 68 rules       | PowerShell cmdlets       |
| **macOS**          | 76 rules       | Bash/Zsh commands        |
| **Linux**          | 76 rules       | Bash/Zsh commands        |
| **Cross-Platform** | 57 rules       | Git, Python, Docker, npm |

---

## Version Compatibility

| Component             | Tested Versions                     | Notes                            |
|:----------------------|:------------------------------------|:---------------------------------|
| **Junie Plugin**      | 2025.1+                             | MCP support requires 2025.1+     |
| **JetBrains IDEs**    | 2024.3+, 2025.x                     | PyCharm, IntelliJ IDEA, WebStorm |
| **Node.js**           | v18+                                | Required for MCP servers         |
| **Operating Systems** | Win 10/11, macOS 12+, Ubuntu 20.04+ |                                  |

---

## Related Files

- `../guidelines.md` — AI collaboration rules (main entry point)
- `../generic/config.yaml` — Generic Junie settings
- `../project/config.yaml` — Project-specific settings
- `../mcp/mcp.json` — MCP server configuration

---

*Part of the Junie Configuration Template System*
