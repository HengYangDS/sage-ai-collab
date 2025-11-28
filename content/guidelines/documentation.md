# Documentation Guidelines

> **Load Time**: On-demand (~150 tokens)  
> **Purpose**: Clear, maintainable, useful documentation

---

## 4.1 Documentation Philosophy

### Core Principles

- **Accuracy**: Always up-to-date with code
- **Clarity**: Understandable by target audience
- **Completeness**: Covers all necessary information
- **Accessibility**: Easy to find and navigate

### Xin-Da-Ya Applied to Docs

| Principle   | Application                               |
|-------------|-------------------------------------------|
| **信 (Xin)** | Technically accurate, no misleading info  |
| **达 (Da)**  | Clear structure, appropriate detail level |
| **雅 (Ya)**  | Well-formatted, consistent style          |

---

## 4.2 Documentation Types

### README.md Structure

```markdown
# Project Name

Brief description (1-2 sentences)

## Features
- Key feature 1
- Key feature 2

## Quick Start
\`\`\`bash
pip install project-name
project-name --help
\`\`\`

## Installation
Detailed installation instructions

## Usage
Common usage patterns with examples

## Configuration
Configuration options and environment variables

## Contributing
How to contribute to the project

## License
License information
```

### API Documentation

```python
def fetch_user(
    user_id: str,
    include_profile: bool = False,
    timeout: float = 30.0
) -> User:
    """Fetch a user by their unique identifier.
    
    Retrieves user data from the database, optionally including
    the full profile information.
    
    Args:
        user_id: Unique identifier (UUID format).
        include_profile: If True, includes profile data.
        timeout: Maximum wait time in seconds.
        
    Returns:
        User object with requested data.
        
    Raises:
        UserNotFoundError: If no user matches the ID.
        TimeoutError: If request exceeds timeout.
        
    Example:
        >>> user = fetch_user("abc-123", include_profile=True)
        >>> print(user.name)
        "Alice"
    """
```

---

## 4.3 Code Comments

### When to Comment

| Scenario             | Comment Type    | Example                                        |
|----------------------|-----------------|------------------------------------------------|
| Complex algorithm    | Explain logic   | `# Using Dijkstra's for shortest path`         |
| Non-obvious decision | Explain why     | `# JSON preferred over XML for browser compat` |
| Workaround           | Document reason | `# HACK: API bug requires retry`               |
| Public API           | Full docstring  | Args, Returns, Raises, Example                 |

### When NOT to Comment

```python
# BAD: Obvious comments
counter = 0  # Initialize counter to zero
counter += 1  # Increment counter

# GOOD: Self-documenting code
user_count = 0
user_count += 1
```

---

## 4.4 Changelog Format

### Keep a Changelog Style

```markdown
# Changelog

## [Unreleased]
### Added
- New feature description

## [2.0.0] - 2024-01-15
### Added
- Major new feature

### Changed
- Breaking change description

### Deprecated
- Feature to be removed

### Removed
- Removed feature

### Fixed
- Bug fix description

### Security
- Security fix description
```

---

## 4.5 Architecture Documentation

### ADR (Architecture Decision Record)

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need a reliable, scalable database for user data.

## Decision
We will use PostgreSQL 15+.

## Consequences
### Positive
- ACID compliance
- JSON support
- Strong ecosystem

### Negative
- Requires more ops expertise than SQLite
- Higher infrastructure cost
```

---

## 4.6 Documentation Maintenance

### Keep Docs Current

- [ ] Update docs with every code change
- [ ] Review docs during code review
- [ ] Test code examples regularly
- [ ] Remove outdated information

### Documentation Debt Signs

- Outdated examples that don't work
- Missing documentation for new features
- Inconsistent terminology
- Broken links or references

---

## 4.7 Quick Reference

### Markdown Best Practices

| Element      | Usage                   |
|--------------|-------------------------|
| `# H1`       | Document title only     |
| `## H2`      | Major sections          |
| `### H3`     | Subsections             |
| `` `code` `` | Inline code, file names |
| `**bold**`   | Important terms         |
| `> quote`    | Notes, warnings         |

### Documentation Checklist

- [ ] README is complete and current
- [ ] API has full docstrings
- [ ] Complex code is commented
- [ ] Changelog is maintained
- [ ] Examples are tested and work

---

*Part of AI Collaboration Knowledge Base v2.0.0*
