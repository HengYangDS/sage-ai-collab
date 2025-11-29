# Default Behaviors and Calibration

> **Load Priority**: Always Load (~150 tokens)  
> **Purpose**: Establish baseline behaviors and calibration parameters  
> **Configuration**: See `sage.yaml` for actual values (Single Source of Truth)

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

## ⚙️ Configuration Reference

> **Single Source of Truth**: All actual configuration values are defined in `sage.yaml`.
> This section describes the configuration structure and purpose only.

### Timeout Configuration

> **Location**: `sage.yaml` → `timeout`

| Level | Key | Purpose |
|-------|-----|---------|
| T1 | `operations.cache_lookup` | Cache hit operations |
| T2 | `operations.file_read` | Single file operations |
| T3 | `operations.layer_load` | Layer/directory loading |
| T4 | `operations.full_load` | Complete KB load |
| T5 | `operations.analysis` | Complex analysis |
| - | `operations.mcp_call` | MCP tool timeout |
| - | `operations.search` | Search operations |
| - | `global_max` | Absolute maximum timeout |
| - | `default` | Default if not specified |

**Additional Features** (see `sage.yaml`):
- `strategies.on_timeout` - Timeout handling strategies
- `circuit_breaker` - Circuit breaker pattern configuration

### Loading Configuration

> **Location**: `sage.yaml` → `loading`

| Key | Purpose |
|-----|---------|
| `max_tokens` | Maximum tokens to load per request |
| `default_layers` | Layers loaded by default |
| `always` | Files always pre-cached |

### Quality Thresholds

> **Location**: `sage.yaml` → `quality`

| Category | Keys | Purpose |
|----------|------|---------|
| Code Quality | `min_test_coverage`, `max_function_lines`, `max_file_lines`, `max_complexity` | Code quality metrics |
| Code Style | `max_line_length`, `min_type_hint_coverage` | Style enforcement |
| Documentation | `max_doc_line_length` | Markdown formatting |

### Other Configuration Sections

> **Location**: `sage.yaml`

| Section | Purpose |
|---------|---------|
| `guidelines.sections` | Alias mapping for guidelines |
| `triggers` | Keyword-based context loading |
| `plugins` | Plugin configuration (cache, etc.) |
| `logging` | Logging level, format, timestamps |
| `di` | Dependency injection container |

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

> **Location**: `sage.yaml` → `timeout.fallback`

When timeout or error occurs, the system applies configured fallback actions:

| Situation | Config Key | Action |
|-----------|------------|--------|
| Timeout (< 5s) | `timeout_short` | Return partial results |
| Timeout (> 5s) | `timeout_long` | Return core principles |
| File not found | `file_not_found` | Return helpful error |
| Parse error | `parse_error` | Return raw content |
| Network error | `network_error` | Use cached content |

**Golden Rule**: Always return something useful, never hang or crash.

---

*All configuration values are defined in `sage.yaml` (Single Source of Truth).*
