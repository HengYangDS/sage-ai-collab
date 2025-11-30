---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---

# Quick Start Guide

> Get up and running with SAGE Knowledge Base in 5 minutes

---

## Table of Contents

- [1. Installation](#1-installation)
- [2. CLI Basics](#2-cli-basics)
- [3. MCP Setup](#3-mcp-setup)
- [4. Python Basics](#4-python-basics)
- [5. Next Steps](#5-next-steps)

---

## 1. Installation

### 1.1 Requirements

- Python 3.12 or higher
- Miniconda (recommended) or venv

### 1.2 Setup Environment (Recommended)

```bash
# Create conda environment (recommended)
conda create -n sage-kb python=3.12
conda activate sage-kb

# Or use venv as alternative:
# python -m venv .venv
# source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate     # Windows
```

### 1.3 Install from PyPI

```bash
# Basic installation
pip install sage-kb

# With MCP support
pip install sage-kb[mcp]

# With all optional features
pip install sage-kb[all]
```

### 1.4 Install from Source

```bash
# Clone the repository
git clone https://github.com/HengYangDS/sage-kb.git
cd sage-kb

# Setup conda environment
conda env create -f environment.yml
conda activate sage-kb

# Install in development mode
pip install -e ".[dev]"
```

### 1.5 Verify Installation

```bash
# Check version
sage --version

# View help
sage --help
```

---

## 2. CLI Basics

### 2.1 Get Knowledge

Retrieve knowledge from a specific layer:

```bash
# Get core principles
sage get --layer core

# Get specific topic
sage get --topic timeout

# Get with filtering
sage get --layer practices --format json
```

### 2.2 Search Knowledge

Search across the knowledge base:

```bash
# Simple search
sage search "error handling"

# Search in specific layer
sage search "timeout" --layer core

# Limit results
sage search "pattern" --limit 5
```

### 2.3 View Information

Display system information:

```bash
# Show knowledge base info
sage info

# Show layer statistics
sage info --layers

# Show configuration
sage info --config
```

### 2.4 Common Options

| Option      | Short | Description                    |
|-------------|-------|--------------------------------|
| `--help`    | `-h`  | Show help message              |
| `--version` | `-v`  | Show version                   |
| `--verbose` |       | Enable verbose output          |
| `--format`  | `-f`  | Output format (text/json/yaml) |
| `--layer`   | `-l`  | Filter by layer                |

---

## 3. MCP Setup

### 3.1 What is MCP?

MCP (Model Context Protocol) enables AI agents to access SAGE knowledge directly. This allows AI assistants to retrieve
relevant context during conversations.

### 3.2 Start MCP Server

```bash
# Start with default settings
sage serve

# Start on custom port
sage serve --port 8080

# Start with verbose logging
sage serve --verbose
```

### 3.3 Configure AI Client

Add SAGE to your AI client's MCP configuration:

```json
{
  "mcpServers": {
    "sage": {
      "command": "sage",
      "args": [
        "serve"
      ],
      "env": {}
    }
  }
}
```

### 3.4 Test Connection

Once configured, your AI assistant can use SAGE tools:

- `sage_get` — Retrieve knowledge by layer/topic
- `sage_search` — Search knowledge base
- `sage_info` — Get system information

---

## 4. Python Basics

### 4.1 Import SAGE

```python
from sage import get_knowledge, search_knowledge
from sage.core.config import get_config
```

### 4.2 Get Knowledge

```python
# Get core knowledge
knowledge = get_knowledge(layer="core")
print(knowledge.content)

# Get specific topic
timeout_info = get_knowledge(topic="timeout")
```

### 4.3 Search Knowledge

```python
# Search for content
results = search_knowledge("error handling")

for result in results:
    print(f"{result.path}: {result.title}")
```

### 4.4 Async Usage

```python
import asyncio
from sage import async_get_knowledge


async def main():
    knowledge = await async_get_knowledge(layer="core")
    print(knowledge.content)


asyncio.run(main())
```

---

## 5. Next Steps

### 5.1 Explore Knowledge Layers

SAGE organizes knowledge into four layers:

| Layer          | Content                             | Priority |
|----------------|-------------------------------------|----------|
| **Core**       | Fundamental principles and concepts | Highest  |
| **Guidelines** | Standards and conventions           | High     |
| **Frameworks** | Reusable patterns and structures    | Medium   |
| **Practices**  | Specific implementation guidance    | Normal   |

### 5.2 Customize Configuration

Edit `config/sage.yaml` to customize:

- Timeout settings
- Loading strategies
- Enabled features

### 5.3 Add Custom Content

Place your own knowledge files in:

- `.knowledge/` — Generic, reusable knowledge
- `.context/` — Project-specific knowledge

### 5.4 Learn More

- [Advanced Usage Guide](ADVANCED.md) — Deep dive into features
- [API Reference](../api/INDEX.md) — Complete API documentation
- [Design Documents](../design/00-OVERVIEW.md) — Architecture details

---

## Troubleshooting

### Common Issues

| Issue                 | Solution                                         |
|-----------------------|--------------------------------------------------|
| Command not found     | Ensure SAGE is in PATH: `pip show sage-kb`       |
| Import error          | Check Python version: `python --version`         |
| MCP connection failed | Verify server is running: `sage serve --verbose` |
| Slow loading          | Check timeout settings in `config/sage.yaml`     |

### Get Help

```bash
# CLI help
sage --help
sage get --help

# Report issues
# https://github.com/HengYangDS/sage-kb/issues
```

---

## Related

- [Advanced Usage](ADVANCED.md) — Configuration and customization
- [CLI Reference](../api/CLI.md) — Complete CLI documentation
- [Python API](../api/PYTHON.md) — Python API reference

---

*SAGE Knowledge Base - Quick Start Guide*
