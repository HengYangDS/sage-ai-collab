# Extending Capabilities

> Guide to creating and registering custom capabilities

---

## 1. Overview

This guide explains how to extend SAGE with custom capabilities following the established patterns and conventions.

---

## 2. Capability Architecture

### 2.1 Base Interface

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")

class Capability(ABC, Generic[TInput, TOutput]):
    """Base class for all capabilities."""
    
    name: str           # Unique identifier
    family: str         # One of: analyzers, checkers, monitors, converters, generators
    version: str = "1.0.0"
    
    @abstractmethod
    def execute(self, input: TInput, context: Context) -> TOutput:
        """Execute the capability."""
        pass
    
    def validate_input(self, input: TInput) -> bool:
        """Validate input before execution."""
        return True
    
    def on_error(self, error: Exception, input: TInput) -> TOutput | None:
        """Handle execution errors."""
        raise error
```

### 2.2 Context Object

```python
@dataclass
class Context:
    """Execution context passed to capabilities."""
    
    config: Config              # Configuration
    event_bus: EventBus         # Event publishing
    logger: Logger              # Logging
    timeout: Timeout            # Timeout settings
    metadata: dict[str, Any]    # Additional metadata
```

---

## 3. Creating a Custom Capability

### 3.1 Step-by-Step Process

| Step | Action | File |
|------|--------|------|
| 1 | Choose family | Determine which of 5 families fits |
| 2 | Define I/O types | Create input/output dataclasses |
| 3 | Implement class | Extend `Capability` base |
| 4 | Register | Add to capability registry |
| 5 | Configure | Add configuration options |
| 6 | Test | Write unit tests |
| 7 | Document | Add to family documentation |

### 3.2 Example: Custom Analyzer

```python
# src/sage/capabilities/analyzers/sentiment_analyzer.py

from dataclasses import dataclass
from sage.core.capability import Capability, Context

@dataclass
class SentimentInput:
    text: str
    language: str = "en"

@dataclass
class SentimentOutput:
    sentiment: str  # positive, negative, neutral
    confidence: float
    details: dict[str, float]

class SentimentAnalyzer(Capability[SentimentInput, SentimentOutput]):
    name = "sentiment_analyzer"
    family = "analyzers"
    version = "1.0.0"
    
    def execute(self, input: SentimentInput, context: Context) -> SentimentOutput:
        # Analyze sentiment
        scores = self._analyze(input.text, input.language)
        
        return SentimentOutput(
            sentiment=self._determine_sentiment(scores),
            confidence=max(scores.values()),
            details=scores
        )
    
    def _analyze(self, text: str, language: str) -> dict[str, float]:
        # Implementation details
        ...
    
    def _determine_sentiment(self, scores: dict[str, float]) -> str:
        # Determine overall sentiment
        ...
```

---

## 4. Registration

### 4.1 Automatic Registration

```python
# Use decorator for automatic registration
from sage.core.registry import register_capability

@register_capability
class SentimentAnalyzer(Capability[SentimentInput, SentimentOutput]):
    name = "sentiment_analyzer"
    family = "analyzers"
    ...
```

### 4.2 Manual Registration

```python
# Or register manually in module __init__.py
from sage.core.registry import CapabilityRegistry
from .sentiment_analyzer import SentimentAnalyzer

def register(registry: CapabilityRegistry):
    registry.register(SentimentAnalyzer())
```

### 4.3 Plugin-Based Registration

```python
# Via plugin manifest
# plugins/my_plugin/manifest.yaml
name: my_plugin
version: 1.0.0
capabilities:
  - name: sentiment_analyzer
    class: my_plugin.analyzers.SentimentAnalyzer
    family: analyzers
```

---

## 5. Configuration

### 5.1 Capability Configuration

```yaml
# config/capabilities.yaml
capabilities:
  analyzers:
    sentiment_analyzer:
      enabled: true
      default_language: en
      confidence_threshold: 0.7
      cache_results: true
```

### 5.2 Accessing Configuration

```python
class SentimentAnalyzer(Capability[SentimentInput, SentimentOutput]):
    def execute(self, input: SentimentInput, context: Context) -> SentimentOutput:
        # Access configuration
        threshold = context.config.get(
            "capabilities.analyzers.sentiment_analyzer.confidence_threshold",
            default=0.7
        )
        ...
```

---

## 6. Error Handling

### 6.1 Error Types

| Error | When | Handling |
|-------|------|----------|
| `ValidationError` | Invalid input | Return None or default |
| `TimeoutError` | Execution timeout | Use cached result |
| `ResourceError` | Missing resource | Graceful degradation |
| `ExecutionError` | Runtime failure | Log and retry |

### 6.2 Error Handler Implementation

```python
class SentimentAnalyzer(Capability[SentimentInput, SentimentOutput]):
    def validate_input(self, input: SentimentInput) -> bool:
        if not input.text:
            raise ValidationError("Text cannot be empty")
        if len(input.text) > 10000:
            raise ValidationError("Text too long")
        return True
    
    def on_error(self, error: Exception, input: SentimentInput) -> SentimentOutput:
        if isinstance(error, TimeoutError):
            # Return cached or default result
            return SentimentOutput(
                sentiment="neutral",
                confidence=0.0,
                details={}
            )
        raise error
```

---

## 7. Testing

### 7.1 Unit Test Structure

```python
# tests/capabilities/analyzers/test_sentiment_analyzer.py

import pytest
from sage.capabilities.analyzers import SentimentAnalyzer

class TestSentimentAnalyzer:
    def setup_method(self):
        self.analyzer = SentimentAnalyzer()
        self.context = create_test_context()
    
    def test_positive_sentiment(self):
        input = SentimentInput(text="I love this!")
        result = self.analyzer.execute(input, self.context)
        assert result.sentiment == "positive"
        assert result.confidence > 0.7
    
    def test_invalid_input(self):
        input = SentimentInput(text="")
        with pytest.raises(ValidationError):
            self.analyzer.execute(input, self.context)
```

---

## 8. Best Practices

### 8.1 Design Principles

| Principle | Description |
|-----------|-------------|
| **Single Responsibility** | One capability, one purpose |
| **Stateless** | No shared state between executions |
| **Idempotent** | Same input → same output |
| **Timeout-Aware** | Respect timeout constraints |
| **Configurable** | Externalize parameters |

### 8.2 Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Class | PascalCase + purpose | `SentimentAnalyzer` |
| Name attribute | snake_case | `sentiment_analyzer` |
| Input class | PascalCase + Input | `SentimentInput` |
| Output class | PascalCase + Output | `SentimentOutput` |

---

## 9. Family-Specific Guidelines

| Family | Input Focus | Output Focus | Key Concern |
|--------|-------------|--------------|-------------|
| **analyzers** | Content | Insights | Accuracy |
| **checkers** | Content | Pass/Fail | Completeness |
| **monitors** | System state | Metrics | Real-time |
| **converters** | Source format | Target format | Fidelity |
| **generators** | Specification | Artifact | Consistency |

---

## Related

- `CAPABILITY_MODEL.md` — Capability system overview
- `ANALYZERS.md` — Analyzer examples
- `../plugins/EXTENSION_POINTS.md` — Plugin extension points
- `../core_engine/DI_CONTAINER.md` — Dependency injection

---

*AI Collaboration Knowledge Base*
