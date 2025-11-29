# CLI Reference

> SAGE Command-Line Interface Documentation

---

## Overview

The SAGE CLI provides interactive access to the knowledge base via terminal. Built with Typer and Rich for a modern CLI experience.

```bash
sage [OPTIONS] COMMAND [ARGS]
```

---

## Commands

### sage get

Load knowledge by layer or topic.

```bash
sage get [LAYER] [OPTIONS]
```

**Arguments:**

| Argument | Description | Default |
|----------|-------------|---------|
| `LAYER` | Knowledge layer to load | `core` |

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--timeout`, `-t` | Timeout in milliseconds | `2000` |
| `--format`, `-f` | Output format (rich/plain/json) | `rich` |
| `--no-cache` | Bypass cache | `false` |

**Examples:**

```bash
# Load core knowledge
sage get core

# Load guidelines with custom timeout
sage get guidelines --timeout 5000

# Load frameworks as JSON
sage get frameworks --format json
```

**Layers:**

| Layer | Description |
|-------|-------------|
| `core` | Core principles and defaults |
| `guidelines` | Coding and collaboration guidelines |
| `frameworks` | Conceptual frameworks |
| `practices` | Best practices and patterns |
| `all` | All layers (uses T4 timeout) |

---

### sage search

Search the knowledge base.

```bash
sage search QUERY [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `QUERY` | Search query string |

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--limit`, `-l` | Maximum results | `10` |
| `--layer` | Limit to specific layer | `all` |
| `--timeout`, `-t` | Timeout in milliseconds | `2000` |

**Examples:**

```bash
# Basic search
sage search "timeout"

# Search with limit
sage search "autonomy" --limit 5

# Search specific layer
sage search "pattern" --layer frameworks
```

---

### sage serve

Start the MCP server.

```bash
sage serve [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--host`, `-h` | Server host | `localhost` |
| `--port`, `-p` | Server port | `8000` |
| `--reload` | Enable auto-reload | `false` |

**Examples:**

```bash
# Start with defaults
sage serve

# Custom host and port
sage serve --host 0.0.0.0 --port 9000

# Development mode with reload
sage serve --reload
```

---

### sage info

Display system information.

```bash
sage info [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--json` | Output as JSON | `false` |

**Output includes:**

- Version information
- Configuration status
- Knowledge base statistics
- Cache status
- Plugin status

**Examples:**

```bash
# Rich formatted output
sage info

# JSON output for scripting
sage info --json
```

---

### sage config

Manage configuration.

```bash
sage config [SUBCOMMAND] [OPTIONS]
```

**Subcommands:**

| Command | Description |
|---------|-------------|
| `show` | Display current configuration |
| `get KEY` | Get specific config value |
| `set KEY VALUE` | Set config value |
| `reset` | Reset to defaults |

**Examples:**

```bash
# Show all config
sage config show

# Get specific value
sage config get timeout.t3

# Set value
sage config set mcp.port 9000
```

---

## Global Options

These options are available for all commands:

| Option | Description | Default |
|--------|-------------|---------|
| `--help` | Show help message | - |
| `--version` | Show version | - |
| `--verbose`, `-v` | Verbose output | `false` |
| `--quiet`, `-q` | Minimal output | `false` |
| `--config`, `-c` | Config file path | `config/sage.yaml` |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | General error |
| `2` | Invalid arguments |
| `3` | Timeout exceeded |
| `4` | Configuration error |

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SAGE_CONFIG` | Config file path | `config/sage.yaml` |
| `SAGE_LOG_LEVEL` | Logging level | `INFO` |
| `SAGE_CACHE_DIR` | Cache directory | `.cache/` |
| `SAGE_NO_COLOR` | Disable colors | `false` |

---

## Configuration

CLI behavior can be configured in `config/services/cli.yaml`:

```yaml
cli:
  default_format: rich
  default_timeout: 2000
  pager: true
  colors: true
```

---

## Related

- [API Index](index.md) — API overview
- [MCP Protocol](mcp.md) — MCP server documentation
- `config/services/cli.yaml` — CLI configuration

---

*SAGE Knowledge Base - CLI Reference*
