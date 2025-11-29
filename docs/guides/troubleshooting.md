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

### 1.1 Health Check

```bash
# Check SAGE installation
sage info

# Verify configuration
sage config --validate

# Test knowledge base access
sage get --layer core --timeout 5000
```

### 1.2 Common Symptoms

| Symptom               | Likely Cause         | Section                             |
|-----------------------|----------------------|-------------------------------------|
| Command not found     | Installation issue   | [2.1](#21-command-not-found)        |
| Import errors         | Missing dependencies | [2.2](#22-import-errors)            |
| Timeout errors        | Performance/config   | [6.1](#61-timeout-errors)           |
| Empty results         | Path/config issue    | [5.2](#52-knowledge-base-not-found) |
| MCP connection failed | Server/port issue    | [4.1](#41-connection-refused)       |

---

## 2. Installation Issues

### 2.1 Command Not Found

**Symptom**: `sage: command not found` or `'sage' is not recognized`

**Solutions**:

1. **Verify installation**:
   ```bash
   pip show sage-kb
   ```

2. **Check PATH**:
   ```bash
   # Find where pip installs scripts
   python -m site --user-base
   
   # Add to PATH if needed (Linux/macOS)
   export PATH="$PATH:$(python -m site --user-base)/bin"
   
   # Windows
   # Add %APPDATA%\Python\Python312\Scripts to PATH
   ```

3. **Use module directly**:
   ```bash
   python -m sage --help
   ```

4. **Reinstall**:
   ```bash
   pip uninstall sage-kb
   pip install sage-kb
   ```

### 2.2 Import Errors

**Symptom**: `ModuleNotFoundError` or `ImportError`

**Solutions**:

1. **Check Python version**:
   ```bash
   python --version  # Requires 3.12+
   ```

2. **Verify virtual environment**:
   ```bash
   # Ensure conda environment is activated (recommended)
   conda env list  # Check active environment
   which python    # Should point to conda env
   
   # Reinstall in correct environment
   pip install -e ".[all]"
   ```

3. **Install missing dependencies**:
   ```bash
   pip install -e ".[all]"
   ```

### 2.3 Permission Errors

**Symptom**: `PermissionError` during installation

**Solutions**:

1. **Use conda environment** (recommended):
   ```bash
   conda create -n sage-kb python=3.12
   conda activate sage-kb
   pip install sage-kb
   ```

   Or use venv as alternative:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   pip install sage-kb
   ```

2. **User installation**:
   ```bash
   pip install --user sage-kb
   ```

---

## 3. CLI Issues

### 3.1 No Output

**Symptom**: Commands return nothing or empty results

**Diagnosis**:

```bash
# Enable debug output
sage --debug get --layer core

# Check configuration
sage config --show
```

**Solutions**:

1. **Verify content path**:
   ```bash
   # Check if content directory exists
   ls content/  # or: dir content\
   
   # Verify in config
   sage config --show | grep content_root
   ```

2. **Check file permissions**:
   ```bash
   # Ensure readable
   ls -la content/core/
   ```

### 3.2 Invalid Command Arguments

**Symptom**: `Error: Invalid value for...` or argument errors

**Solutions**:

1. **Check help**:
   ```bash
   sage --help
   sage get --help
   ```

2. **Verify layer names**:
   ```bash
   # Valid layers: core, guidelines, practices, frameworks, scenarios
   sage get --layer core
   ```

3. **Quote special characters**:
   ```bash
   sage search "timeout pattern"
   ```

### 3.3 Encoding Issues

**Symptom**: `UnicodeDecodeError` or garbled output

**Solutions**:

1. **Set UTF-8 encoding**:
   ```bash
   # Linux/macOS
   export LANG=en_US.UTF-8
   
   # Windows PowerShell
   [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
   ```

2. **Check file encoding**:
   ```python
   # Files should be UTF-8
   with open(file, encoding='utf-8') as f:
       content = f.read()
   ```

---

## 4. MCP Server Issues

### 4.1 Connection Refused

**Symptom**: `Connection refused` or `Cannot connect to MCP server`

**Diagnosis**:

```bash
# Check if server is running
ps aux | grep sage  # Linux/macOS
tasklist | findstr sage  # Windows

# Check port availability
netstat -an | grep 8080
```

**Solutions**:

1. **Start the server**:
   ```bash
   sage serve --port 8080
   ```

2. **Check port conflicts**:
   ```bash
   # Use different port
   sage serve --port 8081
   ```

3. **Verify firewall settings**:
   ```bash
   # Allow port in firewall if needed
   ```

### 4.2 Server Crashes

**Symptom**: Server starts but crashes immediately

**Diagnosis**:

```bash
# Run with debug logging
sage serve --debug --log-level DEBUG
```

**Solutions**:

1. **Check logs**:
   ```bash
   cat .logs/sage.log
   ```

2. **Verify dependencies**:
   ```bash
   pip install -e ".[mcp]"
   ```

3. **Check configuration**:
   ```bash
   sage config --validate
   ```

### 4.3 Slow Responses

**Symptom**: MCP server responds slowly or times out

**Solutions**:

1. **Enable caching**:
   ```yaml
   # config/sage.yaml
   cache:
     enabled: true
     ttl: 300
   ```

2. **Reduce content scope**:
   ```yaml
   loading:
     smart_loading: true
     max_files_per_layer: 50
   ```

3. **Increase timeout**:
   ```yaml
   timeouts:
     mcp_request: 10000  # 10 seconds
   ```

---

## 5. Configuration Issues

### 5.1 Config File Not Found

**Symptom**: `Configuration file not found` or using defaults

**Diagnosis**:

```bash
# Show config locations searched
sage config --show-paths
```

**Solutions**:

1. **Create config file**:
   ```bash
   # Create default config
   sage config --init
   
   # Or manually create
   mkdir -p config
   touch config/sage.yaml
   ```

2. **Specify config path**:
   ```bash
   sage --config /path/to/sage.yaml get --layer core
   ```

### 5.2 Knowledge Base Not Found

**Symptom**: `Knowledge base path not found` or empty results

**Solutions**:

1. **Verify path exists**:
   ```bash
   ls -la content/
   ```

2. **Update configuration**:
   ```yaml
   # config/sage.yaml
   knowledge_base:
     root: ./content
     layers:
       - core
       - guidelines
       - practices
   ```

3. **Use absolute path**:
   ```yaml
   knowledge_base:
     root: /absolute/path/to/content
   ```

### 5.3 Invalid YAML

**Symptom**: `YAML parsing error` or config not loading

**Solutions**:

1. **Validate YAML**:
   ```bash
   python -c "import yaml; yaml.safe_load(open('config/sage.yaml'))"
   ```

2. **Check common issues**:
    - Indentation (use spaces, not tabs)
    - Colons followed by space
    - Quotes around special characters

3. **Use YAML validator**:
   ```bash
   pip install yamllint
   yamllint config/sage.yaml
   ```

---

## 6. Performance Issues

### 6.1 Timeout Errors

**Symptom**: `TimeoutError` or operations taking too long

**Diagnosis**:

```bash
# Check current timeouts
sage config --show | grep timeout

# Profile operation
sage --debug --profile get --layer core
```

**Solutions**:

1. **Increase timeouts**:
   ```yaml
   # config/sage.yaml
   timeouts:
     t1_cache: 100
     t2_file: 500
     t3_layer: 2000
     t4_full: 5000
     t5_analysis: 10000
   ```

2. **Enable smart loading**:
   ```yaml
   loading:
     smart_loading: true
     lazy_load: true
   ```

3. **Reduce content scope**:
   ```bash
   sage get --layer core  # Instead of all layers
   ```

### 6.2 High Memory Usage

**Symptom**: Memory errors or system slowdown

**Solutions**:

1. **Enable streaming**:
   ```yaml
   loading:
     streaming: true
     chunk_size: 1000
   ```

2. **Limit cache size**:
   ```yaml
   cache:
     max_size: 100  # Maximum items
     max_memory: 50MB
   ```

3. **Use lazy loading**:
   ```yaml
   loading:
     lazy_load: true
   ```

### 6.3 Slow Startup

**Symptom**: CLI or server takes long to start

**Solutions**:

1. **Disable preloading**:
   ```yaml
   loading:
     preload: false
   ```

2. **Reduce initial scope**:
   ```yaml
   loading:
     startup_layers:
       - core  # Only load core at startup
   ```

---

## 7. Getting Help

### 7.1 Collect Debug Information

Before reporting issues:

```bash
# System information
python --version
pip show sage-kb

# Configuration
sage config --show

# Debug output
sage --debug get --layer core 2>&1 | tee debug.log

# Log files
cat .logs/sage.log
```

### 7.2 Log Files

| Log       | Location          | Content                  |
|-----------|-------------------|--------------------------|
| Main log  | `.logs/sage.log`  | General application logs |
| Error log | `.logs/error.log` | Errors and exceptions    |
| Debug log | `.logs/debug.log` | Detailed debug info      |

### 7.3 Reporting Issues

When reporting issues, include:

1. **Environment**:
    - OS and version
    - Python version
    - SAGE version

2. **Steps to reproduce**:
    - Exact commands run
    - Configuration used

3. **Expected vs actual behavior**

4. **Relevant logs and error messages**

### 7.4 Resources

- **Documentation**: `docs/guides/`
- **API Reference**: `docs/api/`
- **GitHub Issues**: Report bugs and feature requests
- **Discussions**: Ask questions and share tips

---

## Quick Reference

### Diagnostic Commands

```bash
# Health check
sage info

# Configuration
sage config --show
sage config --validate

# Debug mode
sage --debug <command>

# Verbose logging
sage --log-level DEBUG <command>
```

### Common Fixes

| Issue              | Quick Fix                  |
|--------------------|----------------------------|
| Command not found  | `pip install sage-kb`      |
| Import error       | `pip install -e ".[all]"`  |
| Config not found   | `sage config --init`       |
| Timeout            | Increase timeout in config |
| Connection refused | `sage serve --port 8080`   |

---

*Part of SAGE Knowledge Base*
