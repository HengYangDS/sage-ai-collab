# Documentation Guidelines

> Clear, maintainable, useful documentation

---

## Table of Contents

[1. Documentation Philosophy](#1-documentation-philosophy) · [2. Document Types](#2-document-types) · [3. Structure Standards](#3-structure-standards) · [4. Writing Style](#4-writing-style) · [5. Code Examples](#5-code-examples) · [6. Maintenance](#6-maintenance)

---

## 1. Documentation Philosophy

| Principle              | Application              |
|------------------------|--------------------------|
| Audience-first         | Write for the reader     |
| Progressive disclosure | Overview → details       |
| DRY                    | Single source of truth   |
| Up-to-date             | Update with code changes |

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

## 3. Structure Standards

### 3.1 File Format

```markdown
# Title

> Single-line purpose

---

## 1. Section

### 1.1 Subsection

---

## Related

- `path/file.md` — Description

---

*Part of SAGE Knowledge Base*
```

### 3.2 Heading Rules

| Level | Use For             | Numbering  |
|-------|---------------------|------------|
| H1    | Document title      | None       |
| H2    | Main sections       | 1., 2., 3. |
| H3    | Subsections         | 1.1, 1.2   |
| H4    | Details (sparingly) | 1.1.1      |

---

## 4. Writing Style

| Rule          | ❌ Avoid            | ✓ Prefer            |
|---------------|--------------------|---------------------|
| Active voice  | "File is read"     | "Loader reads file" |
| Present tense | "This will create" | "This creates"      |
| Specific      | "Configure system" | "Set `MAX=100`"     |
| Concise       | "In order to"      | "To"                |

---

## 5. Code Examples

**Good examples are**: Complete · Minimal · Commented · Runnable

```python
# ✓ Shows input and output
result = process("input")
print(result)  # Output: "processed"
```

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

- `practices/documentation/standards.md` — Full standards
- `config/capabilities/documentation.yaml` — TOC configuration

---

*Part of SAGE Knowledge Base*
