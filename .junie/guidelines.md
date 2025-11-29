# Project Guidelines

> **Purpose**: Primary entry point for JetBrains Junie AI collaboration.
> **Compatibility**: Junie v2024.3+, MCP v1.0+
> **Schema Version**: 1.0

---

## 🔄 About This File

This file contains **generic AI collaboration rules** that apply to any project.
Project-specific information is defined in separate files:

- **Project Variables**: `project.yaml` — Project identity, tech stack, commands
- **Project Guidelines**: `project-guidelines.md` — Project-specific documentation

---

## 🤖 AI Collaboration Rules

### Autonomy Levels

| Level | Name                        | Description           | Example Tasks                                        |
|-------|-----------------------------|-----------------------|------------------------------------------------------|
| L1-L2 | Minimal/Low (0-40%)         | Ask before changes    | Breaking changes, new dependencies, critical systems |
| L3-L4 | Medium/Medium-High (40-80%) | Proceed, report after | Bug fixes, refactoring, routine development ⭐        |
| L5-L6 | High/Full (80-100%)         | High autonomy         | Formatting, comments, docs, trusted patterns         |

**Default**: L4 (Medium-High) for mature collaboration.

### Key Behaviors

1. **Follow existing patterns** in the codebase
2. **Run tests** before committing changes
3. **Update relevant documentation** when modifying features
4. **Output files to designated temp directory** — All temporary/intermediate files must go to the configured output directory (typically `.outputs/`), never project root
5. **Create session records** for significant work sessions (see Session History below)
6. **Use English** for code and documentation (unless project specifies otherwise)
7. **Respect timeout limits** when applicable

### Session History Management

At session end, create records in the designated history directory (typically `.history/`):

| Directory | Purpose |
|-----------|---------|
| `conversations/` | Key decisions and outcomes |
| `handoffs/` | Task continuation context |
| `current/` | Active work state |

**Naming Conventions**:
- Conversations: `YYYY-MM-DD-topic.md`
- Handoffs: `YYYY-MM-DD-task-handoff.md`
- Sessions: `session-YYYYMMDD-HHMM.md`

### Session Automation (MCP Tools)

Use these MCP tools to automate session tracking:

| Tool | When to Call | Purpose |
|------|--------------|---------|
| `session_start` | Beginning of significant work (>30 min expected) | Creates session state file |
| `session_end` | Work completed or session ending | Creates conversation/handoff record |
| `session_status` | Start of new session, or to check state | Shows active sessions and recent records |

**Automatic Trigger Rules**:

| Trigger Condition | Action |
|-------------------|--------|
| Session begins with complex task | Call `session_status()` then `session_start(task, description)` |
| Important decision made | Document in current session file |
| Session duration > 30 minutes | Ensure session tracking is active |
| Work completed successfully | Call `session_end(summary)` |
| Work incomplete/interrupted | Call `session_end(summary, next_steps="...")` for handoff |
| Resuming after break | Call `session_status()` to check for active sessions |

**Usage Examples**:
```
# Start tracking a session
session_start(task="Implement authentication", description="Add JWT-based auth to API")

# Check current status
session_status()

# End with completed work
session_end(summary="Implemented JWT authentication with refresh tokens")

# End with incomplete work (creates handoff)
session_end(summary="Partial auth implementation", next_steps="Add refresh token logic, write tests")
```

### Expert Committee Pattern

For complex decisions, simulate a **Level 5 Expert Committee** review with multiple expert groups:

- **Architecture** — System design, scalability, maintainability
- **Engineering Practice** — Code quality, testing, CI/CD
- **Domain Knowledge** — Business logic, requirements alignment
- **AI Collaboration** — Human-AI interaction patterns

---

## ⏱️ Timeout Hierarchy

When implementing time-sensitive operations, consider a tiered timeout approach:

| Tier | Duration | Use Case |
|------|----------|----------|
| T1 | ~100ms | Cache lookup, in-memory operations |
| T2 | ~500ms | Single file read, simple queries |
| T3 | ~2s | Layer/module loading |
| T4 | ~5s | Full system initialization |
| T5 | ~10s | Complex analysis, external calls |

**Principle**: Always have fallback strategies for timeout scenarios.

---

## 📐 Coding Standards

### General Principles

- **Formatter**: Use project's configured formatter
- **Type Hints**: Required for statically-typed languages
- **Docstrings**: Follow project's documentation style
- **Naming**: Follow project's naming conventions

### Architecture Patterns

- Follow the project's established architecture patterns
- Maintain layer separation (e.g., Core → Services → Capabilities)
- Use dependency injection where applicable
- Implement proper error handling and logging

---

## 📝 Documentation Standards

### Key Principles

1. **Single Source of Truth (SSOT)** — One authoritative location per topic
2. **Index Maintenance** — Keep navigation indexes up to date
3. **Cross-References** — Link related documents appropriately
4. **Version Tracking** — Note significant changes

### Documentation Locations

| Type | Typical Location |
|------|------------------|
| User-facing docs | `docs/` |
| API documentation | `docs/api/` |
| Design documents | `docs/design/` |
| Project context | `.context/` |
| Generic knowledge | `content/` |

---

## 📁 Standard Directory Structure

A well-organized project typically includes:

```
project-root/
├── .junie/          # AI collaboration configuration
├── .context/        # Project-specific knowledge (optional)
├── .history/        # AI session history (optional)
├── .outputs/        # Temporary files (git-ignored)
├── config/          # Runtime configuration
├── docs/            # User-facing documentation
├── src/             # Source code
├── tests/           # Test suite
└── tools/           # Development tools
```

### Hidden Directories

| Directory | Purpose |
|-----------|---------|
| `.junie/` | Junie AI configuration |
| `.context/` | Project-specific knowledge base |
| `.history/` | AI session records |
| `.outputs/` | Temporary/intermediate files |

---

## 🔗 References

For project-specific information, see:

- **Project Variables**: `project.yaml`
- **Project Guidelines**: `project-guidelines.md`
- **Quick Reference**: `quickref.md`
- **Configuration**: `config.yaml`
- **MCP Settings**: `mcp/mcp.json`

---

## 📋 Template Information

This `.junie/` configuration follows the **Thin Layer** principle:

| File | Purpose |
|------|---------|
| `README.md` | Directory documentation |
| `guidelines.md` | Generic AI collaboration rules (this file) |
| `config.yaml` | Junie-specific settings |
| `quickref.md` | Quick reference card |
| `project.yaml` | Project variables definition |
| `project-guidelines.md` | Project-specific guidelines |
| `mcp/mcp.json` | MCP server configuration |

**Reusability**: Files marked as 🔄 Generic can be copied to new projects without modification.
Files marked as 📌 Project must be customized for each project.

---

*Part of the Junie Configuration Template System*
