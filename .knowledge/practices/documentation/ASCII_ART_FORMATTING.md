# ASCII Art Formatting Best Practices

> Guidelines for consistent rendering of ASCII art boxes and diagrams

---

## Table of Contents

- [1. Problem](#1-problem)
- [2. Root Cause](#2-root-cause)
- [3. Solution](#3-solution)
- [4. Patterns](#4-patterns)
- [5. Checklist](#5-checklist)

---

## 1. Problem

ASCII art boxes and diagrams may render with misaligned borders across different environments:

```
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

Different environments render character widths differently:

| Environment          | Emoji Width Behavior |
|:---------------------|:---------------------|
| Terminal (monospace) | Often 2 columns      |
| IDE editor           | Varies by font       |
| Markdown preview     | Varies by renderer   |
| GitHub               | Usually 2 columns    |
| Web browser          | Font-dependent       |

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

```
│ ├── Junie integration: ✅ Complete                          │
```

**After** (consistent):

```
│ ├── Junie integration: [OK] Complete                        │
```

---

## 4. Patterns

### 4.1 Recommended Pattern

```
┌─────────────────────────────────────────────────────────────┐
│ Title: Description                                          │
│ ├── Item one: [OK] Status                                   │
│ ├── Item two: [X] Failed                                    │
│ └── Item three: [!] Warning                                 │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Anti-Pattern

```
┌─────────────────────────────────────────────────────────────┐
│ Title: Description                                          │
│ ├── Item one: ✅ Status                                     │  ← Unpredictable
│ ├── Item two: ❌ Failed                                     │  ← Unpredictable
│ └── Item three: ⚠️ Warning                                  │  ← Unpredictable
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Checklist

When creating ASCII art boxes or diagrams:

- [ ] Use only ASCII characters for content inside boxes
- [ ] Box-drawing characters (─│┌┐└┘├┤) are acceptable (consistent width)
- [ ] Replace emojis with ASCII equivalents: `[OK]`, `[X]`, `[!]`
- [ ] Test rendering in target environment before committing
- [ ] Count character positions manually if alignment is critical

---

## Related

- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — General documentation formatting
- `.knowledge/references/unicode/CHARACTER_WIDTH.md` — Unicode width reference (if exists)

---

*AI Collaboration Knowledge Base*
