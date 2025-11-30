---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~600
---

# Timeout & Loading Design

> 5-level timeout protection with graceful degradation and smart loading

---

## Document Series

This document is part of the Timeout & Loading Design series:

| Document                       | Content                                |
|--------------------------------|----------------------------------------|
| **04-timeout-loading.md** (this) | Philosophy, hierarchy, configuration |
| `04a-circuit-breaker.md`       | Circuit breaker and graceful degradation |
| `04b-smart-loading.md`         | Smart loading and token efficiency     |

---

## Table of Contents

- [1. Timeout Philosophy](#1-timeout-philosophy)
- [2. 5-Level Timeout Hierarchy](#2-5-level-timeout-hierarchy)
- [3. Timeout Configuration](#3-timeout-configuration)

---

## 1. Timeout Philosophy

```yaml
timeout:
  philosophy: "No operation should block indefinitely"

  principles:
    - name: "Fail Fast"
      description: "Detect and report failures quickly"
    - name: "Graceful Degradation"
      description: "Return partial results rather than nothing"
    - name: "User Feedback"
      description: "Always inform user of timeout status"
    - name: "Configurable"
      description: "Allow timeout adjustment per context"
```

---

## 2. 5-Level Timeout Hierarchy

| Level  | Name    | Timeout  | Scope            | Fallback Action        |
|--------|---------|----------|------------------|------------------------|
| **T1** | Cache   | 100ms    | Cache lookup     | Return stale or skip   |
| **T2** | File    | 500ms    | Single file read | Use fallback content   |
| **T3** | Layer   | 2,000ms  | Full layer load  | Partial load + warning |
| **T4** | Full    | 5,000ms  | Complete KB load | Emergency core only    |
| **T5** | Complex | 10,000ms | Analysis/search  | Abort + summary        |

### 2.1 Timeout Flow Diagram

```
Request arrives
       │
       ▼
┌──────────────────┐
│ T1: Cache (100ms)│──timeout──▶ Skip cache, proceed
└────────┬─────────┘
         │ hit/miss
         ▼
┌──────────────────┐
│ T2: File (500ms) │──timeout──▶ Use embedded fallback
└────────┬─────────┘
         │ success
         ▼
┌──────────────────┐
│ T3: Layer (2s)   │──timeout──▶ Return partial + warning
└────────┬─────────┘
         │ success
         ▼
┌──────────────────┐
│ T4: Full (5s)    │──timeout──▶ Emergency core only
└────────┬─────────┘
         │ success
         ▼
    Return result
```

### 2.2 Level Selection Guide

| Operation Type         | Recommended Level | Rationale                   |
|------------------------|-------------------|-----------------------------|
| Cache lookup           | T1 (100ms)        | Fast, can skip on miss      |
| Single file read       | T2 (500ms)        | Local I/O should be quick   |
| Layer/directory load   | T3 (2s)           | Multiple files, acceptable  |
| Full KB load           | T4 (5s)           | Complete load, user waiting |
| Search/analysis        | T5 (10s)          | Complex operations          |

---

## 3. Timeout Configuration

### 3.1 YAML Configuration

```yaml
# sage.yaml - Timeout Configuration
timeout:
  global_max_ms: 10000      # T5: Absolute maximum
  default_ms: 5000          # T4: Default for most operations

  levels:
    cache_ms: 100           # T1: Cache operations
    file_ms: 500            # T2: Single file operations
    layer_ms: 2000          # T3: Layer-level operations
    full_ms: 5000           # T4: Full KB operations
    complex_ms: 10000       # T5: Complex analysis

  circuit_breaker:
    enabled: true
    failure_threshold: 3     # Open after N failures
    reset_timeout_ms: 30000  # Try again after 30s
    half_open_requests: 1    # Test requests when half-open

  fallback:
    strategy: "graceful"     # graceful | strict | none
    cache_stale_ms: 60000    # Use stale cache up to 60s
```

### 3.2 TimeoutConfig Class

```python
# src/sage/core/timeout.py
"""
Timeout Configuration and Management.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class TimeoutConfig:
    """Timeout configuration with 5-level hierarchy."""
    
    # Level timeouts (milliseconds)
    cache_ms: int = 100      # T1
    file_ms: int = 500       # T2
    layer_ms: int = 2000     # T3
    full_ms: int = 5000      # T4
    complex_ms: int = 10000  # T5
    
    # Global settings
    global_max_ms: int = 10000
    default_ms: int = 5000
    
    # Fallback settings
    fallback_strategy: str = "graceful"
    cache_stale_ms: int = 60000
    
    def get_timeout(self, level: str) -> int:
        """Get timeout for specific level."""
        timeouts = {
            "cache": self.cache_ms,
            "file": self.file_ms,
            "layer": self.layer_ms,
            "full": self.full_ms,
            "complex": self.complex_ms,
        }
        return timeouts.get(level, self.default_ms)
    
    def get_level_name(self, timeout_ms: int) -> str:
        """Get level name for a timeout value."""
        if timeout_ms <= self.cache_ms:
            return "T1 (Cache)"
        elif timeout_ms <= self.file_ms:
            return "T2 (File)"
        elif timeout_ms <= self.layer_ms:
            return "T3 (Layer)"
        elif timeout_ms <= self.full_ms:
            return "T4 (Full)"
        else:
            return "T5 (Complex)"
```

### 3.3 Environment Variable Overrides

| Variable                    | Default | Description              |
|-----------------------------|---------|--------------------------|
| `SAGE_TIMEOUT_GLOBAL_MAX_MS`| 10000   | Absolute maximum timeout |
| `SAGE_TIMEOUT_DEFAULT_MS`   | 5000    | Default timeout          |
| `SAGE_TIMEOUT_CACHE_MS`     | 100     | T1 cache timeout         |
| `SAGE_TIMEOUT_FILE_MS`      | 500     | T2 file timeout          |
| `SAGE_TIMEOUT_LAYER_MS`     | 2000    | T3 layer timeout         |

---

## Related

- `docs/design/04a-circuit-breaker.md` — Circuit breaker and graceful degradation
- `docs/design/04b-smart-loading.md` — Smart loading and token efficiency
- `docs/design/01-architecture.md` — Overall architecture
- `.knowledge/frameworks/resilience/timeout_patterns.md` — Timeout patterns

---

*Part of SAGE Knowledge Base*
