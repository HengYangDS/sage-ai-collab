# Common Pitfalls - SAGE Project Reference

> Project-specific pitfall notes for SAGE Knowledge Base

---

## Generic Pitfalls Reference

For the comprehensive guide on common software development pitfalls, see:

**→ `.knowledge/practices/engineering/COMMON_PITFALLS.md`**

This includes:

- Architecture Pitfalls (Circular Dependencies, Timeout Protection, Coupling)
- Implementation Pitfalls (Mutable Defaults, Exception Handling, Async Context)
- Configuration Pitfalls (Hardcoded Values, Environment Config, Secrets)
- Testing Pitfalls (Behavior Testing, Flaky Tests, Edge Cases)
- AI Collaboration Pitfalls (Context, Instructions, Review)

---

## SAGE-Specific Pitfalls

### Timeout Hierarchy Violations

**Severity**: High

**Context**: SAGE uses a strict timeout hierarchy (T1-T5).

**Common Mistakes**:

- Using T4 timeout for cache operations (should be T1)
- Missing timeout on plugin hooks
- Not implementing graceful degradation

**Prevention**:

- Reference `.context/policies/TIMEOUT_HIERARCHY.md`
- Use `TimeoutManager` for all I/O operations
- Implement fallback for each timeout level

---

### Plugin Hook Priority Conflicts

**Severity**: Medium

**Context**: Multiple plugins may hook the same event.

**Common Mistakes**:

- Not considering hook execution order
- Assuming hook results are isolated
- Missing error handling in hooks

**Prevention**:

- Document plugin priorities in metadata
- Use `tryfirst`/`trylast` appropriately
- Wrap hooks in try/except

---

### Knowledge Layer Loading Order

**Severity**: Medium

**Context**: SAGE loads knowledge in priority order.

**Common Mistakes**:

- Assuming all layers are loaded
- Not checking loading status
- Missing fallback content

**Prevention**:

- Always check `loading_status` before use
- Implement graceful degradation
- Use smart loading triggers

---

## Related

- `.knowledge/practices/engineering/COMMON_PITFALLS.md` — Generic pitfalls guide
- `.context/intelligence/learning/LESSONS_LEARNED.md` — SAGE-specific lessons
- `.context/policies/TIMEOUT_HIERARCHY.md` — Timeout policy

---

*Last updated: 2025-11-30*
*AI Collaboration Knowledge Base*
