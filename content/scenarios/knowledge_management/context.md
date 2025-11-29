# Knowledge Management Scenario

> Context and guidelines for knowledge management tasks using SAGE

---

## Scenario Overview

| Aspect | Description |
|--------|-------------|
| **Domain** | Knowledge base organization and maintenance |
| **Task Types** | Content creation, structuring, updating, search optimization |
| **Autonomy Level** | L4 (Medium-High) for routine updates, L3 for structural changes |
| **Key Concerns** | Consistency, discoverability, maintainability |

---

## Common Tasks

### Content Organization

- Creating new knowledge documents
- Organizing content into appropriate layers
- Maintaining index files and navigation
- Cross-referencing related content

### Knowledge Capture

- Documenting decisions (ADRs)
- Recording conventions and patterns
- Capturing session learnings
- Creating templates for reuse

### Maintenance

- Updating outdated content
- Fixing broken references
- Improving search keywords
- Archiving deprecated content

---

## Best Practices

### Document Structure

Follow the standard SAGE document format:

```markdown
# Title

> Brief description

---

## Table of Contents

[1. Section](#1-section) · [2. Another](#2-another)

---

## 1. Section

Content...

---

## Related

- Links to related content

---

*Footer*
```

### Layer Assignment

| Layer | Content Type | Examples |
|-------|--------------|----------|
| `core` | Fundamental principles | Philosophy, defaults |
| `guidelines` | How-to guidance | Code style, collaboration rules |
| `frameworks` | Conceptual models | Autonomy levels, timeout patterns |
| `practices` | Actionable patterns | Engineering practices, documentation |

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Files | `snake_case.md` | `timeout_patterns.md` |
| Directories | `snake_case` | `ai_collaboration` |
| ADRs | `ADR-NNNN-title.md` | `ADR-0001-architecture.md` |

### Cross-References

Use relative paths for internal references:

```markdown
- See `content/core/principles.md` for core philosophy
- Related: `../frameworks/autonomy/levels.md`
```

---

## Workflow Guidelines

### Creating New Content

1. **Identify the layer**: Where does this content belong?
2. **Check existing content**: Avoid duplication
3. **Follow the template**: Use standard format
4. **Add to index**: Update relevant index.md files
5. **Cross-reference**: Link related content

### Updating Content

1. **Preserve history**: Document significant changes
2. **Update references**: Check for broken links
3. **Maintain consistency**: Follow existing patterns
4. **Test navigation**: Verify discoverability

### Archiving Content

1. **Move to `.archive/`**: Preserve but hide
2. **Update references**: Remove or redirect links
3. **Document reason**: Note why archived
4. **Keep metadata**: Preserve creation date, author

---

## Token Budget

For knowledge management tasks:

| Task | Budget | Layers |
|------|--------|--------|
| Content review | 3000 | core, practices/documentation |
| New document | 4000 | core, guidelines, templates |
| Restructuring | 5000 | all relevant layers |
| Search optimization | 2000 | core, practices |

---

## Common Patterns

### Knowledge Capture Pattern

```
1. Identify knowledge worth capturing
2. Determine appropriate format (ADR, convention, guide)
3. Choose correct location (.context/ vs content/)
4. Create document using template
5. Update navigation/index
6. Commit with descriptive message
```

### Content Discovery Pattern

```
1. Use sage search for keyword discovery
2. Check index files for navigation
3. Review related content links
4. Identify gaps in coverage
5. Plan additions/updates
```

---

## Related Scenarios

- `python_backend/` — Python development context
- `data_pipeline/` — Data processing context
- `typescript_frontend/` — Frontend development context

---

## Related Content

- `content/practices/documentation/` — Documentation practices
- `content/templates/` — Document templates
- `.context/conventions/file_structure.md` — File organization rules
- `docs/guides/advanced.md#custom-knowledge` — Adding custom knowledge

---

*SAGE Knowledge Base - Knowledge Management Scenario*
