# Document Optimization Workflow

> Systematic workflow for batch document optimization and quality assurance

---

## Table of Contents

- [1. Optimization Process](#1-optimization-process)
- [2. Quality Checklist](#2-quality-checklist)
- [3. Token Efficiency & Quality Metrics](#3-token-efficiency--quality-metrics)
- [4. Common Issues](#4-common-issues)

---

## 1. Optimization Process

### 1.1 Workflow Steps

```text
1. Establish Standards (DOCUMENTATION_STANDARDS.md)
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

| Phase | Focus              | Files                        |
|-------|--------------------|------------------------------|
| 1     | Standards document | `DOCUMENTATION_STANDARDS.md` |
| 2     | Index files        | `*/INDEX.md`                 |
| 3     | Core content       | High-traffic files           |
| 4     | Supporting content | Remaining files              |

### 1.3 Batch Processing Tips

| Tip                          | Benefit            |
|------------------------------|--------------------|
| Process by directory         | Maintain context   |
| Fix one issue type at a time | Consistency        |
| Use search/replace patterns  | Efficiency         |
| Verify after each batch      | Catch errors early |

---

## 2. Quality Checklist

### 2.1 Header Check

- [ ] H1 title present (no emoji in production)
- [ ] Single-line blockquote purpose
- [ ] Horizontal rule after header
- [ ] No metadata clutter (version, dates, etc.)

### 2.2 Structure Check

- [ ] TOC present if > 60 lines or > 3 H2 headings
- [ ] TOC uses vertical list format `- [Section](#anchor)`
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
- [ ] Standard footer: `*AI Collaboration Knowledge Base*`
- [ ] No custom signatures

---

## 3. Token Efficiency & Quality Metrics

> **Full Reference**: See `DOCUMENTATION_STANDARDS.md` Section 3 (Token Efficiency) for patterns, compression techniques, anti-patterns, and target metrics.

### 3.1 Quick Measurement Commands

| What to Count   | How                                   |
|-----------------|---------------------------------------|
| Line count      | `wc -l FILE.md`                       |
| H2 count        | `grep -c "^## " FILE.md`              |
| Missing TOC     | Lines > 60 AND no "Table of Contents" |
| Missing Related | No "## Related" section               |

---

## 4. Common Issues

### 4.1 Issue Patterns

| Issue               | Frequency | Fix                     |
|---------------------|-----------|-------------------------|
| Missing TOC         | High      | Add inline TOC          |
| Unnumbered sections | High      | Add section numbers     |
| Missing Related     | Medium    | Add 3-5 links           |
| Non-standard footer | Medium    | Replace with standard   |
| Verbose headers     | Low       | Compress to single line |

### 4.2 Prevention

| Practice              | Benefit                      |
|-----------------------|------------------------------|
| Use document template | Correct structure from start |
| Review before commit  | Catch issues early           |
| Periodic audits       | Maintain consistency         |
| Automate checks       | Scale quality assurance      |

---

## Related

- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Documentation format standards
- `.knowledge/practices/documentation/KNOWLEDGE_ORGANIZATION.md` — Knowledge hierarchy patterns
- `.knowledge/guidelines/DOCUMENTATION.md` — Documentation guidelines

---

*AI Collaboration Knowledge Base*
