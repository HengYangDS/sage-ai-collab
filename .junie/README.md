# .junie Configuration

> JetBrains Junie AI collaboration configuration directory

---

## Table of Contents

- [1. Directory Structure](#1-directory-structure)
- [2. Usage](#2-usage)
- [3. Customization Guidelines](#3-customization-guidelines)
- [4. Version Information](#4-version-information)

---

## 1. Directory Structure

```text
.junie/
├── guidelines.md           # 🔄 Main entry point (generic AI rules)
├── README.md               # 🔄 This file - directory documentation
│
├── generic/                # 🔄 Generic settings (reusable)
│   ├── config.yaml         # Junie settings
│   └── QUICKREF.md         # Quick reference card
│
├── mcp/                    # 🔄 MCP server configuration
│   └── mcp.json            # MCP servers definition
│
├── schema/                 # 🔄 JSON Schema validation
│   ├── config.schema.json  # Config file schema
│   └── mcp.schema.json     # MCP config schema
│
├── docs/                   # 🔄 Junie documentation
│   ├── README.md           # Documentation index
│   ├── guides/             # User guides
│   │   ├── QUICK_START.md
│   │   └── ACTION_ALLOWLIST.md
│   ├── mcp/                # MCP integration
│   │   ├── OVERVIEW.md
│   │   ├── CONFIGURATION.md
│   │   ├── SERVERS.md
│   │   ├── MEMORY.md
│   │   └── TROUBLESHOOTING.md
│   ├── operations/         # Operations guides
│   │   ├── MAINTENANCE.md
│   │   ├── MIGRATION.md
│   │   ├── METRICS.md
│   │   └── RECOVERY.md
│   ├── reference/          # Reference materials
│   │   ├── GLOSSARY.md
│   │   ├── REGEX.md
│   │   ├── RULES_WINDOWS.md
│   │   └── RULES_UNIX.md
│   └── vision/             # Future vision
│       └── FUTURE_PROTOCOLS.md
│
└── project/                # 📌 Project-specific files (must customize)
    ├── config.yaml         # Project variables definition
    └── QUICKREF.md         # Project-specific quick reference
```

### Legend

- 🔄 **Generic**: Reusable across projects with minimal or no changes
- 📌 **Project**: Must be customized for each project

---

## 2. Usage

### New Project Setup

1. **Copy the entire `.junie/` directory** to your project

2. **Keep generic files unchanged**:
    - `guidelines.md` (root)
    - `generic/` directory
    - `mcp/` directory
    - `docs/` directory

3. **Customize project-specific files**:
    - `project/config.yaml` — Define your project variables
    - `project/GUIDELINES.md` — Add project-specific guidelines

### File Relationships

```text
┌─────────────────────────────────────────────────────────────┐
│                     .junie/ Directory                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐                                       │
│  │  guidelines.md   │  ◄── Main entry point                 │
│  │  (Generic Rules) │                                       │
│  └────────┬─────────┘                                       │
│           │                                                 │
│           ▼                                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         Generic Directories (Reusable)              │    │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────┐   │    │
│  │  │ generic/   │  │ mcp/       │  │ docs/        │   │    │
│  │  │ (Settings) │  │ (MCP)      │  │ (Docs)       │   │    │
│  │  └────────────┘  └────────────┘  └──────────────┘   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              project/ (Customize)                   │    │
│  │  ┌────────────────┐  ┌────────────────┐             │    │
│  │  │ config.yaml    │  │ QUICKREF.md    │             │    │
│  │  │ (Variables)    │  │ (Project Ref)  │             │    │
│  │  └────────────────┘  └────────────────┘             │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Customization Guidelines

| Directory/File         | When to Modify                                       |
|------------------------|------------------------------------------------------|
| `guidelines.md` (root) | Only when changing generic AI collaboration patterns |
| `generic/*`            | Only when adding new generic features                |
| `mcp/*`                | Only when changing MCP server configuration          |
| `docs/*`               | Only when updating documentation                     |
| `project/*`            | Freely customize for your specific project           |

---

## 4. Version Information

- **Schema Version**: 1.0
- **Compatibility**: JetBrains Junie v2024.3+, MCP v1.0+

---

*AI Collaboration Knowledge Base*
