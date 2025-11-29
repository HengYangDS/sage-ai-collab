# DevOps Scenario Context

> Pre-configured context for CI/CD, infrastructure, and operations

---

## Table of Contents

- [1. Scenario Profile](#1-scenario-profile)
- [2. Relevant Knowledge](#2-relevant-knowledge)
- [3. Project Structure](#3-project-structure)
- [4. CI/CD Patterns](#4-cicd-patterns)
- [5. Infrastructure as Code](#5-infrastructure-as-code)
- [6. Monitoring & Alerting](#6-monitoring--alerting)
- [7. Common Tasks](#7-common-tasks)
- [8. Autonomy Calibration](#8-autonomy-calibration)
- [9. Quick Commands](#9-quick-commands)

---

## 1. Scenario Profile

```yaml
scenario: devops
languages: [ yaml, bash, python, hcl ]
tools: [ docker, kubernetes, terraform, github-actions, gitlab-ci ]
focus: [ ci/cd, infrastructure, monitoring, security ]
autonomy_default: L2
```

---

## 2. Relevant Knowledge

| Priority      | Files                                                                                     |
|---------------|-------------------------------------------------------------------------------------------|
| **Auto-Load** | `core/principles.md` · `practices/engineering/error_handling.md` · `templates/runbook.md` |
| **On-Demand** | `practices/engineering/logging.md` · `frameworks/resilience/timeout_patterns.md`          |

---

## 3. Project Structure

| Directory         | Purpose                   |
|-------------------|---------------------------|
| `.github/`        | GitHub Actions workflows  |
| `.gitlab/`        | GitLab CI configuration   |
| `infrastructure/` | Terraform/IaC modules     |
| `kubernetes/`     | K8s manifests             |
| `docker/`         | Dockerfiles and compose   |
| `scripts/`        | Automation scripts        |
| `monitoring/`     | Dashboards, alerts config |
| `docs/runbooks/`  | Operational runbooks      |

---

## 4. CI/CD Patterns

### 4.1 GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Run tests
        run: pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Deploy to production
        run: |
          # Add deployment commands
          echo "Deploying version ${{ github.sha }}"
```

### 4.2 GitLab CI Pipeline

```yaml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

test:
  stage: test
  image: python:3.12
  script:
    - pip install -e ".[dev]"
    - pytest --cov=src
  coverage: '/TOTAL.*\s+(\d+%)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main

deploy:
  stage: deploy
  environment:
    name: production
    url: https://app.example.com
  script:
    - kubectl set image deployment/app app=$DOCKER_IMAGE
  only:
    - main
  when: manual
```

### 4.3 Multi-Stage Dockerfile

```dockerfile
# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app
COPY pyproject.toml .
COPY src/ src/

RUN pip install build && \
    python -m build --wheel

# Runtime stage
FROM python:3.12-slim AS runtime

WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Install from wheel
COPY --from=builder /app/dist/*.whl .
RUN pip install --user *.whl && rm *.whl

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

---

## 5. Infrastructure as Code

### 5.1 Terraform Module Structure

```hcl
# modules/app/main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "environment" {
  type        = string
  description = "Deployment environment"
}

variable "instance_type" {
  type    = string
  default = "t3.small"
}

resource "aws_instance" "app" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type
  
  tags = {
    Name        = "app-${var.environment}"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

output "instance_id" {
  value = aws_instance.app.id
}
```

### 5.2 Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: app
          image: ghcr.io/org/app:latest
          ports:
            - containerPort: 8000
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-url
---
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8000
  type: ClusterIP
```

---

## 6. Monitoring & Alerting

### 6.1 Key Metrics

| Category         | Metrics                                   |
|------------------|-------------------------------------------|
| **Availability** | Uptime %, Error rate, SLA compliance      |
| **Performance**  | Response time (p50, p95, p99), Throughput |
| **Resources**    | CPU, Memory, Disk, Network                |
| **Business**     | Active users, Transactions, Revenue       |

### 6.2 Alert Rules

| Severity     | Condition            | Response                 |
|--------------|----------------------|--------------------------|
| **Critical** | Service down > 1 min | Page on-call immediately |
| **High**     | Error rate > 5%      | Page within 5 min        |
| **Medium**   | Latency p99 > 2s     | Notify channel           |
| **Low**      | Disk > 80%           | Create ticket            |

### 6.3 Prometheus Alert Example

```yaml
groups:
  - name: app-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          / sum(rate(http_requests_total[5m])) > 0.05
        for: 2m
        labels:
          severity: high
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) > 2
        for: 5m
        labels:
          severity: medium
        annotations:
          summary: "High latency detected"
          description: "p99 latency is {{ $value }}s"
```

---

## 7. Common Tasks

| Task                    | Steps                                                      |
|-------------------------|------------------------------------------------------------|
| **Add CI job**          | Define job → Set triggers → Add steps → Test in branch     |
| **Create infra module** | Define variables → Write resources → Output values → Test  |
| **Add K8s resource**    | Write manifest → Apply to staging → Verify → Apply to prod |
| **Set up monitoring**   | Define metrics → Create dashboard → Add alerts             |
| **Add secret**          | Create in vault → Reference in config → Deploy             |

---

## 8. Autonomy Calibration

| Task Type                  | Level | Notes                       |
|----------------------------|-------|-----------------------------|
| Add CI test step           | L3-L4 | Low risk                    |
| Modify deployment config   | L2    | Production impact           |
| Change infrastructure      | L1-L2 | Full review required        |
| Update monitoring          | L3    | Improves observability      |
| Add new environment        | L2    | Security review needed      |
| Modify secrets/credentials | L1    | High security impact        |
| Scale resources            | L2-L3 | Cost and performance impact |
| Rollback deployment        | L2    | Use established procedures  |

---

## 9. Quick Commands

| Category      | Commands                                                   |
|---------------|------------------------------------------------------------|
| **Docker**    | `docker build -t app .` · `docker compose up -d`           |
| **K8s**       | `kubectl apply -f .` · `kubectl rollout status`            |
| **Terraform** | `terraform plan` · `terraform apply` · `terraform destroy` |
| **Debug**     | `kubectl logs -f` · `kubectl exec -it -- /bin/sh`          |
| **Secrets**   | `kubectl create secret` · `vault kv put`                   |

---

## Security Checklist

| Area        | Check                                             |
|-------------|---------------------------------------------------|
| **Secrets** | No hardcoded secrets, use vault/secrets manager   |
| **Images**  | Scan for vulnerabilities, use minimal base images |
| **Network** | Limit ingress/egress, use network policies        |
| **Access**  | RBAC configured, least privilege principle        |
| **Audit**   | Enable audit logging, monitor suspicious activity |

---

## Related

- `templates/runbook.md` — Operational runbook template
- `templates/postmortem.md` — Incident postmortem template
- `practices/engineering/error_handling.md` — Error handling
- `frameworks/resilience/timeout_patterns.md` — Resilience patterns

---

*Part of SAGE Knowledge Base*
