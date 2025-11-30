---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---

# Frequently Asked Questions

> Common questions and answers about SAGE Knowledge Base

---

## Table of Contents

- [General](#general)
- [Installation](#installation)
- [CLI Usage](#cli-usage)
- [MCP Integration](#mcp-integration)
- [Configuration](#configuration)
- [Performance](#performance)
- [Development](#development)

---

## General

### What is SAGE?

SAGE (Smart AI-Guided Expertise) is a knowledge management system designed for AI-human collaboration. It provides
structured knowledge through CLI, MCP server, and Python API.

### What does SAGE stand for?

SAGE represents the protocol flow:

- **S**ource — Knowledge sourcing and loading
- **A**nalyze — Processing and analysis
- **G**enerate — Multi-channel output
- **E**volve — Metrics and optimization

### Who should use SAGE?

- AI assistants needing structured knowledge
- Developers wanting organized documentation
- Teams building AI-enhanced workflows
- Projects requiring knowledge management

---

## Installation

### What Python version is required?

Python 3.12 or higher is required.

### How do I install SAGE?

```bash
# Basic installation
pip install sage-kb

# With MCP support
pip install sage-kb[mcp]

# Development installation
pip install -e ".[dev]"
```

### Why can't I find the `sage` command?

Ensure the installation directory is in your PATH:

```bash
# Check where pip installs scripts
pip show sage-kb | grep Location

# Add to PATH if needed
export PATH="$PATH:$(python -m site --user-base)/bin"
```

---

## CLI Usage

### How do I get knowledge?

```bash
# Get core principles
sage get core

# Get specific layer
sage get --layer guidelines

# Search knowledge
sage search "timeout"
```

### What layers are available?

| Layer        | Content                      |
|--------------|------------------------------|
| `core`       | Core principles and defaults |
| `guidelines` | Practical guidelines         |
| `frameworks` | Conceptual frameworks        |
| `practices`  | Implementation practices     |

### How do I see system info?

```bash
sage info
sage info --verbose
```

---

## MCP Integration

### How do I start the MCP server?

```bash
# Start with stdio (for AI clients)
sage serve

# Start with specific transport
sage serve --transport sse --port 3000
```

### How do I configure Claude Desktop?

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sage": {
      "command": "sage",
      "args": [
        "serve"
      ]
    }
  }
}
```

### What MCP tools are available?

| Tool               | Description                 |
|--------------------|-----------------------------|
| `get_knowledge`    | Retrieve knowledge by layer |
| `search_knowledge` | Search knowledge base       |
| `kb_info`          | Get system information      |
| `get_framework`    | Get specific framework      |

### Why isn't my AI client seeing SAGE tools?

1. Verify server is running: `sage serve --verbose`
2. Check client configuration
3. Restart the AI client
4. Check logs for errors

---

## Configuration

### Where is the configuration file?

Main configuration is at `config/sage.yaml`. Environment-specific overrides can use environment variables.

### How do I override configuration?

```bash
# Environment variables
export SAGE_TIMEOUT_CACHE_LOOKUP=200ms
export SAGE_LOGGING_LEVEL=DEBUG

# Custom config file
sage --config custom.yaml get core
```

### What are the timeout levels?

| Level | Timeout | Scope            |
|-------|---------|------------------|
| T1    | 100ms   | Cache lookup     |
| T2    | 500ms   | Single file      |
| T3    | 2s      | Layer load       |
| T4    | 5s      | Full KB load     |
| T5    | 10s     | Complex analysis |

---

## Performance

### Why is SAGE slow to start?

Try these optimizations:

1. Enable lazy loading in config
2. Reduce preloaded layers
3. Check disk I/O performance
4. Profile with `sage --profile info`

### How do I improve response times?

1. Use appropriate timeout levels
2. Enable caching
3. Limit result sizes with `--max-results`
4. Use layer-specific queries instead of full search

### What is the recommended token budget?

Default is 4000 tokens. Adjust based on your use case:

```yaml
token_budget:
  default: 4000
  layers:
    core: 500
    guidelines: 1000
```

---

## Development

### How do I run tests?

```bash
# All tests
pytest tests/

# With coverage
pytest tests/ --cov=sage

# Specific category
pytest tests/unit/
```

### How do I create a plugin?

See the [Plugin Development Guide](plugin_development.md) for detailed instructions.

Quick start:

```python
from sage.plugins import PluginBase, hookimpl


class MyPlugin(PluginBase):
    name = "my-plugin"

    @hookimpl
    def register_tools(self, registry):
        registry.add_tool(self.my_tool)
```

### How do I contribute?

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run `pytest` and `ruff check`
5. Submit a pull request

### Where do I report bugs?

Open an issue on GitHub:
https://github.com/HengYangDS/sage-kb/issues

---

## Troubleshooting

### Common Issues

| Issue              | Solution                      |
|--------------------|-------------------------------|
| Command not found  | Check PATH, reinstall         |
| Import error       | Install with all dependencies |
| Timeout errors     | Increase timeout in config    |
| MCP not connecting | Check server, restart client  |

### Getting Help

1. Check [Troubleshooting Guide](troubleshooting.md)
2. Search existing issues
3. Ask in discussions
4. Open a new issue with details

### Debug Mode

```bash
# Enable maximum logging
sage --debug get core

# With timing information
sage --debug --timing get core
```

---

## Related

- [Quick Start](quickstart.md) — Getting started
- [Advanced Usage](advanced.md) — Advanced features
- [Troubleshooting](troubleshooting.md) — Problem solving
- [Plugin Development](plugin_development.md) — Creating plugins

---

*SAGE Knowledge Base - FAQ*
