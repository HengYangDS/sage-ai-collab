# Documentation Standards

> Unified standards for token-efficient, AI-friendly documentation

---

## 1. Document Format

### 1.1 Header Format

```markdown
# Document Title

> Single-line purpose statement

---
```

**Rules**:

- H1 title only (no emojis in production docs)
- One-line blockquote for purpose
- Horizontal rule separator
- No token estimates, load priorities, or version in header

### 1.2 Footer Format

```markdown
---

*Part of SAGE Knowledge Base*
```

**Rules**:

- Horizontal rule before footer
- Italic tagline only
- No custom messages or signatures

### 1.3 Section Numbering

| Level | Format               | Example                     |
|-------|----------------------|-----------------------------|
| H2    | `## 1. Section`      | `## 1. Overview`            |
| H3    | `### 1.1 Subsection` | `### 1.1 Core Concepts`     |
| H4    | `#### 1.1.1 Detail`  | `#### 1.1.1 Implementation` |

**Rules**:

- All H2 sections numbered (1., 2., 3.)
- H3 subsections use decimal notation (1.1, 1.2)
- H4 for deeper nesting (1.1.1) — use sparingly
- Related/References section unnumbered at end

---

## 2. Content Structure

### 2.1 File Organization

```
content/
├── [layer]/
│   ├── index.md          # Layer navigation
│   └── [topic]/
│       └── [file].md     # Topic content
```

**Naming**: `lowercase_with_underscores.md`

### 2.2 Section Order

1. Title + Purpose (header)
2. TOC (if > 60 lines or > 3 headings)
3. Numbered content sections
4. Related/References (unnumbered)
5. Footer

### 2.3 TOC Rules

| Condition     | Threshold | Action  |
|---------------|-----------|---------|
| Line count    | > 60      | Add TOC |
| Heading count | > 3       | Add TOC |

**TOC Format** (inline with `·` separator for token efficiency):

```markdown
## Table of Contents

[1. Section](#1-section) · [2. Section](#2-section) · [3. Section](#3-section)

---
```

**Rules**:

- List only H2 sections (not H3 subsections)
- Use `·` separator between links
- Include section numbers in link text
- Anchor format: `#N-section-name` (lowercase, hyphens)

---

## 3. Token Efficiency

### 3.1 High-Efficiency Patterns

| Pattern      | Use For                | Token Impact       |
|--------------|------------------------|--------------------|
| Tables       | Structured comparisons | -40% vs paragraphs |
| Inline code  | Commands, values       | Precise, scannable |
| Bullet lists | Enumerations           | -30% vs paragraphs |
| Code blocks  | Examples               | Clear boundaries   |

### 3.2 Avoid

| Anti-Pattern         | Problem         | Alternative     |
|----------------------|-----------------|-----------------|
| Long paragraphs      | High token cost | Tables/bullets  |
| Redundant headers    | Noise           | Merge sections  |
| Repeated info        | Waste           | Cross-reference |
| Excessive formatting | Token overhead  | Minimal markup  |

### 3.3 Target Metrics

| Metric             | Target |
|--------------------|--------|
| Tokens per section | < 500  |
| Lines per file     | < 300  |
| Headings per file  | 5-15   |

---

## 4. Writing Standards

### 4.1 Style Rules

| Rule          | ❌ Avoid                  | ✓ Prefer                       |
|---------------|--------------------------|--------------------------------|
| Active voice  | "File is read by loader" | "Loader reads file"            |
| Present tense | "This will create"       | "This creates"                 |
| Specific      | "Configure system"       | "Set `MAX=100` in config.yaml" |
| Concise       | "In order to"            | "To"                           |

### 4.2 Code Examples

**Good examples are**: Complete · Minimal · Commented · Runnable

```python
# ✓ Good: focused, complete
def greet(name: str) -> str:
    return f"Hello, {name}"


# Usage
print(greet("World"))  # Output: Hello, World
```

### 4.3 Cross-References

**Format**: `[Display Text](relative/path.md)` or in Related section:

```markdown
## Related

- `path/file.md` — Brief description
```

---

## 5. Content Types

| Type          | Structure                            | Use For            |
|---------------|--------------------------------------|--------------------|
| **Index**     | Navigation table + descriptions      | Layer entry points |
| **Guide**     | Numbered steps + examples            | How-to content     |
| **Reference** | Tables + code blocks                 | API, config docs   |
| **Framework** | Concepts + patterns + examples       | Conceptual models  |
| **Practice**  | Patterns + anti-patterns + checklist | Best practices     |

---

## 6. Maintenance

### 6.1 Update Triggers

| Event         | Action               |
|---------------|----------------------|
| Code change   | Update affected docs |
| API change    | Update reference     |
| New feature   | Add guide            |
| User question | Improve clarity      |

### 6.2 Quality Checklist

- [ ] Header follows format
- [ ] Sections numbered correctly
- [ ] Footer present
- [ ] Links verified
- [ ] Examples tested
- [ ] Token-efficient (tables over paragraphs)

---

## Related

- `optimization_workflow.md` — Batch optimization process
- `knowledge_organization.md` — Knowledge hierarchy patterns
- `../../guidelines/documentation.md` — Documentation guidelines
- `../ai_collaboration/token_optimization.md` — Token efficiency

---

*Part of SAGE Knowledge Base*
