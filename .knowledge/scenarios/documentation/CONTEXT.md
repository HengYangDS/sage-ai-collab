# Documentation Scenario Context

> Pre-configured context for technical writing and documentation projects

---

## Table of Contents

- [1. Scenario Profile](#1-scenario-profile)
- [2. Relevant Knowledge](#2-relevant-knowledge)
- [3. Project Structure](#3-project-structure)
- [4. Document Types](#4-document-types)
- [5. Writing Patterns](#5-writing-patterns)
- [6. Quality Standards](#6-quality-standards)
- [7. Common Tasks](#7-common-tasks)
- [8. Autonomy Calibration](#8-autonomy-calibration)
- [9. Quick Commands](#9-quick-commands)

---

## 1. Scenario Profile

```yaml
scenario: documentation
languages: [ markdown, restructuredtext, asciidoc ]
tools: [ mkdocs, sphinx, docusaurus, vitepress ]
focus: [ technical_writing, api_docs, tutorials, reference ]
autonomy_default: L4
```
---

## 2. Relevant Knowledge

| Priority      | Files                                                                                                       |
|---------------|-------------------------------------------------------------------------------------------------------------|
| **Auto-Load** | `core/PRINCIPLES.md`<br/>`.knowledge/guidelines/DOCUMENTATION.md`<br/>`.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` |
| **On-Demand** | `.knowledge/practices/documentation/KNOWLEDGE_ORGANIZATION.md`<br/>`.knowledge/templates/INDEX.md`                                  |

---

## 3. Project Structure

| Directory      | Purpose                     |
|----------------|-----------------------------|
| `docs/`        | User-facing documentation   |
| `docs/guides/` | How-to guides and tutorials |
| `docs/api/`    | API reference documentation |
| `docs/design/` | Design documents and ADRs   |
| `docs/assets/` | Images, diagrams, media     |
| `.knowledge/`  | Knowledge base content      |
| `templates/`   | Document templates          |

---

## 4. Document Types

### 4.1 Documentation Quadrant (Diátaxis)

| Type             | Purpose                | User Need                |
|------------------|------------------------|--------------------------|
| **Tutorial**     | Learning-oriented      | "I want to learn"        |
| **How-to Guide** | Problem-oriented       | "I want to accomplish X" |
| **Reference**    | Information-oriented   | "I need to look up Y"    |
| **Explanation**  | Understanding-oriented | "I want to understand Z" |

### 4.2 Document Templates

| Document Type | Template                  | Use Case               |
|---------------|---------------------------|------------------------|
| API Reference | `.knowledge/templates/API_SPEC.md`   | Endpoint documentation |
| Architecture  | `.knowledge/templates/ADR.md`        | Design decisions       |
| Runbook       | `.knowledge/templates/RUNBOOK.md`    | Operational guides     |
| Postmortem    | `.knowledge/templates/POSTMORTEM.md` | Incident reports       |

---

## 5. Writing Patterns

### 5.1 Document Structure

```markdown
# [Title]
> [One-line description]
---
## Table of Contents
[Section links]
---
## 1. [First Section]
[Content]
---
## 2. [Second Section]
[Content]
---
## Related
- [Related doc 1]
- [Related doc 2]
---
*[Footer/attribution]*
```
### 5.2 Section Formatting

| Element        | Format          | Example                 |
|----------------|-----------------|-------------------------|
| **Title**      | `# Title`       | `# User Guide`          |
| **Section**    | `## N. Section` | `## 1. Getting Started` |
| **Subsection** | `### N.N Title` | `### 1.1 Prerequisites` |
| **Table**      | Markdown table  | `                       | Col | Col |` |
| **Code**       | Fenced blocks   | ` ```python `           |
| **Note**       | Blockquote      | `> **Note**: ...`       |

### 5.3 Writing Style

| Principle         | Description              | Example                                               |
|-------------------|--------------------------|-------------------------------------------------------|
| **Active voice**  | Subject performs action  | "Click the button" not "The button should be clicked" |
| **Present tense** | Current state            | "The function returns" not "The function will return" |
| **Second person** | Address reader directly  | "You can configure..."                                |
| **Concise**       | Remove unnecessary words | "To start" not "In order to start"                    |
| **Specific**      | Avoid vague terms        | "3 seconds" not "a short time"                        |

### 5.4 Code Documentation

```python
def process_data(
    input_path: str,
    output_path: str,
    *,
    chunk_size: int = 1000,
    validate: bool = True,
) -> ProcessResult:
    """Process data from input file and write to output.
    Reads data in chunks, applies transformations, and writes results.
    Supports validation and progress tracking.
    Args:
        input_path: Path to input file (CSV or JSON).
        output_path: Path for output file.
        chunk_size: Number of records per chunk. Defaults to 1000.
        validate: Whether to validate data. Defaults to True.
    Returns:
        ProcessResult containing success status and statistics.
    Raises:
        FileNotFoundError: If input_path doesn't exist.
        ValidationError: If validate=True and data is invalid.
    Example:
        >>> result = process_data("input.csv", "output.csv")
        >>> print(f"Processed {result.total_rows} rows")
        Processed 5000 rows
    """
```
---

## 6. Quality Standards

### 6.1 Documentation Checklist

| Category          | Check                                   |
|-------------------|-----------------------------------------|
| **Accuracy**      | Information is correct and up-to-date   |
| **Completeness**  | All necessary information included      |
| **Clarity**       | Easy to understand, no ambiguity        |
| **Consistency**   | Follows style guide, uniform formatting |
| **Accessibility** | Readable, proper headings, alt text     |

### 6.2 Review Criteria

| Level         | Focus                                      |
|---------------|--------------------------------------------|
| **Technical** | Accuracy, completeness, code examples work |
| **Editorial** | Grammar, style, clarity, consistency       |
| **User**      | Usability, findability, task completion    |

### 6.3 Information Density

| Content Type    | Target Density | Approach                  |
|-----------------|----------------|---------------------------|
| Quick reference | High           | Tables, bullet points     |
| Tutorial        | Medium         | Step-by-step with context |
| Explanation     | Low-Medium     | Narrative with examples   |
| Reference       | High           | Structured, searchable    |

---

## 7. Common Tasks

| Task                 | Steps                                                         |
|----------------------|---------------------------------------------------------------|
| **Create new doc**   | Choose type → Use template → Write content → Review → Publish |
| **Update existing**  | Identify changes → Update content → Update metadata → Review  |
| **Add code example** | Write code → Test code → Add to doc → Explain                 |
| **Add diagram**      | Create diagram → Export → Add to assets → Reference           |
| **Restructure docs** | Analyze current → Plan new structure → Migrate → Redirect     |

### 7.1 Documentation Workflow

```text
1. Plan
   └── Identify audience, purpose, scope
2. Draft
   └── Use template, write content, add examples
3. Review
   ├── Technical review (accuracy)
   ├── Editorial review (clarity)
   └── User review (usability)
4. Publish
   └── Build, deploy, announce
5. Maintain
   └── Monitor feedback, update regularly
```
---

## 8. Autonomy Calibration

| Task Type            | Level | Notes                     |
|----------------------|-------|---------------------------|
| Fix typo/grammar     | L5    | Trivial change            |
| Update example       | L4    | Test before committing    |
| Add new section      | L3-L4 | Follow existing structure |
| Restructure document | L3    | Plan and review           |
| Change navigation    | L2-L3 | User experience impact    |
| Delete content       | L2    | Information loss risk     |
| API doc changes      | L2-L3 | Must match code           |
| Create new guide     | L3    | Review outline first      |

---

## 9. Quick Commands

| Category       | Commands                                             |
|----------------|------------------------------------------------------|
| **MkDocs**     | `mkdocs serve`<br/>`mkdocs build`<br/>`mkdocs gh-deploy` |
| **Sphinx**     | `make html`<br/>`sphinx-autobuild docs docs/_build`    |
| **Docusaurus** | `npm start`<br/>`npm run build`                        |
| **VitePress**  | `npm run docs:dev`<br/>`npm run docs:build`            |
| **Lint**       | `markdownlint .`<br/>`vale docs/`                      |

---

## Style Quick Reference

### Headings

- Use sentence case: "Getting started" not "Getting Started"
- Be descriptive: "Configure authentication" not "Configuration"
- Limit depth to 3-4 levels

### Lists

- Use bullets for unordered items
- Use numbers for sequential steps
- Keep parallel structure

### Tables

- Use for structured data comparison
- Keep columns to 3-5 for readability
- Align numbers right, text left

### Code

- Always specify language for syntax highlighting
- Keep examples concise but complete
- Include expected output when helpful

### Links

- Use descriptive link text: "see the configuration guide" not "click here"
- Prefer relative links for internal docs
- Check links regularly

---

## Related

- `.knowledge/guidelines/DOCUMENTATION.md` — Documentation guidelines
- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Documentation standards
- `.knowledge/practices/documentation/KNOWLEDGE_ORGANIZATION.md` — Knowledge organization
- `.knowledge/frameworks/cognitive/INFORMATION_DENSITY.md` — Information density

---

*AI Collaboration Knowledge Base*

