# Document Template

> Standard template for all Markdown documents in SAGE Knowledge Base

---

## 1. Template Structure

```markdown
# Document Title

> Single-line purpose description

---

## 1. First Section

Content.

### 1.1 Subsection

More content.

---

## 2. Second Section

| Column A | Column B |
|----------|----------|
| Value 1  | Value 2  |

---

## Related

- `path/FILE.md` — Description

---

*Part of SAGE Knowledge Base*
```

---

## 2. Rules

### 2.1 Frontmatter

| Rule | Description |
|------|-------------|
| **No Frontmatter** | Do not use YAML frontmatter (`---` blocks at start) |
| **Metadata in content** | If needed, use a table in the document body |

### 2.2 Table of Contents

| Condition | TOC Required |
|-----------|--------------|
| Lines > 100 | Optional |
| H2 sections > 5 | Optional |
| Lines ≤ 100 AND H2 ≤ 5 | Not needed |

### 2.3 Section Separators

```markdown
---

## Section Title
```

- Use `---` (horizontal rule) before each H2 section
- No separator before the first H1 title

### 2.4 Line Count

| Limit | Action |
|-------|--------|
| < 300 lines | ✅ Ideal |
| 300-500 lines | ⚠️ Consider splitting |
| > 500 lines | ❌ Must split |

### 2.5 Related Section

| Rule | Description |
|------|-------------|
| Position | Last section before footer |
| Count | 2-5 links |
| Format | `- \`path/FILE.md\` — Description` |

### 2.6 Footer

```markdown
---

*Part of SAGE Knowledge Base*
```

- Always present
- Consistent across all documents

---

## 3. Heading Conventions

### 3.1 Hierarchy

| Level | Usage | Example |
|-------|-------|---------|
| H1 (`#`) | Document title only | `# SAGE Protocol` |
| H2 (`##`) | Major sections | `## 1. Overview` |
| H3 (`###`) | Subsections | `### 1.1 Purpose` |
| H4 (`####`) | Sub-subsections | `#### Implementation` |

### 3.2 Numbering

- H2 sections: numbered (`## 1.`, `## 2.`, etc.)
- H3 subsections: decimal numbered (`### 1.1`, `### 1.2`)
- Exception: `## Related` section is unnumbered

---

## 4. Content Guidelines

### 4.1 Tables

```markdown
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
```

- Use for structured data
- Align pipes for readability
- Keep tables concise (≤ 10 rows ideal)

### 4.2 Code Blocks

```markdown
\`\`\`python
def example():
    pass
\`\`\`
```

- Always specify language
- Keep blocks focused (< 30 lines)

### 4.3 Lists

- Use `-` for unordered lists
- Use `1.` for ordered lists
- Indent with 2 spaces for nested items

---

## 5. Checklist

- [ ] No Frontmatter
- [ ] Single-line description after H1
- [ ] `---` before each H2
- [ ] Numbered H2 sections
- [ ] < 300 lines
- [ ] Related section with 2-5 links
- [ ] Standard footer

---

## Related

- `.context/conventions/NAMING.md` — File naming rules
- `.context/conventions/DIRECTORY_STRUCTURE.md` — Where to place documents
- `.knowledge/guidelines/DOCUMENTATION.md` — General documentation guidelines

---

*AI Collaboration Knowledge Base*
