# Release Notes Template

> **Purpose**: Template for documenting software releases
> **Use When**: Publishing a new version of software or documentation

---

## Overview

This template helps create consistent, informative release notes that communicate changes to users and stakeholders.

---

## Template

```markdown
# Release Notes: [Product Name] v[X.Y.Z]

> **Release Date**: [YYYY-MM-DD]
> **Release Type**: [Major | Minor | Patch | Hotfix]

---

## Highlights

[2-3 sentences summarizing the most important changes in this release]

---

## What's New

### ✨ New Features

- **[Feature Name]**: [Brief description of what it does and why it's useful]
    - [Additional detail if needed]
    - [Usage example or link to docs]

- **[Feature Name]**: [Brief description]

### 🚀 Improvements

- **[Area]**: [What was improved and the benefit]
- **[Area]**: [What was improved and the benefit]

### 🐛 Bug Fixes

- Fixed [brief description of bug] ([#issue-number])
- Fixed [brief description of bug] ([#issue-number])
- Fixed [brief description of bug]

### 📚 Documentation

- Added [new documentation]
- Updated [updated documentation]
- Improved [documentation improvements]

---

## Breaking Changes

⚠️ **Important**: This release contains breaking changes.

### [Breaking Change 1]

**What changed**: [Description of the change]

**Migration steps**:

1. [Step 1]
2. [Step 2]
3. [Step 3]

**Before**:

```[language]
[old code/config]
```

**After**:

```[language]
[new code/config]
```

---

## Deprecations

The following features are deprecated and will be removed in [version]:

| Feature       | Replacement   | Removal Version |
|---------------|---------------|-----------------|
| [Old feature] | [New feature] | [X.Y.Z]         |
| [Old API]     | [New API]     | [X.Y.Z]         |

---

## Known Issues

- [Issue description] — Workaround: [workaround if available]
- [Issue description] — Fix planned for [version]

---

## Upgrade Guide

### Prerequisites

- [Requirement 1]
- [Requirement 2]

### Upgrade Steps

1. **Backup**: [Backup instructions]
2. **Update**: [Update command/instructions]
3. **Migrate**: [Migration steps if needed]
4. **Verify**: [Verification steps]

```bash
# Example upgrade commands
[upgrade command 1]
[upgrade command 2]
```

---

## Compatibility

| Component    | Minimum Version | Recommended   |
|--------------|-----------------|---------------|
| Python       | 3.11            | 3.12          |
| [Dependency] | [Min]           | [Recommended] |

---

## Contributors

Thanks to everyone who contributed to this release:

- @[contributor1] — [contribution area]
- @[contributor2] — [contribution area]
- Community contributors

---

## Links

- **Full Changelog**: [link to detailed changelog]
- **Documentation**: [link to docs]
- **Issues**: [link to issue tracker]
- **Download**: [link to download/install]

---

*Released by [Team/Person] on [DATE]*

```

---

## Instructions

### 1. Header Information

- Use semantic versioning (MAJOR.MINOR.PATCH)
- Include release date in ISO format
- Classify release type

### 2. Highlights Section

- Write for non-technical readers
- Focus on user value, not technical details
- Keep to 2-3 sentences

### 3. Changes Sections

Organize changes by category:

| Category | Icon | Content |
|----------|------|---------|
| New Features | ✨ | New functionality |
| Improvements | 🚀 | Enhancements to existing |
| Bug Fixes | 🐛 | Fixed issues |
| Documentation | 📚 | Doc changes |
| Security | 🔒 | Security fixes |
| Performance | ⚡ | Performance improvements |

### 4. Breaking Changes

- Clearly mark breaking changes
- Provide migration steps
- Show before/after examples

### 5. Upgrade Guide

- List prerequisites
- Provide step-by-step instructions
- Include verification steps

---

## Example

```markdown
# Release Notes: SAGE Knowledge Base v0.2.0

> **Release Date**: 2025-11-29
> **Release Type**: Minor

---

## Highlights

This release introduces MCP streaming support for real-time knowledge delivery and significantly improves search performance. We've also added new DevOps scenario templates to help teams get started quickly.

---

## What's New

### ✨ New Features

- **MCP Streaming**: Real-time streaming responses for large knowledge bases
  - Reduces time-to-first-byte by 80%
  - See `docs/api/mcp.md` for usage

- **DevOps Scenarios**: Pre-configured contexts for CI/CD workflows
  - GitHub Actions templates
  - Kubernetes deployment examples

### 🚀 Improvements

- **Search Performance**: 3x faster full-text search with new indexing
- **CLI Output**: Improved formatting with syntax highlighting
- **Memory Usage**: Reduced baseline memory by 40%

### 🐛 Bug Fixes

- Fixed timeout handling in nested layer loading (#123)
- Fixed cache invalidation on config change (#125)
- Fixed Unicode handling in search results (#127)

---

## Breaking Changes

⚠️ **Important**: Configuration format has changed.

### Configuration Schema Update

**What changed**: Timeout configuration moved under `performance` section.

**Migration steps**:
1. Update your `config/sage.yaml`
2. Move timeout settings to new location
3. Restart services

**Before**:
```yaml
timeouts:
  t1_cache: 100
```

**After**:

```yaml
performance:
  timeouts:
    t1_cache: 100
```

---

## Upgrade Guide

### Prerequisites

- Python 3.12+
- Backup your configuration

### Upgrade Steps

1. **Backup**: `cp config/sage.yaml config/sage.yaml.bak`
2. **Update**: `pip install --upgrade sage-kb`
3. **Migrate config**: Update configuration as shown above
4. **Verify**: `sage info`

---

*Released by SAGE Team on 2025-11-29*

```

---

## Best Practices

1. **User-focused**: Write for your audience
2. **Complete**: Include all changes, even small ones
3. **Actionable**: Provide clear upgrade instructions
4. **Linked**: Reference issues, PRs, and docs
5. **Consistent**: Use same format for all releases

---

## Related

- `templates/adr.md` — Architecture Decision Record
- `practices/engineering/git_workflow.md` — Release process
- `CHANGELOG.md` — Project changelog

---

*Template from SAGE Knowledge Base*
