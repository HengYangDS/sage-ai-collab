# Git Workflow

> Git branching strategy, commit conventions, and collaboration practices

---

## Table of Contents

- [1. Branching Strategy](#1-branching-strategy)

- [2. Commit Conventions](#2-commit-conventions)

- [3. Pull Request Process](#3-pull-request-process)

- [4. Release Management](#4-release-management)

- [5. Best Practices](#5-best-practices)

---

## 1. Branching Strategy

### 1.1 Branch Types

| Branch      | Purpose                 | Naming                  | Lifetime  |

|-------------|-------------------------|-------------------------|-----------|

| `main`      | Production-ready code   | -                       | Permanent |

| `develop`   | Integration branch      | -                       | Permanent |

| `feature/*` | New features            | `feature/add-search`    | Temporary |

| `bugfix/*`  | Bug fixes               | `bugfix/fix-timeout`    | Temporary |

| `hotfix/*`  | Urgent production fixes | `hotfix/critical-error` | Temporary |

| `release/*` | Release preparation     | `release/v1.0.0`        | Temporary |

### 1.2 Branch Flow

```
main ─────●─────────────────●─────────────────●──── (releases)

          │                 ↑                 ↑

          │                 │                 │

develop ──●──●──●──●──●──●──●──●──●──●──●──●──●──── (integration)

             │     ↑     │     ↑

             │     │     │     │

feature/a ───●─────┘     │     │

                         │     │

feature/b ───────────────●─────┘

```
### 1.3 Branch Rules

| Rule                   | Description                             |

|------------------------|-----------------------------------------|

| **Protected branches** | `main` and `develop` require PR reviews |

| **No direct commits**  | Always use feature branches             |

| **Up-to-date**         | Rebase/merge from develop before PR     |

| **Clean history**      | Squash commits when merging             |

---

## 2. Commit Conventions

### 2.1 Commit Message Format

```text
<type>(<scope>): <subject>

<body>

<footer>

```
### 2.2 Commit Types

| Type       | Description      | Example                                  |

|------------|------------------|------------------------------------------|

| `feat`     | New feature      | `feat(cli): add search command`          |

| `fix`      | Bug fix          | `fix(loader): handle empty files`        |

| `docs`     | Documentation    | `docs: update API reference`             |

| `style`    | Formatting       | `style: fix indentation`                 |

| `refactor` | Code refactoring | `refactor(core): simplify timeout logic` |

| `perf`     | Performance      | `perf: optimize search algorithm`        |

| `test`     | Tests            | `test: add loader unit tests`            |

| `chore`    | Maintenance      | `chore: update dependencies`             |

| `ci`       | CI/CD changes    | `ci: add coverage report`                |

### 2.3 Scope Examples

| Scope    | Area          |

|----------|---------------|

| `core`   | Core layer    |

| `cli`    | CLI service   |

| `mcp`    | MCP service   |

| `api`    | API service   |

| `config` | Configuration |

| `docs`   | Documentation |

| `tests`  | Test suite    |

### 2.4 Good Commit Examples

```bash
# Feature commit

feat(mcp): add sage_search tool with pagination

Add new MCP tool for searching knowledge base with:

- Query parameter for search terms

- Limit parameter for max results

- Pagination support via offset

Closes #123

# Bug fix commit

fix(loader): handle timeout gracefully

Return partial content instead of raising exception

when T3 timeout occurs during layer loading.

Fixes #456

# Documentation commit

docs(api): add Python API reference

Add comprehensive documentation for:

- get_knowledge() function

- search_knowledge() function

- Configuration options

```
### 2.5 Commit Best Practices

| Practice             | Description                          |

|----------------------|--------------------------------------|

| **Atomic commits**   | One logical change per commit        |

| **Present tense**    | "add feature" not "added feature"    |

| **Imperative mood**  | "fix bug" not "fixes bug"            |

| **No period**        | Subject line without trailing period |

| **72 char limit**    | Wrap body at 72 characters           |

| **Reference issues** | Include issue numbers in footer      |

---

## 3. Pull Request Process

### 3.1 PR Checklist

```markdown
## Description

[Describe what this PR does]

## Type of Change

- [ ] Bug fix (non-breaking change fixing an issue)

- [ ] New feature (non-breaking change adding functionality)

- [ ] Breaking change (fix or feature causing existing functionality to change)

- [ ] Documentation update

## Checklist

- [ ] Code follows project style guidelines

- [ ] Self-reviewed the code

- [ ] Added/updated tests

- [ ] Tests pass locally

- [ ] Updated documentation

- [ ] No new warnings

## Related Issues

Closes #[issue number]

```
### 3.2 PR Workflow

```text
1. Create Branch

   └── git checkout -b feature/my-feature develop

2. Make Changes

   └── Implement feature with atomic commits

3. Push Branch

   └── git push origin feature/my-feature

4. Open PR

   └── Create PR against develop branch

5. Review Process

   ├── Automated checks (CI)

   ├── Code review by maintainer

   └── Address feedback

6. Merge

   └── Squash and merge after approval

```
### 3.3 Review Guidelines

| Aspect            | Check                       |

|-------------------|-----------------------------|

| **Correctness**   | Does it solve the problem?  |

| **Tests**         | Are there adequate tests?   |

| **Style**         | Does it follow conventions? |

| **Performance**   | Any performance concerns?   |

| **Security**      | Any security implications?  |

| **Documentation** | Is it properly documented?  |

---

## 4. Release Management

### 4.1 Version Numbering

Follow [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH

Example: 1.2.3

```
| Component | Increment When                     |

|-----------|------------------------------------|

| **MAJOR** | Breaking changes                   |

| **MINOR** | New features (backward compatible) |

| **PATCH** | Bug fixes (backward compatible)    |

### 4.2 Release Process

```bash
# 1. Create release branch

git checkout -b release/v1.2.0 develop

# 2. Update version

# Edit pyproject.toml, CHANGELOG.md

# 3. Final testing

pytest tests/ -v

# 4. Merge to main

git checkout main

git merge release/v1.2.0

# 5. Tag release

git tag -a v1.2.0 -m "Release v1.2.0"

git push origin v1.2.0

# 6. Merge back to develop

git checkout develop

git merge release/v1.2.0

# 7. Delete release branch

git branch -d release/v1.2.0

```
### 4.3 Changelog Format

```markdown
## [1.2.0] - 2025-11-29

### Added

- New feature X

- New feature Y

### Changed

- Updated behavior of Z

### Fixed

- Bug in component A

- Issue with feature B

### Deprecated

- Old API method (use new method instead)

### Removed

- Legacy feature C

### Security

- Fixed vulnerability in D

```
---

## 5. Best Practices

### 5.1 Daily Workflow

```bash
# Start of day: Update local branches

git checkout develop

git pull origin develop

# Create feature branch

git checkout -b feature/my-feature

# Work on feature (commit frequently)

git add .

git commit -m "feat(scope): description"

# Keep branch updated

git fetch origin

git rebase origin/develop

# Push changes

git push origin feature/my-feature

```
### 5.2 Handling Conflicts

```bash
# During rebase

git rebase origin/develop

# If conflicts occur

# 1. Resolve conflicts in affected files

# 2. Stage resolved files

git add <resolved-files>

# 3. Continue rebase

git rebase --continue

# Or abort if needed

git rebase --abort

```
### 5.3 Useful Aliases

```bash
# Add to ~/.gitconfig

[alias]

    co = checkout

    br = branch

    ci = commit

    st = status

    lg = log --oneline --graph --decorate

    unstage = reset HEAD --

    last = log -1 HEAD

    amend = commit --amend --no-edit

```
### 5.4 Common Commands

| Task               | Command                            |

|--------------------|------------------------------------|

| Create branch      | `git checkout -b feature/name`     |

| Switch branch      | `git checkout branch-name`         |

| Update from remote | `git pull --rebase origin develop` |

| View history       | `git log --oneline -20`            |

| Undo last commit   | `git reset --soft HEAD~1`          |

| Stash changes      | `git stash push -m "message"`      |

| Apply stash        | `git stash pop`                    |

| Cherry-pick        | `git cherry-pick <commit-hash>`    |

---

## Git Hooks

### 5.5 Pre-commit Hook

```bash
#!/bin/sh

# .git/hooks/pre-commit

# Run linting

ruff check src/

# Run type checking

mypy src/sage/

# Run tests

pytest tests/unit/ -q

```
### 5.6 Commit-msg Hook

```bash
#!/bin/sh

# .git/hooks/commit-msg

# Validate commit message format

commit_regex='^(feat|fix|docs|style|refactor|perf|test|chore|ci)(\(.+\))?: .{1,50}'

if ! grep -qE "$commit_regex" "$1"; then

    echo "Invalid commit message format"

    echo "Expected: type(scope): subject"

    exit 1

fi

```
---

## Related

- `.knowledge/practices/engineering/CI_CD.md` — CI/CD configuration

- `.knowledge/practices/engineering/CODE_REVIEW.md` — Code review guidelines

- `.context/conventions/` — Coding conventions

---

*AI Collaboration Knowledge Base*

