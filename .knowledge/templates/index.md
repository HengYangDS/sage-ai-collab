# Document Templates

> Reusable templates for common documents

---

## Table of Contents

- [1. Available Templates](#1-available-templates)
- [2. Expert Committee Template](#2-expert-committee-template)
- [3. Project Setup Template](#3-project-setup-template)
- [4. Conversation Record Template](#4-conversation-record-template)
- [5. Session State Template](#5-session-state-template)
- [6. Task Handoff Template](#6-task-handoff-template)
- [7. Template Format Standard](#7-template-format-standard)
- [8. Creating New Templates](#8-creating-new-templates)

---

## 1. Available Templates

| Template                  | File                       | Tokens | Purpose                            |
|---------------------------|----------------------------|--------|------------------------------------|
| **Expert Committee**      | `expert_committee.md`      | ~150   | 24-expert review template          |
| **Project Setup**         | `project_setup.md`         | ~150   | Project initialization checklist   |
| **Conversation Record**   | `conversation_record.md`   | ~200   | AI session documentation           |
| **Session State**         | `session_state.md`         | ~250   | Current session context capture    |
| **Task Handoff**          | `task_handoff.md`          | ~300   | Task continuation between sessions |
| **ADR**                   | `adr.md`                   | ~200   | Architecture Decision Record       |
| **API Spec**              | `api_spec.md`              | ~250   | API specification document         |
| **Runbook**               | `runbook.md`               | ~250   | Operational runbook                |
| **Postmortem**            | `postmortem.md`            | ~250   | Incident postmortem report         |
| **Troubleshooting Guide** | `troubleshooting_guide.md` | ~300   | Problem diagnosis and solutions    |
| **Release Notes**         | `release_notes.md`         | ~350   | Software release documentation     |
| **Meeting Notes**         | `meeting_notes.md`         | ~300   | Meeting records and action items   |
| **Case Study**            | `case_study.md`            | ~230   | Problem-solving case documentation |

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

## 4. Conversation Record Template

**File**: `conversation_record.md`

### When to Use

- Recording significant AI collaboration sessions
- Documenting design discussions and decisions
- Capturing problem-solving sessions with learnings
- Preserving insights for future reference

### Structure

- Context and participants
- Key discussion points
- Decisions made with rationale
- Action items and follow-ups
- Learnings and insights

### Location

Store in `.history/conversations/` with naming: `YYYY-MM-DD-topic.md`

---

## 5. Session State Template

**File**: `session_state.md`

### When to Use

- Starting complex multi-step tasks
- Before taking breaks during active work
- When session may be interrupted
- Beginning exploratory or research tasks

### Structure

- Current task objective and scope
- Progress tracking (completed/current/remaining)
- Working context (files, decisions, dependencies)
- Quick resume guide for continuation

### Location

Store in `.history/current/` with naming: `session-YYYYMMDD-HHMM.md`

---

## 6. Task Handoff Template

**File**: `task_handoff.md`

### When to Use

- Ending session with incomplete work
- Passing tasks to different AI session
- Requesting human review or input
- Before extended breaks

### Structure

- Task summary and current status
- Context for continuation (files, decisions)
- Technical context and dependencies
- Blockers, risks, and recommended next steps

### Location

Store in `.history/handoffs/` with naming: `YYYY-MM-DD-task-handoff.md`

---

## 7. Template Format Standard

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

## 8. Creating New Templates

1. Identify repeated documentation patterns
2. Create template with `[PLACEHOLDER]` markers
3. Add to `templates/` directory
4. Update this index
5. Add trigger keywords if applicable

---

## Related

- `practices/documentation/documentation_standards.md` — Documentation standards (SSOT)
- `frameworks/cognitive/expert_committee.md` — Expert committee framework
- `guidelines/documentation.md` — Documentation guidelines

---

*Part of SAGE Knowledge Base*
