# SAGE Test Suite

> Comprehensive testing guide for SAGE Knowledge Base

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Running Tests](#2-running-tests)
- [3. Test Structure](#3-test-structure)
- [4. Writing Tests](#4-writing-tests)
- [5. Fixtures](#5-fixtures)
- [6. Performance Tests](#6-performance-tests)
- [7. CI Integration](#7-ci-integration)

---

## 1. Overview

### Test Categories

| Category        | Location             | Purpose               | Run Time        |
|-----------------|----------------------|-----------------------|-----------------|
| **Unit**        | `tests/unit/`        | Component isolation   | Fast (<1s each) |
| **Integration** | `tests/integration/` | Component interaction | Medium (1-5s)   |
| **Performance** | `tests/performance/` | Benchmarks & stress   | Slow (5-30s)    |

### Test Statistics

```
tests/
├── unit/           # ~800 tests
├── integration/    # ~30 tests
└── performance/    # ~15 benchmarks
```

---

## 2. Running Tests

### Quick Commands

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=sage --cov-report=html

# Run specific category
pytest tests/unit/
pytest tests/integration/
pytest tests/performance/

# Run specific module
pytest tests/unit/core/test_loader.py

# Run specific test
pytest tests/unit/core/test_loader.py::test_load_core_success
```

### Common Options

```bash
# Verbose output
pytest tests/ -v

# Show print statements
pytest tests/ -s

# Stop on first failure
pytest tests/ -x

# Run last failed tests
pytest tests/ --lf

# Parallel execution
pytest tests/ -n auto

# With markers
pytest tests/ -m "not slow"
pytest tests/ -m "integration"
```

### Test Markers

| Marker                     | Description       | Usage                   |
|----------------------------|-------------------|-------------------------|
| `@pytest.mark.unit`        | Unit tests        | Default                 |
| `@pytest.mark.integration` | Integration tests | `pytest -m integration` |
| `@pytest.mark.performance` | Performance tests | `pytest -m performance` |
| `@pytest.mark.slow`        | Slow tests (>5s)  | `pytest -m "not slow"`  |
| `@pytest.mark.asyncio`     | Async tests       | Auto-detected           |

---

## 3. Test Structure

### Directory Layout

```
tests/
├── conftest.py                 # Global fixtures
├── fixtures/
│   ├── configs/               # Test configuration files
│   │   └── test_sage.yaml
│   ├── mock_responses/        # Mocked API responses
│   │   └── mcp_responses.json
│   └── sample_.knowledge/        # Test content files
│       └── core/
│           └── test_principles.md
├── unit/
│   ├── capabilities/
│   │   ├── analyzers/
│   │   │   └── test_code_analyzer.py
│   │   ├── checkers/
│   │   │   └── test_quality_checker.py
│   │   └── monitors/
│   │       └── test_health_monitor.py
│   ├── core/
│   │   ├── di/
│   │   │   └── test_container.py
│   │   ├── events/
│   │   │   └── test_event_bus.py
│   │   ├── logging/
│   │   │   └── test_structured_logging.py
│   │   ├── memory/
│   │   │   └── test_memory_store.py
│   │   └── test_loader.py
│   ├── plugins/
│   │   └── test_plugin_manager.py
│   └── services/
│       ├── test_cli_service.py
│       └── test_mcp_service.py
├── integration/
│   ├── test_cli_e2e.py
│   ├── test_loader_e2e.py
│   └── test_mcp_e2e.py
└── performance/
    ├── benchmarks/
    │   └── baseline.json
    ├── test_load_performance.py
    ├── test_search_performance.py
    ├── test_timeout_stress.py
    └── test_token_efficiency.py
```

### Naming Conventions

| Element        | Convention  | Example                         |
|----------------|-------------|---------------------------------|
| Test files     | `test_*.py` | `test_loader.py`                |
| Test classes   | `Test*`     | `TestKnowledgeLoader`           |
| Test functions | `test_*`    | `test_load_core_success`        |
| Fixtures       | Descriptive | `sample_content`, `mock_loader` |

---

## 4. Writing Tests

### Unit Test Example

```python
# tests/unit/core/test_loader.py
import pytest
from sage.core.loader import KnowledgeLoader
from sage.core.exceptions import LoadError

class TestKnowledgeLoader:
    """Tests for KnowledgeLoader."""
    
    @pytest.fixture
    def loader(self, tmp_path):
        """Create loader with test content."""
        return KnowledgeLoader(content_path=tmp_path)
    
    def test_load_core_success(self, loader, sample_content):
        """Test successful core layer loading."""
        result = loader.load_sync("core")
        
        assert result is not None
        assert "principles" in result.content
        assert result.tokens > 0
    
    def test_load_nonexistent_layer(self, loader):
        """Test loading non-existent layer raises error."""
        with pytest.raises(LoadError) as exc_info:
            loader.load_sync("nonexistent")
        
        assert "not found" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_load_async(self, loader, sample_content):
        """Test async loading."""
        result = await loader.load("core", timeout_ms=2000)
        
        assert result.content is not None
```

### Integration Test Example

```python
# tests/integration/test_cli_e2e.py
import pytest
from typer.testing import CliRunner
from sage.services.cli import app

runner = CliRunner()

class TestCLIEndToEnd:
    """End-to-end CLI tests."""
    
    def test_get_core_command(self):
        """Test 'sage get core' command."""
        result = runner.invoke(app, ["get", "core"])
        
        assert result.exit_code == 0
        assert "principles" in result.stdout.lower()
    
    def test_search_command(self):
        """Test 'sage search' command."""
        result = runner.invoke(app, ["search", "timeout"])
        
        assert result.exit_code == 0
        assert len(result.stdout) > 0
    
    def test_info_command(self):
        """Test 'sage info' command."""
        result = runner.invoke(app, ["info"])
        
        assert result.exit_code == 0
        assert "version" in result.stdout.lower()
```

### Async Test Example

```python
# tests/unit/core/test_timeout.py
import pytest
import asyncio
from sage.core.timeout import TimeoutManager, TimeoutLevel

class TestTimeoutManager:
    """Tests for TimeoutManager."""
    
    @pytest.fixture
    def timeout_mgr(self):
        return TimeoutManager()
    
    @pytest.mark.asyncio
    async def test_execute_within_timeout(self, timeout_mgr):
        """Test operation completes within timeout."""
        async def fast_operation():
            await asyncio.sleep(0.01)
            return "done"
        
        result = await timeout_mgr.execute(
            fast_operation(),
            level=TimeoutLevel.T2
        )
        
        assert result == "done"
    
    @pytest.mark.asyncio
    async def test_execute_timeout_exceeded(self, timeout_mgr):
        """Test timeout exception when exceeded."""
        async def slow_operation():
            await asyncio.sleep(10)
            return "done"
        
        with pytest.raises(asyncio.TimeoutError):
            await timeout_mgr.execute(
                slow_operation(),
                level=TimeoutLevel.T1  # 100ms
            )
```

---

## 5. Fixtures

### Global Fixtures (conftest.py)

```python
# tests/conftest.py
import pytest
from pathlib import Path

@pytest.fixture(scope="session")
def project_root():
    """Return project root directory."""
    return Path(__file__).parent.parent

@pytest.fixture(scope="session")
def content_path(project_root):
    """Return content directory path."""
    return project_root / "content"

@pytest.fixture
def sample_content(tmp_path):
    """Create sample content for testing."""
    core_dir = tmp_path / "core"
    core_dir.mkdir()
    
    (core_dir / "principles.md").write_text("""
# Core Principles

Test principles content.
""")
    
    return tmp_path

@pytest.fixture
def mock_config():
    """Return mock configuration."""
    return {
        "timeout": {
            "operations": {
                "cache_lookup": "100ms",
                "file_read": "500ms",
            }
        }
    }
```

### Fixture Files

**Test Configuration (`fixtures/configs/test_sage.yaml`):**

```yaml
# Minimal test configuration
timeout:
  operations:
    cache_lookup: 50ms
    file_read: 200ms
    layer_load: 1000ms

logging:
  level: DEBUG
  
knowledge:
  content_path: tests/fixtures/sample_content
```

**Sample Content (`fixtures/sample_.knowledge/core/test_principles.md`):**

```markdown
# Test Principles

> Test content for unit tests

## Principle 1

Test principle content.
```

### Using Fixtures

```python
# Access fixture in test
def test_with_fixture(sample_content, mock_config):
    loader = KnowledgeLoader(
        content_path=sample_content,
        config=mock_config
    )
    result = loader.load_sync("core")
    assert result is not None

# Parametrized fixtures
@pytest.fixture(params=["core", "guidelines", "frameworks"])
def layer_name(request):
    return request.param

def test_all_layers(layer_name, loader):
    result = loader.load_sync(layer_name)
    assert result is not None
```

---

## 6. Performance Tests

### Benchmark Structure

```python
# tests/performance/test_load_performance.py
import pytest
from sage.core.loader import KnowledgeLoader

class TestLoadPerformance:
    """Performance benchmarks for loading."""
    
    @pytest.mark.performance
    def test_core_load_time(self, benchmark, loader):
        """Benchmark core layer load time."""
        result = benchmark(loader.load_sync, "core")
        
        assert result is not None
        # Assert P95 < 500ms (T2 timeout)
        assert benchmark.stats["mean"] < 0.5
    
    @pytest.mark.performance
    def test_full_load_time(self, benchmark, loader):
        """Benchmark full knowledge base load."""
        def load_all():
            return loader.load_all_sync()
        
        result = benchmark(load_all)
        
        # Assert P95 < 5s (T4 timeout)
        assert benchmark.stats["mean"] < 5.0
```

### Running Benchmarks

```bash
# Run performance tests
pytest tests/performance/ -v

# With benchmark output
pytest tests/performance/ --benchmark-only

# Compare with baseline
pytest tests/performance/ --benchmark-compare=baseline.json

# Save new baseline
pytest tests/performance/ --benchmark-save=baseline
```

### Stress Tests

```python
# tests/performance/test_timeout_stress.py
import pytest
import asyncio
from sage.core.timeout import TimeoutManager

class TestTimeoutStress:
    """Stress tests for timeout handling."""
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_concurrent_operations(self, timeout_mgr):
        """Test many concurrent operations."""
        async def operation(n):
            await asyncio.sleep(0.01)
            return n
        
        tasks = [
            timeout_mgr.execute(operation(i), level="T2")
            for i in range(100)
        ]
        
        results = await asyncio.gather(*tasks)
        assert len(results) == 100
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_circuit_breaker_recovery(self, timeout_mgr):
        """Test circuit breaker under stress."""
        failures = 0
        successes = 0
        
        for i in range(50):
            try:
                await timeout_mgr.execute(
                    self._maybe_fail(i),
                    level="T1"
                )
                successes += 1
            except Exception:
                failures += 1
        
        # Circuit breaker should prevent cascade
        assert successes > failures
```

---

## 7. CI Integration

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.12', '3.13', '3.14']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: pip install -e ".[dev]"
      
      - name: Run tests
        run: pytest tests/ --cov=sage --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
```

### Coverage Requirements

| Module              | Minimum Coverage |
|---------------------|------------------|
| `sage.core`         | 90%              |
| `sage.services`     | 85%              |
| `sage.capabilities` | 80%              |
| Overall             | 85%              |

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: pytest tests/unit/ -x --tb=short
        language: system
        pass_filenames: false
        always_run: true
```

---

## Quick Reference

| Task               | Command                                 |
|--------------------|-----------------------------------------|
| Run all tests      | `pytest tests/`                         |
| Run with coverage  | `pytest tests/ --cov=sage`              |
| Run unit tests     | `pytest tests/unit/`                    |
| Run fast tests     | `pytest tests/ -m "not slow"`           |
| Run specific file  | `pytest tests/unit/core/test_loader.py` |
| Debug failing test | `pytest tests/ -x -v --tb=long`         |
| Parallel execution | `pytest tests/ -n auto`                 |

---

## Related

- `docs/guides/advanced.md` — Advanced usage
- `.knowledge/practices/engineering/testing_strategy.md` — Testing strategy
- `.github/workflows/ci.yml` — CI configuration
- `pyproject.toml` — pytest configuration

---


---

*AI Collaboration Knowledge Base*
