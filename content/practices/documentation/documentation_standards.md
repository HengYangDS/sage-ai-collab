# Documentation Standards (SSOT)

> Single source of truth for documentation writing standards

---

## Table of Contents

- [1. Format](#1-format)
- [2. Structure](#2-structure)
- [3. Token Efficiency](#3-token-efficiency)
- [4. Writing](#4-writing)
- [5. Organization](#5-organization)
- [6. Quality](#6-quality)

---

## 1. Format

### 1.1 Document Template

```markdown
# Title

> Single-line purpose

---

## Table of Contents (if >60 lines or >3 H2)

- [1. Section](#1-section)
- [2. Section](#2-section)

---

## 1. Section

### 1.1 Subsection

---

## Related

- `path/file.md` — Description

---

*Part of SAGE Knowledge Base*
```

### 1.2 Heading Rules

| Level | Format               | Numbering  | Use                 |
|-------|----------------------|------------|---------------------|
| H1    | `# Title`            | None       | Document title only |
| H2    | `## N. Section`      | 1., 2., 3. | Main sections       |
| H3    | `### N.N Subsection` | 1.1, 1.2   | Subsections         |
| H4    | `#### N.N.N Detail`  | 1.1.1      | Use sparingly       |

### 1.3 TOC Rules

| Condition                   | Action                                    |
|-----------------------------|-------------------------------------------|
| >60 lines OR >3 H2 headings | Add TOC                                   |
| Format                      | Vertical list with `- [Section](#anchor)` |
| Content                     | H2 sections only                          |
| Anchor                      | `#N-section-name` (lowercase, hyphens)    |

---

## 2. Structure

### 2.1 Section Order

1. Title + Purpose (header)
2. TOC (conditional)
3. Numbered content sections
4. Related (unnumbered)
5. Footer

### 2.2 Content Types

| Type      | Structure                              | Use For            |
|-----------|----------------------------------------|--------------------|
| Index     | Navigation table + descriptions        | Layer entry points |
| Guide     | Numbered steps + examples              | How-to content     |
| Reference | Tables + code blocks                   | API, config docs   |
| Framework | Concepts + patterns + examples         | Conceptual models  |
| Practice  | Patterns + anti-patterns + checklist   | Best practices     |
| Template  | Placeholders `[MARKER]` + instructions | Reusable documents |

### 2.3 Cross-References

| Element         | Format                          |
|-----------------|---------------------------------|
| Related section | Unnumbered, at document end     |
| Link format     | `path/file.md` — Description    |
| Link count      | 3-5 per document                |
| Priority        | Same layer first, then adjacent |

---

## 3. Token Efficiency

> **深入优化技术**: 参见 `practices/ai_collaboration/token_optimization.md`

### 3.1 High-Impact Patterns

| Pattern              | Savings | Use For                |
|----------------------|---------|------------------------|
| Tables vs paragraphs | ~40%    | Structured comparisons |
| Lists vs paragraphs  | ~30%    | Enumerations, steps    |
| Vertical TOC         | ~50%    | Document navigation    |
| Cross-references     | ~70%    | Repeated content       |

### 3.2 Anti-Patterns

| Avoid             | Problem         | Fix                   |
|-------------------|-----------------|-----------------------|
| Long paragraphs   | High token cost | Convert to table/list |
| Repeated content  | Waste           | Add cross-reference   |
| Verbose headers   | Overhead        | Single-line format    |
| Deep nesting (>3) | Complexity      | Flatten structure     |
| "In order to"     | Verbose         | "To"                  |
| "It is important" | Filler          | "Note:"               |

### 3.3 Target Metrics

| Metric               | Target |
|----------------------|--------|
| Tokens per section   | <500   |
| Lines per file       | <300   |
| H2 headings per file | 5-15   |
| Nesting depth        | ≤3     |
| Related links        | 3-5    |

---

## 4. Writing

### 4.1 Style Rules

| Rule          | ❌ Avoid                  | ✓ Prefer                       |
|---------------|--------------------------|--------------------------------|
| Active voice  | "File is read by loader" | "Loader reads file"            |
| Present tense | "This will create"       | "This creates"                 |
| Specific      | "Configure system"       | "Set `MAX=100` in config.yaml" |
| Concise       | "In order to"            | "To"                           |

### 4.2 Code Examples

**Requirements**: Complete · Minimal · Commented · Runnable

```python
# ✓ Good: focused, shows input/output
def greet(name: str) -> str:
    return f"Hello, {name}"


print(greet("World"))  # Output: Hello, World
```

### 4.3 File Naming

| Type     | Convention              | Example                      |
|----------|-------------------------|------------------------------|
| Markdown | `snake_case.md`         | `documentation_standards.md` |
| ADR      | `ADR-NNNN-title.md`     | `ADR-0001-fastmcp-choice.md` |
| Session  | `YYYY-MM-DD-topic.md`   | `2025-11-29-timeout.md`      |
| Handoff  | `YYYY-MM-DD-handoff.md` | `2025-11-29-api-handoff.md`  |

---

## 5. Organization

### 5.1 Layer Architecture

| Layer         | Purpose                 | Token Budget | Load Timing    |
|---------------|-------------------------|--------------|----------------|
| `core/`       | Foundational principles | ~500         | Always         |
| `guidelines/` | Standards, conventions  | ~1200        | By role/task   |
| `frameworks/` | Deep conceptual models  | ~2000        | On-demand      |
| `practices/`  | Actionable patterns     | ~1500        | Implementation |
| `scenarios/`  | Context presets         | ~500         | By trigger     |
| `templates/`  | Ready-to-use templates  | ~300         | Direct copy    |

### 5.2 Directory Conventions

| Directory   | Purpose                    | Git Policy |
|-------------|----------------------------|------------|
| `.context/` | Project-specific knowledge | Tracked    |
| `.history/` | Session history, handoffs  | Tracked    |
| `.archive/` | Historical/deprecated      | Tracked    |
| `.backups/` | Pre-change snapshots       | Tracked    |
| `.logs/`    | Runtime logs               | Ignored    |
| `.outputs/` | Intermediate files         | Ignored    |
| `content/`  | Generic reusable knowledge | Tracked    |
| `docs/`     | User-facing documentation  | Tracked    |

### 5.3 Content Placement

| Content Type         | Location                |
|----------------------|-------------------------|
| Project conventions  | `.context/conventions/` |
| Universal guidelines | `content/guidelines/`   |
| ADR records          | `.context/decisions/`   |
| API documentation    | `docs/api/`             |
| Session handoffs     | `.history/handoffs/`    |
| Deprecated content   | `.archive/`             |

### 5.4 MECE Principle

| Aspect                  | Application               |
|-------------------------|---------------------------|
| Mutually Exclusive      | No overlapping content    |
| Collectively Exhaustive | Complete coverage         |
| Single location         | Each concept defined once |
| Cross-reference         | Link, don't duplicate     |

---

## 6. Quality

### 6.1 Quality Checklist

**Header**:

- [ ] H1 title (no emoji in production)
- [ ] Single-line blockquote purpose
- [ ] Horizontal rule after header

**Structure**:

- [ ] TOC if >60 lines or >3 H2
- [ ] TOC uses vertical list format
- [ ] H2 sections numbered
- [ ] H3 uses decimal notation

**Content**:

- [ ] Tables for comparisons
- [ ] Lists for enumerations
- [ ] No redundant info (cross-ref)
- [ ] Code blocks for examples

**Navigation**:

- [ ] Related section present
- [ ] 3-5 cross-references
- [ ] Relative path links
- [ ] `—` separator in descriptions

**Footer**:

- [ ] Horizontal rule before
- [ ] `*Part of SAGE Knowledge Base*`

### 6.2 Update Triggers

| Event         | Action               |
|---------------|----------------------|
| Code change   | Update affected docs |
| API change    | Update reference     |
| New feature   | Add guide            |
| User question | Improve clarity      |

### 6.3 Optimization Workflow

```
1. Review against checklist
       ↓
2. Identify deviations
       ↓
3. Batch apply fixes
       ↓
4. Verify consistency
```

---

## Related

- `knowledge_organization.md` — Layer architecture details
- `optimization_workflow.md` — Full optimization process
- `project_directory_structure.md` — Directory conventions details
- `content/templates/index.md` — Document templates

---

*Part of SAGE Knowledge Base*
