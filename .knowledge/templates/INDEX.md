# Document Templates

> Reusable templates for common documents

---

## Table of Contents

- [1. Template Usage Guidelines](#1-template-usage-guidelines)
- [2. Available Templates](#2-available-templates)
- [3. Expert Committee Template](#3-expert-committee-template)
- [4. Project Setup Template](#4-project-setup-template)
- [5. Conversation Record Template](#5-conversation-record-template)
- [6. Session State Template](#6-session-state-template)
- [7. Task Handoff Template](#7-task-handoff-template)
- [8. Template Format Standard](#8-template-format-standard)
- [9. Creating New Templates](#9-creating-new-templates)

---

## 1. Template Usage Guidelines

> ⚠️ **Important**: All documents in `.knowledge/` must comply with MECE boundaries and policies.

### 1.1 MECE Boundary Requirements

| Requirement | Description |
|-------------|-------------|
| **No Project Names** | Do not include specific project names (e.g., "MyProject", "my-app") |
| **No Project Paths** | Do not reference project-specific config paths |
| **Generic Footer** | Use `*AI Collaboration Knowledge Base*` as footer |
| **Universal Content** | Content must be reusable across ANY project |

### 1.2 Frontmatter Policy

| Policy | Description |
|--------|-------------|
| **No Frontmatter** | Documents must start with `# Title`, not YAML frontmatter |
| **No Version Tags** | Version tracking via Git, not in-document metadata |
| **No Token Counts** | Token estimates are not maintained in files |

### 1.3 When Using Templates

1. **Copy** the template to appropriate location
2. **Remove** any placeholder markers `[MARKER]`
3. **Verify** no project-specific content is added to `.knowledge/`
4. **Check** document starts with `# Title` (no frontmatter)

**Validation**: Run `python tools/check_mece_boundaries.py` before committing.

---

## 2. Available Templates

| Template                  | File                       | Tokens | Purpose                            |
|---------------------------|----------------------------|--------|------------------------------------|
| **Expert Committee**      | `EXPERT_COMMITTEE.md`      | ~150   | 24-expert review template          |
| **Project Setup**         | `PROJECT_SETUP.md`         | ~150   | Project initialization checklist   |
| **Conversation Record**   | `CONVERSATION_RECORD.md`   | ~200   | AI session documentation           |
| **Session State**         | `SESSION_STATE.md`         | ~250   | Current session context capture    |
| **Task Handoff**          | `TASK_HANDOFF.md`          | ~300   | Task continuation between sessions |
| **ADR**                   | `ADR.md`                   | ~200   | Architecture Decision Record       |
| **API Spec**              | `API_SPEC.md`              | ~250   | API specification document         |
| **Runbook**               | `RUNBOOK.md`               | ~250   | Operational runbook                |
| **Postmortem**            | `POSTMORTEM.md`            | ~250   | Incident postmortem report         |
| **Troubleshooting Guide** | `TROUBLESHOOTING_GUIDE.md` | ~300   | Problem diagnosis and solutions    |
| **Release Notes**         | `RELEASE_NOTES.md`         | ~350   | Software release documentation     |
| **Meeting Notes**         | `MEETING_NOTES.md`         | ~300   | Meeting records and action items   |
| **Case Study**            | `CASE_STUDY.md`            | ~230   | Problem-solving case documentation |
| **Convention**            | `CONVENTION.md`            | ~80    | Code/project convention template   |
| **Guide**                 | `GUIDE.md`                 | ~80    | Step-by-step guide template        |
| **Practice**              | `PRACTICE.md`              | ~75    | Best practice pattern template     |

---

## 2. Expert Committee Template

**File**: `EXPERT_COMMITTEE.md`

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
```text
---

## 3. Project Setup Template

**File**: `PROJECT_SETUP.md`

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

**File**: `CONVERSATION_RECORD.md`

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

Store in `.history/conversations/` with naming: `YYYY-MM-DD-TOPIC.md`

---

## 5. Session State Template

**File**: `SESSION_STATE.md`

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

**File**: `TASK_HANDOFF.md`

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

Store in `.history/handoffs/` with naming: `YYYY-MM-DD-TASK-HANDOFF.md`

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
*Template from AI Collaboration Knowledge Base*
```text
---

## 8. Creating New Templates

1. Identify repeated documentation patterns
2. Create template with `[PLACEHOLDER]` markers
3. Add to `templates/` directory
4. Update this index
5. Add trigger keywords if applicable

---

## Related

- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Documentation standards
- `.knowledge/frameworks/cognitive/EXPERT_COMMITTEE.md` — Expert committee framework
- `.knowledge/guidelines/DOCUMENTATION.md` — Documentation guidelines

---

*AI Collaboration Knowledge Base*
