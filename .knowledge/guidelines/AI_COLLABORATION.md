---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~950
---

# AI Collaboration Guidelines

> Human-AI interaction patterns, autonomy levels, execution modes

---

## Table of Contents

- [1. Instruction Types](#1-instruction-types)
- [2. Execution Modes](#2-execution-modes)
- [3. Autonomy Levels](#3-autonomy-levels)
- [4. Communication Patterns](#4-communication-patterns)
- [5. Context Management](#5-context-management)
- [6. Collaboration Workflow](#6-collaboration-workflow)

---

## 1. Instruction Types

| Type            | Format           | Example                        |
|-----------------|------------------|--------------------------------|
| **Direct**      | Specific command | "Create file X with content Y" |
| **Goal-based**  | Outcome desired  | "Make the tests pass"          |
| **Exploratory** | Investigation    | "Analyze why X fails"          |
| **Iterative**   | Refinement       | "Improve the solution"         |

---

## 2. Execution Modes

| Mode           | Description             | Use When                    |
|----------------|-------------------------|-----------------------------|
| **Single**     | One task, one response  | Simple, isolated tasks      |
| **Batch**      | Multiple related tasks  | Refactoring, migrations     |
| **Iterative**  | Refine through feedback | Complex, uncertain scope    |
| **Autonomous** | Self-directed execution | Routine, well-defined tasks |

---

## 3. Autonomy Levels

| Level | Range   | Behavior                       |
|-------|---------|--------------------------------|
| L1    | 0-20%   | Ask before all changes         |
| L2    | 20-40%  | Ask before significant changes |
| L3    | 40-60%  | Proceed routine, ask novel     |
| L4    | 60-80%  | Proceed, report after          |
| L5    | 80-95%  | High autonomy, minimal checks  |
| L6    | 95-100% | Full autonomy                  |

### 3.1 Level Selection

| Context              | Recommended |
|----------------------|-------------|
| New collaboration    | L2-L3       |
| Established trust    | L4-L5       |
| Production/sensitive | L1-L2       |
| Routine tasks        | L4-L5       |

---

## 4. Communication Patterns

### 4.1 Effective Instructions

| ✓ Good                 | ❌ Avoid           |
|------------------------|-------------------|
| Specific, measurable   | Vague, ambiguous  |
| Context provided       | Assumed knowledge |
| Success criteria clear | Open-ended        |
| Constraints stated     | Implicit limits   |

### 4.2 Feedback Types

| Type          | When            | Example              |
|---------------|-----------------|----------------------|
| Approval      | Work correct    | "Good, proceed"      |
| Correction    | Work incorrect  | "Change X to Y"      |
| Clarification | Need more info  | "What about Z?"      |
| Redirect      | Wrong direction | "Focus on A instead" |

---

## 5. Context Management

### 5.1 Context Building

| Element     | Purpose                 |
|-------------|-------------------------|
| Background  | Why this task matters   |
| Constraints | Limitations to respect  |
| Examples    | Illustrate expectations |
| References  | Related information     |

### 5.2 Context Efficiency

| Strategy               | Benefit              |
|------------------------|----------------------|
| Progressive disclosure | Load info as needed  |
| Summarize history      | Reduce token usage   |
| Reference files        | Don't repeat content |

---

## 6. Collaboration Workflow

| Phase      | Human Actions               | AI Actions            |
|------------|-----------------------------|-----------------------|
| **Start**  | Define task, set level      | Confirm understanding |
| **During** | Monitor, respond, feedback  | Execute, report, ask  |
| **After**  | Review, feedback, calibrate | Document, learn       |

---

## Related

- `.knowledge/frameworks/autonomy/LEVELS.md` — Autonomy level definitions (L1-L6)
- `.knowledge/practices/ai_collaboration/WORKFLOW.md` — Detailed workflow practices
- `.knowledge/practices/ai_collaboration/CONTEXT_MANAGEMENT.md` — Context management
- `.knowledge/practices/ai_collaboration/SESSION_MANAGEMENT.md` — Session management

---

*Part of SAGE Knowledge Base*
