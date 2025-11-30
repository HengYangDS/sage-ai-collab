# 信达雅 (Xìn Dá Yǎ)

> The three pillars of SAGE design philosophy: Faithfulness, Expressiveness, Elegance

---

## 1. Origin

信达雅 originates from Yan Fu's (严复) translation principles, now adapted as SAGE's core design philosophy:

| Chinese | Pinyin | English | SAGE Interpretation |
|---------|--------|---------|---------------------|
| 信 | Xìn | Faithfulness | Accurate, truthful representation |
| 达 | Dá | Expressiveness | Clear, effective communication |
| 雅 | Yǎ | Elegance | Refined, maintainable design |

---

## 2. 信 (Faithfulness)

### 2.1 Definition

**Faithfulness** means the system accurately represents knowledge without distortion or loss.

### 2.2 Principles

| Principle | Description |
|-----------|-------------|
| **Accuracy** | Information is correct and verified |
| **Completeness** | No important details omitted |
| **Traceability** | Source and provenance are clear |
| **Consistency** | Same input yields same output |

### 2.3 Application

```
Knowledge Source → SAGE Processing → Output
      ↓                  ↓              ↓
  Original          Preserved       Faithful
  meaning           integrity       representation
```

### 2.4 Anti-Patterns

- ❌ Summarizing away critical details
- ❌ Adding information not in source
- ❌ Changing meaning during transformation
- ❌ Losing context or attribution

---

## 3. 达 (Expressiveness)

### 3.1 Definition

**Expressiveness** means the system communicates clearly and effectively to its audience.

### 3.2 Principles

| Principle | Description |
|-----------|-------------|
| **Clarity** | Easy to understand |
| **Accessibility** | Appropriate for audience |
| **Directness** | No unnecessary complexity |
| **Actionability** | Enables user action |

### 3.3 Application

```
User Need → SAGE Response → User Understanding
    ↓            ↓               ↓
  Question    Clear           Actionable
  or task     answer          outcome
```

### 3.4 Anti-Patterns

- ❌ Using jargon without explanation
- ❌ Providing irrelevant information
- ❌ Burying important points
- ❌ Being verbose without value

---

## 4. 雅 (Elegance)

### 4.1 Definition

**Elegance** means the system is refined, maintainable, and aesthetically pleasing in design.

### 4.2 Principles

| Principle | Description |
|-----------|-------------|
| **Simplicity** | No unnecessary complexity |
| **Consistency** | Uniform patterns throughout |
| **Maintainability** | Easy to understand and modify |
| **Beauty** | Pleasing structure and form |

### 4.3 Application

```
Requirements → SAGE Design → Implementation
      ↓            ↓              ↓
   Complex      Elegant        Maintainable
   needs        solution       codebase
```

### 4.4 Anti-Patterns

- ❌ Over-engineering solutions
- ❌ Inconsistent patterns
- ❌ Clever but unreadable code
- ❌ Ignoring established conventions

---

## 5. Balance and Trade-offs

### 5.1 Priority Order

When principles conflict, prioritize:

```
信 (Faithfulness) > 达 (Expressiveness) > 雅 (Elegance)
```

**Rationale:**
1. Truth must never be sacrificed for clarity
2. Clarity must never be sacrificed for beauty
3. Beauty emerges from truth and clarity

### 5.2 Trade-off Examples

| Scenario | Resolution |
|----------|------------|
| Accurate but unclear | Add explanation, keep accuracy |
| Clear but inaccurate | Fix accuracy, adjust clarity |
| Elegant but incomplete | Add completeness, simplify later |

---

## 6. Practical Guidelines

### 6.1 For Documentation

| Principle | Guideline |
|-----------|-----------|
| 信 | Cite sources, verify facts |
| 达 | Use clear language, provide examples |
| 雅 | Follow templates, maintain consistency |

### 6.2 For Code

| Principle | Guideline |
|-----------|-----------|
| 信 | Correct behavior, tested thoroughly |
| 达 | Clear naming, good documentation |
| 雅 | Clean architecture, consistent style |

### 6.3 For APIs

| Principle | Guideline |
|-----------|-----------|
| 信 | Accurate responses, proper errors |
| 达 | Intuitive interface, good docs |
| 雅 | Consistent design, RESTful patterns |

---

## Related

- `DESIGN_AXIOMS.md` — Core design axioms
- `../protocols/SAGE_PROTOCOL.md` — SAGE protocol
- `.knowledge/frameworks/design/AXIOMS.md` — Design framework

---

*Part of SAGE Knowledge Base*
