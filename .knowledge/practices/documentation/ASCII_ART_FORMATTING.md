# ASCII Art Formatting Best Practices

> Guidelines for consistent rendering of ASCII art boxes and diagrams

---

## Table of Contents

- [1. Problem](#1-problem)
- [2. Root Cause](#2-root-cause)
- [3. Solution](#3-solution)
- [4. Checklist](#4-checklist)

---

## 1. Problem

ASCII art boxes and diagrams may render with misaligned borders across different environments:

```text
┌─────────────────────────────────────────┐
│ Example with emoji: ✅ Complete         │  ← Misaligned!
│ Example without emoji: OK              │
└─────────────────────────────────────────┘
```
The right border `│` appears misaligned because emojis and special Unicode characters have unpredictable display widths.

---

## 2. Root Cause

### 2.1 Character Width Variability

| Character Type | Byte Width | Display Width | Predictable |
|:---------------|:-----------|:--------------|:------------|
| ASCII (A-Z)    | 1 byte     | 1 column      | ✓ Yes       |
| Emoji (✅)      | 3-4 bytes  | 1-2 columns   | ✗ No        |
| CJK (中文)       | 3 bytes    | 2 columns     | Mostly      |
| Box drawing    | 3 bytes    | 1 column      | ✓ Yes       |

### 2.2 Environment Differences

Emoji display width varies by environment (terminal, IDE, Markdown preview, GitHub, browser) — making consistent
alignment impossible.

---

## 3. Solution

### 3.1 Use ASCII-Only Characters

Replace emojis and special Unicode with ASCII equivalents:

| Avoid | Use Instead | Notes             |
|:------|:------------|:------------------|
| ✅     | `[OK]`      | Status indicator  |
| ❌     | `[X]`       | Failure indicator |
| ⚠️    | `[!]`       | Warning indicator |
| ✓     | `[v]`       | Checkmark         |
| →     | `-->`       | Arrow             |
| •     | `-` or `*`  | Bullet point      |

### 3.2 Example Fix

**Before** (problematic):

```text
│ ├── Junie integration: ✅ Complete                          │
```
**After** (consistent):

```text
│ ├── Junie integration: [OK] Complete                        │
```
---

## 4. Checklist

When creating ASCII art boxes or diagrams:

- [ ] Use only ASCII characters for content inside boxes
- [ ] Box-drawing characters (─│┌┐└┘├┤) are acceptable (consistent width)
- [ ] Replace emojis with ASCII equivalents: `[OK]`, `[X]`, `[!]`
- [ ] Test rendering in target environment before committing
- [ ] Count character positions manually if alignment is critical

---

## Related

- `.knowledge/practices/documentation/INDEX.md` — Documentation practices index
- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Document format standards
- `.knowledge/practices/documentation/CODE_BLOCK_STANDARDS.md` — Code block standards

---

*AI Collaboration Knowledge Base*
