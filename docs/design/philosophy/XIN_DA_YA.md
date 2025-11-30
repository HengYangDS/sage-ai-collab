# 信达雅 (Xìn Dá Yǎ)

> SAGE design philosophy: Faithfulness, Expressiveness, Elegance
>
> **Authoritative Definition**: `.knowledge/core/PRINCIPLES.md`

---

## 1. Overview

信达雅 originates from Yan Fu's (严复) translation principles, now adapted as SAGE's core design philosophy.

> **See**: `.knowledge/core/PRINCIPLES.md` for the authoritative definition of 信达雅 and 术法道 frameworks.

| Chinese | Pinyin | English | SAGE Application |
|---------|--------|---------|------------------|
| 信 | Xìn | Faithfulness | Accurate, truthful representation |
| 达 | Dá | Expressiveness | Clear, effective communication |
| 雅 | Yǎ | Elegance | Refined, maintainable design |

---

## 2. Priority Order

**信 → 达 → 雅** (Faithfulness before Clarity before Elegance)

- Never sacrifice correctness for beauty
- Never sacrifice clarity for brevity
- Elegance emerges from faithful, clear solutions

---

## 3. SAGE-Specific Applications

This section describes how 信达雅 applies specifically to SAGE's design decisions.

### 3.1 Knowledge Representation (信)

| Principle | Application in SAGE |
|-----------|---------------------|
| Accuracy | Knowledge content verified before inclusion |
| Completeness | All relevant context preserved |
| Traceability | Source and version tracked |
| Consistency | Same query yields same result |

### 3.2 User Interface (达)

| Principle | Application in SAGE |
|-----------|---------------------|
| Clarity | CLI output easy to understand |
| Accessibility | Multiple interfaces (CLI, MCP, Python) |
| Directness | Minimal steps to get knowledge |
| Actionability | Results directly usable |

### 3.3 Architecture (雅)

| Principle | Application in SAGE |
|-----------|---------------------|
| Simplicity | Minimal dependencies |
| Consistency | Uniform patterns across modules |
| Maintainability | Clear separation of concerns |
| Beauty | Clean, readable codebase |

---

## 4. Design Decision Examples

### 4.1 Timeout Hierarchy Design

| Aspect | 信 (Faithful) | 达 (Clear) | 雅 (Elegant) |
|--------|---------------|------------|--------------|
| Design | 5 distinct levels | Named levels (T1-T5) | Progressive fallback |
| Outcome | Predictable behavior | Easy to configure | Graceful degradation |

### 4.2 Knowledge Layer Design

| Aspect | 信 (Faithful) | 达 (Clear) | 雅 (Elegant) |
|--------|---------------|------------|--------------|
| Design | Priority hierarchy | Named layers | Single responsibility |
| Outcome | Correct precedence | Easy navigation | Clean architecture |

---

## 5. Anti-Patterns

### 5.1 Violating 信 (Faithfulness)

- ❌ Summarizing away critical details
- ❌ Adding information not in source
- ❌ Changing meaning during transformation

### 5.2 Violating 达 (Expressiveness)

- ❌ Using jargon without explanation
- ❌ Providing irrelevant information
- ❌ Burying important points

### 5.3 Violating 雅 (Elegance)

- ❌ Over-engineering solutions
- ❌ Inconsistent patterns
- ❌ Clever but unreadable code

---

## Related

- `.knowledge/core/PRINCIPLES.md` — **Authoritative 信达雅 definition**
- `DESIGN_AXIOMS.md` — Design axioms derived from 信达雅
- `../INDEX.md` — Design documentation index

---

*Part of SAGE Knowledge Base*
