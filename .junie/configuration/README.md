# Junie Configuration Guide

> Comprehensive guide for Junie AI Assistant configuration (v1.0.0, Production-Ready)

---

## Table of Contents

- [1. Documentation Structure](#1-documentation-structure)
- [2. Quick Navigation](#2-quick-navigation)
- [3. Key Metrics](#3-key-metrics)
- [4. Platform Quick Reference](#4-platform-quick-reference)
- [5. Version Compatibility](#5-version-compatibility)

---

## 1. Documentation Structure

This guide has been split into focused documents for easier navigation and maintenance:

| Document                                      | Description                                     | Time      |
|:----------------------------------------------|:------------------------------------------------|:----------|
| [📋 Introduction](01-introduction.md)         | Document overview, navigation, key metrics      | 5 min     |
| [📘 Action Allowlist](02-action-allowlist.md) | 87 Terminal rules for 90%+ auto-approval        | 30 min    |
| [🚀 MCP Integration](03-mcp-integration.md)   | 60-75% token efficiency improvement             | 1-2 hours |
| [🔮 Future Vision](04-future-vision.md)       | A2A multi-agent collaboration (2026+)           | 30-60 min |
| [📎 Appendix](05-appendix.md)                 | Regex reference, complete rules list, changelog | 15 min    |

---

## 2. Quick Navigation

**Choose your path based on your goal**:

| Your Goal                            | Go To                                                                                       | Time Required |
|:-------------------------------------|:--------------------------------------------------------------------------------------------|:--------------|
| 🚀 **Quick Setup** (first-time user) | [Quick Start](02-action-allowlist.md#quick-start)                                           | 10-30 min     |
| 🔧 **Add Terminal Rules**            | [Configuration Rules Explained](02-action-allowlist.md#configuration-rules-explained)       | 15 min        |
| 📋 **Copy All Rules**                | [Appendix B: Complete Rules List](05-appendix.md#appendix-b-complete-rules-list-plain-text) | 5 min         |
| 🔌 **Setup MCP Integration**         | [MCP Integration Guide](03-mcp-integration.md)                                              | 1-2 hours     |
| 🐛 **Fix Configuration Issues**      | [Troubleshooting](02-action-allowlist.md#troubleshooting)                                   | 10-20 min     |
| 🔮 **Learn Future Protocols**        | [Future Protocol Vision](04-future-vision.md)                                               | 30-60 min     |
| 📖 **Understand the Mechanism**      | [Action Allowlist Mechanism](02-action-allowlist.md#action-allowlist-mechanism)             | 15 min        |

---

## 3. Key Metrics

- 📊 **87 Total Rules** (57 cross-platform + 30 platform-specific)
- ⚡ **90%+ Auto-Approval Rate** after full configuration
- 🔒 **Zero Security Incidents** with dangerous character exclusion
- 💪 **5-10x Efficiency Improvement** in AI collaboration
- 🚀 **60-75% Token Efficiency** with MCP integration

---

## 4. Platform Quick Reference

| Platform           | Terminal Rules | Configuration File                                                             | Key Commands             |
|:-------------------|:---------------|:-------------------------------------------------------------------------------|:-------------------------|
| **Windows**        | 68 rules       | `%APPDATA%\JetBrains\<Product><Version>\options\junie.xml`                     | PowerShell cmdlets       |
| **macOS**          | 76 rules       | `~/Library/Application Support/JetBrains/<Product><Version>/options/junie.xml` | Bash/Zsh commands        |
| **Linux**          | 76 rules       | `~/.config/JetBrains/<Product><Version>/options/junie.xml`                     | Bash/Zsh commands        |
| **Cross-Platform** | 57 rules       | Same format                                                                    | Git, Python, Docker, npm |

> **Note**: Replace `<Product><Version>` with your IDE, e.g., `PyCharm2025.2`, `IntelliJIdea2025.2`

---

## 5. Version Compatibility

| Component             | Tested Versions                         | Notes                                  |
|:----------------------|:----------------------------------------|:---------------------------------------|
| **Junie Plugin**      | 2025.1+                                 | MCP support requires 2025.1 or later   |
| **JetBrains IDEs**    | 2024.3+, 2025.x                         | PyCharm, IntelliJ IDEA, WebStorm, etc. |
| **Node.js**           | v18+                                    | Required for MCP servers               |
| **Operating Systems** | Windows 10/11, macOS 12+, Ubuntu 20.04+ | Other Linux distros should work        |

> **💡 Tip**: Check your Junie version via `Settings | Plugins | Junie`. For MCP features, ensure you have the latest
> plugin version.

---

## Related

- `01-introduction.md` — Document overview and navigation
- `02-action-allowlist.md` — Terminal rules configuration
- `03-mcp-integration.md` — MCP setup and best practices
- `04-future-vision.md` — Protocol roadmap
- `05-appendix.md` — References and resources

---

*Part of the Junie Configuration Guide*
