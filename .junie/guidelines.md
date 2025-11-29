# Project Guidelines

> Primary entry point for JetBrains Junie AI collaboration

---

## Table of Contents

- [1. About This File](#1-about-this-file)
- [2. AI Reading Order](#2-ai-reading-order)
- [3. AI Collaboration Rules](#3-ai-collaboration-rules)
- [4. Timeout Hierarchy](#4-timeout-hierarchy)
- [5. Coding Standards](#5-coding-standards)
- [6. Documentation Standards](#6-documentation-standards)
- [7. Directory Structure](#7-directory-structure)
- [8. References](#8-references)
- [9. Template Information](#9-template-information)

---

## 1. About This File

This file contains **generic AI collaboration rules** that apply to any project.
Project-specific information is defined in separate files:

- **Project Config**: `project/config.yaml` — Project identity, tech stack, commands
- **Project Quick Reference**: `project/quickref.md` — Project-specific documentation

Generic configuration files are located in:

- **Settings**: `generic/config.yaml` — Junie settings
- **Quick Reference**: `generic/quickref.md` — Quick lookup card
- **MCP Config**: `mcp/mcp.json` — MCP server configuration
- **Documentation**: `docs/` — Junie documentation

---

## 2. AI Reading Order

When starting a new session, load files in this priority order:

### Priority 1: Essential (Always Load)

| File                  | Purpose                        | When          |
|:----------------------|:-------------------------------|:--------------|
| `guidelines.md`       | Core AI rules, autonomy levels | Every session |
| `project/config.yaml` | Project identity, tech stack   | Every session |

### Priority 2: Context (Load as Needed)

| File                  | Purpose                   | When             |
|:----------------------|:--------------------------|:-----------------|
| `project/quickref.md` | Project-specific patterns | Complex tasks    |
| `generic/quickref.md` | Quick lookup card         | Reference needed |
| `mcp/mcp.json`        | MCP server configuration  | MCP operations   |

### Priority 3: Reference (On Demand)

| File               | Purpose             | When                |
|:-------------------|:--------------------|:--------------------|
| `docs/README.md`   | Documentation index | Finding docs        |
| `docs/guides/*`    | How-to guides       | Specific guidance   |
| `docs/mcp/*`       | MCP documentation   | MCP troubleshooting |
| `docs/reference/*` | Technical reference | Detailed lookup     |

### Loading Strategy

```
Session Start
    │
    ├─► Load guidelines.md (this file)
    │
    ├─► Load project/config.yaml
    │
    ├─► Check task complexity
    │       │
    │       ├─► Simple task → Proceed
    │       │
    │       └─► Complex task → Load quickref.md files
    │
    └─► MCP needed? → Load mcp/mcp.json
```

---

## 3. AI Collaboration Rules

### Autonomy Levels

| Level | Name                        | Description           | Example Tasks                                        |
|:------|:----------------------------|:----------------------|:-----------------------------------------------------|
| L1-L2 | Minimal/Low (0-40%)         | Ask before changes    | Breaking changes, new dependencies, critical systems |
| L3-L4 | Medium/Medium-High (40-80%) | Proceed, report after | Bug fixes, refactoring, routine development ⭐        |
| L5-L6 | High/Full (80-100%)         | High autonomy         | Formatting, comments, docs, trusted patterns         |

**Default**: L4 (Medium-High) for mature collaboration.

**Detailed Examples by Level**:

| Level | Example Commands/Actions                                                       |
|:------|:-------------------------------------------------------------------------------|
| L1    | `rm -rf`, `DROP TABLE`, adding new external dependencies, API breaking changes |
| L2    | Database schema changes, modifying CI/CD pipelines, updating auth logic        |
| L3    | Adding new test files, refactoring single functions, updating error messages   |
| L4    | Bug fixes, code cleanup, adding logging, implementing documented features      |
| L5    | Running `git status`, `pytest`, `ruff check`, updating docstrings              |
| L6    | Formatting code, fixing typos, updating comments, adjusting whitespace         |

### Key Behaviors

1. **Follow existing patterns** in the codebase
2. **Run tests** before committing changes
3. **Update relevant documentation** when modifying features
4. **Output files to designated temp directory** — All temporary/intermediate files must go to the configured output
   directory (typically `.outputs/`), never project root
5. **Create session records** for significant work sessions (see Session History below)
6. **Use English** for code and documentation (unless project specifies otherwise)
7. **Respect timeout limits** when applicable

### Session History Management

At session end, create records in the designated history directory (typically `.history/`):

| Directory        | Purpose                    |
|:-----------------|:---------------------------|
| `conversations/` | Key decisions and outcomes |
| `handoffs/`      | Task continuation context  |
| `current/`       | Active work state          |

**Naming Conventions**:

- Conversations: `YYYY-MM-DD-topic.md`
- Handoffs: `YYYY-MM-DD-task-handoff.md`
- Sessions: `session-YYYYMMDD-HHMM.md`

### Session Automation (MCP Tools)

Use these MCP tools to automate session tracking.

> **Note**: These session management tools require a custom MCP server implementation or can be
> simulated manually by creating files in `.history/`. If no session MCP server is configured,
> use manual file creation as the fallback approach (see Session History Management above).

| Tool             | When to Call                                     | Purpose                                  |
|:-----------------|:-------------------------------------------------|:-----------------------------------------|
| `session_start`  | Beginning of significant work (>30 min expected) | Creates session state file               |
| `session_end`    | Work completed or session ending                 | Creates conversation/handoff record      |
| `session_status` | Start of new session, or to check state          | Shows active sessions and recent records |

**Automatic Trigger Rules**:

| Trigger Condition                | Action                                                          |
|:---------------------------------|:----------------------------------------------------------------|
| Session begins with complex task | Call `session_status()` then `session_start(task, description)` |
| Important decision made          | Document in current session file                                |
| Session duration > 30 minutes    | Ensure session tracking is active                               |
| Work completed successfully      | Call `session_end(summary)`                                     |
| Work incomplete/interrupted      | Call `session_end(summary, next_steps="...")` for handoff       |
| Resuming after break             | Call `session_status()` to check for active sessions            |

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

## 4. Timeout Hierarchy

When implementing time-sensitive operations, consider a tiered timeout approach:

| Tier | Duration | Use Case                           |
|:-----|:---------|:-----------------------------------|
| T1   | ~100ms   | Cache lookup, in-memory operations |
| T2   | ~500ms   | Single file read, simple queries   |
| T3   | ~2s      | Layer/module loading               |
| T4   | ~5s      | Full system initialization         |
| T5   | ~10s     | Complex analysis, external calls   |

**Principle**: Always have fallback strategies for timeout scenarios.

---

## 5. Coding Standards

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

## 6. Documentation Standards

### Key Principles

1. **Single Source of Truth (SSOT)** — One authoritative location per topic
2. **Index Maintenance** — Keep navigation indexes up to date
3. **Cross-References** — Link related documents appropriately
4. **Version Tracking** — Note significant changes

### Documentation Locations

| Type              | Typical Location |
|:------------------|:-----------------|
| User-facing docs  | `docs/`          |
| API documentation | `docs/api/`      |
| Design documents  | `docs/design/`   |
| Project context   | `.context/`      |
| Generic knowledge | `.knowledge/`    |

---

## 7. Directory Structure

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

| Directory   | Purpose                         |
|:------------|:--------------------------------|
| `.junie/`   | Junie AI configuration          |
| `.context/` | Project-specific knowledge base |
| `.history/` | AI session records              |
| `.outputs/` | Temporary/intermediate files    |

---

## 8. References

For project-specific information, see:

- **Project Config**: `project/config.yaml`
- **Project Quick Reference**: `project/quickref.md`

For generic configuration, see:

- **Quick Reference**: `generic/quickref.md`
- **Configuration**: `generic/config.yaml`
- **MCP Settings**: `mcp/mcp.json`
- **Documentation**: `docs/`

---

## 9. Template Information

This `.junie/` configuration follows the **Thin Layer** principle with clear separation:

### Root Files (🔄 Generic)

| File            | Purpose                                    |
|:----------------|:-------------------------------------------|
| `README.md`     | Directory documentation                    |
| `guidelines.md` | Generic AI collaboration rules (this file) |

### Root Directories

| Directory  | Type | Purpose                                     |
|:-----------|:-----|:--------------------------------------------|
| `generic/` | 🔄   | Generic settings (config.yaml, quickref.md) |
| `mcp/`     | 🔄   | MCP server configuration                    |
| `schema/`  | 🔄   | JSON Schema validation files                |
| `docs/`    | 🔄   | Junie documentation                         |
| `project/` | 📌   | Project-specific files                      |

### Project Directory (`project/`) — 📌 Customize

| File          | Purpose                          |
|:--------------|:---------------------------------|
| `config.yaml` | Project variables definition     |
| `quickref.md` | Project-specific quick reference |

**Reusability**:

- 🔄 Generic files can be copied to new projects without modification
- 📌 Project files must be customized for each project

---

*Part of the Junie Configuration Template System*
