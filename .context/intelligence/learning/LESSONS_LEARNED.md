# Lessons Learned

> Key insights and learnings from SAGE Knowledge Base development

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Architecture Lessons](#2-architecture-lessons)
- [3. Implementation Lessons](#3-implementation-lessons)
- [4. Process Lessons](#4-process-lessons)
- [5. AI Collaboration Lessons](#5-ai-collaboration-lessons)

---

## 1. Overview

This document captures significant lessons learned during the development of SAGE Knowledge Base. These insights help
avoid repeating mistakes and reinforce successful patterns.

### 1.1 Document Format

Each lesson follows this structure:

- **Context**: What situation led to this learning
- **Challenge**: What problem was encountered
- **Solution**: How it was resolved
- **Lesson**: The generalizable insight

---

## 2. Architecture Lessons

### 2.1 Timeout Hierarchy Design

**Context**: Initial implementation had inconsistent timeout handling across components.

**Challenge**: Some operations would hang indefinitely, causing poor user experience.

**Solution**: Implemented 5-level timeout hierarchy (T1-T5) with clear escalation.

**Lesson**: Design timeout strategy upfront. Every I/O operation needs a timeout. Graceful degradation is better than
hanging.

| Level | Timeout | Use Case         |
|:------|:--------|:-----------------|
| T1    | 100ms   | Cache lookup     |
| T2    | 500ms   | Single file      |
| T3    | 2s      | Layer load       |
| T4    | 5s      | Full KB load     |
| T5    | 10s     | Complex analysis |

### 2.2 Three-Layer Architecture

**Context**: Started with a monolithic design that became hard to extend.

**Challenge**: Adding new features required changes across the codebase.

**Solution**: Refactored to Core → Services → Plugins architecture.

**Lesson**: Clear layer boundaries with defined interfaces make the system more maintainable. Core should have zero
external dependencies.

### 2.3 Event-Driven Communication

**Context**: Components had tight coupling through direct method calls.

**Challenge**: Changes in one component cascaded to others.

**Solution**: Introduced EventBus for component communication.

**Lesson**: Event-driven architecture reduces coupling and makes testing easier. Components should communicate through
events, not direct calls.

---

## 3. Implementation Lessons

### 3.1 Configuration Management

**Context**: Configuration was scattered across multiple files without clear organization.

**Challenge**: Hard to find where settings were defined, inconsistent formats.

**Solution**: Modular YAML configuration with clear hierarchy.

**Lesson**: Configuration should follow the same principles as code: single responsibility, clear naming, documented
defaults.

```
config/
├── sage.yaml          # Main entry point
├── core/              # Core settings
├── knowledge/         # Knowledge loading
└── services/          # Service configs
```

### 3.2 Protocol-First Design

**Context**: Interfaces were implicit, defined by implementation.

**Challenge**: Changing implementation broke dependent code.

**Solution**: Define protocols (interfaces) first, then implement.

**Lesson**: `typing.Protocol` enables duck typing with type safety. Define contracts before implementation.

```python
# Define protocol
class LoaderProtocol(Protocol):
    async def load(self, path: str) -> Content: ...


# Implementation can vary
class FileLoader:  # Implicitly implements LoaderProtocol
    async def load(self, path: str) -> Content: ...
```

### 3.3 Dependency Injection

**Context**: Components created their own dependencies.

**Challenge**: Testing required mocking at module level, inflexible.

**Solution**: Implemented DI container for dependency management.

**Lesson**: DI makes code testable and configurable. Pass dependencies in, don't create them inside.

---

## 4. Process Lessons

### 4.1 Documentation-Driven Development

**Context**: Documentation was written after implementation.

**Challenge**: Docs became outdated, inconsistent with code.

**Solution**: Write documentation alongside or before code.

**Lesson**: Documentation is part of the deliverable. Update docs in the same commit as code changes.

### 4.2 Incremental Refactoring

**Context**: Attempted large-scale refactoring in single PRs.

**Challenge**: Large changes were hard to review and debug.

**Solution**: Break refactoring into small, incremental steps.

**Lesson**: Small changes are easier to review, test, and revert. Each change should be complete and functional.

### 4.3 Test Coverage Strategy

**Context**: Tests were added inconsistently.

**Challenge**: Some critical paths had no coverage.

**Solution**: Test pyramid approach: unit → integration → e2e.

**Lesson**: Focus on testing behavior, not implementation. Integration tests catch more real issues than unit tests
alone.

### 4.4 Documentation Naming Convention Evolution

**Context**: Project started with lowercase `snake_case.md` naming for documentation files.

**Challenge**: Multiple issues emerged during project evolution:
1. Lowercase names lacked visual distinction from code files
2. Date format `YYYY-MM-DD` in filenames caused inconsistency
3. External tool directories (`.junie/`) had conflicting conventions
4. Large-scale renaming required updating hundreds of cross-references

**Solution**: Implemented systematic naming convention changes:
1. Adopted `UPPER_SNAKE_CASE.md` for all documentation (lowercase `.md` extension)
2. Changed date format from `YYYY-MM-DD` to `YYYYMMDD` for compactness
3. Documented explicit exceptions (e.g., `.junie/guidelines.md` for tool compatibility)
4. Created batch processing scripts (`tools/fix_md_extension.py`) for bulk updates

**Lesson**: 
- **Plan naming conventions early** — Changing conventions late requires significant rework
- **Document exceptions explicitly** — External tool requirements may conflict with internal standards
- **Automate bulk changes** — Scripts reduce errors and ensure consistency across large codebases
- **Update references atomically** — File renames must include reference updates in the same commit

| Aspect | Before | After | Rationale |
|:-------|:-------|:------|:----------|
| Case | `snake_case.md` | `UPPER_SNAKE_CASE.md` | Visual distinction |
| Extension | `.MD` (attempted) | `.md` | Cross-platform compatibility |
| Date | `YYYY-MM-DD` | `YYYYMMDD` | Compact, no hyphen issues |
| Exceptions | Implicit | Explicit in standards | Clarity and maintainability |

---

## 5. AI Collaboration Lessons

### 5.1 Context Management

**Context**: AI sessions started with full context every time.

**Challenge**: Token budget exceeded, important context lost.

**Solution**: Layered context loading with priorities.

**Lesson**: Less is more for AI context. Core principles always, details on-demand.

### 5.2 Autonomy Calibration

**Context**: Unclear when AI should ask vs proceed.

**Challenge**: Either too many questions or unexpected changes.

**Solution**: 6-level autonomy framework with clear guidelines.

**Lesson**: Explicit autonomy levels prevent misunderstandings. Default to lower autonomy for risky operations.

### 5.3 Session Continuity

**Context**: Context lost between AI sessions.

**Challenge**: Repeated work, inconsistent decisions.

**Solution**: `.history/` directory for session tracking, handoff templates.

**Lesson**: Document session state and decisions. Future sessions can pick up where previous left off.

### 5.4 Knowledge Directory Boundaries (MECE)

**Context**: Three directories (`.knowledge/`, `.context/`, `.junie/`) for different knowledge types.

**Challenge**: Content boundaries were not strictly enforced:
1. Generic `.knowledge/` contained project-specific references (e.g., "SAGE CLI commands")
2. Footers branded with project name ("Part of SAGE Knowledge Base")
3. Unclear criteria for what belongs where

**Solution**: Established strict MECE (Mutually Exclusive, Collectively Exhaustive) boundaries:

| Directory | Scope | Content Criteria |
|:----------|:------|:-----------------|
| `.knowledge/` | Universal | Reusable across ANY project, NO project-specific references |
| `.context/` | Project-Specific | Only for THIS project, contains project names/paths |
| `.junie/` | Tool Config | JetBrains Junie configuration, follows tool conventions |

**Lesson**:
- **Define boundaries upfront** — Establish clear MECE criteria before adding content
- **No brand in generic knowledge** — Universal knowledge must be project-agnostic
- **Audit regularly** — Review content placement during major refactoring
- **Generalize or relocate** — Content with project references either generalize or move to `.context/`

### 5.5 Frontmatter Metadata Anti-Pattern

**Context**: Added YAML frontmatter (version, tokens, last_updated) to all markdown files.

**Challenge**: Frontmatter became maintenance burden:
1. Token counts became stale immediately after edits
2. Version numbers never updated consistently
3. `last_updated` dates conflicted with Git history
4. Added ~6 lines overhead to every file

**Solution**: Removed all frontmatter from `.knowledge/` documents:
1. Created `tools/remove_frontmatter.py` for batch removal
2. Updated `DOCUMENTATION_STANDARDS.md` to prohibit frontmatter
3. Added "Frontmatter Policy" section to `PROJECT_DIRECTORY_STRUCTURE.md`

**Lesson**:
- **Git is the source of truth** — Version control provides authoritative history
- **Avoid redundant metadata** — Information that Git tracks shouldn't be duplicated
- **Simpler is better** — Documents should start with content, not boilerplate
- **Automate cleanup** — Batch scripts essential for removing patterns across many files

| Metadata | Problem | Alternative |
|:---------|:--------|:------------|
| `version` | Never updated | Git tags/commits |
| `last_updated` | Conflicts with Git | `git log` |
| `tokens` | Stale after edits | Calculate on-demand |
| `status` | Rarely accurate | Git branches |

---

## Applying Lessons

### When Starting New Feature

1. Review relevant lessons
2. Apply architectural patterns
3. Consider failure modes
4. Document decisions

### When Encountering Issues

1. Check if similar issue documented
2. Apply known solutions
3. Document new learnings
4. Update this file

---

## Related

- `.context/decisions/` — Architecture Decision Records
- `.context/intelligence/calibration/PATTERNS.md` — Successful patterns
- `.context/intelligence/learning/COMMON_PITFALLS.md` — Pitfalls to avoid
- `.knowledge/practices/engineering/INCREMENTAL_IMPROVEMENT.md` — Incremental approach
- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Documentation naming conventions

---

*Last updated: 2025-11-30*
*AI Collaboration Knowledge Base*
