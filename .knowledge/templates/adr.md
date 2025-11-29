# Architecture Decision Record (ADR) Template

> **Purpose**: Document significant architectural decisions
> **Use When**: Making decisions that affect system structure, technology choices, or design patterns

---

## Template

```markdown
# ADR-[NNNN]: [Title]

> **Status**: [Proposed | Accepted | Deprecated | Superseded]
> **Date**: [YYYY-MM-DD]
> **Deciders**: [List of people involved]

---

## Context

[Describe the issue motivating this decision. What is the problem we're trying to solve?]

---

## Decision Drivers

- [Driver 1: e.g., performance requirement]
- [Driver 2: e.g., maintainability concern]
- [Driver 3: e.g., team expertise]

---

## Considered Options

### Option 1: [Name]

**Description**: [Brief description]

| Pros | Cons |
|------|------|
| [Pro 1] | [Con 1] |
| [Pro 2] | [Con 2] |

### Option 2: [Name]

**Description**: [Brief description]

| Pros | Cons |
|------|------|
| [Pro 1] | [Con 1] |
| [Pro 2] | [Con 2] |

### Option 3: [Name]

**Description**: [Brief description]

| Pros | Cons |
|------|------|
| [Pro 1] | [Con 1] |
| [Pro 2] | [Con 2] |

---

## Decision

[State the decision and explain why this option was chosen]

**Chosen Option**: [Option Name]

**Rationale**:
- [Reason 1]
- [Reason 2]
- [Reason 3]

---

## Consequences

### Positive

- [Positive consequence 1]
- [Positive consequence 2]

### Negative

- [Negative consequence 1]
- [Negative consequence 2]

### Risks

| Risk | Mitigation |
|------|------------|
| [Risk 1] | [Mitigation strategy] |
| [Risk 2] | [Mitigation strategy] |

---

## Implementation

### Action Items

- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

### Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| [Phase 1] | [Duration] | [Deliverable] |
| [Phase 2] | [Duration] | [Deliverable] |

---

## References

- [Link to related document 1]
- [Link to related document 2]

---

*ADR from SAGE Knowledge Base*
```

---

## Instructions

### 1. Numbering

Use sequential 4-digit numbers: `ADR-0001`, `ADR-0002`, etc.

### 2. Status Lifecycle

| Status         | Meaning                 |
|----------------|-------------------------|
| **Proposed**   | Under discussion        |
| **Accepted**   | Approved and active     |
| **Deprecated** | No longer recommended   |
| **Superseded** | Replaced by another ADR |

### 3. Best Practices

| Practice          | Description                    |
|-------------------|--------------------------------|
| Be concise        | Focus on key points            |
| Be specific       | Avoid vague language           |
| Include context   | Future readers need background |
| Link related ADRs | Maintain traceability          |
| Update status     | Keep lifecycle current         |

### 4. File Naming

```
.context/decisions/ADR-NNNN-short-title.md
```

Example: `ADR-0001-fastmcp-choice.md`

---

## Example

```markdown
# ADR-0001: Use FastMCP for MCP Server

> **Status**: Accepted
> **Date**: 2025-11-15
> **Deciders**: Core Team

## Context

Need to implement MCP (Model Context Protocol) server for AI collaboration.

## Decision Drivers

- Rapid development requirement
- Python ecosystem preference
- Type safety needs

## Considered Options

### Option 1: FastMCP

| Pros | Cons |
|------|------|
| Simple API | Newer library |
| Type hints | Smaller community |

### Option 2: Raw MCP SDK

| Pros | Cons |
|------|------|
| Full control | More boilerplate |
| Direct access | Complex setup |

## Decision

**Chosen Option**: FastMCP

FastMCP provides the right balance of simplicity and capability.

## Consequences

### Positive
- Faster development
- Cleaner code

### Negative
- Dependency on FastMCP updates
```

---

## Related

- `frameworks/patterns/decision.md` — Decision quality framework
- `practices/decisions/autonomy_cases.md` — Autonomy level examples
- `guidelines/planning.md` — Architecture planning

---

*Template from SAGE Knowledge Base*
