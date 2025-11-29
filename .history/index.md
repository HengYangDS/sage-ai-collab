# Session History Navigation

> AI session history and task handoffs for SAGE Knowledge Base

---

## Table of Contents

- [1. Directory Structure](#1-directory-structure)
- [2. Usage Guidelines](#2-usage-guidelines)
- [3. Naming Conventions](#3-naming-conventions)

---

## 1. Directory Structure

| Directory        | Purpose                           |
|------------------|-----------------------------------|
| `current/`       | Current session state and context |
| `conversations/` | Conversation records and logs     |
| `handoffs/`      | Task handoff documents            |

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

### 2.4 Example Files

Files prefixed with `_example-` are **reference templates**, not actual session records:

- `_example-2025-11-29-history-completeness-review.md` — Sample conversation record
- `_example-session-20251129-2214.md` — Sample session state
- `_example-2025-11-29-history-enhancement-handoff.md` — Sample handoff document

**Usage**: Copy and rename (removing `_example-` prefix) when creating new records. These files demonstrate the expected
format and content structure.

**Note**: Example files are excluded from retention policies and archival processes.

---

## 3. Naming Conventions

| Type         | Format                       | Example                        |
|--------------|------------------------------|--------------------------------|
| Conversation | `YYYY-MM-DD-topic.md`        | `2025-11-29-timeout-design.md` |
| Handoff      | `YYYY-MM-DD-task-handoff.md` | `2025-11-29-api-handoff.md`    |
| Session      | `session-YYYYMMDD-HHMM.md`   | `session-20251129-2100.md`     |

---

## Retention Policy

| Category      | Retention  | Action                        |
|---------------|------------|-------------------------------|
| Current       | Session    | Clear on completion           |
| Conversations | 30 days    | Archive to `.archive/`        |
| Handoffs      | Until done | Archive after task completion |

---

## Related

- `.context/` — Project-specific knowledge
- `.archive/` — Historical archives
- `content/` — Generic knowledge base

---

*Part of SAGE Knowledge Base - Session History*
