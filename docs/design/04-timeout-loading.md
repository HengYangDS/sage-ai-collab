---
title: SAGE Knowledge Base - Timeout & Loading Design
version: 1.0.0
date: 2025-11-28
status: production-ready
---

# Timeout & Loading Design

> **5-level timeout protection with graceful degradation and smart loading**

## Timeout Philosophy

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

## 5-Level Timeout Hierarchy

| Level  | Name    | Timeout  | Scope            | Fallback Action        |
|--------|---------|----------|------------------|------------------------|
| **T1** | Cache   | 100ms    | Cache lookup     | Return stale or skip   |
| **T2** | File    | 500ms    | Single file read | Use fallback content   |
| **T3** | Layer   | 2,000ms  | Full layer load  | Partial load + warning |
| **T4** | Full    | 5,000ms  | Complete KB load | Emergency core only    |
| **T5** | Complex | 10,000ms | Analysis/search  | Abort + summary        |

### Timeout Flow Diagram

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

---

## Timeout Configuration

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

### TimeoutConfig Class

```python
# src/sage/core/timeout.py
"""
Timeout Configuration and Management.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import yaml


@dataclass
class TimeoutConfig:
    """Timeout configuration with defaults."""

    # Individual timeouts
    cache_ms: int = 100
    file_ms: int = 500
    layer_ms: int = 2000
    full_ms: int = 5000
    complex_ms: int = 10000

    # Global
    global_max_ms: int = 10000
    default_ms: int = 5000

    # Circuit breaker
    circuit_breaker_enabled: bool = True
    failure_threshold: int = 3
    reset_timeout_ms: int = 30000

    @classmethod
    def from_yaml(cls, path: Path) -> "TimeoutConfig":
        """Load timeout config from YAML file."""
        if not path.exists():
            return cls()

        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

        timeout_config = config.get("timeout", {})
        levels = timeout_config.get("levels", {})
        circuit = timeout_config.get("circuit_breaker", {})

        return cls(
            cache_ms=levels.get("cache_ms", 100),
            file_ms=levels.get("file_ms", 500),
            layer_ms=levels.get("layer_ms", 2000),
            full_ms=levels.get("full_ms", 5000),
            complex_ms=levels.get("complex_ms", 10000),
            global_max_ms=timeout_config.get("global_max_ms", 10000),
            default_ms=timeout_config.get("default_ms", 5000),
            circuit_breaker_enabled=circuit.get("enabled", True),
            failure_threshold=circuit.get("failure_threshold", 3),
            reset_timeout_ms=circuit.get("reset_timeout_ms", 30000),
        )

    def get_timeout(self, level: str) -> int:
        """Get timeout for a specific level."""
        timeouts = {
            "cache"  : self.cache_ms,
            "file"   : self.file_ms,
            "layer"  : self.layer_ms,
            "full"   : self.full_ms,
            "complex": self.complex_ms,
        }
        return timeouts.get(level, self.default_ms)
```

---

## Circuit Breaker Pattern

### States

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

### Implementation

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
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Rejecting requests
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
    _half_open_successes: int = field(default=0, repr=False)

    @property
    def state(self) -> CircuitState:
        """Get current circuit state, checking for timeout transition."""
        if self._state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._state = CircuitState.HALF_OPEN
                self._half_open_successes = 0
                logger.info("Circuit breaker transitioning to half-open")
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
        """
        Execute operation with circuit breaker protection.
        
        Args:
            operation: Async function to execute
            fallback: Optional fallback if circuit is open
            
        Returns:
            Result from operation or fallback
            
        Raises:
            CircuitOpenError: If circuit is open and no fallback provided
        """
        state = self.state

        if state == CircuitState.OPEN:
            logger.warning("Circuit is open, rejecting request")
            if fallback:
                return await fallback()
            raise CircuitOpenError("Circuit breaker is open")

        try:
            result = await operation()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            if fallback and self._state == CircuitState.OPEN:
                return await fallback()
            raise

    def _on_success(self) -> None:
        """Handle successful operation."""
        if self._state == CircuitState.HALF_OPEN:
            self._half_open_successes += 1
            if self._half_open_successes >= self.half_open_requests:
                self._state = CircuitState.CLOSED
                self._failure_count = 0
                logger.info("Circuit breaker closed after successful test")
        else:
            self._failure_count = 0

    def _on_failure(self) -> None:
        """Handle failed operation."""
        self._failure_count += 1
        self._last_failure_time = datetime.now()

        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.OPEN
            logger.warning("Circuit breaker reopened after test failure")
        elif self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN
            logger.warning(
                f"Circuit breaker opened after {self._failure_count} failures"
            )

    def reset(self) -> None:
        """Manually reset the circuit breaker."""
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None


class CircuitOpenError(Exception):
    """Raised when circuit breaker is open."""
    pass
```

---

## Graceful Degradation

### 4-Level Degradation Strategy

| Level  | Trigger    | Response           | User Impact                   |
|--------|------------|--------------------|-------------------------------|
| **D1** | T1 timeout | Skip cache         | None (transparent)            |
| **D2** | T2 timeout | Use stale cache    | Minor (possibly outdated)     |
| **D3** | T3 timeout | Partial content    | Moderate (incomplete)         |
| **D4** | T4 timeout | Emergency fallback | Significant (minimal content) |

### Fallback Content Hierarchy

```
Priority 1: Fresh content from filesystem
    │
    └── Timeout? ───▶ Priority 2: Cached content (< 60s old)
                          │
                          └── Not available? ───▶ Priority 3: Package fallback
                                                      │
                                                      └── Not available? ───▶ Priority 4: Emergency core
```

### Emergency Fallback Content

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
    Please retry or check system status.
```

---

## Timeout-Aware Loader

```python
# src/sage/core/loader.py
"""
TimeoutLoader - Knowledge loading with timeout protection.

Features:
- 5-level timeout hierarchy
- Circuit breaker integration
- Graceful degradation
- External fallback content
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List
import asyncio
import importlib.resources
import yaml
import time

from sage.core.timeout import TimeoutConfig
from sage.core.circuit_breaker import CircuitBreaker
from sage.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class LoadResult:
    """Result of a load operation."""
    content: str
    complete: bool
    duration_ms: int
    layers_loaded: int
    status: str  # success | partial | fallback | timeout
    tokens: int = 0
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.tokens == 0:
            self.tokens = len(self.content) // 4


class TimeoutLoader:
    """
    Knowledge loader with comprehensive timeout protection.
    
    Features:
    - Per-layer timeout enforcement
    - Global timeout cap
    - Circuit breaker for repeated failures
    - Graceful degradation to fallback content
    """

    # Emergency fallback (truly last resort, ~3 lines)
    _EMERGENCY_FALLBACK = "# Emergency\nBe accurate. Be clear. Be elegant."

    def __init__(
        self,
        config_path: Optional[Path] = None,
        timeout_config: Optional[TimeoutConfig] = None
    ):
        self.config_path = config_path or Path("sage.yaml")
        self.timeout_config = timeout_config or TimeoutConfig.from_yaml(self.config_path)
        self._cache: dict[str, str] = {}
        self._fallback_content: str | None = None
        self._circuit_breaker = CircuitBreaker(
            failure_threshold=self.timeout_config.failure_threshold,
            reset_timeout_ms=self.timeout_config.reset_timeout_ms,
        )

        logger.info(
            "loader initialized",
            config_path=str(self.config_path),
            timeout_full_ms=self.timeout_config.full_ms
        )

    def _load_fallback_content(self) -> str:
        """
        Load fallback from package data YAML file.
        
        Priority:
        1. Package data file (src/sage/data/fallback_core.yaml)
        2. Emergency fallback (hardcoded ~3 lines)
        """
        if self._fallback_content is not None:
            return self._fallback_content

        try:
            files = importlib.resources.files("sage.data")
            fallback_file = files.joinpath("fallback_core.yaml")
            with fallback_file.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                self._fallback_content = data.get("fallback", {}).get(
                    "core_principles",
                    self._EMERGENCY_FALLBACK
                )
                logger.debug("fallback loaded from package data")
        except Exception as e:
            logger.warning("fallback load failed, using emergency", error=str(e))
            self._fallback_content = self._EMERGENCY_FALLBACK

        return self._fallback_content

    async def load_with_timeout(
        self,
        layers: List[str],
        timeout_ms: Optional[int] = None
    ) -> LoadResult:
        """
        Load knowledge with strict timeout guarantees.
        
        Args:
            layers: List of layers to load (e.g., ["core", "guidelines"])
            timeout_ms: Override timeout (uses config default if None)
            
        Returns:
            LoadResult with content and status
        """
        start = time.monotonic()
        timeout = (timeout_ms or self.timeout_config.full_ms) / 1000
        results: List[str] = []
        layers_loaded = 0

        for layer in layers:
            remaining = timeout - (time.monotonic() - start)
            if remaining <= 0:
                logger.warning("timeout reached", layers_loaded=layers_loaded)
                break

            try:
                content = await asyncio.wait_for(
                    self._load_layer(layer),
                    timeout=min(remaining, self.timeout_config.layer_ms / 1000)
                )
                results.append(content)
                layers_loaded += 1
                logger.debug("layer loaded", layer=layer)
            except asyncio.TimeoutError:
                logger.warning("layer timeout", layer=layer)
                results.append(self._load_fallback_content())

        duration = int((time.monotonic() - start) * 1000)
        complete = layers_loaded == len(layers)

        return LoadResult(
            content="\n\n".join(results),
            complete=complete,
            duration_ms=duration,
            layers_loaded=layers_loaded,
            status="success" if complete else "partial",
            metadata={"timeout_ms": timeout_ms or self.timeout_config.full_ms}
        )

    async def _load_layer(self, layer: str) -> str:
        """Load a single layer with caching."""
        if layer in self._cache:
            return self._cache[layer]

        content = await self._read_layer_content(layer)
        self._cache[layer] = content
        return content

    async def _read_layer_content(self, layer: str) -> str:
        """Read layer content from filesystem."""
        content_path = Path("content") / layer
        if not content_path.exists():
            logger.warning("layer not found", layer=layer)
            return self._load_fallback_content()

        # Read all markdown files in layer directory
        contents = []
        for md_file in sorted(content_path.glob("**/*.md")):
            try:
                contents.append(md_file.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error("file read error", file=str(md_file), error=str(e))

        return "\n\n".join(contents) if contents else self._load_fallback_content()

    async def get_fallback(self) -> str:
        """Get fallback content for emergency situations."""
        return self._load_fallback_content()
```

---

## Token Efficiency

### Efficiency Comparison

| Approach            | Tokens | Load Time | Improvement       |
|---------------------|--------|-----------|-------------------|
| **Old**: Load all   | ~6,000 | ~2s       | Baseline          |
| **New**: Smart load | ~600   | ~200ms    | **90% reduction** |

### Four-Layer Progressive Loading

| Layer  | Directory           | Tokens       | Load Timing   | Timeout |
|--------|---------------------|--------------|---------------|---------|
| **L0** | index.md            | ~100         | Always        | 100ms   |
| **L1** | content/core/       | ~500         | Always        | 500ms   |
| **L2** | content/guidelines/ | ~100-200/ch  | On-demand     | 500ms   |
| **L3** | content/frameworks/ | ~300-500/doc | Complex tasks | 2s      |
| **L4** | content/practices/  | ~200-400/doc | On-demand     | 2s      |

### Smart Loading Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                    SMART LOADING                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Always Load (~600 tokens):                                 │
│  ┌─────────────┐  ┌─────────────────────────────┐          │
│  │  index.md   │  │  content/core/*.md          │          │
│  │  (~100)     │  │  (~500)                     │          │
│  └─────────────┘  └─────────────────────────────┘          │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  On-Demand (triggered by keywords):                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  guidelines/   frameworks/   practices/   scenarios/ │   │
│  │  (~1,200)      (~2,000)      (~1,500)     (~500)    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Total Available: ~6,000 tokens                             │
│  Default Load: ~600 tokens (10%)                            │
│  Maximum Load: ~4,000 tokens (with triggers)                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Smart Loading Triggers

### Trigger Configuration

```yaml
# sage.yaml - Smart Loading Configuration
loading:
  max_tokens: 4000
  default_layers: [ "core" ]

  triggers:
    - pattern: "code|style|format|lint"
      layers: [ "guidelines/02_code_style" ]
      priority: high

    - pattern: "test|pytest|coverage"
      layers: [ "guidelines/03_engineering" ]
      priority: high

    - pattern: "autonomy|decision|approval"
      layers: [ "frameworks/autonomy" ]
      priority: medium

    - pattern: "timeout|performance|slow"
      layers: [ "frameworks/timeout" ]
      priority: high

    - pattern: "expert|committee|review"
      layers: [ "frameworks/cognitive" ]
      priority: low

    - pattern: "python|backend|api"
      layers: [ "scenarios/python_backend" ]
      priority: medium
```

### Smart Loader Implementation

```python
# src/sage/core/smart_loader.py
"""
Smart Loader - Context-aware knowledge loading.
"""
import re
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
import yaml


@dataclass
class LoadTrigger:
    """Trigger for conditional content loading."""
    pattern: str
    layers: List[str]
    priority: str = "medium"

    def matches(self, query: str) -> bool:
        """Check if query matches this trigger."""
        return bool(re.search(self.pattern, query, re.IGNORECASE))


class SmartLoader:
    """
    Context-aware loader that selects content based on triggers.
    
    Features:
    - Keyword-based content selection
    - Priority-based loading order
    - Token budget management
    - Compression for efficiency
    """

    def __init__(self, config_path: Path = Path("sage.yaml")):
        self.config_path = config_path
        self.triggers: List[LoadTrigger] = []
        self.max_tokens = 4000
        self.default_layers = ["core"]
        self._load_config()

    def _load_config(self) -> None:
        """Load trigger configuration from YAML."""
        if not self.config_path.exists():
            return

        with open(self.config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

        loading = config.get("loading", {})
        self.max_tokens = loading.get("max_tokens", 4000)
        self.default_layers = loading.get("default_layers", ["core"])

        for trigger_config in loading.get("triggers", []):
            self.triggers.append(
                LoadTrigger(
                    pattern=trigger_config["pattern"],
                    layers=trigger_config["layers"],
                    priority=trigger_config.get("priority", "medium")
                )
            )

    def get_layers_for_query(self, query: str) -> List[str]:
        """
        Determine which layers to load based on query.
        
        Args:
            query: User query or task description
            
        Returns:
            List of layer paths to load
        """
        layers = list(self.default_layers)

        # Sort triggers by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_triggers = sorted(
            self.triggers,
            key=lambda t: priority_order.get(t.priority, 1)
        )

        # Add matching trigger layers
        for trigger in sorted_triggers:
            if trigger.matches(query):
                for layer in trigger.layers:
                    if layer not in layers:
                        layers.append(layer)

        return layers

    def estimate_tokens(self, layers: List[str]) -> int:
        """Estimate total tokens for given layers."""
        # Token estimates per layer type
        estimates = {
            "core"      : 500,
            "guidelines": 150,  # Per chapter
            "frameworks": 400,  # Per framework
            "practices" : 300,  # Per practice
            "scenarios" : 200,  # Per scenario
        }

        total = 0
        for layer in layers:
            base = layer.split("/")[0] if "/" in layer else layer
            total += estimates.get(base, 200)

        return total


class ContentCompressor:
    """Compress content for token efficiency."""

    @staticmethod
    def compress(content: str, target_tokens: int) -> str:
        """
        Compress content to fit within token budget.
        
        Strategies:
        1. Remove duplicate whitespace
        2. Summarize long sections
        3. Extract headers only for very long content
        """
        current_tokens = len(content) // 4

        if current_tokens <= target_tokens:
            return content

        # Strategy 1: Remove excessive whitespace
        compressed = re.sub(r'\n{3,}', '\n\n', content)
        compressed = re.sub(r' {2,}', ' ', compressed)

        if len(compressed) // 4 <= target_tokens:
            return compressed

        # Strategy 2: Keep only headers and first paragraph
        lines = compressed.split('\n')
        result = []
        for i, line in enumerate(lines):
            if line.startswith('#') or (i > 0 and lines[i - 1].startswith('#')):
                result.append(line)

        return '\n'.join(result)

    @staticmethod
    def extract_headers(content: str) -> str:
        """Extract only headers for lazy loading."""
        return '\n'.join(
            line for line in content.split('\n')
            if line.startswith('#')
        )
```

---

## Performance Benchmarks

### Target Metrics

| Metric             | Target | Measurement         |
|--------------------|--------|---------------------|
| Cache hit response | <50ms  | 95th percentile     |
| Core layer load    | <200ms | Average             |
| Full KB load       | <2s    | Worst case          |
| Timeout accuracy   | ±10%   | Of configured value |

### Benchmark Tests

```python
# tests/performance/bench_loader.py
"""
Performance benchmarks for the loader.
"""
import pytest
import asyncio
import time


@pytest.mark.benchmark
class TestLoaderPerformance:

    async def test_cache_hit_performance(self, loader):
        """Cache hit should be <50ms."""
        # Warm cache
        await loader.load_with_timeout(["core"])

        # Measure cached load
        start = time.monotonic()
        result = await loader.load_with_timeout(["core"])
        duration = (time.monotonic() - start) * 1000

        assert duration < 50, f"Cache hit took {duration}ms, expected <50ms"

    async def test_core_load_performance(self, loader, temp_content):
        """Core layer load should be <200ms."""
        start = time.monotonic()
        result = await loader.load_with_timeout(["core"])
        duration = (time.monotonic() - start) * 1000

        assert duration < 200, f"Core load took {duration}ms, expected <200ms"

    async def test_timeout_accuracy(self, loader):
        """Timeout should be accurate within ±10%."""
        timeout_ms = 1000

        start = time.monotonic()
        try:
            await asyncio.wait_for(
                loader._simulate_slow_operation(),
                timeout=timeout_ms / 1000
            )
        except asyncio.TimeoutError:
            pass

        duration = (time.monotonic() - start) * 1000
        expected_range = (timeout_ms * 0.9, timeout_ms * 1.1)

        assert expected_range[0] <= duration <= expected_range[1], \
            f"Timeout of {duration}ms outside expected range {expected_range}"
```

---

## References

- **Architecture**: See `01-architecture.md`
- **Services**: See `03-services.md`
- **Plugin System**: See `05-plugin-memory.md`

---

**Document Status**: Pending Level 5 Expert Committee Evaluation  
**Last Updated**: 2025-11-29
