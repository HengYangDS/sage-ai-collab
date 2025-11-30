# Contributing to SAGE Knowledge Base

> Guidelines and instructions for contributing to SAGE Knowledge Base

---

## Table of Contents

- [1. Code of Conduct](#1-code-of-conduct)
- [2. Getting Started](#2-getting-started)
- [3. Development Setup](#3-development-setup)
- [4. Making Contributions](#4-making-contributions)
- [5. Code Standards](#5-code-standards)
- [6. Testing](#6-testing)
- [7. Documentation](#7-documentation)
- [8. Submitting Changes](#8-submitting-changes)
- [9. Quick Reference](#9-quick-reference)
- [10. Recognition](#10-recognition)

---

## 1. Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- Be respectful and considerate
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Accept responsibility for mistakes

---

## 2. Getting Started

### 2.1 Types of Contributions

| Type             | Description             | Difficulty   |
|------------------|-------------------------|--------------|
| 🐛 Bug fixes     | Fix reported issues     | Beginner     |
| 📚 Documentation | Improve docs, fix typos | Beginner     |
| ✨ Features       | Add new functionality   | Intermediate |
| 🏗️ Architecture | Core system changes     | Advanced     |
| 🧪 Testing       | Add or improve tests    | Intermediate |

### 2.2 First Contribution

Look for issues labeled:

- `good first issue` - Simple, well-defined tasks
- `help wanted` - We'd love assistance
- `documentation` - Docs improvements

---

## 3. Development Setup

### 3.1 Prerequisites

- Python 3.12+
- Git
- Virtual environment tool (conda/miniconda recommended, or venv)

### 3.2 Setup Steps

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/sage-kb.git
cd sage-kb

# 3. Create virtual environment (conda recommended)
conda env create -f environment.yml
conda activate sage-kb

# Or use venv as alternative:
# python -m venv .venv
# source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -e ".[all]"

# 5. Install pre-commit hooks
pip install pre-commit
pre-commit install

# 6. Verify setup
pytest tests/
sage info
```

### 3.3 Project Structure

```
sage-kb/
├── src/sage/          # Source code
│   ├── core/          # Core functionality
│   ├── services/      # CLI, MCP, API services
│   └── capabilities/  # Analyzers, checkers
├── .knowledge/           # Knowledge content
├── docs/              # Documentation
├── tests/             # Test suite
└── config/            # Configuration files
```

---

## 4. Making Contributions

### 4.1 Workflow

```text
1. Create Issue (if not exists)
      ↓
2. Fork & Clone
      ↓
3. Create Branch
      ↓
4. Make Changes
      ↓
5. Test & Lint
      ↓
6. Commit
      ↓
7. Push & Create PR
      ↓
8. Review & Merge
```

### 4.2 Branch Naming

| Type    | Format                | Example                       |
|---------|-----------------------|-------------------------------|
| Feature | `feature/description` | `feature/add-mcp-streaming`   |
| Bug fix | `bugfix/description`  | `bugfix/fix-timeout-handling` |
| Docs    | `docs/description`    | `docs/update-api-guide`       |
| Hotfix  | `hotfix/description`  | `hotfix/security-patch`       |

### 4.3 Creating a Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

---

## 5. Code Standards

### 5.1 Python Style

We use **Ruff** for linting and formatting:

```bash
# Check code
ruff check src/

# Auto-fix issues
ruff check --fix src/

# Format code
ruff format src/
```

### 5.2 Key Standards

| Standard    | Requirement                   |
|-------------|-------------------------------|
| Line length | 88 characters                 |
| Type hints  | Required for public functions |
| Docstrings  | Google style                  |
| Imports     | Sorted by ruff                |

### 5.3 Example Code

```python
from typing import Optional


def process_content(
    content: str,
    max_length: Optional[int] = None,
) -> str:
    """Process content with optional length limit.
    
    Args:
        content: The content to process.
        max_length: Maximum length of output. If None, no limit.
    
    Returns:
        Processed content string.
    
    Raises:
        ValueError: If content is empty.
    """
    if not content:
        raise ValueError("Content cannot be empty")

    result = content.strip()
    if max_length is not None:
        result = result[:max_length]

    return result
```

### 5.4 Type Checking

```bash
# Run mypy
mypy src/
```

---

## 6. Testing

### 6.1 Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific tests
pytest tests/unit/
pytest tests/integration/
pytest -k "test_loader"

# Verbose output
pytest -v
```

### 6.2 Writing Tests

```python
import pytest
from sage.core.loader import Loader


class TestLoader:
    """Tests for the Loader class."""

    def test_load_file_success(self, tmp_path):
        """Test successful file loading."""
        # Arrange
        file = tmp_path / "TEST.md"
        file.write_text("# Test Content")
        loader = Loader()

        # Act
        result = loader.load(file)

        # Assert
        assert result.content == "# Test Content"

    def test_load_file_not_found(self):
        """Test loading non-existent file raises error."""
        loader = Loader()

        with pytest.raises(FileNotFoundError):
            loader.load("NONEXISTENT.md")
```

### 6.3 Test Requirements

- All new features need tests
- Bug fixes should include regression tests
- Maintain >80% coverage
- Tests must pass before merge

---

## 7. Documentation

### 7.1 Types of Documentation

| Type     | Location       | Purpose           |
|----------|----------------|-------------------|
| API docs | `docs/api/`    | API reference     |
| Guides   | `docs/guides/` | How-to guides     |
| Design   | `docs/design/` | Architecture docs |
| Content  | `.knowledge/`  | Knowledge content |

### 7.2 Documentation Style

- Use Markdown format
- Include code examples
- Keep language clear and concise
- Update when changing features

### 7.3 Adding Knowledge Content

```bash
# Add to appropriate layer
.knowledge/
├── core/          # Fundamental principles
├── guidelines/    # Standards and rules
├── practices/     # How-to guides
├── frameworks/    # Methodologies
└── scenarios/     # Context-specific
```

---

## 8. Submitting Changes

### 8.1 Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:

```
feat(cli): add export command for knowledge layers
fix(loader): handle empty files gracefully
docs(api): update MCP protocol documentation
```

### 8.2 Pull Request Process

1. **Create PR** with clear title and description
2. **Fill template** with all required information
3. **Pass CI checks** (tests, linting, type checks)
4. **Request review** from maintainers
5. **Address feedback** promptly
6. **Squash commits** if requested

### 8.3 PR Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing

- [ ] Tests added/updated
- [ ] All tests passing

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### 8.4 Review Process

- At least one approval required
- All CI checks must pass
- No unresolved comments
- Maintainers may request changes

---

## 9. Quick Reference

### 9.1 Common Commands

```bash
# Development
pip install -e ".[all]"    # Install with all extras
pytest                      # Run tests
ruff check --fix src/      # Fix lint issues
mypy src/                  # Type check

# Git workflow
git checkout -b feature/x  # Create branch
git commit -m "feat: ..."  # Commit
git push origin feature/x  # Push

# Pre-commit
pre-commit run --all-files # Run all hooks
```

### 9.2 Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Create an Issue with reproduction steps
- **Features**: Propose in Discussion first

---

## 10. Recognition

Contributors will be:

- Listed in CHANGELOG for their contributions
- Acknowledged in release notes
- Added to contributors list (for significant contributions)

Thank you for contributing to SAGE Knowledge Base!

---

## Related

- `README.md` — Project overview and quick start
- `CHANGELOG.md` — Version history and changes
- `.knowledge/guidelines/CODE_STYLE.md` — Code style guidelines
- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Documentation standards
- `.context/conventions/NAMING.md` — Naming conventions

---

*AI Collaboration Knowledge Base*
