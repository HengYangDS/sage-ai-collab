---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~1100
---

# Token Optimization Principles

> Maximize knowledge density per token in AI collaboration

---

## Table of Contents

- [1. Core Principles](#1-core-principles)
- [2. High-Efficiency Patterns](#2-high-efficiency-patterns)
- [3. Content Compression](#3-content-compression)
- [4. Anti-Patterns](#4-anti-patterns)
- [5. Document Optimization](#5-document-optimization)
- [6. Tiered Loading](#6-tiered-loading)
- [7. Quick Reference](#7-quick-reference)

---

## 1. Core Principles

| Principle                 | Application         |
|---------------------------|---------------------|
| Density over verbosity    | Tables > paragraphs |
| Structure over prose      | Bullets > sentences |
| Reference over repeat     | Links > duplication |
| Progressive over complete | Load as needed      |

---

## 2. High-Efficiency Patterns

| Pattern       | Token Savings | Use Case         |
|---------------|---------------|------------------|
| Tables        | ~40%          | Structured data  |
| Bullet lists  | ~30%          | Enumerations     |
| Code blocks   | ~20%          | Examples         |
| Abbreviations | ~15%          | Common terms     |
| References    | ~70%          | Repeated content |

---

## 3. Content Compression

### 3.1 Text Compression

| Before                         | After        | Savings |
|--------------------------------|--------------|---------|
| "In order to"                  | "To"         | 75%     |
| "It is important to note that" | "Note:"      | 80%     |
| "There are several ways to"    | "Ways to:"   | 70%     |
| Passive voice                  | Active voice | 20%     |

### 3.2 Structure Compression

| Technique              | Application          |
|------------------------|----------------------|
| Headers as summaries   | Key info in heading  |
| Tables for comparisons | Replace paragraphs   |
| Code for examples      | Replace descriptions |
| Links for details      | Replace repetition   |

---

## 4. Anti-Patterns

| Anti-Pattern         | Problem         | Solution           |
|----------------------|-----------------|--------------------|
| Long paragraphs      | High token cost | Use tables/bullets |
| Repeated information | Waste           | Cross-reference    |
| Verbose explanations | Inefficient     | Compress           |
| Unnecessary context  | Noise           | Filter             |
| Embedded images      | No AI benefit   | Remove or describe |

---

## 5. Document Optimization

### 5.1 Target Metrics

| Metric             | Target |
|--------------------|--------|
| Tokens per section | < 500  |
| Lines per file     | < 300  |
| Info density       | High   |

### 5.2 Optimization Process

| Step | Action                    |
|------|---------------------------|
| 1    | Identify verbose sections |
| 2    | Convert to tables/bullets |
| 3    | Remove redundancy         |
| 4    | Add cross-references      |
| 5    | Validate completeness     |

> **详细格式规范**: 参见 `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md`

---

## 6. Tiered Loading

| Tier      | Content         | When to Load      |
|-----------|-----------------|-------------------|
| Always    | Core principles | Every session     |
| On-demand | Guidelines      | When relevant     |
| Deep      | Frameworks      | Complex decisions |
| Reference | Full details    | Specific queries  |

---

## 7. Quick Reference

| ✓ Do               | ❌ Don't            |
|--------------------|--------------------|
| Use tables         | Write paragraphs   |
| Reference files    | Repeat content     |
| Load progressively | Dump everything    |
| Compress text      | Be verbose         |
| Structure clearly  | Use prose for data |

---

## 8. Practical Examples

### Example 1: Before/After Optimization

**Before** (~120 tokens):
```
In order to ensure that the application performs well, it is important 
to note that you should implement caching for frequently accessed data.
There are several ways to accomplish this task effectively.
```

**After** (~40 tokens):
```
Performance: Implement caching for frequent data access.
Options: Redis | Memcached | In-memory
```

### Example 2: Context Loading

**Inefficient**:
```
Load: entire docs/ directory (5000+ tokens)
```

**Optimized**:
```
Load: docs/api/AUTH.md lines 1-50 (~200 tokens)
```

---

## Related

- `.knowledge/practices/ai_collaboration/CONTEXT_MANAGEMENT.md` — Context efficiency
- `.knowledge/frameworks/cognitive/INFORMATION_DENSITY.md` — Density framework

---

*Part of SAGE Knowledge Base*
