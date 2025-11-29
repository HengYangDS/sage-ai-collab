# AI Collaboration Patterns - SAGE Project Reference

> Project-specific calibration and patterns for SAGE Knowledge Base

---

## Table of Contents

- [1. Generic Patterns Reference](#1-generic-patterns-reference)
- [2. SAGE-Specific Calibration Data](#2-sage-specific-calibration-data)
- [3. SAGE-Specific Patterns](#3-sage-specific-patterns)

---

## 1. Generic Patterns Reference

For the comprehensive guide on AI collaboration patterns, see:

**→ `.knowledge/practices/ai_collaboration/interaction_patterns.md`**

This includes:

- Interaction Patterns (Session Start, Progressive Disclosure, Clarification Request, Batch Operation)
- Knowledge Capture Patterns (Decision Point, Convention Discovery, Session Handoff, Problem-Solution)
- Optimization Strategies (Context Window, Token Budget, Parallel Task, Error Recovery)
- Anti-Patterns (Over-Engineering, Silent Assumptions, Monolithic Changes, Context Overload)

---

## 2. SAGE-Specific Calibration Data

### Autonomy Level Calibration

Current calibration for SAGE project:

| Task Type             | Recommended Level | Notes                      |
|:-----------------------|:-------------------|:----------------------------|
| Documentation updates | L5 (High)         | Well-established patterns  |
| Code formatting       | L5 (High)         | Ruff handles automatically |
| Bug fixes             | L4 (Medium-High)  | Verify with tests          |
| New features          | L3 (Medium)       | Discuss design first       |
| Architecture changes  | L2 (Low)          | Requires approval          |
| Breaking changes      | L1 (Minimal)      | Full review required       |

### Response Time Expectations

| Operation           | Expected Time | Timeout Level |
|:---------------------|:---------------|:---------------|
| Simple query        | < 100ms       | T1            |
| Single file read    | < 500ms       | T2            |
| Multi-file analysis | < 2s          | T3            |
| Full KB load        | < 5s          | T4            |
| Complex analysis    | < 10s         | T5            |

### Quality Thresholds

| Metric        | Target | Action if Below        |
|:---------------|:--------|:------------------------|
| Test coverage | > 80%  | Add tests before merge |
| Type coverage | > 90%  | Add type hints         |
| Doc coverage  | > 70%  | Add docstrings         |
| Complexity    | < 10   | Refactor function      |

---

## 3. SAGE-Specific Patterns

### Session Start for SAGE

When starting a SAGE development session:

1. Review `.junie/guidelines.md` for project context
2. Check `.history/current/` for active sessions
3. Review recent commits for context continuity
4. Reference `.context/policies/` for runtime settings

### Knowledge Layer Loading

When working with SAGE knowledge layers:

1. Core layer loads first (always)
2. Guidelines load by task type
3. Frameworks load on-demand
4. Use smart triggers from `config/knowledge/triggers.yaml`

### Timeout-Aware Operations

For all I/O operations in SAGE:

1. Reference `.context/policies/timeout_hierarchy.md`
2. Use appropriate timeout level (T1-T5)
3. Implement fallback for timeout scenarios
4. Log timeout events for calibration

---

## Related

- `.knowledge/practices/ai_collaboration/interaction_patterns.md` — Generic patterns
- `.knowledge/frameworks/autonomy/levels.md` — Autonomy level definitions
- `.context/policies/timeout_hierarchy.md` — Timeout policy
- `.context/intelligence/calibration.md` — Detailed calibration data
- `.junie/guidelines.md` — Project collaboration guidelines

---

*Last updated: 2025-11-30*
*Part of SAGE Knowledge Base - Project Intelligence*
