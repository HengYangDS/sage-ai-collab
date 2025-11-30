# Data Pipeline Scenario Context

> Pre-configured context for data processing and ETL workflows

---

## Table of Contents

- [1. Scenario Profile](#1-scenario-profile)
- [2. Relevant Knowledge](#2-relevant-knowledge)
- [3. Project Structure](#3-project-structure)
- [4. Common Patterns](#4-common-patterns)
- [5. Testing Patterns](#5-testing-patterns)
- [6. Data Quality](#6-data-quality)
- [7. Common Tasks](#7-common-tasks)
- [8. Autonomy Calibration](#8-autonomy-calibration)
- [9. Quick Commands](#9-quick-commands)

---

## 1. Scenario Profile

```yaml
scenario: data_pipeline
languages: [ python, sql ]
frameworks: [ pandas, polars, dbt, airflow, prefect ]
focus: [ etl, transformation, validation, scheduling ]
autonomy_default: L2
```
---

## 2. Relevant Knowledge

| Priority      | Files                                                                                     |
|---------------|-------------------------------------------------------------------------------------------|
| **Auto-Load** | `core/PRINCIPLES.md`<br/>`.knowledge/guidelines/PYTHON.md`<br/>`.knowledge/practices/engineering/design/ERROR_HANDLING.md` |
| **On-Demand** | `.knowledge/practices/engineering/operations/LOGGING.md`<br/>`.knowledge/practices/engineering/quality/TESTING_STRATEGY.md`          |

---

## 3. Project Structure

| Directory           | Purpose                 |
|---------------------|-------------------------|
| `src/extractors/`   | Data extraction modules |
| `src/transformers/` | Transformation logic    |
| `src/loaders/`      | Data loading modules    |
| `src/validators/`   | Data quality checks     |
| `src/models/`       | Data models and schemas |
| `src/utils/`        | Utility functions       |
| `dags/`             | Airflow DAG definitions |
| `sql/`              | SQL transformations     |
| `tests/`            | Test suite              |
| `config/`           | Pipeline configurations |

---

## 4. Common Patterns

### 4.1 Extractor Pattern

```python
from abc import ABC, abstractmethod
from typing import Iterator
import pandas as pd
class BaseExtractor(ABC):
    """Base class for data extractors."""
    def __init__(self, config: dict):
        self.config = config
    @abstractmethod
    def extract(self) -> Iterator[pd.DataFrame]:
        """Extract data in chunks."""
        pass
    def validate_source(self) -> bool:
        """Validate source accessibility."""
        return True
class DatabaseExtractor(BaseExtractor):
    """Extract data from database."""
    def __init__(self, config: dict):
        super().__init__(config)
        self.connection = self._create_connection()
    def extract(self) -> Iterator[pd.DataFrame]:
        query = self.config["query"]
        chunk_size = self.config.get("chunk_size", 10000)
        for chunk in pd.read_sql(query, self.connection, chunksize=chunk_size):
            yield chunk
```
### 4.2 Transformer Pattern

```python
from typing import Callable
import pandas as pd
class DataTransformer:
    """Chain transformations on data."""
    def __init__(self):
        self._transforms: list[Callable] = []
    def add(self, transform: Callable) -> "DataTransformer":
        """Add transformation to chain."""
        self._transforms.append(transform)
        return self
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply all transformations."""
        result = df.copy()
        for transform in self._transforms:
            result = transform(result)
        return result
# Usage
transformer = (
    DataTransformer()
    .add(lambda df: df.dropna())
    .add(lambda df: df.rename(columns=str.lower))
    .add(normalize_dates)
)
result = transformer.apply(raw_data)
```
### 4.3 Loader Pattern

```python
from enum import Enum
import pandas as pd
class LoadMode(Enum):
    APPEND = "append"
    REPLACE = "replace"
    UPSERT = "upsert"
class DataLoader:
    """Load data to destination."""
    def __init__(self, connection, table: str, mode: LoadMode = LoadMode.APPEND):
        self.connection = connection
        self.table = table
        self.mode = mode
    def load(self, df: pd.DataFrame) -> int:
        """Load dataframe to destination."""
        if self.mode == LoadMode.REPLACE:
            self._truncate_table()
        elif self.mode == LoadMode.UPSERT:
            return self._upsert(df)
        rows = df.to_sql(
            self.table,
            self.connection,
            if_exists="append",
            index=False
        )
        return rows or len(df)
```
### 4.4 Pipeline Pattern

```python
from dataclasses import dataclass
from typing import Optional
import logging
@dataclass
class PipelineResult:
    success: bool
    rows_processed: int
    errors: list[str]
class Pipeline:
    """ETL Pipeline orchestration."""
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)
    def run(
        self,
        extractor: BaseExtractor,
        transformer: DataTransformer,
        loader: DataLoader,
    ) -> PipelineResult:
        """Execute the pipeline."""
        total_rows = 0
        errors = []
        try:
            for chunk in extractor.extract():
                transformed = transformer.apply(chunk)
                rows = loader.load(transformed)
                total_rows += rows
                self.logger.info(f"Processed {rows} rows")
        except Exception as e:
            errors.append(str(e))
            self.logger.error(f"Pipeline failed: {e}")
        return PipelineResult(
            success=len(errors) == 0,
            rows_processed=total_rows,
            errors=errors
        )
```
---

## 5. Testing Patterns

### 5.1 Transformer Testing

```python
import pytest
import pandas as pd
from transformers import DataTransformer, normalize_dates
@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "date" : ["2025-01-01", "2025-01-02"],
            "VALUE": [100, 200],
            "name" : ["Alice", None]
        }
    )
def test_transformer_chain(sample_data):
    transformer = (
        DataTransformer()
        .add(lambda df: df.dropna())
        .add(lambda df: df.rename(columns=str.lower))
    )
    result = transformer.apply(sample_data)
    assert len(result) == 1
    assert "value" in result.columns
    assert "VALUE" not in result.columns
def test_normalize_dates(sample_data):
    result = normalize_dates(sample_data)
    assert pd.api.types.is_datetime64_any_dtype(result["date"])
```
### 5.2 Pipeline Integration Testing

```python
import pytest
from unittest.mock import Mock, patch
def test_pipeline_success():
    # Arrange
    extractor = Mock()
    extractor.extract.return_value = [pd.DataFrame({"a": [1, 2]})]
    transformer = Mock()
    transformer.apply.return_value = pd.DataFrame({"a": [1, 2]})
    loader = Mock()
    loader.load.return_value = 2
    pipeline = Pipeline("test")
    # Act
    result = pipeline.run(extractor, transformer, loader)
    # Assert
    assert result.success
    assert result.rows_processed == 2
    assert len(result.errors) == 0
```
---

## 6. Data Quality

### 6.1 Validation Rules

| Check Type       | Example                           |
|------------------|-----------------------------------|
| **Null check**   | `df["id"].notna().all()`          |
| **Unique check** | `df["id"].is_unique`              |
| **Range check**  | `df["age"].between(0, 150).all()` |
| **Format check** | `df["email"].str.match(r".*@.*")` |
| **Referential**  | Foreign key exists                |

### 6.2 Validation Framework

```python
from dataclasses import dataclass
from typing import Callable
import pandas as pd
@dataclass
class ValidationResult:
    passed: bool
    message: str
    failed_rows: int = 0
class DataValidator:
    """Validate data quality."""
    def __init__(self):
        self._rules: list[tuple[str, Callable]] = []
    def add_rule(self, name: str, check: Callable) -> "DataValidator":
        self._rules.append((name, check))
        return self
    def validate(self, df: pd.DataFrame) -> list[ValidationResult]:
        results = []
        for name, check in self._rules:
            try:
                passed, failed_count = check(df)
                results.append(ValidationResult(passed, name, failed_count))
            except Exception as e:
                results.append(ValidationResult(False, f"{name}: {e}"))
        return results
# Usage
validator = (
    DataValidator()
    .add_rule("id_not_null", lambda df: (df["id"].notna().all(), df["id"].isna().sum()))
    .add_rule("id_unique", lambda df: (df["id"].is_unique, df["id"].duplicated().sum()))
)
```
---

## 7. Common Tasks

| Task                   | Steps                                                  |
|------------------------|--------------------------------------------------------|
| **Add Extractor**      | Create class → Implement extract() → Add config → Test |
| **Add Transformation** | Define function → Add to chain → Test with sample data |
| **Add Validation**     | Define rule → Add to validator → Set failure action    |
| **Schedule Pipeline**  | Create DAG → Set schedule → Configure alerts           |
| **Add Data Source**    | Define connection → Create extractor → Update config   |

---

## 8. Autonomy Calibration

| Task Type                | Level | Notes                      |
|--------------------------|-------|----------------------------|
| Add transformation       | L3-L4 | Test thoroughly            |
| Modify schema            | L1-L2 | Breaking change risk       |
| Add validation rule      | L4    | Low risk, improves quality |
| Change extraction query  | L2-L3 | Verify data consistency    |
| Production deployment    | L1    | Full review required       |
| Performance optimization | L3    | Benchmark before/after     |
| Add new data source      | L2    | Security review needed     |

---

## 9. Quick Commands

| Category  | Commands                                            |
|-----------|-----------------------------------------------------|
| **Run**   | `python -m pipelines.main`<br/>`airflow dags trigger` |
| **Test**  | `pytest tests/`<br/>`pytest --cov=src`                |
| **Lint**  | `ruff check .`<br/>`mypy src/`                        |
| **DB**    | `dbt run`<br/>`dbt test`<br/>`alembic upgrade head`     |
| **Debug** | `python -m pipelines.debug --sample 100`            |

---

## Related

- `.knowledge/guidelines/PYTHON.md` — Python guidelines
- `.knowledge/practices/engineering/design/ERROR_HANDLING.md` — Error handling
- `.knowledge/practices/engineering/operations/LOGGING.md` — Logging practices
- `.knowledge/frameworks/resilience/TIMEOUT_PATTERNS.md` — Timeout patterns

---

*AI Collaboration Knowledge Base*

