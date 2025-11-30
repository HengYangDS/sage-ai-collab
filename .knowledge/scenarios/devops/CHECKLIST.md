---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---

# DevOps Checklist

> Task checklist for CI/CD and infrastructure management

---

## Version Control

- [ ] Branch strategy defined
- [ ] Commit message convention
- [ ] Code review process
- [ ] Protected branches configured
- [ ] PR templates created

## CI Pipeline

- [ ] Build automation configured
- [ ] Unit tests in pipeline
- [ ] Integration tests in pipeline
- [ ] Code quality checks (lint, format)
- [ ] Security scanning enabled
- [ ] Artifact versioning

## CD Pipeline

- [ ] Deployment automation
- [ ] Environment promotion strategy
- [ ] Rollback procedure documented
- [ ] Blue-green or canary deployment
- [ ] Feature flags integrated

## Infrastructure

- [ ] Infrastructure as Code (IaC)
- [ ] Environment parity (dev/staging/prod)
- [ ] Resource tagging strategy
- [ ] Cost monitoring enabled
- [ ] Capacity planning done

## Containerization

- [ ] Dockerfile optimized
- [ ] Base image security
- [ ] Multi-stage builds
- [ ] Image scanning enabled
- [ ] Registry configured
- [ ] Resource limits set

## Kubernetes (if applicable)

- [ ] Manifests or Helm charts
- [ ] Resource requests/limits
- [ ] Health checks configured
- [ ] HPA configured
- [ ] Network policies defined
- [ ] Secrets management

## Monitoring

- [ ] Application metrics collected
- [ ] Infrastructure metrics collected
- [ ] Dashboards created
- [ ] Log aggregation setup
- [ ] Distributed tracing (if needed)

## Alerting

- [ ] Alert rules defined
- [ ] Escalation policy
- [ ] On-call rotation
- [ ] Runbooks for alerts
- [ ] Alert fatigue addressed

## Security

- [ ] Secrets in vault/manager
- [ ] IAM roles minimal
- [ ] Network segmentation
- [ ] SSL/TLS certificates managed
- [ ] Vulnerability scanning

## Disaster Recovery

- [ ] Backup strategy defined
- [ ] Backup testing schedule
- [ ] RTO/RPO documented
- [ ] DR runbook created
- [ ] Failover tested

## Documentation

- [ ] Architecture diagram
- [ ] Deployment procedures
- [ ] Incident response playbook
- [ ] Service catalog updated

---

## Related

- `.knowledge/scenarios/devops/context.md` — DevOps context
- `.knowledge/practices/engineering/ci_cd.md` — CI/CD practices
- `.knowledge/practices/engineering/monitoring.md` — Monitoring practices

---

*SAGE Knowledge Base - DevOps Checklist*
---

*Part of SAGE Knowledge Base*
