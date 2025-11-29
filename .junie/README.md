# .junie Configuration

> JetBrains Junie AI collaboration configuration directory.

---

## File Structure

| File | Type | Purpose |
|------|------|---------|
| `README.md` | 🔄 Generic | This file - directory documentation |
| `guidelines.md` | 🔄 Generic | AI collaboration rules (reusable across projects) |
| `config.yaml` | 🔄 Generic | Junie settings and configuration |
| `quickref.md` | 🔄 Generic | Quick reference card template |
| `project.yaml` | 📌 Project | Project-specific variables definition |
| `project-guidelines.md` | 📌 Project | Project-specific guidelines and documentation |
| `mcp/mcp.json` | 🔄 Generic | MCP server configuration |

### Legend

- 🔄 **Generic**: Reusable across projects with minimal or no changes
- 📌 **Project**: Must be customized for each project

---

## Usage

### New Project Setup

1. **Copy generic files** to your project's `.junie/` directory:
   - `README.md`
   - `guidelines.md`
   - `config.yaml`
   - `quickref.md`
   - `mcp/mcp.json`

2. **Create project-specific files**:
   - `project.yaml` — Define your project variables
   - `project-guidelines.md` — Add project-specific documentation

3. **Customize** `project.yaml` with your project's:
   - Name and description
   - Tech stack
   - Directory structure
   - Commands
   - Key files

### Customization Guidelines

| File Type | When to Modify |
|-----------|----------------|
| 🔄 Generic | Only when changing AI collaboration patterns or adding new generic features |
| 📌 Project | Freely customize for your specific project needs |

---

## File Relationships

```
┌─────────────────────────────────────────────────────────┐
│                    .junie/ Directory                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────┐      ┌──────────────────┐         │
│  │  guidelines.md   │      │  project.yaml    │         │
│  │  (Generic Rules) │◄────►│  (Variables)     │         │
│  └──────────────────┘      └──────────────────┘         │
│           │                         │                    │
│           │                         ▼                    │
│           │                ┌──────────────────┐         │
│           │                │ project-         │         │
│           │                │ guidelines.md    │         │
│           │                │ (Project Docs)   │         │
│           │                └──────────────────┘         │
│           ▼                                              │
│  ┌──────────────────┐      ┌──────────────────┐         │
│  │  config.yaml     │      │  quickref.md     │         │
│  │  (Settings)      │      │  (Quick Lookup)  │         │
│  └──────────────────┘      └──────────────────┘         │
│                                                          │
│  ┌──────────────────┐                                   │
│  │  mcp/mcp.json    │                                   │
│  │  (MCP Servers)   │                                   │
│  └──────────────────┘                                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Version Information

- **Schema Version**: 1.0
- **Compatibility**: JetBrains Junie v2024.3+, MCP v1.0+

---

*Part of the Junie Configuration Template System*
