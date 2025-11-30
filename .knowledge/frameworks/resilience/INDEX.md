---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~400
---

# Resilience Framework

> Fault tolerance and graceful degradation patterns

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Documents](#2-documents)
- [3. Key Concepts](#3-key-concepts)

---

## 1. Overview

The Resilience Framework provides patterns for building fault-tolerant systems that gracefully handle failures,
timeouts, and degraded conditions while maintaining useful functionality.

---

## 2. Documents

| Document              | Description                              |
|-----------------------|------------------------------------------|
| `TIMEOUT_PATTERNS.md` | Timeout handling and fallback strategies |

---

## 3. Key Concepts

### 3.1 Timeout Hierarchy (T1-T5)

| Level | Timeout | Scope            | Action on Timeout      |
|-------|---------|------------------|------------------------|
| T1    | 100ms   | Cache lookup     | Return cached/fallback |
| T2    | 500ms   | Single file      | Use partial/fallback   |
| T3    | 2s      | Layer load       | Load partial + warning |
| T4    | 5s      | Full KB load     | Emergency core only    |
| T5    | 10s     | Complex analysis | Abort + summary        |

### 3.2 Resilience Principles

- **Never hang**: Always return within timeout
- **Graceful degradation**: Partial results over no results
- **Circuit breaker**: Prevent cascade failures
- **Fallback chains**: Multiple fallback strategies

---

## Related

- `.context/policies/TIMEOUT_HIERARCHY.md` — Timeout configuration
- `.context/decisions/ADR-0003-TIMEOUT-HIERARCHY.md` — Timeout ADR
- `config/core/timeout.yaml` — Timeout settings

---

*Part of SAGE Knowledge Base*
