# Documentation Standards Practice Guide

> **Load Time**: On-demand (~200 tokens)  
> **Purpose**: Practical standards for effective documentation  
> **Version**: 0.1.0

---

## Overview

This guide provides practical standards for creating and maintaining documentation that serves both human readers and AI
collaborators effectively.

---

## 1. Document Structure Standards

### 1.1 File Naming Convention

```
[category]_[topic]_[qualifier].md

Examples:
- api_authentication_guide.md
- setup_development_quickstart.md
- architecture_decision_001.md
```

### 1.2 Standard Document Header

```markdown
# Document Title

> **Load Time**: [timing] (~[tokens] tokens)  
> **Purpose**: [brief purpose statement]  
> **Version**: [semver]  
> **Last Updated**: [date]

---
```

### 1.3 Section Organization

```markdown
# Title (H1) - One per document

## Major Section (H2)

### Subsection (H3)

#### Detail (H4) - Use sparingly
```

---

## 2. Content Types

### 2.1 Reference Documentation

```markdown
## API Reference: [Function/Class]

### Signature

\`\`\`python
def function_name(param1: Type, param2: Type = default) -> ReturnType:
\`\`\`

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| param1 | Type | Yes | Description |
| param2 | Type | No | Description (default: X) |

### Returns

Description of return value.

### Raises

- `ExceptionType`: When condition occurs

### Example

\`\`\`python
result = function_name("value", param2=True)
\`\`\`
```

### 2.2 Tutorial/Guide Documentation

```markdown
## Guide: [Topic]

### Prerequisites

- Prerequisite 1
- Prerequisite 2

### Steps

#### Step 1: [Action]

Description of what to do.

\`\`\`bash
command to run
\`\`\`

Expected result: [what should happen]

#### Step 2: [Action]

...

### Verification

How to verify success.

### Troubleshooting

Common issues and solutions.
```

### 2.3 Decision Records (ADR)

```markdown
# ADR-[NNN]: [Title]

## Status

[Proposed | Accepted | Deprecated | Superseded]

## Context

What is the issue that we're seeing that is motivating this decision?

## Decision

What is the change that we're proposing and/or doing?

## Consequences

### Positive

- Benefit 1
- Benefit 2

### Negative

- Tradeoff 1
- Tradeoff 2

### Neutral

- Observation 1
```

---

## 3. Writing Standards

### 3.1 Clarity Guidelines

| Guideline     | Bad Example                      | Good Example                               |
|---------------|----------------------------------|--------------------------------------------|
| Be specific   | "Configure the system"           | "Set `MAX_CONNECTIONS=100` in config.yaml" |
| Active voice  | "The file is read by the loader" | "The loader reads the file"                |
| Present tense | "This will create a user"        | "This creates a user"                      |
| Avoid jargon  | "Utilize the endpoint"           | "Use the endpoint"                         |

### 3.2 Code Examples

```markdown
Good code example characteristics:

- Complete and runnable
- Minimal but sufficient
- Well-commented for non-obvious parts
- Shows expected output
- Handles errors appropriately
```

### 3.3 Tables vs Lists

**Use Tables When:**

- Comparing multiple items
- Showing structured data
- Reference information

**Use Lists When:**

- Sequential steps
- Simple enumerations
- Hierarchical information

---

## 4. AI-Friendly Documentation

### 4.1 Token Efficiency

```markdown
# High Token Efficiency

- Use tables for structured data
- Concise headers
- Code blocks for examples
- Bullet points for lists

# Low Token Efficiency (Avoid)

- Long paragraphs
- Repeated information
- Excessive formatting
- Embedded images (describe instead)
```

### 4.2 Scannable Structure

```markdown
## Section Name

**Key Point**: Brief summary of this section.

### Details

- Detail 1
- Detail 2

### Example

\`\`\`
code
\`\`\`
```

### 4.3 Cross-References

```markdown
# Good Cross-References

See [Autonomy Levels](../03_frameworks/autonomy/levels.md) for details.

# For AI Context

Related: `03_frameworks/autonomy/levels.md` (autonomy definitions)
```

---

## 5. Maintenance Standards

### 5.1 Review Checklist

- [ ] All code examples tested and working
- [ ] Links verified
- [ ] Version numbers current
- [ ] No outdated information
- [ ] Consistent terminology
- [ ] Proper formatting

### 5.2 Update Triggers

| Trigger       | Action                       |
|---------------|------------------------------|
| Code change   | Update affected docs         |
| API change    | Update reference + changelog |
| New feature   | Add guide + reference        |
| Bug found     | Add troubleshooting          |
| User question | Improve clarity              |

### 5.3 Deprecation Process

```markdown
> ⚠️ **Deprecated**: This feature is deprecated as of v2.0.0.
> Use [new_feature](link) instead.
> Will be removed in v3.0.0.
```

---

## 6. Documentation Types Matrix

| Type          | Audience   | Update Frequency | Token Priority |
|---------------|------------|------------------|----------------|
| README        | All        | Per release      | High           |
| API Reference | Developers | Per API change   | Medium         |
| Tutorials     | New users  | Quarterly        | Low            |
| ADRs          | Team       | Per decision     | Low            |
| Changelog     | All        | Per release      | High           |
| Comments      | Developers | With code        | N/A            |

---

## 7. Templates

### 7.1 README Template

```markdown
# Project Name

Brief description (1-2 sentences).

## Features

- Feature 1
- Feature 2

## Quick Start

\`\`\`bash
installation command
usage command
\`\`\`

## Documentation

- [Guide](link)
- [API Reference](link)

## Contributing

See [CONTRIBUTING.md](link).

## License

[License type]
```

### 7.2 Changelog Entry

```markdown
## [Version] - YYYY-MM-DD

### Added

- New feature description

### Changed

- Change description

### Fixed

- Bug fix description

### Removed

- Removed feature description
```

---

## 8. Quality Metrics

| Metric           | Target                      | Measurement        |
|------------------|-----------------------------|--------------------|
| Completeness     | 100% public API             | API coverage check |
| Accuracy         | 100% examples work          | Automated testing  |
| Freshness        | < 1 month since code change | Git diff analysis  |
| Readability      | Grade 8 reading level       | Readability score  |
| Token Efficiency | < 500 tokens/section        | Token counter      |

---

## Quick Reference

### Do

- ✅ Keep documents focused and single-purpose
- ✅ Use consistent formatting
- ✅ Include working examples
- ✅ Update with code changes
- ✅ Link to related documents

### Don't

- ❌ Duplicate information
- ❌ Use screenshots for code
- ❌ Leave TODOs in published docs
- ❌ Assume reader knowledge
- ❌ Use inconsistent terminology

---

*Version 0.1.0 | Part of AI Collaboration Knowledge Base*
