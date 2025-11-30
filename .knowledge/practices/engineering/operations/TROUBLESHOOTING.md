# Troubleshooting Guide

> Common issues, debugging techniques, and solutions for AI Collaboration Knowledge Base

---

## Table of Contents

- [1. Quick Diagnostics](#1-quick-diagnostics)

- [2. Common Errors](#2-common-errors)

- [3. Debugging Techniques](#3-debugging-techniques)

- [4. Log Analysis](#4-log-analysis)

- [5. Performance Issues](#5-performance-issues)

- [6. Configuration Problems](#6-configuration-problems)

- [7. MCP Server Issues](#7-mcp-server-issues)

- [8. Recovery Procedures](#8-recovery-procedures)

---

## 1. Quick Diagnostics

### 1.1 Health Check Commands

```bash
# Check system health

sage info

# Verify configuration

sage config validate

# Test MCP connection

sage serve --dry-run

# Check knowledge base integrity

sage check --all

```
### 1.2 Diagnostic Checklist

| Check             | Command                    | Expected Result        |

|-------------------|----------------------------|------------------------|

| Python version    | `python --version`         | ≥ 3.12                 |

| Dependencies      | `pip check`                | No broken dependencies |

| Config file       | `test -f config/app.yaml` | File exists            |

| Content directory | `ls .knowledge/`           | Directories present    |

---

## 2. Common Errors

### 2.1 Import Errors

**Symptom**: `ModuleNotFoundError: No module named 'sage'`
**Causes & Solutions**:

| Cause                    | Solution                           |

|--------------------------|------------------------------------|

| Package not installed    | `pip install -e .`                 |

| Wrong Python environment | Activate correct conda env or venv |

| Path issues              | Check `PYTHONPATH`                 |

**Debug Steps**:

```python
import sys

print(sys.path)  # Check if src/ is in path

```
### 2.2 Configuration Errors

**Symptom**: `ConfigurationError: Invalid configuration`
**Common Issues**:

| Issue                  | Solution                                  |

|------------------------|-------------------------------------------|

| YAML syntax error      | Validate with `yamllint config/app.yaml` |

| Missing required field | Check against schema                      |

| Type mismatch          | Ensure correct data types                 |

**Debug Example**:

```python
import yaml

with open("config/app.yaml") as f:

    try:

        config = yaml.safe_load(f)

    except yaml.YAMLError as e:

        print(f"YAML Error: {e}")

```
### 2.3 Timeout Errors

**Symptom**: `TimeoutError: Operation timed out`
**Timeout Levels Reference**:

| Level | Timeout | Typical Cause     |

|-------|---------|-------------------|

| T1    | 100ms   | Slow cache lookup |

| T2    | 500ms   | Large file read   |

| T3    | 2s      | Directory scan    |

| T4    | 5s      | Full KB load      |

| T5    | 10s     | Complex analysis  |

**Solutions**:

- Increase timeout in config

- Optimize content size

- Use lazy loading

- Enable caching

### 2.4 MCP Connection Errors

**Symptom**: `ConnectionError: Failed to connect to MCP server`
**Solutions**:

| Issue              | Solution                 |

|--------------------|--------------------------|

| Server not running | Start with `sage serve`  |

| Port conflict      | Change port in config    |

| Firewall blocking  | Allow port in firewall   |

| SSL issues         | Check certificate config |

---

## 3. Debugging Techniques

### 3.1 Enable Debug Logging

```python
# In code

import logging

logging.getLogger("sage").setLevel(logging.DEBUG)

# Via environment

export

SAGE_LOG_LEVEL = DEBUG

# Via config

# config/core/logging.yaml

default_level: DEBUG

```
### 3.2 Interactive Debugging

```python
# Add breakpoint

import pdb;

pdb.set_trace()

# Or use IPython

from IPython import embed;

embed()

# Or use breakpoint() (Python 3.7+)

breakpoint()

```
### 3.3 Trace Execution

```python
# Trace function calls

import sys

def trace_calls(frame, event, arg):

    if event == 'call':

        print(f"Call: {frame.f_code.co_name}")

    return trace_calls

sys.settrace(trace_calls)

```
### 3.4 Memory Profiling

```python
# Install: pip install memory-profiler

from memory_profiler import profile

@profile

def memory_intensive_function():

    # Your code here

    pass

```
---

## 4. Log Analysis

### 4.1 Log Locations

| Log Type    | Location           | Purpose          |

|-------------|--------------------|------------------|

| Application | `.logs/sage.log`   | General app logs |

| Access      | `.logs/access.log` | Request logs     |

| Error       | `.logs/error.log`  | Error details    |

| Debug       | `.logs/debug.log`  | Verbose debug    |

### 4.2 Log Patterns

**Error Pattern**:

```text
[ERROR] 2025-01-15 10:30:45 | module.name | Error message

        Traceback: ...

        Context: {"key": "value"}

```
**Parsing Logs**:

```bash
# Find errors

grep "\[ERROR\]" .logs/sage.log

# Find specific module issues

grep "loader" .logs/sage.log

# Get recent errors

tail -100 .logs/error.log

# Watch logs in real-time

tail -f .logs/sage.log

```
### 4.3 Structured Log Query

```python
import json

def parse_structured_log(log_file):

    with open(log_file) as f:

        for line in f:

            try:

                entry = json.loads(line)

                if entry.get("level") == "ERROR":

                    print(f"{entry['timestamp']}: {entry['message']}")

            except json.JSONDecodeError:

                continue

```
---

## 5. Performance Issues

### 5.1 Slow Loading

**Diagnosis**:

```python
import time

start = time.perf_counter()

# Operation

elapsed = time.perf_counter() - start

print(f"Elapsed: {elapsed:.3f}s")

```
**Common Causes**:

| Cause          | Solution                 |

|----------------|--------------------------|

| Large files    | Split into smaller files |

| Too many files | Implement lazy loading   |

| No caching     | Enable file caching      |

| Sync I/O       | Use async operations     |

### 5.2 High Memory Usage

**Diagnosis**:

```python
import tracemalloc

tracemalloc.start()

# Your code

snapshot = tracemalloc.take_snapshot()

top_stats = snapshot.statistics('lineno')

for stat in top_stats[:10]:

    print(stat)

```
**Solutions**:

- Use generators instead of lists

- Implement streaming for large data

- Clear caches periodically

- Use memory-mapped files

### 5.3 CPU Bottlenecks

**Diagnosis**:

```python
import cProfile

import pstats

profiler = cProfile.Profile()

profiler.enable()

# Your code

profiler.disable()

stats = pstats.Stats(profiler)

stats.sort_stats('cumulative')

stats.print_stats(10)

```
---

## 6. Configuration Problems

### 6.1 Validate Configuration

```python
from sage.core.config import load_config, validate_config

try:

    config = load_config()

    validate_config(config)

    print("Configuration is valid")

except Exception as e:

    print(f"Configuration error: {e}")

```
### 6.2 Common Config Issues

| Issue        | Symptom           | Solution           |

|--------------|-------------------|--------------------|

| Missing file | FileNotFoundError | Create config file |

| Invalid YAML | YAMLError         | Fix syntax         |

| Wrong types  | TypeError         | Check schema       |

| Missing keys | KeyError          | Add required keys  |

### 6.3 Environment Override Issues

```bash
# Check environment variables

env | grep SAGE_

# Common overrides

SAGE_LOG_LEVEL=DEBUG

SAGE_CONFIG_PATH=/custom/path

SAGE_TIMEOUT_DEFAULT=5000

```
---

## 7. MCP Server Issues

### 7.1 Server Won't Start

**Checklist**:

1. Check if port is available: `lsof -i :8080`
2. Verify MCP package installed: `pip show mcp`
3. Check config: `config/services/mcp.yaml`
4. Review logs: `.logs/mcp.log`
### 7.2 Tool Registration Failures

**Symptom**: Tools not appearing in MCP client

**Debug**:

```python
from sage.services.mcp_server import create_app

app = create_app()

print(f"Registered tools: {list(app.tools.keys())}")

```
### 7.3 Request/Response Issues

**Enable request logging**:

```yaml
# config/services/mcp.yaml

logging:

  requests: true

  responses: true

  level: DEBUG

```
---

## 8. Recovery Procedures

### 8.1 Corrupted Configuration

```bash
# Backup current config

cp config/app.yaml config/app.yaml.bak

# Reset to defaults

sage config reset

# Or restore from backup

cp config/app.yaml.backup config/app.yaml

```
### 8.2 Database/Cache Corruption

```bash
# Clear cache

rm -rf .cache/*

# Rebuild indices

sage rebuild --indices

# Verify integrity

sage check --integrity

```
### 8.3 Failed Migration Recovery

```bash
# List available backups

sage backup list

# Restore from backup

sage backup restore --name pre_migration_backup

# Verify restoration

sage check --all

```
### 8.4 Emergency Procedures

| Scenario            | Procedure                               |

|---------------------|-----------------------------------------|

| Server crash        | Check logs → Restart → Review errors    |

| Data loss           | Restore from backup → Verify integrity  |

| Config corruption   | Reset config → Reapply settings         |

| Dependency conflict | Create fresh conda env/venv → Reinstall |

---

## Quick Reference

### Error Code Reference

| Code | Meaning      | Action                    |

|------|--------------|---------------------------|

| E001 | Config error | Check config syntax       |

| E002 | Timeout      | Increase timeout/optimize |

| E003 | Not found    | Check paths               |

| E004 | Permission   | Check file permissions    |

| E005 | Connection   | Check network/service     |

### Debug Environment Variables

```bash
export SAGE_DEBUG=1

export SAGE_LOG_LEVEL=DEBUG

export SAGE_TRACE=1

export SAGE_PROFILE=1

```
---

## Related

- `.knowledge/practices/engineering/LOGGING.md` — Logging best practices

- `.knowledge/practices/engineering/ERROR_HANDLING.md` — Error handling patterns

- `.context/policies/TIMEOUT_HIERARCHY.md` — Timeout configuration

- `docs/guides/CONFIGURATION.md` — Configuration guide

---

*AI Collaboration Knowledge Base*
