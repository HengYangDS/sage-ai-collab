# CI/CD Practices

> Continuous Integration and Continuous Deployment best practices for the projects

---

## Table of Contents

- [1. Overview](#1-overview)

- [2. GitHub Actions](#2-github-actions)

- [3. Testing Pipeline](#3-testing-pipeline)

- [4. Quality Gates](#4-quality-gates)

- [5. Deployment Strategies](#5-deployment-strategies)

- [6. Secrets Management](#6-secrets-management)

---

## 1. Overview

### 1.1 CI/CD Philosophy

| Principle               | Description                            |

|-------------------------|----------------------------------------|

| **Automate Everything** | Manual steps introduce errors          |

| **Fail Fast**           | Catch issues early in the pipeline     |

| **Keep It Simple**      | Complex pipelines are hard to maintain |

| **Version Everything**  | Config as code, reproducible builds    |

### 1.2 Pipeline Stages

```mermaid
flowchart LR
    L["Lint<br/>Ruff, MyPy"] --> T["Test<br/>pytest, coverage"]
    T --> B["Build<br/>wheel, Docker"]
    B --> P["Publish<br/>PyPI, GHCR"]
    P --> D["Deploy<br/>Staging, Production"]
```
---

## 2. GitHub Actions

### 2.1 Basic CI Workflow

```yaml
# .github/workflows/ci.yml

name: CI

on:

  push:

    branches: [ main, develop ]

  pull_request:

    branches: [ main ]

jobs:

  lint:

    runs-on: ubuntu-latest

    steps:

      - uses: actions/checkout@v4

      - name: Set up Python

        uses: actions/setup-python@v5

        with:

          python-version: '3.12'

          cache: 'pip'

      - name: Install dependencies

        run: pip install ruff mypy

      - name: Run Ruff

        run: ruff check src/

      - name: Run MyPy

        run: mypy src/

  test:

    runs-on: ubuntu-latest

    strategy:

      matrix:

        python-version: [ '3.11', '3.12' ]

    steps:

      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}

        uses: actions/setup-python@v5

        with:

          python-version: ${{ matrix.python-version }}

          cache: 'pip'

      - name: Install dependencies

        run: pip install -e ".[dev]"

      - name: Run tests

        run: pytest --cov=src --cov-report=xml

      - name: Upload coverage

        uses: codecov/codecov-action@v4

        with:

          file: coverage.xml

```
### 2.2 Release Workflow

```yaml
# .github/workflows/release.yml

name: Release

on:

  push:

    tags:

      - 'v*'

jobs:

  build:

    runs-on: ubuntu-latest

    steps:

      - uses: actions/checkout@v4

      - name: Set up Python

        uses: actions/setup-python@v5

        with:

          python-version: '3.12'

      - name: Install build tools

        run: pip install build twine

      - name: Build package

        run: python -m build

      - name: Publish to PyPI

        env:

          TWINE_USERNAME: __token__

          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}

        run: twine upload dist/*

  docker:

    runs-on: ubuntu-latest

    permissions:

      contents: read

      packages: write

    steps:

      - uses: actions/checkout@v4

      - name: Log in to GHCR

        uses: docker/login-action@v3

        with:

          registry: ghcr.io

          username: ${{ github.actor }}

          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push

        uses: docker/build-push-action@v5

        with:

          context: .

          push: true

          tags: |

            ghcr.io/${{ github.repository }}:${{ github.ref_name }}

            ghcr.io/${{ github.repository }}:latest

```
### 2.3 Scheduled Jobs

```yaml
# .github/workflows/scheduled.yml

name: Scheduled Tasks

on:

  schedule:

    - cron: '0 0 * * 1'  # Weekly on Monday

jobs:

  dependency-check:

    runs-on: ubuntu-latest

    steps:

      - uses: actions/checkout@v4

      - name: Check for updates

        run: pip list --outdated

      - name: Security audit

        run: pip-audit

```
---

## 3. Testing Pipeline

### 3.1 Test Categories

| Category        | Scope                 | Speed  | When to Run    |

|-----------------|-----------------------|--------|----------------|

| **Unit**        | Single function/class | Fast   | Every commit   |

| **Integration** | Multiple components   | Medium | Every PR       |

| **E2E**         | Full system           | Slow   | Before release |

| **Performance** | Benchmarks            | Varies | Weekly/Release |

### 3.2 Test Configuration

```yaml
# pyproject.toml

[ tool.pytest.ini_options ]

  testpaths = ["tests"]

  addopts = [

  "-v",

  "--strict-markers",

  "--cov=src",

  "--cov-report=term-missing",

]

  markers = [

  "unit: Unit tests",

  "integration: Integration tests",

  "slow: Slow tests",

]

  [ tool.coverage.run ]

  branch = true

  source = ["src"]

  [ tool.coverage.report ]

  exclude_lines = [

  "pragma: no cover",

  "if TYPE_CHECKING:",

  "raise NotImplementedError",

]

```
### 3.3 Running Tests

```bash
# All tests

pytest

# Unit tests only

pytest -m unit

# With coverage

pytest --cov=src --cov-report=html

# Parallel execution

pytest -n auto

```
---

## 4. Quality Gates

### 4.1 Required Checks

| Check             | Tool       | Threshold          |

|-------------------|------------|--------------------|

| **Linting**       | Ruff       | No errors          |

| **Type Check**    | MyPy       | No errors          |

| **Test Coverage** | pytest-cov | ≥ 80%              |

| **Security**      | pip-audit  | No vulnerabilities |

| **Complexity**    | Ruff       | < 10 per function  |

### 4.2 Pre-commit Hooks

```yaml
# .pre-commit-config.yaml

repos:

  - repo: https://github.com/astral-sh/ruff-pre-commit

    rev: v0.7.0

    hooks:

      - id: ruff

        args: [ --fix ]

      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy

    rev: v1.13.0

    hooks:

      - id: mypy

        additional_dependencies: [ types-PyYAML ]

  - repo: https://github.com/commitizen-tools/commitizen

    rev: v3.29.0

    hooks:

      - id: commitizen

```
### 4.3 Branch Protection

```yaml
# Repository settings

branch_protection:

  main:

    required_status_checks:

      - lint

      - test

      - type-check

    required_reviews: 1

    dismiss_stale_reviews: true

    require_code_owner_reviews: true

```
---

## 5. Deployment Strategies

### 5.1 Environments

| Environment     | Purpose             | Deployment      |

|-----------------|---------------------|-----------------|

| **Development** | Local testing       | Manual          |

| **Staging**     | Integration testing | Auto on develop |

| **Production**  | Live system         | Manual approval |

### 5.2 Deployment Methods

#### Blue-Green Deployment

```mermaid
flowchart TB
    subgraph Servers
        B["Blue (v1.0)<br/>Active"]
        G["Green (v1.1)<br/>Standby"]
    end
    B --> LB["Load Balancer"]
    G --> LB
    LB --> T["Traffic"]
```
#### Rolling Update

```yaml
# kubernetes deployment

spec:

  strategy:

    type: RollingUpdate

    rollingUpdate:

      maxSurge: 1

      maxUnavailable: 0

```
### 5.3 Rollback Procedure

```bash
# Quick rollback to previous version

git revert HEAD

git push origin main

# Or deploy specific version

git checkout v1.0.0

# trigger deployment

```
---

## 6. Secrets Management

### 6.1 Secret Types

| Type             | Storage           | Example            |

|------------------|-------------------|--------------------|

| **API Keys**     | GitHub Secrets    | `PYPI_TOKEN`       |

| **Credentials**  | Vault/AWS Secrets | Database passwords |

| **Certificates** | Secure storage    | SSL/TLS certs      |

### 6.2 GitHub Secrets

```yaml
# Access in workflow

env:

  API_KEY: ${{ secrets.API_KEY }}

# Environment-specific secrets

environment: production

env:

  DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }}

```
### 6.3 Best Practices

- Never commit secrets to repository

- Rotate secrets regularly

- Use environment-specific secrets

- Audit secret access

- Use OIDC for cloud providers when possible

---

## Quick Reference

```bash
# Local CI simulation

pre-commit run --all-files

pytest --cov=src

mypy src/

# Trigger workflow manually

gh workflow run ci.yml

# View workflow runs

gh run list

# Download artifacts

gh run download <run-id>

```
---

## Related

- `.knowledge/practices/engineering/GIT_WORKFLOW.md` — Git workflow and versioning

- `.knowledge/practices/engineering/TESTING_STRATEGY.md` — Testing best practices

- `.knowledge/scenarios/devops/CONTEXT.md` — DevOps scenario context

- `.knowledge/templates/RUNBOOK.md` — Operational runbook template

---

*AI Collaboration Knowledge Base*

