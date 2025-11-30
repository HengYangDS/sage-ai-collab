---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~900
---

# Circuit Breaker & Graceful Degradation

> Fault tolerance patterns for SAGE timeout management

---

## Table of Contents

- [1. Circuit Breaker Pattern](#1-circuit-breaker-pattern)
- [2. Graceful Degradation](#2-graceful-degradation)
- [3. Fallback Architecture](#3-fallback-architecture)

---

## 1. Circuit Breaker Pattern

### 1.1 States

```
     ┌─────────────────────────────────────────────────────┐
     │                                                     │
     │    ┌──────────┐         ┌──────────┐              │
     │    │  CLOSED  │──fail──▶│   OPEN   │              │
     │    │ (normal) │  (N×)   │ (reject) │              │
     │    └────┬─────┘         └────┬─────┘              │
     │         │                    │                     │
     │    success              timeout                    │
     │         │                    │                     │
     │         │              ┌─────▼─────┐              │
     │         │              │HALF-OPEN  │              │
     │         │              │  (test)   │              │
     │         │              └─────┬─────┘              │
     │         │                    │                     │
     │         │         success    │    fail            │
     │         ◀────────────────────┴──────────▶         │
     │                                                     │
     └─────────────────────────────────────────────────────┘
```

### 1.2 Implementation

```python
# src/sage/core/circuit_breaker.py
"""
Circuit Breaker Pattern for fault tolerance.
"""
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Callable, TypeVar, Awaitable
import asyncio

T = TypeVar("T")


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Rejecting requests
    HALF_OPEN = "half_open"  # Testing recovery


@dataclass
class CircuitBreaker:
    """
    Circuit breaker for protecting against cascading failures.
    
    Usage:
        breaker = CircuitBreaker(failure_threshold=3)
        result = await breaker.call(risky_operation)
    """
    failure_threshold: int = 3
    reset_timeout_ms: int = 30000
    half_open_requests: int = 1

    # Internal state
    _state: CircuitState = field(default=CircuitState.CLOSED, repr=False)
    _failure_count: int = field(default=0, repr=False)
    _last_failure_time: Optional[datetime] = field(default=None, repr=False)

    @property
    def state(self) -> CircuitState:
        """Get current circuit state, checking for timeout transition."""
        if self._state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._state = CircuitState.HALF_OPEN
        return self._state

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self._last_failure_time is None:
            return True
        elapsed = datetime.now() - self._last_failure_time
        return elapsed > timedelta(milliseconds=self.reset_timeout_ms)

    async def call(
        self,
        operation: Callable[[], Awaitable[T]],
        fallback: Optional[Callable[[], Awaitable[T]]] = None
    ) -> T:
        """Execute operation with circuit breaker protection."""
        state = self.state

        if state == CircuitState.OPEN:
            if fallback:
                return await fallback()
            raise CircuitOpenError("Circuit is open")

        try:
            result = await operation()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            if fallback:
                return await fallback()
            raise

    def _on_success(self) -> None:
        """Handle successful operation."""
        self._failure_count = 0
        self._state = CircuitState.CLOSED

    def _on_failure(self) -> None:
        """Handle failed operation."""
        self._failure_count += 1
        self._last_failure_time = datetime.now()
        if self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN


class CircuitOpenError(Exception):
    """Raised when circuit breaker is open."""
    pass
```

### 1.3 Configuration

```yaml
# sage.yaml - Circuit Breaker Configuration
timeout:
  circuit_breaker:
    enabled: true
    failure_threshold: 3     # Open after N failures
    reset_timeout_ms: 30000  # Try again after 30s
    half_open_requests: 1    # Test requests when half-open
```

---

## 2. Graceful Degradation

### 2.1 4-Level Degradation Strategy

| Level  | Trigger    | Response           | User Impact                   |
|--------|------------|--------------------|-------------------------------|
| **D1** | T1 timeout | Skip cache         | None (transparent)            |
| **D2** | T2 timeout | Use stale cache    | Minor (possibly outdated)     |
| **D3** | T3 timeout | Partial content    | Moderate (incomplete)         |
| **D4** | T4 timeout | Emergency fallback | Significant (minimal content) |

### 2.2 Fallback Content Hierarchy

```
Priority 1: Fresh content from filesystem
    │
    └── Timeout? ───▶ Priority 2: Cached content (< 60s old)
                          │
                          └── Not available? ───▶ Priority 3: Package fallback
                                                      │
                                                      └── Not available? ───▶ Priority 4: Emergency core
```

### 2.3 Emergency Fallback Content

```yaml
# src/sage/data/fallback_core.yaml
fallback:
  core_principles: |
    # SAGE Core Principles (Emergency Fallback)

    ## 信达雅 (Xin-Da-Ya)
    - **信 (Faithfulness)**: Be accurate and reliable
    - **达 (Clarity)**: Be clear and accessible  
    - **雅 (Elegance)**: Be refined and sustainable

    ## Quick Reference (6-Level Autonomy)
    - L1-L2 (Minimal/Low): Ask before changes
    - L3-L4 (Medium/Medium-High): Proceed and report ⭐
    - L5-L6 (High/Full): High autonomy mode

    ## Timeout Notice
    Full knowledge base unavailable. Using emergency fallback.
```

---

## 3. Fallback Architecture

### 3.1 5-Layer System Fallback

```
Layer 1: TECHNICAL ──────────────────────────────────────────────────┐
         timeout → return_partial_with_warning                       │
         file_not_found → use_template_or_create                     │
         service_down → use_alternative_channel                      │
                                                                     │
Layer 2: KNOWLEDGE ──────────────────────────────────────────────────┤
         content_not_loaded → provide_summary                        │
         framework_unavailable → provide_core_principle              │
                                                                     │
Layer 3: CAPABILITY ─────────────────────────────────────────────────┤
         plugin_unavailable → use_builtin_alternative                │
         advanced_search → basic_search                              │
         service_unavailable → priority: [api, mcp, cli, file]       │
                                                                     │
Layer 4: INTELLIGENCE ───────────────────────────────────────────────┤
         expert_committee_unavailable → use_simplified_decision      │
         analysis_timeout → provide_heuristics                       │
                                                                     │
Layer 5: HUMAN ──────────────────────────────────────────────────────┘
         autonomy_limit_reached → escalate_to_human
         high_uncertainty (confidence < 70%) → clarify_with_user
```

### 3.2 Fallback Strategy by Layer

| Layer        | Scope                    | Fallback Strategy                 | User Impact      |
|--------------|--------------------------|-----------------------------------|------------------|
| Technical    | Timeout, I/O errors      | Cache, partial results, retry     | Transparent      |
| Knowledge    | Content loading          | Summary, core principles          | Reduced detail   |
| Capability   | Plugin/service failures  | Built-in alternatives             | Reduced features |
| Intelligence | Analysis/decision limits | Simplified frameworks, heuristics | Manual effort    |
| Human        | Autonomy boundaries      | Escalation, clarification         | User decision    |

**Key Insight**: Fallback = "How to maintain value delivery when optimal path is unavailable"

---

## Related

- `docs/design/04-TIMEOUT-LOADING.md` — Timeout hierarchy overview
- `docs/design/04B-SMART-LOADING.md` — Smart loading and token efficiency
- `.knowledge/frameworks/resilience/TIMEOUT_PATTERNS.md` — Timeout patterns

---

*Part of SAGE Knowledge Base*
