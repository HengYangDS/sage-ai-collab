---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~300
---

# Python Backend Checklist

> Task checklist for Python backend development

---

## Project Setup

- [ ] Python version specified (3.12+)
- [ ] Virtual environment created
- [ ] `pyproject.toml` configured
- [ ] Dependencies installed
- [ ] Pre-commit hooks setup
- [ ] CI/CD pipeline configured

## Code Quality

- [ ] Type hints on all public functions
- [ ] Docstrings (Google style)
- [ ] Ruff linting passes
- [ ] MyPy type checking passes
- [ ] Test coverage > 80%

## API Development

- [ ] OpenAPI schema defined
- [ ] Request validation (Pydantic)
- [ ] Error handling standardized
- [ ] Authentication implemented
- [ ] Authorization enforced
- [ ] Rate limiting configured
- [ ] CORS settings appropriate

## Database

- [ ] Migrations up to date
- [ ] Indexes on query columns
- [ ] Connection pooling configured
- [ ] Transactions used appropriately
- [ ] N+1 queries eliminated

## Security

- [ ] No hardcoded secrets
- [ ] Input validation complete
- [ ] SQL injection prevented
- [ ] HTTPS enforced
- [ ] Security headers set

## Performance

- [ ] Response times < 200ms (P95)
- [ ] Caching implemented
- [ ] Async where beneficial
- [ ] Profiling completed

## Deployment

- [ ] Environment variables documented
- [ ] Health check endpoint
- [ ] Logging configured
- [ ] Monitoring setup
- [ ] Rollback procedure documented

---

## Related

- `.knowledge/scenarios/python_backend/context.md` — Python backend context
- `.knowledge/guidelines/python.md` — Python guidelines
- `.knowledge/practices/engineering/testing_strategy.md` — Testing strategies

---

*SAGE Knowledge Base - Python Backend Checklist*
---

*Part of SAGE Knowledge Base*
