# Documentation Standards

> Single source of truth for document format and structure standards

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

- `path/FILE.md` — Description

---

*AI Collaboration Knowledge Base*
```text
**Note**: Frontmatter metadata (version, tokens, etc.) is NOT used. Document content speaks for itself.

### 1.2 Heading Rules

| Level | Format | Numbering | Use |
|-------|--------|-----------|-----|
| H1 | `# Title` | None | Document title only |
| H2 | `## N. Section` | 1., 2., 3. | Main sections |
| H3 | `### N.N Subsection` | 1.1, 1.2 | Subsections |
| H4 | `#### N.N.N Detail` | 1.1.1 | Use sparingly |

### 1.3 TOC Rules

| Condition | Action |
|-----------|--------|
| >60 lines OR >3 H2 headings | Add TOC |
| Format | Vertical list `- [Section](#anchor)` |
| Content | H2 sections only |
| Anchor | `#N-section-name` (lowercase, hyphens) |

### 1.4 File Naming

| Type | Convention | Example |
|------|------------|---------|
| Markdown | `UPPER_SNAKE_CASE.md` | `DOCUMENTATION_STANDARDS.md` |
| ADR | `ADR_NNNN_TITLE.md` | `ADR_0001_ARCHITECTURE.md` |
| Session | `YYYYMMDD-TOPIC.md` | `20251130-TIMEOUT.md` |
| Index | `INDEX.md` | `INDEX.md` |

**Exception**: `.junie/` directory uses `lowercase.md` to comply with Junie tool conventions.

---

## 2. Structure

### 2.1 Section Order

1. Title + Purpose (header)
2. TOC (conditional)
3. Numbered content sections
4. Related (unnumbered)
5. Footer

### 2.2 Content Types

| Type | Structure | Use For |
|------|-----------|---------|
| Index | Navigation table + descriptions | Layer entry points |
| Guide | Numbered steps + examples | How-to content |
| Reference | Tables + code blocks | API, config docs |
| Framework | Concepts + patterns + examples | Conceptual models |
| Practice | Patterns + anti-patterns + checklist | Best practices |
| Template | Placeholders `[MARKER]` + instructions | Reusable documents |

### 2.3 Cross-References

| Element | Format |
|---------|--------|
| Related section | Unnumbered, at document end |
| Link format | `path/FILE.md` — Description |
| Link count | 3-5 per document |
| Priority | Same layer first, then adjacent |

### 2.4 Path Format Standard

**Rule**: All paths MUST use **project-root-relative paths** (starting with `.`).

| ✅ Correct | ❌ Incorrect |
|-----------|-------------|
| `.knowledge/guidelines/DOCUMENTATION.md` | `DOCUMENTATION.md` |
| `.knowledge/practices/documentation/INDEX.md` | `../practices/documentation/INDEX.md` |

**Rationale**:
- Unambiguous location regardless of current file
- IDE-friendly with Ctrl+Click navigation
- No broken links when files move within directory

**Rules**:
1. Start with `.` (project root)
2. Use forward slashes `/` (cross-platform)
3. Include `.md` extension
4. Never use `../` relative paths

---

## 3. Token Efficiency

### 3.1 High-Impact Patterns

| Pattern | Savings | Use For |
|---------|---------|---------|
| Tables vs paragraphs | ~40% | Structured comparisons |
| Lists vs paragraphs | ~30% | Enumerations, steps |
| Vertical TOC | ~50% | Document navigation |
| Cross-references | ~70% | Repeated content |

### 3.2 Anti-Patterns

| Avoid | Problem | Fix |
|-------|---------|-----|
| Long paragraphs | High token cost | Convert to table/list |
| Repeated content | Waste | Add cross-reference |
| Verbose headers | Overhead | Single-line format |
| Deep nesting (>3) | Complexity | Flatten structure |
| "In order to" | Verbose | "To" |
| "It is important" | Filler | "Note:" |

### 3.3 Target Metrics

| Metric | Target |
|--------|--------|
| Tokens per section | <500 |
| Lines per file | <300 |
| H2 headings per file | 5-15 |
| Nesting depth | ≤3 |
| Related links | 3-5 |

---

## 4. Writing

### 4.1 Style Rules

| Rule | ❌ Avoid | ✅ Prefer |
|------|----------|----------|
| Active voice | "File is read by loader" | "Loader reads file" |
| Present tense | "This will create" | "This creates" |
| Specific | "Configure system" | "Set `MAX=100`" |
| Concise | "In order to" | "To" |

### 4.2 Code Examples

**Requirements**: Complete · Minimal · Commented · Runnable

```python
# ✓ Good: focused, shows input/output
def greet(name: str) -> str:
    return f"Hello, {name}"

print(greet("World"))  # Output: Hello, World
```text
> **Full Standards**: See `CODE_BLOCK_STANDARDS.md`

---

## 5. Organization

### 5.1 Layer Architecture

> **SSOT**: See `.knowledge/practices/documentation/KNOWLEDGE_ORGANIZATION.md` for complete `.knowledge/` layer definitions.

| Layer | Token Budget | Load Timing |
|-------|--------------|-------------|
| `core/` | ~500 | Always |
| `guidelines/` | ~1,200 | By role/task |
| `frameworks/` | ~2,000 | On-demand |
| `practices/` | ~1,500 | Implementation |
| `references/` | ~300 | On-demand |
| `scenarios/` | ~500 | By trigger |
| `templates/` | ~300 | Direct copy |

### 5.2 Directory Conventions

| Directory | Purpose | Git Policy |
|-----------|---------|------------|
| `.knowledge/` | Generic reusable knowledge | Tracked |
| `.context/` | Project-specific knowledge | Tracked |
| `.history/` | Session history, handoffs | Tracked |
| `.archive/` | Historical/deprecated | Tracked |
| `.outputs/` | Intermediate files | Ignored |
| `docs/` | User-facing documentation | Tracked |

### 5.3 Content Placement

| Content Type | Location |
|--------------|----------|
| Project conventions | `.context/conventions/` |
| Universal guidelines | `.knowledge/guidelines/` |
| ADR records | `.context/decisions/` |
| API documentation | `docs/api/` |
| Session handoffs | `.history/handoffs/` |

### 5.4 MECE Principle

| Aspect | Application |
|--------|-------------|
| Mutually Exclusive | No overlapping content |
| Collectively Exhaustive | Complete coverage |
| Single location | Each concept defined once |
| Cross-reference | Link, don't duplicate |

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
- [ ] Project-root-relative paths
- [ ] `—` separator in descriptions

**Footer**:
- [ ] Horizontal rule before
- [ ] `*AI Collaboration Knowledge Base*`

### 6.2 Update Triggers

| Event | Action |
|-------|--------|
| Code change | Update affected docs |
| API change | Update reference |
| New feature | Add guide |
| User question | Improve clarity |

### 6.3 Optimization Workflow

```text
1. Review against checklist
       ↓
2. Identify deviations
       ↓
3. Batch apply fixes
       ↓
4. Verify consistency
```text
> **Full Workflow**: See `OPTIMIZATION_WORKFLOW.md`

---

## Related

- `.knowledge/practices/documentation/INDEX.md` — Documentation practices index
- `.knowledge/practices/documentation/DIAGRAM_STANDARDS.md` — Diagram creation standards
- `.knowledge/practices/documentation/TABLE_STANDARDS.md` — Table creation standards
- `.knowledge/practices/documentation/CODE_BLOCK_STANDARDS.md` — Code block standards
- `.knowledge/guidelines/DOCUMENTATION.md` — Documentation guidelines (rules overview)

---

*AI Collaboration Knowledge Base*
