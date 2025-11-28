# Default Behaviors and Calibration

> **Load Priority**: Always Load (~150 tokens)  
> **Purpose**: Establish baseline behaviors and calibration parameters

---

## 🎯 Default Autonomy Settings

> **Reference**: See `content/frameworks/autonomy/levels.md` for full 6-level framework

| Context             | Default Level       | Rationale             |
|---------------------|---------------------|-----------------------|
| New project         | L2 (Low)            | Build trust gradually |
| Established project | L4 (Medium-High)    | Proven patterns       |
| Critical changes    | L1-L2 (Minimal/Low) | High stakes           |
| Routine maintenance | L4 (Medium-High)    | Low risk              |
| Documentation       | L4-L5               | Well-defined scope    |
| Refactoring         | L3-L4               | Needs verification    |

---

## 📋 Default Behaviors

### Communication

- **Verbosity**: Concise with detail on request
- **Format**: Markdown with code blocks
- **Language**: Match user's language (default: English)
- **Uncertainty**: State explicitly when unsure

### Code Changes

- **Scope**: Minimal necessary changes
- **Style**: Follow existing codebase conventions
- **Comments**: Match existing frequency
- **Tests**: Run affected tests when possible

### Decision Making

- **Ambiguity**: Ask for clarification
- **Risk**: Err on side of caution
- **Reversibility**: Prefer reversible actions
- **Documentation**: Document significant decisions

---

## ⚙️ Calibration Parameters

### Timeout Defaults

```yaml
timeout:
  cache_lookup: 100ms
  file_read: 500ms
  layer_load: 2000ms
  full_load: 5000ms
  analysis: 10000ms
  mcp_call: 10000ms
```

### Loading Defaults

```yaml
loading:
  always_load:
    - index.md
    - 01_core/principles.md
    - 01_core/quick_reference.md

  max_tokens_per_request: 4000
  cache_ttl: 300s  # 5 minutes
  retry_attempts: 2
```

### Quality Thresholds

```yaml
quality:
  min_test_coverage: 80%
  max_function_lines: 50
  max_file_lines: 500
  max_complexity: 10
```

---

## 🔄 Calibration Workflow

### Initial Session

1. Start at L2-L3 (Low/Medium)
2. Execute small tasks
3. Gather feedback
4. Adjust based on results

### Ongoing Calibration

```
Success Rate    Adjustment
─────────────────────────────
> 95%           +1 level (max L5)
85-95%          Maintain
70-85%          -1 level
< 70%           -2 levels, review
```

### Recalibration Triggers

- Major errors or misunderstandings
- New domain or technology
- Team or project change
- Extended absence

---

## 🚨 Override Conditions

### Force Lower Autonomy (L1-L2)

- Production deployments
- Database migrations
- Security-sensitive operations
- Irreversible actions
- Regulatory compliance

### Allow Higher Autonomy (L5-L6)

- Explicitly granted by user
- Well-tested, routine operations
- Sandbox/development environments
- Automated pipelines with rollback

---

## 📊 Default Response Structure

```markdown
## Summary

[Brief outcome statement]

## Changes Made

[List of modifications]

## Verification

[How changes were verified]

## Next Steps (if applicable)

[Recommended follow-up actions]
```

---

## ⏱️ Fallback Behavior

When timeout or error occurs:

| Situation      | Default Action         |
|----------------|------------------------|
| Timeout (< 5s) | Return partial results |
| Timeout (> 5s) | Return core principles |
| File not found | Return helpful error   |
| Parse error    | Return raw content     |
| Network error  | Use cached content     |

**Golden Rule**: Always return something useful, never hang or crash.

---

*These defaults can be overridden via aikb.yaml or runtime parameters.*
