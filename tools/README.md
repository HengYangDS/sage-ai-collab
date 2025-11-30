---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---

# SAGE Development Tools

> Utilities and scripts for SAGE Knowledge Base development

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Development Scripts](#2-development-scripts)
- [3. Knowledge Graph](#3-knowledge-graph)
- [4. Monitors](#4-monitors)
- [5. Migration Toolkit](#5-migration-toolkit)
- [6. Timeout Manager](#6-timeout-manager)

---

## 1. Overview

```
tools/
├── dev_scripts/
│   └── setup_dev.py          # Development environment setup
├── knowledge_graph/
│   └── knowledge_graph_builder.py  # Knowledge graph visualization
├── monitors/
│   └── timeout_monitor.py    # Real-time timeout monitoring
├── migration_toolkit.py      # Content migration utilities
└── timeout_manager.py        # Timeout testing and tuning
```

---

## 2. Development Scripts

### setup_dev.py

Sets up the development environment with all necessary dependencies and configurations.

**Usage:**

```bash
# Full setup
python tools/dev_scripts/setup_dev.py

# Setup with options
python tools/dev_scripts/setup_dev.py --skip-hooks  # Skip pre-commit hooks
python tools/dev_scripts/setup_dev.py --minimal     # Minimal setup
python tools/dev_scripts/setup_dev.py --reset       # Reset to clean state
```

**What it does:**

1. Creates virtual environment (if not exists) - conda recommended, venv as fallback
2. Installs all dependencies (`pip install -e ".[dev]"`)
3. Sets up pre-commit hooks
4. Creates necessary directories (`.logs/`, `.outputs/`, `.cache/`)
5. Validates configuration files
6. Runs initial test suite

**Environment Variables:**

| Variable              | Description                         | Default |
|-----------------------|-------------------------------------|---------|
| `SAGE_DEV_VENV`       | Virtual environment path (for venv) | `.venv` |
| `SAGE_DEV_SKIP_TESTS` | Skip initial tests                  | `false` |

---

## 3. Knowledge Graph

### knowledge_graph_builder.py

Builds and visualizes the knowledge graph from content files.

**Usage:**

```bash
# Build graph from content directory
python tools/knowledge_graph/knowledge_graph_builder.py

# With options
python tools/knowledge_graph/knowledge_graph_builder.py \
    --source .knowledge/ \
    --output .outputs/knowledge_graph.json \
    --format json

# Generate visualization
python tools/knowledge_graph/knowledge_graph_builder.py \
    --visualize \
    --output .outputs/graph.html
```

**Features:**

- **Node extraction**: Identifies knowledge nodes from markdown files
- **Relationship mapping**: Detects cross-references and dependencies
- **Clustering**: Groups related content by topic
- **Export formats**: JSON, GraphML, DOT, HTML visualization

**Output Formats:**

| Format  | File            | Use Case               |
|---------|-----------------|------------------------|
| JSON    | `graph.json`    | API consumption        |
| GraphML | `graph.graphml` | Graph analysis tools   |
| DOT     | `graph.dot`     | Graphviz visualization |
| HTML    | `graph.html`    | Interactive web view   |

**Example Output (JSON):**

```json
{
  "nodes": [
    {
      "id": "core/principles",
      "label": "Core Principles",
      "type": "content",
      "layer": "core",
      "tokens": 450
    }
  ],
  "edges": [
    {
      "source": "guidelines/python",
      "target": "core/principles",
      "type": "references"
    }
  ]
}
```

---

## 4. Monitors

### timeout_monitor.py

Real-time monitoring of timeout events and circuit breaker status.

**Usage:**

```bash
# Start monitoring
python tools/monitors/timeout_monitor.py

# With options
python tools/monitors/timeout_monitor.py \
    --interval 1000 \      # Update interval in ms
    --level T2 \           # Filter by timeout level
    --output .logs/timeouts.log

# Dashboard mode
python tools/monitors/timeout_monitor.py --dashboard
```

**Dashboard Output:**

```
╔══════════════════════════════════════════════════════════════╗
║                    SAGE Timeout Monitor                       ║
╠══════════════════════════════════════════════════════════════╣
║ Level │ Threshold │ Current │ Avg (1m) │ Timeouts │ Status   ║
╠═══════╪═══════════╪═════════╪══════════╪══════════╪══════════╣
║ T1    │ 100ms     │ 45ms    │ 52ms     │ 0        │ ✓ OK     ║
║ T2    │ 500ms     │ 230ms   │ 280ms    │ 2        │ ✓ OK     ║
║ T3    │ 2s        │ 1.2s    │ 1.4s     │ 0        │ ✓ OK     ║
║ T4    │ 5s        │ 3.1s    │ 3.5s     │ 1        │ ⚠ WARN   ║
║ T5    │ 10s       │ --      │ --       │ 0        │ ✓ OK     ║
╠══════════════════════════════════════════════════════════════╣
║ Circuit Breaker: CLOSED │ Failures: 1/3 │ Recovery: --       ║
╚══════════════════════════════════════════════════════════════╝
```

**Alerts:**

```bash
# Configure alerts
python tools/monitors/timeout_monitor.py \
    --alert-threshold 5 \    # Alert after 5 timeouts
    --alert-email admin@example.com
```

---

## 5. Migration Toolkit

### migration_toolkit.py

Utilities for migrating content between versions and formats.

**Usage:**

```bash
# Check migration status
python tools/migration_toolkit.py status

# Migrate content structure
python tools/migration_toolkit.py migrate \
    --from-version 0.0.x \
    --to-version 0.1.0

# Validate migrated content
python tools/migration_toolkit.py validate

# Rollback if needed
python tools/migration_toolkit.py rollback --to-backup backup_20251129
```

**Migration Commands:**

| Command    | Description                                 |
|------------|---------------------------------------------|
| `status`   | Show current version and pending migrations |
| `migrate`  | Run migration to target version             |
| `validate` | Validate content after migration            |
| `rollback` | Revert to previous backup                   |
| `backup`   | Create manual backup before migration       |

**Example Migration:**

```bash
# Step 1: Check what needs migrating
python tools/migration_toolkit.py status
# Output: Current: 0.0.9, Target: 0.1.0, Pending: 3 migrations

# Step 2: Create backup
python tools/migration_toolkit.py backup --name pre-migration

# Step 3: Run migration
python tools/migration_toolkit.py migrate --to-version 0.1.0

# Step 4: Validate
python tools/migration_toolkit.py validate
# Output: ✓ All content valid

# Step 5: If issues, rollback
python tools/migration_toolkit.py rollback --to-backup pre-migration
```

**Migration Types:**

- **Structure**: Directory reorganization
- **Format**: Markdown frontmatter changes
- **Config**: Configuration file updates
- **Index**: Search index rebuilding

---

## 6. Timeout Manager

### timeout_manager.py

Testing and tuning utility for timeout configurations.

**Usage:**

```bash
# Run timeout tests
python tools/timeout_manager.py test

# Benchmark operations
python tools/timeout_manager.py benchmark \
    --operation file_read \
    --iterations 100

# Tune timeouts based on benchmarks
python tools/timeout_manager.py tune \
    --target-percentile 95 \
    --output config/core/timeout.yaml

# Stress test
python tools/timeout_manager.py stress \
    --duration 60s \
    --concurrency 10
```

**Test Output:**

```
Timeout Level Tests
═══════════════════════════════════════════════════════════════
Level │ Operation      │ Threshold │ P50    │ P95    │ P99    │ Result
──────┼────────────────┼───────────┼────────┼────────┼────────┼────────
T1    │ cache_lookup   │ 100ms     │ 12ms   │ 45ms   │ 78ms   │ ✓ PASS
T2    │ file_read      │ 500ms     │ 120ms  │ 340ms  │ 480ms  │ ✓ PASS
T3    │ layer_load     │ 2000ms    │ 850ms  │ 1600ms │ 1900ms │ ✓ PASS
T4    │ full_load      │ 5000ms    │ 2100ms │ 3800ms │ 4500ms │ ✓ PASS
T5    │ analysis       │ 10000ms   │ 4200ms │ 7500ms │ 9200ms │ ✓ PASS
═══════════════════════════════════════════════════════════════
Overall: 5/5 PASSED
```

**Tuning Recommendations:**

```bash
python tools/timeout_manager.py tune --recommend
# Output:
# Recommended timeout adjustments:
#   T1: 100ms → 80ms   (headroom: 22ms)
#   T2: 500ms → 400ms  (headroom: 60ms)
#   T3: 2000ms → 1800ms (headroom: 200ms)
#   T4: No change recommended
#   T5: No change recommended
```

---

## Common Workflows

### Setting Up Development

```bash
# 1. Clone repository
git clone https://github.com/HengYangDS/sage-kb.git
cd sage-kb

# 2. Setup conda environment (recommended)
conda env create -f environment.yml
conda activate sage-kb

# Or use venv as alternative:
# python -m venv .venv
# source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate     # Windows

# 3. Run setup script
python tools/dev_scripts/setup_dev.py

# 4. Verify setup
sage info
pytest tests/ -v --tb=short
```

### Analyzing Knowledge Structure

```bash
# 1. Build knowledge graph
python tools/knowledge_graph/knowledge_graph_builder.py --visualize

# 2. Open visualization
open .outputs/graph.html  # or start on Windows
```

### Performance Tuning

```bash
# 1. Benchmark current performance
python tools/timeout_manager.py benchmark --all

# 2. Start monitoring
python tools/monitors/timeout_monitor.py --dashboard &

# 3. Run workload
sage get core guidelines frameworks

# 4. Get tuning recommendations
python tools/timeout_manager.py tune --recommend
```

### Content Migration

```bash
# 1. Check status
python tools/migration_toolkit.py status

# 2. Backup
python tools/migration_toolkit.py backup

# 3. Migrate
python tools/migration_toolkit.py migrate --to-version X.Y.Z

# 4. Validate
python tools/migration_toolkit.py validate
```

---

## Related

- `docs/guides/ADVANCED.md` — Advanced usage guide
- `docs/design/04-TIMEOUT-LOADING.md` — Timeout design
- `config/core/timeout.yaml` — Timeout configuration
- `tests/performance/` — Performance tests

---

*SAGE Knowledge Base - Development Tools*
