# Changelog

> All notable changes to SAGE Knowledge Base

---

## Format

This changelog follows [Keep a Changelog](https://keepachangelog.com/) format.

Types of changes:
- **Added** — New features
- **Changed** — Changes in existing functionality
- **Deprecated** — Soon-to-be removed features
- **Removed** — Removed features
- **Fixed** — Bug fixes
- **Security** — Vulnerability fixes

---

## [Unreleased]

### Added

- Complete docs/design restructure following v9.0 plan
- 12 subdirectory structure with MECE organization
- All capability family documentation (5 families)
- Service layer documentation (CLI, MCP, API)
- Knowledge system documentation
- Memory state documentation
- Configuration documentation
- Evolution documentation

### Changed

- Migrated from numbered prefixes to UPPER_SNAKE_CASE naming
- Reorganized content into four-layer architecture
- Updated all cross-references

---

## [0.4.0] - 2025-11-30

### Added

- Plugin architecture documentation
- Extension points documentation
- Plugin lifecycle documentation
- Bundled plugins documentation
- Capability model documentation

### Changed

- Refined timeout resilience patterns
- Updated circuit breaker documentation

---

## [0.3.0] - 2025-11-15

### Added

- CLI service implementation
- MCP service implementation
- API service framework
- Service layer architecture
- Error handling patterns

### Changed

- Unified service interfaces
- Standardized error codes

### Fixed

- Timeout handling in services
- Response format consistency

---

## [0.2.0] - 2025-10-30

### Added

- SAGE protocol implementation
- Source protocol
- Analyze protocol
- Generate protocol
- Evolve protocol
- DI container
- Event bus
- Bootstrap system

### Changed

- Core architecture refinement
- Protocol interfaces

---

## [0.1.0] - 2025-10-15

### Added

- Initial project structure
- Directory layout
- Basic documentation
- Development setup
- CI/CD pipeline
- Test framework

---

## Version History Summary

| Version | Date | Highlights |
|---------|------|------------|
| 0.4.0 | 2025-11-30 | Plugin system, capabilities |
| 0.3.0 | 2025-11-15 | Services (CLI, MCP, API) |
| 0.2.0 | 2025-10-30 | Core protocols, DI, events |
| 0.1.0 | 2025-10-15 | Initial release |

---

## Migration Guides

### 0.3.x → 0.4.x

```python
# Old: Direct capability access
from sage.capabilities import analyzer

# New: Registry-based access
from sage.core.registry import get_capability
analyzer = get_capability("analyzer")
```

### 0.2.x → 0.3.x

```python
# Old: Direct service initialization
cli = CLIService()

# New: Container-based initialization
container = get_container()
cli = container.resolve(CLIService)
```

---

## Deprecation Notices

| Feature | Deprecated | Removed | Alternative |
|---------|------------|---------|-------------|
| Direct protocol access | 0.3.0 | 0.5.0 | Use DI container |
| Legacy config format | 0.4.0 | 1.0.0 | Use YAML DSL |

---

## Related

- `ROADMAP.md` — Future plans
- `MILESTONES.md` — Project milestones
- `EVALUATION_CRITERIA.md` — Quality criteria

---

*Part of SAGE Knowledge Base*
