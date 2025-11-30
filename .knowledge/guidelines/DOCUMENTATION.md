# Documentation Guidelines

> Clear, maintainable, useful documentation

---

## Table of Contents

- [1. Philosophy](#1-philosophy)
- [2. Document Types](#2-document-types)
- [3. Structure](#3-structure)
- [4. Writing Style](#4-writing-style)
- [5. Elements](#5-elements)
- [6. Maintenance](#6-maintenance)

---

## 1. Philosophy

| Principle                  | Application              |
|----------------------------|--------------------------|
| **Audience-first**         | Write for the reader     |
| **Progressive disclosure** | Overview → details       |
| **DRY**                    | Single source of truth   |
| **Up-to-date**             | Update with code changes |

### 1.1 信达雅 (Xin-Da-Ya) Priority

**信 → 达 → 雅** (Faithfulness → Clarity → Elegance)

- Never sacrifice correctness for beauty
- Never sacrifice clarity for brevity
- Elegance emerges from faithful, clear solutions

---

## 2. Document Types

| Type          | Purpose                | Update Frequency |
|---------------|------------------------|------------------|
| README        | Project entry point    | Per release      |
| API Reference | Function/class docs    | Per API change   |
| Guides        | How-to content         | As needed        |
| ADRs          | Architecture decisions | Per decision     |
| Changelog     | Release history        | Per release      |

---

## 3. Structure

### 3.1 Standard Template

```markdown
# Title

> Single-line purpose

---

## 1. Section

### 1.1 Subsection

---

## Related

- `path/FILE.md` — Description

---

*AI Collaboration Knowledge Base*
```text
### 3.2 Heading Rules

| Level | Use For             | Numbering  |
|-------|---------------------|------------|
| H1    | Document title      | None       |
| H2    | Main sections       | 1., 2., 3. |
| H3    | Subsections         | 1.1, 1.2   |
| H4    | Details (sparingly) | 1.1.1      |

### 3.3 TOC Rules

- Add TOC if >60 lines or >3 H2 sections
- Use vertical list format: `- [Section](#anchor)`
- Include H2 sections only

> **Full Standards**: See `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md`

---

## 4. Writing Style

| Rule          | ❌ Avoid            | ✅ Prefer            |
|---------------|--------------------|---------------------|
| Active voice  | "File is read"     | "Loader reads file" |
| Present tense | "This will create" | "This creates"      |
| Specific      | "Configure system" | "Set `MAX=100`"     |
| Concise       | "In order to"      | "To"                |

---

## 5. Elements

Documentation uses four primary elements. Each has dedicated standards.

| Element         | Purpose                           | Key Rule                |
|-----------------|-----------------------------------|-------------------------|
| **Diagrams**    | Visualize flows and relationships | Must use Mermaid        |
| **Tables**      | Present structured data           | 3-5 columns, 5-15 rows  |
| **Code Blocks** | Show code examples                | Always specify language |
| **Quotes**      | Highlight important info          | Use sparingly           |

### 5.1 Diagrams

| Rule       | Requirement                                             |
|------------|---------------------------------------------------------|
| **Tool**   | Must use Mermaid                                        |
| **Types**  | 21 types available (Flowchart and Sequence are primary) |
| **Limits** | Max 15 nodes, max 2 nesting levels                      |

**Selection Guide**:

| Scenario         | Type       |
|------------------|------------|
| Process/workflow | Flowchart  |
| API interactions | Sequence   |
| Data models      | Class / ER |
| State machines   | State      |

> **Full Standards**: See `.knowledge/practices/documentation/DIAGRAM_STANDARDS.md`

### 5.2 Tables

| Rule          | Requirement                            |
|---------------|----------------------------------------|
| **Purpose**   | Structured, comparable data            |
| **Columns**   | 3-5 recommended, 7 maximum             |
| **Rows**      | 5-15 recommended, 25 maximum           |
| **Alignment** | Text left, numbers right, icons center |

> **Full Standards**: See `.knowledge/practices/documentation/TABLE_STANDARDS.md`

### 5.3 Code Blocks

| Rule            | Requirement                               |
|-----------------|-------------------------------------------|
| **Language ID** | Always specify (`python`, `yaml`, etc.)   |
| **Size**        | 5-25 lines recommended                    |
| **Quality**     | Complete · Minimal · Commented · Runnable |

**Example**:

```python
# ✓ Good: focused, shows input/output
result = process("input")
print(result)  # Output: "processed"
```text
> **Full Standards**: See `.knowledge/practices/documentation/CODE_BLOCK_STANDARDS.md`

### 5.4 Quote Blocks

| Type    | Syntax              | Use Case               |
|---------|---------------------|------------------------|
| Note    | `> **Note**:`       | Additional information |
| Warning | `> **⚠️ Warning**:` | Caution required       |
| Tip     | `> **💡 Tip**:`     | Helpful suggestion     |

---

## 6. Maintenance

### 6.1 Update Triggers

| Event         | Action               |
|---------------|----------------------|
| Code change   | Update affected docs |
| API change    | Update reference     |
| User question | Improve clarity      |

### 6.2 Quality Checklist

- [ ] Links verified
- [ ] Examples tested
- [ ] Sections numbered
- [ ] Footer present

---

## Related

- `.knowledge/practices/documentation/INDEX.md` — Documentation practices index
- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Full documentation standards
- `.knowledge/practices/documentation/DIAGRAM_STANDARDS.md` — Diagram creation standards
- `.knowledge/practices/documentation/TABLE_STANDARDS.md` — Table creation standards
- `.knowledge/practices/documentation/CODE_BLOCK_STANDARDS.md` — Code block standards
- `.knowledge/core/PRINCIPLES.md` — Core principles (信达雅 · 术法道)

---

*AI Collaboration Knowledge Base*
