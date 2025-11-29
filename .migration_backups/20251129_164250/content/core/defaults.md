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
- **Language**: Match the user’s language (default: English)
- **Uncertainty**: State explicitly when unsure

### Code Changes

- **Scope**: Minimal necessary changes
- **Style**: Follow existing codebase conventions
- **Comments**: Match existing frequency
- **Tests**: Run affected tests when possible

### Decision-Making

- **Ambiguity**: Ask for clarification
- **Risk**: Err on the side of caution
- **Reversibility**: Prefer reversible actions
- **Documentation**: Document significant decisions

---

## ⚙️ Calibration Parameters

### Timeout Defaults

```yaml
timeout:
  cache_lookup: 100ms    # T1 - Cache hits
  file_read: 500ms       # T2 - Single file operations
  layer_load: 2s         # T3 - Layer/directory loading
  full_load: 5s          # T4 - Complete KB load
  analysis: 10s          # T5 - Complex analysis
  mcp_call: 10s          # MCP tool timeout
  search: 3s             # Search operations
```

### Loading Defaults

```yaml
loading:
  max_tokens: 4000                   # Maximum tokens to load
  default_layers:
    - core                           # Always start with core

  always:                            # Always loaded (pre-cached)
    - index.md
    - content/core/principles.md
    - content/core/quick_reference.md
```

### Quality Thresholds

```yaml
quality:
  # Code quality thresholds
  min_test_coverage: 95                # Minimum test coverage percentage
  max_function_lines: 50               # Maximum lines per function
  max_file_lines: 500                  # Maximum lines per file
  max_complexity: 10                   # Maximum cyclomatic complexity

  # Code style thresholds
  max_line_length: 100                 # Maximum line length (characters)
  min_type_hint_coverage: 50           # Minimum type hint coverage percentage

  # Documentation thresholds
  max_doc_line_length: 120             # Maximum line length in markdown
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

- Explicitly granted by the user
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

[How changes to be verified]

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

*These defaults can be overridden via sage.yaml or runtime parameters.*
