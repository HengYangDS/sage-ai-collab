---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---

# Changelog

All notable changes to SAGE Knowledge Base will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- AI collaboration patterns documentation (`.context/intelligence/patterns.md`)
- Comprehensive API documentation (`docs/api/`)
- User guides (`docs/guides/`)
- Extended scenario documentation for knowledge management, MCP integration, and plugin development
- Design documentation index (`docs/design/index.md`)
- Framework index files for all `.knowledge/frameworks/` subdirectories
- Archive index (`.archive/index.md`)

### Changed

- Updated configuration structure to modular YAML format
- Improved documentation cross-references
- Standardized layer terminology: "Tools" → "Capabilities" in guidelines
- Renamed `.context/configurations/` to `.context/policies/` for semantic clarity
- Updated all cross-references to reflect policies directory rename (16 files)

### Fixed

- README.md Python API example now uses proper async/await syntax
- Root `index.md` project structure now includes `.backups/` and `config/environments/`
- `.junie/guidelines.md` project structure now complete with all directories

## [0.1.0] - 2025-11-29

### Added

#### Core Infrastructure

- 5-level timeout hierarchy (T1: 100ms → T5: 10s)
- Circuit breaker pattern for fault tolerance
- Smart task-based loading with token budget management
- Graceful degradation - never hangs, always returns useful content
- EventBus for decoupled component communication
- Dependency injection container

#### Knowledge Management

- 4-layer knowledge structure (Core, Guidelines, Frameworks, Practices)
- Content directory with reusable knowledge
- Project context directory (`.context/`)
- Session history tracking (`.history/`)
- Modular configuration system (`config/`)

#### Services

- CLI service using Typer + Rich
- MCP server using FastMCP
- REST API using FastAPI + Uvicorn (optional)

#### Architecture Decisions

- ADR-0001: Three-layer architecture
- ADR-0002: SAGE protocol design
- ADR-0003: Timeout hierarchy
- ADR-0004: Dependency injection
- ADR-0005: Event-driven architecture
- ADR-0006: Protocol-first design
- ADR-0007: Modular configuration
- ADR-0008: Plugin system

#### Documentation

- Design documents (`docs/design/00-09`)
- Code conventions (`.context/conventions/`)
- Document templates (`.knowledge/templates/`)
- AI collaboration guidelines (`.junie/guidelines.md`)

#### Development Tools

- Ruff for linting and formatting
- MyPy for type checking
- pytest with asyncio support
- Pre-commit hooks configuration
- GitHub Actions CI/CD workflows

### Technical Details

#### Dependencies

- Python 3.12+
- PyYAML >= 6.0
- Pydantic >= 2.0
- Typer >= 0.9.0
- Rich >= 13.0
- structlog >= 24.0

#### Optional Dependencies

- MCP support: mcp >= 1.0, httpx >= 0.25, uvicorn >= 0.22
- Development: pytest, pytest-asyncio, pytest-cov, ruff, mypy

---

## Version History

| Version | Date       | Highlights                         |
|---------|------------|------------------------------------|
| 0.1.0   | 2025-11-29 | Initial release with core features |

---

[Unreleased]: https://github.com/HengYangDS/sage-kb/compare/v0.1.0...HEAD

[0.1.0]: https://github.com/HengYangDS/sage-kb/releases/tag/v0.1.0
