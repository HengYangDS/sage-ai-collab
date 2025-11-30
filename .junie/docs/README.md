---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---

# Junie Documentation

> Comprehensive documentation for JetBrains Junie AI Assistant configuration

---

## Table of Contents

1. [Overview](#1-overview)
2. [Documentation Structure](#2-documentation-structure)
3. [File Length Policy](#3-file-length-policy)
4. [Quick Navigation](#4-quick-navigation)
5. [Key Metrics](#5-key-metrics)
6. [Platform Reference](#6-platform-reference)
7. [Version Compatibility](#7-version-compatibility)
8. [Related](#8-related)

---

## 1. Overview

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

## 2. Documentation Structure

```
docs/
├── README.md                 # This file - main index
├── guides/                   # 📘 User Guides
│   ├── QUICK-START.md        # First-time setup (~10 min)
│   └── ACTION-ALLOWLIST.md   # Terminal rules configuration (~30 min)
├── mcp/                      # 🔌 MCP Integration
│   ├── OVERVIEW.md           # Architecture and concepts (~15 min)
│   ├── CONFIGURATION.md      # Setup and configuration (~30 min)
│   ├── SERVERS.md            # Server reference (~20 min)
│   ├── MEMORY.md             # Memory best practices (~15 min)
│   └── TROUBLESHOOTING.md    # Problem solving (~10 min)
├── operations/               # 🔧 Operations Guide
│   ├── MAINTENANCE.md        # Daily operations (~10 min)
│   ├── MIGRATION.md          # Version migration (~10 min)
│   ├── METRICS.md            # Efficiency tracking (~10 min)
│   └── RECOVERY.md           # Error recovery (~10 min)
├── reference/                # 📚 Reference Materials
│   ├── GLOSSARY.md           # Terminology (~5 min)
│   ├── REGEX.md              # Regex patterns (~10 min)
│   ├── RULES-WINDOWS.md      # Windows rules (copy-paste)
│   └── RULES-UNIX.md         # macOS/Linux rules (copy-paste)
└── vision/                   # 🔮 Future Vision
    └── FUTURE-PROTOCOLS.md   # Protocol roadmap (~30 min)
```

---

## 3. File Length Policy

Some documentation files exceed the recommended 300-line limit. This is an **intentional design decision**.

### Policy Rationale

| Principle              | Explanation                                                   |
|:-----------------------|:--------------------------------------------------------------|
| **Content Integrity**  | Splitting would break logical flow and cross-references       |
| **Single Source**      | Each file is the authoritative source for its topic           |
| **Reduced Navigation** | Users find complete information without jumping between files |
| **Search Efficiency**  | Full-text search works better with consolidated content       |

### Files Exceeding 300 Lines

| File                         | Lines | Justification                                       |
|:-----------------------------|:------|:----------------------------------------------------|
| `mcp/CONFIGURATION.md`       | ~527  | Complete server setup requires all details together |
| `mcp/SERVERS.md`             | ~451  | All server docs in one reference                    |
| `mcp/TROUBLESHOOTING.md`     | ~437  | Comprehensive problem-solving guide                 |
| `mcp/MEMORY.md`              | ~386  | Complete memory patterns and examples               |
| `operations/RECOVERY.md`     | ~398  | All recovery procedures in one place                |
| `guides/ACTION-ALLOWLIST.md` | ~325  | Complete rule configuration guide                   |

### When to Split vs. Keep Together

| Keep Together When                   | Split When                        |
|:-------------------------------------|:----------------------------------|
| Content has strong interdependencies | Sections are independently useful |
| Users need complete context          | File exceeds 800 lines            |
| Topic is single logical unit         | Distinct audiences for sections   |
| Cross-references would be excessive  | Natural chapter boundaries exist  |

---

## 4. Quick Navigation

### By Goal

| Your Goal                       | Go To                                                                   | Time      |
|:--------------------------------|:------------------------------------------------------------------------|:----------|
| 🚀 **First-time setup**         | [Quick Start](guides/QUICK-START.md)                                    | 10 min    |
| 📘 **Configure Terminal rules** | [Action Allowlist](guides/ACTION-ALLOWLIST.md)                          | 30 min    |
| 🔌 **Setup MCP servers**        | [MCP Configuration](mcp/CONFIGURATION.md)                               | 30 min    |
| 📋 **Copy all rules**           | [Windows](reference/RULES-WINDOWS.md) / [Unix](reference/RULES-UNIX.md) | 5 min     |
| 🐛 **Fix issues**               | [MCP Troubleshooting](mcp/TROUBLESHOOTING.md)                           | 10-20 min |
| 🔮 **Learn future protocols**   | [Future Protocols](vision/FUTURE-PROTOCOLS.md)                          | 30 min    |

### By Role

| Role              | Recommended Path                              |
|:------------------|:----------------------------------------------|
| **New User**      | Quick Start → Action Allowlist → MCP Overview |
| **Administrator** | Operations (all) → Migration → Metrics        |
| **Advanced User** | MCP Configuration → Memory → Future Protocols |

---

## 5. Key Metrics

| Metric                 | Target    | Description                           |
|:-----------------------|:----------|:--------------------------------------|
| **Terminal Rules**     | 87 rules  | Cross-platform command automation     |
| **Auto-Approval Rate** | 90%+      | Commands auto-approved after setup    |
| **Token Efficiency**   | 60-75%    | Improvement with MCP integration      |
| **Security**           | Zero risk | Dangerous character exclusion pattern |

---

## 6. Platform Reference

| Platform           | Terminal Rules | Key Commands             |
|:-------------------|:---------------|:-------------------------|
| **Windows**        | 68 rules       | PowerShell cmdlets       |
| **macOS**          | 76 rules       | Bash/Zsh commands        |
| **Linux**          | 76 rules       | Bash/Zsh commands        |
| **Cross-Platform** | 57 rules       | Git, Python, Docker, npm |

---

## 7. Version Compatibility

| Component             | Tested Versions                     | Notes                                |
|:----------------------|:------------------------------------|:-------------------------------------|
| **Junie Plugin**      | 2024.3+                             | Basic features; MCP requires 2025.1+ |
| **JetBrains IDEs**    | 2024.3+, 2025.x                     | PyCharm, IntelliJ IDEA, WebStorm     |
| **Node.js**           | v18+                                | Required for MCP servers             |
| **Operating Systems** | Win 10/11, macOS 12+, Ubuntu 20.04+ |                                      |

---

## 8. Related

- `../GUIDELINES.md` — AI collaboration rules (main entry point)
- `../generic/config.yaml` — Generic Junie settings
- `../project/config.yaml` — Project-specific settings
- `../mcp/mcp.json` — MCP server configuration

---

*Part of the Junie Configuration Template System*
