# Document Optimization Workflow

> Systematic workflow for batch document optimization and quality assurance

---

## Table of Contents

[1. Optimization Process](#1-optimization-process) · [2. Quality Checklist](#2-quality-checklist) · [3. Token Efficiency Patterns](#3-token-efficiency-patterns) · [4. Quality Metrics](#4-quality-metrics) · [5. Common Issues](#5-common-issues)

---

## 1. Optimization Process

### 1.1 Workflow Steps

```
1. Establish Standards (standards.md)
       ↓
2. Systematic File Review
       ↓
3. Identify Deviation Patterns
       ↓
4. Batch Apply Corrections
       ↓
5. Verify Consistency
```

### 1.2 Review Order

| Phase | Focus | Files |
|-------|-------|-------|
| 1 | Standards document | `standards.md` |
| 2 | Index files | `*/index.md` |
| 3 | Core content | High-traffic files |
| 4 | Supporting content | Remaining files |

### 1.3 Batch Processing Tips

| Tip | Benefit |
|-----|---------|
| Process by directory | Maintain context |
| Fix one issue type at a time | Consistency |
| Use search/replace patterns | Efficiency |
| Verify after each batch | Catch errors early |

---

## 2. Quality Checklist

### 2.1 Header Check

- [ ] H1 title present (no emoji in production)
- [ ] Single-line blockquote purpose
- [ ] Horizontal rule after header
- [ ] No metadata clutter (version, dates, etc.)

### 2.2 Structure Check

- [ ] TOC present if > 60 lines or > 3 H2 headings
- [ ] TOC uses inline `·` separator format
- [ ] H2 sections numbered (1., 2., 3.)
- [ ] H3 subsections use decimal (1.1, 1.2)
- [ ] Nesting depth ≤ 3 levels

### 2.3 Content Check

- [ ] Tables used for structured comparisons
- [ ] Lists used for enumerations
- [ ] No redundant information (use cross-references)
- [ ] Code blocks for examples

### 2.4 Navigation Check

- [ ] Related section present (unnumbered, at end)
- [ ] 3-5 relevant cross-references
- [ ] Links use relative paths
- [ ] Descriptions use `—` separator

### 2.5 Footer Check

- [ ] Horizontal rule before footer
- [ ] Standard footer: `*Part of SAGE Knowledge Base*`
- [ ] No custom signatures

---

## 3. Token Efficiency Patterns

### 3.1 High-Impact Patterns

| Pattern | Token Savings | Application |
|---------|---------------|-------------|
| Tables vs paragraphs | ~40% | Structured comparisons |
| Lists vs paragraphs | ~30% | Enumerations, steps |
| Inline TOC vs list | ~50% | Document navigation |
| References vs repeat | ~70% | Cross-document content |
| Single-line header | ~60% | Document headers |

### 3.2 Compression Techniques

| Before | After | Savings |
|--------|-------|---------|
| "In order to" | "To" | 75% |
| "It is important to note that" | "Note:" | 80% |
| Multi-line metadata | Single blockquote | 60% |
| Verbose explanations | Tables | 40% |

### 3.3 Anti-Patterns to Fix

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Long paragraphs | High token cost | Convert to table/list |
| Repeated content | Waste | Add cross-reference |
| Verbose headers | Overhead | Single-line format |
| Deep nesting | Complexity | Flatten structure |

---

## 4. Quality Metrics

### 4.1 Target Values

| Metric | Target | Rationale |
|--------|--------|-----------|
| Tokens per section | < 500 | Manageable context chunks |
| Lines per file | < 300 | Quick to scan |
| H2 headings per file | 5-15 | Clear but not fragmented |
| Nesting depth | ≤ 3 | Avoid complexity |
| Related links | 3-5 | Sufficient navigation |

### 4.2 Measurement

| What to Count | How |
|---------------|-----|
| Line count | `wc -l file.md` |
| H2 count | `grep -c "^## " file.md` |
| Missing TOC | Lines > 60 AND no "Table of Contents" |
| Missing Related | No "## Related" section |

---

## 5. Common Issues

### 5.1 Issue Patterns

| Issue | Frequency | Fix |
|-------|-----------|-----|
| Missing TOC | High | Add inline TOC |
| Unnumbered sections | High | Add section numbers |
| Missing Related | Medium | Add 3-5 links |
| Non-standard footer | Medium | Replace with standard |
| Verbose headers | Low | Compress to single line |

### 5.2 Prevention

| Practice | Benefit |
|----------|---------|
| Use document template | Correct structure from start |
| Review before commit | Catch issues early |
| Periodic audits | Maintain consistency |
| Automate checks | Scale quality assurance |

---

## Related

- `content/practices/documentation/standards.md` — Documentation format standards
- `content/practices/documentation/knowledge_organization.md` — Knowledge hierarchy patterns
- `content/guidelines/documentation.md` — Documentation guidelines

---

*Part of SAGE Knowledge Base*
