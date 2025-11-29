# Session History Navigation

> AI session history and task handoffs for SAGE Knowledge Base

---

## Table of Contents

[1. Directory Structure](#1-directory-structure) · [2. Usage Guidelines](#2-usage-guidelines) · [3. Naming Conventions](#3-naming-conventions)

---

## 1. Directory Structure

| Directory        | Purpose                              |
|------------------|--------------------------------------|
| `current/`       | Current session state and context    |
| `conversations/` | Conversation records and logs        |
| `handoffs/`      | Task handoff documents               |

---

## 2. Usage Guidelines

### 2.1 Current Session (`current/`)

Store active session state:
- Current task context
- In-progress work artifacts
- Temporary session data

**Cleanup**: Clear after session completion or archival.

### 2.2 Conversations (`conversations/`)

Store conversation records:
- Format: `YYYY-MM-DD-topic.md`
- Include: key decisions, outcomes, learnings

### 2.3 Handoffs (`handoffs/`)

Store task handoff documents for session continuity:
- Format: `YYYY-MM-DD-task-handoff.md`
- Include: task state, next steps, context needed

---

## 3. Naming Conventions

| Type         | Format                        | Example                       |
|--------------|-------------------------------|-------------------------------|
| Conversation | `YYYY-MM-DD-topic.md`         | `2025-11-29-timeout-design.md`|
| Handoff      | `YYYY-MM-DD-task-handoff.md`  | `2025-11-29-api-handoff.md`   |
| Session      | `session-YYYYMMDD-HHMM.md`    | `session-20251129-2100.md`    |

---

## Retention Policy

| Category      | Retention   | Action                        |
|---------------|-------------|-------------------------------|
| Current       | Session     | Clear on completion           |
| Conversations | 30 days     | Archive to `.archive/`        |
| Handoffs      | Until done  | Archive after task completion |

---

## Related

- `.context/` — Project-specific knowledge
- `.archive/` — Historical archives
- `content/` — Generic knowledge base

---

*Part of SAGE Knowledge Base - Session History*
