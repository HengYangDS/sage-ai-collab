# AI Collaboration Patterns

> Patterns for effective human-AI collaboration

---

## Table of Contents

- [1. Communication Patterns](#1-communication-patterns)
- [2. Execution Patterns](#2-execution-patterns)
- [3. Context Patterns](#3-context-patterns)
- [4. Feedback Patterns](#4-feedback-patterns)
- [5. Anti-Patterns](#5-anti-patterns)

---

## 1. Communication Patterns

### 1.1 Request Patterns

| Pattern         | Structure       | Use Case              |
|-----------------|-----------------|-----------------------|
| **Direct**      | "Do X"          | Clear, specific tasks |
| **Goal-based**  | "Achieve Y"     | Outcome-focused       |
| **Exploratory** | "Investigate Z" | Discovery, analysis   |
| **Iterative**   | "Improve on W"  | Refinement            |

### 1.2 Response Patterns

| Pattern          | Structure             | Use Case        |
|------------------|-----------------------|-----------------|
| **Confirmation** | Restate + plan        | Complex tasks   |
| **Progressive**  | Summary → details     | Long outputs    |
| **Checkpoint**   | Status + next steps   | Multi-step work |
| **Completion**   | Result + verification | Task end        |

---

## 2. Execution Patterns

### 2.1 Single Task

```
Request → Confirm → Execute → Report
```

### 2.2 Batch Processing

```
Request → Plan → [Execute → Checkpoint]* → Summary
```

### 2.3 Iterative Refinement

```
Request → Draft → Feedback → Refine → [Repeat] → Finalize
```

---

## 3. Context Patterns

### 3.1 Context Building

| Element     | Purpose                 | Example                       |
|-------------|-------------------------|-------------------------------|
| Background  | Why this matters        | "We're migrating to..."       |
| Constraints | Limits to respect       | "Must maintain compatibility" |
| Examples    | Illustrate expectations | "Like this existing code"     |
| References  | Related information     | "See config.yaml"             |

### 3.2 Context Management

| Strategy          | When                        |
|-------------------|-----------------------------|
| Full context      | New task, complex work      |
| Delta context     | Continuation, small changes |
| Reference context | "As discussed before"       |
| Reset context     | New direction               |

---

## 4. Error Handling Patterns

### 4.1 Error Response

| Step | Action               |
|------|----------------------|
| 1    | Acknowledge error    |
| 2    | Identify cause       |
| 3    | Propose fix          |
| 4    | Implement correction |
| 5    | Verify resolution    |

### 4.2 Recovery Patterns

| Situation        | Pattern              |
|------------------|----------------------|
| Misunderstanding | Clarify → retry      |
| Wrong approach   | Reset → new approach |
| Partial failure  | Salvage → complete   |
| Complete failure | Analyze → restart    |

---

## 5. Autonomy Patterns

### 5.1 Level-Based Behavior

| Level | Communication Pattern      |
|-------|----------------------------|
| L1-L2 | Ask before, confirm after  |
| L3-L4 | Proceed routine, ask novel |
| L5-L6 | Proceed, report completion |

### 5.2 Escalation Pattern

```
Attempt → Uncertain? → Escalate → Guidance → Continue
```

---

## 6. Workflow Patterns

| Phase      | Human                  | AI                    |
|------------|------------------------|-----------------------|
| **Start**  | Define task, set level | Confirm understanding |
| **During** | Monitor, respond       | Execute, checkpoint   |
| **End**    | Review, feedback       | Report, document      |

---

## Related

- `.knowledge/guidelines/ai_collaboration.md` — Collaboration guidelines
- `.knowledge/practices/ai_collaboration/workflow.md` — Workflow practices
- `.knowledge/frameworks/autonomy/levels.md` — Autonomy framework

---

*Part of SAGE Knowledge Base*
