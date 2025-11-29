# Autonomy Calibration

> Calibration data for AI autonomy levels in SAGE Knowledge Base

---

## Table of Contents

[1. Autonomy Framework](#1-autonomy-framework) · [2. Task Classification](#2-task-classification) · [3. Risk Assessment](#3-risk-assessment) · [4. Calibration Examples](#4-calibration-examples) · [5. Escalation Criteria](#5-escalation-criteria)

---

## 1. Autonomy Framework

### 1.1 Six-Level Autonomy Scale

| Level | Name | Autonomy | Description |
|-------|------|----------|-------------|
| **L1** | Minimal | 0-20% | Ask before any action |
| **L2** | Low | 20-40% | Confirm significant changes |
| **L3** | Medium | 40-60% | Proceed with reporting |
| **L4** | Medium-High | 60-80% | Proceed, report after ⭐ |
| **L5** | High | 80-95% | High autonomy with guardrails |
| **L6** | Full | 95-100% | Complete autonomy |

### 1.2 Default Level

**SAGE Project Default: L4 (Medium-High)**

Rationale:
- Mature codebase with established patterns
- Comprehensive test suite (841+ tests)
- Clear conventions documented
- Regular AI collaboration history

### 1.3 Level Adjustment Factors

| Factor | Increase Level | Decrease Level |
|--------|----------------|----------------|
| Task familiarity | Routine task | Novel approach |
| Risk | Low impact | Breaking change |
| Reversibility | Easy to undo | Hard to reverse |
| Scope | Single file | Multi-file refactor |
| Dependencies | No external | External APIs |

---

## 2. Task Classification

### 2.1 L5-L6: High Autonomy (80-100%)

Tasks that can proceed with minimal oversight:

| Task Type | Examples | Autonomy |
|-----------|----------|----------|
| **Formatting** | Code formatting, import sorting | L6 |
| **Comments** | Adding/updating docstrings | L5-L6 |
| **Documentation** | Updating README, adding examples | L5 |
| **Simple fixes** | Typo fixes, obvious bugs | L5 |
| **Test additions** | Adding tests for existing code | L5 |
| **Trusted patterns** | Following established patterns | L5 |

### 2.2 L3-L4: Medium Autonomy (40-80%)

Tasks that proceed with reporting:

| Task Type | Examples | Autonomy |
|-----------|----------|----------|
| **Bug fixes** | Fixing identified issues | L4 |
| **Refactoring** | Improving existing code | L4 |
| **Feature additions** | New features in scope | L3-L4 |
| **Test modifications** | Updating test logic | L4 |
| **Config changes** | Non-breaking config updates | L4 |
| **Dependency updates** | Minor version updates | L3 |

### 2.3 L1-L2: Low Autonomy (0-40%)

Tasks requiring confirmation:

| Task Type | Examples | Autonomy |
|-----------|----------|----------|
| **Breaking changes** | API changes, removing features | L1-L2 |
| **New dependencies** | Adding external packages | L2 |
| **Architecture changes** | Layer modifications | L1 |
| **Security changes** | Auth, permissions | L1 |
| **Data migrations** | Schema changes | L1 |
| **Critical systems** | Core protocol changes | L1-L2 |

---

## 3. Risk Assessment

### 3.1 Risk Matrix

| Impact | Reversible | Autonomy Level |
|--------|------------|----------------|
| Low | Easy | L5-L6 |
| Low | Hard | L4 |
| Medium | Easy | L4 |
| Medium | Hard | L2-L3 |
| High | Easy | L2-L3 |
| High | Hard | L1 |

### 3.2 Impact Categories

**Low Impact:**
- Single file changes
- Documentation updates
- Test additions
- Internal refactoring
- Comments and formatting

**Medium Impact:**
- Multi-file refactoring
- New feature implementation
- Configuration changes
- Dependency updates
- API extensions (additive)

**High Impact:**
- Breaking API changes
- Core infrastructure changes
- Security modifications
- Data model changes
- External integration changes

### 3.3 Reversibility Assessment

**Easy to Reverse:**
- Git can restore (no external effects)
- No state changes
- No external API calls
- No data modifications

**Hard to Reverse:**
- Database migrations
- External API calls made
- Published packages
- Sent notifications
- File system changes outside repo

---

## 4. Calibration Examples

### 4.1 SAGE-Specific Calibrations

| Task | Autonomy | Rationale |
|------|----------|-----------|
| Add new knowledge file to `content/` | L5 | Low risk, follows template |
| Update `timeout_hierarchy.md` | L5 | Documentation only |
| Add new timeout level (T6) | L3 | Requires design discussion |
| Modify EventBus core logic | L2 | Core infrastructure |
| Add new CLI command | L4 | Follows existing patterns |
| Add new MCP tool | L4 | Follows existing patterns |
| Change DI container behavior | L2 | Core infrastructure |
| Update Protocol interface | L2 | Breaking change potential |
| Add new Analyzer capability | L4 | Isolated addition |
| Fix failing test | L5 | Low risk |
| Add test for edge case | L5 | Additive only |
| Refactor single module | L4 | Contained scope |
| Cross-module refactoring | L3 | Wider impact |
| Update `sage.yaml` defaults | L3 | Affects all users |
| Add new exception type | L4 | Additive change |
| Modify exception hierarchy | L2 | Breaking potential |

### 4.2 File-Based Calibration

| File/Directory | Default Autonomy | Notes |
|----------------|------------------|-------|
| `content/**/*.md` | L5 | Knowledge content |
| `docs/**/*.md` | L5 | Documentation |
| `tests/**/*.py` | L5 | Test additions |
| `src/sage/core/*.py` | L3 | Core infrastructure |
| `src/sage/core/protocols.py` | L2 | Interface definitions |
| `src/sage/services/*.py` | L4 | Service layer |
| `src/sage/capabilities/**/*.py` | L4 | Capability additions |
| `config/**/*.yaml` | L3-L4 | Configuration |
| `.context/**/*.md` | L5 | Project knowledge |
| `pyproject.toml` | L2-L3 | Project config |
| `sage.yaml` | L3 | Main config |

### 4.3 Change Type Calibration

| Change Type | Autonomy | Confirmation Needed |
|-------------|----------|---------------------|
| Add (new file) | L4-L5 | No |
| Modify (existing) | L3-L4 | For significant changes |
| Delete | L2 | Yes |
| Rename | L3 | For public APIs |
| Move | L3 | For public APIs |
| Merge | L3-L4 | No |

---

## 5. Escalation Criteria

### 5.1 When to Escalate (Decrease Autonomy)

Always escalate when:

1. **Uncertainty exists**
   - Requirements unclear
   - Multiple valid approaches
   - Trade-offs not obvious

2. **Breaking changes**
   - Public API modifications
   - Protocol interface changes
   - Configuration format changes

3. **Security implications**
   - Authentication changes
   - Authorization modifications
   - Data exposure risks

4. **External effects**
   - Third-party API changes
   - Published package updates
   - User-facing changes

5. **Novel patterns**
   - First implementation of pattern
   - Deviation from conventions
   - New architectural approach

### 5.2 Escalation Process

```
1. Pause implementation
2. Document current state
3. Present options with trade-offs
4. Request clarification/approval
5. Proceed after confirmation
```

### 5.3 When to Proceed (Maintain/Increase Autonomy)

Proceed confidently when:

1. **Clear requirements**
   - Task well-defined
   - Success criteria known
   - Constraints explicit

2. **Established patterns**
   - Similar code exists
   - Conventions documented
   - Tests verify behavior

3. **Low risk**
   - Isolated changes
   - Easy to reverse
   - Good test coverage

4. **Routine operations**
   - Previously approved similar work
   - Standard maintenance
   - Documented procedures

---

## 6. Feedback Loop

### 6.1 Calibration Updates

This calibration should be updated when:

- New patterns are established
- Conventions change
- Risk assessment changes
- Project maturity evolves
- New team members join

### 6.2 Recording Decisions

When making autonomy decisions, consider recording:

```markdown
## Decision: [Task Description]

- **Task**: [What was done]
- **Autonomy Level**: L[N]
- **Rationale**: [Why this level]
- **Outcome**: [Success/Issues]
- **Adjustment**: [Any calibration updates needed]
```

### 6.3 Calibration Review Schedule

| Review Type | Frequency | Focus |
|-------------|-----------|-------|
| Quick review | Per session | Task-level calibration |
| Standard review | Weekly | Pattern updates |
| Deep review | Monthly | Framework alignment |

---

## 7. Quick Reference

### 7.1 Autonomy Decision Tree

```
Is it a breaking change?
  Yes → L1-L2 (confirm first)
  No ↓

Is it core infrastructure?
  Yes → L2-L3 (proceed carefully)
  No ↓

Does it follow existing patterns?
  No → L3 (report approach)
  Yes ↓

Is it isolated/reversible?
  No → L3-L4 (monitor closely)
  Yes → L4-L5 (proceed confidently)
```

### 7.2 Default Autonomy by Action

| Action | Default |
|--------|---------|
| Read/analyze code | L6 |
| Add documentation | L5 |
| Add tests | L5 |
| Fix obvious bugs | L5 |
| Implement features | L4 |
| Refactor code | L4 |
| Change configs | L3-L4 |
| Modify protocols | L2 |
| Change architecture | L1-L2 |

---

## Related

- `patterns.md` — AI interaction patterns
- `optimizations.md` — Project optimizations
- `content/frameworks/autonomy/` — Full autonomy framework
- `.junie/guidelines.md` — Project guidelines

---

*Part of SAGE Knowledge Base - AI Intelligence*
