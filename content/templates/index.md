# Document Templates

> Reusable templates for common documents

---

## Table of Contents

[1. Available Templates](#1-available-templates) · [2. Expert Committee Template](#2-expert-committee-template) · [3. Project Setup Template](#3-project-setup-template) · [4. Template Format Standard](#4-template-format-standard) · [5. Creating New Templates](#5-creating-new-templates)

---

## 1. Available Templates

| Template             | File                  | Tokens | Purpose                          |
|----------------------|-----------------------|--------|----------------------------------|
| **Expert Committee** | `expert_committee.md` | ~150   | 24-expert review template        |
| **Project Setup**    | `project_setup.md`    | ~150   | Project initialization checklist |

---

## 2. Expert Committee Template

**File**: `expert_committee.md`

### When to Use

- Complex architectural decisions
- Cross-cutting design changes
- Quality validation for major features
- Risk assessment for critical systems

### Structure

- 4 expert groups (6 experts each)
- Architecture & Systems
- Knowledge Engineering
- AI Collaboration
- Engineering Practice

### Usage

```markdown
## Expert Committee Review: [Topic]

### Architecture Group Assessment

[Use template prompts]

### Knowledge Group Assessment

[Use template prompts]
...
```

---

## 3. Project Setup Template

**File**: `project_setup.md`

### When to Use

- Starting new projects
- Onboarding to existing projects
- Project health audits
- Documentation initialization

### Includes

- Directory structure checklist
- Configuration file templates
- Documentation requirements
- CI/CD setup guidance

---

## 4. Template Format Standard

All templates follow this structure:

```markdown
# [Template Name]

> **Purpose**: [brief description]
> **Use When**: [trigger conditions]

---

## Overview

[What this template helps accomplish]

## Template

[The actual template content with placeholders]

## Instructions

[How to fill in the template]

## Examples

[Completed example if helpful]

---
*Template from SAGE Knowledge Base*
```

---

## 5. Creating New Templates

1. Identify repeated documentation patterns
2. Create template with `[PLACEHOLDER]` markers
3. Add to `templates/` directory
4. Update this index
5. Add trigger keywords if applicable

### Recommended Templates (Future)

- `adr.md` — Architecture Decision Record
- `api_spec.md` — API specification
- `runbook.md` — Operational runbook
- `postmortem.md` — Incident postmortem

---

## Related

- `practices/documentation/standards.md` — Documentation standards
- `frameworks/cognitive/expert_committee.md` — Expert committee framework
- `guidelines/documentation.md` — Documentation guidelines

---

*Part of SAGE Knowledge Base*
