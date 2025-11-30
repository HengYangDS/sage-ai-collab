
# Troubleshooting Guide

> Common issues and solutions for SAGE Knowledge Base

---

## Table of Contents

- [1. Quick Diagnostics](#1-quick-diagnostics)
- [2. Installation Issues](#2-installation-issues)
- [3. CLI Issues](#3-cli-issues)
- [4. MCP Server Issues](#4-mcp-server-issues)
- [5. Configuration Issues](#5-configuration-issues)
- [6. Performance Issues](#6-performance-issues)
- [7. Getting Help](#7-getting-help)

---

## 1. Quick Diagnostics

### 1.1 Health Check Commands

```bash
sage info                              # Check installation
sage config --validate                 # Verify configuration
sage get --layer core --timeout 5000   # Test knowledge access
```

### 1.2 Common Symptoms

| Symptom               | Likely Cause         | Solution Section |
|-----------------------|----------------------|------------------|
| Command not found     | Installation issue   | [2.1](#21-command-not-found) |
| Import errors         | Missing dependencies | [2.2](#22-import-errors) |
| Timeout errors        | Performance/config   | [6.1](#61-timeout-errors) |
| Empty results         | Path/config issue    | [5.1](#51-knowledge-base-not-found) |
| MCP connection failed | Server/port issue    | [4.1](#41-connection-refused) |

---

## 2. Installation Issues

### 2.1 Command Not Found

**Symptom**: `sage: command not found`

| Solution | Command |
|----------|---------|
| Verify installation | `pip show sage-kb` |
| Use module directly | `python -m sage --help` |
| Reinstall | `pip uninstall sage-kb && pip install sage-kb` |
| Check PATH | Add `$(python -m site --user-base)/bin` to PATH |

### 2.2 Import Errors

**Symptom**: `ModuleNotFoundError` or `ImportError`

| Solution | Command |
|----------|---------|
| Check Python version | `python --version` (requires 3.12+) |
| Verify environment | `which python` |
| Install all deps | `pip install -e ".[all]"` |

### 2.3 Permission Errors

**Symptom**: `PermissionError` during installation

**Recommended**: Use conda environment:
```bash
conda create -n sage-kb python=3.12
conda activate sage-kb
pip install sage-kb
```

---

## 3. CLI Issues

### 3.1 No Output

**Symptom**: Commands return empty results

| Check | Command |
|-------|---------|
| Enable debug | `sage --debug get --layer core` |
| Show config | `sage config --show` |
| Verify content | `ls .knowledge/` |

### 3.2 Invalid Arguments

| Issue | Solution |
|-------|----------|
| Unknown command | Run `sage --help` |
| Invalid layer | Valid: `core`, `guidelines`, `practices`, `frameworks` |
| Special chars | Quote queries: `sage search "timeout pattern"` |

### 3.3 Encoding Issues

**Symptom**: `UnicodeDecodeError`

```bash
# Linux/macOS
export LANG=en_US.UTF-8

# Windows PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

---

## 4. MCP Server Issues

### 4.1 Connection Refused

**Symptom**: `Cannot connect to MCP server`

| Check | Command |
|-------|---------|
| Server running? | `ps aux | grep sage` (Linux) or `tasklist | findstr sage` (Windows) |
| Port in use? | `netstat -an | grep 8080` |
| Start server | `sage serve --port 8080` |
| Try different port | `sage serve --port 8081` |

### 4.2 Server Crashes

**Symptom**: Server starts but crashes immediately

| Solution | Action |
|----------|--------|
| Check logs | `cat .logs/sage.log` |
| Debug mode | `sage serve --debug --log-level DEBUG` |
| Verify deps | `pip install -e ".[mcp]"` |
| Validate config | `sage config --validate` |

### 4.3 Slow Responses

**Solutions**:

```yaml
# config/sage.yaml
cache:
  enabled: true
  ttl: 300

loading:
  smart_loading: true

timeouts:
  mcp_request: 10000  # 10 seconds
```

---

## 5. Configuration Issues

### 5.1 Knowledge Base Not Found

**Symptom**: `Knowledge base not found` or empty results

| Check | Action |
|-------|--------|
| Content exists | `ls .knowledge/core/` |
| Config path | Check `content_root` in `sage.yaml` |
| Permissions | `ls -la .knowledge/` |

### 5.2 Invalid Configuration

**Symptom**: `ConfigurationError` or YAML parsing errors

| Solution | Command |
|----------|---------|
| Validate YAML | `python -c "import yaml; yaml.safe_load(open('sage.yaml'))"` |
| Check syntax | Use YAML validator |
| Reset config | Copy from `config/sage.yaml.example` |

### 5.3 Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `SAGE_CONFIG` | Config file path | `sage.yaml` |
| `SAGE_LOG_LEVEL` | Logging level | `INFO` |
| `SAGE_CACHE_DIR` | Cache directory | `.cache/` |

---

## 6. Performance Issues

### 6.1 Timeout Errors

**Symptom**: `TimeoutError` or slow responses

| Solution | Configuration |
|----------|---------------|
| Increase timeout | `timeout.default_ms: 10000` |
| Enable caching | `cache.enabled: true` |
| Use smart loading | `loading.smart_loading: true` |

### 6.2 High Memory Usage

| Solution | Action |
|----------|--------|
| Limit content | Set `loading.max_files_per_layer: 50` |
| Enable pruning | Set `memory.auto_prune: true` |
| Check token budget | Set `loading.max_tokens: 4000` |

### 6.3 Slow Startup

| Solution | Action |
|----------|--------|
| Preload core only | Set `loading.preload: ["core"]` |
| Disable full scan | Set `loading.lazy: true` |
| Use cache | Ensure `cache.enabled: true` |

---

## 7. Getting Help

### 7.1 Debug Information

Collect this information when reporting issues:

```bash
sage info --json > sage_info.json
sage config --show > sage_config.txt
python --version
pip show sage-kb
```

### 7.2 Support Channels

| Channel | Use For |
|---------|---------|
| GitHub Issues | Bug reports, feature requests |
| Discussions | Questions, ideas |
| Documentation | `docs/` directory |

### 7.3 Reporting Issues

Include in bug reports:
1. SAGE version (`sage --version`)
2. Python version
3. Operating system
4. Steps to reproduce
5. Expected vs actual behavior
6. Error messages and logs

---

## Quick Reference

| Problem | Quick Fix |
|---------|-----------|
| Command not found | `python -m sage` |
| Import error | `pip install -e ".[all]"` |
| Timeout | Increase `timeout.default_ms` |
| Empty results | Check `content_root` path |
| MCP won't start | `sage serve --debug` |
| Slow performance | Enable `cache.enabled: true` |

---

## Related

- `docs/guides/configuration.md` — Configuration guide
- `docs/guides/quickstart.md` — Quick start guide
- `docs/guides/faq.md` — Frequently asked questions

---

*AI Collaboration Knowledge Base*
