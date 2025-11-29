# Project Context Navigation

> Project-specific knowledge base for SAGE Knowledge Base

---

## Table of Contents

[1. Directory Structure](#1-directory-structure) · [2. Content Categories](#2-content-categories) · [3. Quick Access](#3-quick-access)

---

## 1. Directory Structure

| Directory | Purpose | Files |
|-----------|---------|-------|
| `configurations/` | Project-specific configurations | 3 |
| `conventions/` | Project-specific coding conventions | 3 |
| `decisions/` | Architecture Decision Records (ADRs) | 8 |
| `intelligence/` | AI intelligence patterns | 3 |

---

## 2. Content Categories

### 2.1 Configurations

Project-specific configuration documentation:

| Document | Description |
|----------|-------------|
| `timeout_hierarchy.md` | T1-T5 timeout levels and fallback strategies |
| `loading_configurations.md` | Knowledge loading strategies and layer config |
| `runtime_settings.md` | Environment variables, logging, services |

### 2.2 Conventions

Project-specific rules and standards:

| Document | Description |
|----------|-------------|
| `naming.md` | Naming conventions for all code elements |
| `code_patterns.md` | DI, EventBus, timeout, async patterns |
| `file_structure.md` | Directory layout, module organization |

### 2.3 Decisions

Architecture Decision Records documenting significant technical decisions:

| ADR | Title | Status |
|-----|-------|--------|
| ADR-0001 | Three-Layer Architecture | Accepted |
| ADR-0002 | SAGE Protocol Design | Accepted |
| ADR-0003 | Timeout Hierarchy Design | Accepted |
| ADR-0004 | Dependency Injection Container | Accepted |
| ADR-0005 | Event Bus Architecture | Accepted |
| ADR-0006 | Protocol-First Interface Design | Accepted |
| ADR-0007 | Configuration Management | Accepted |
| ADR-0008 | Plugin System Design | Accepted |

### 2.4 Intelligence

AI collaboration patterns and learned behaviors:

| Document | Description |
|----------|-------------|
| `patterns.md` | Successful interaction patterns and templates |
| `optimizations.md` | Code generation preferences, testing, performance |
| `calibration.md` | Autonomy level calibration (L1-L6) |

---

## 3. Quick Access

### 3.1 By Topic

| Topic | Documents |
|-------|-----------|
| **Getting Started** | `conventions/naming.md`, `conventions/file_structure.md` |
| **Architecture** | `decisions/ADR-0001-architecture.md`, `decisions/ADR-0002-sage-protocol.md` |
| **Configuration** | `configurations/runtime_settings.md`, `configurations/loading_configurations.md` |
| **Timeouts** | `configurations/timeout_hierarchy.md`, `decisions/ADR-0003-timeout-hierarchy.md` |
| **DI & Events** | `decisions/ADR-0004-dependency-injection.md`, `decisions/ADR-0005-event-bus.md` |
| **AI Collaboration** | `intelligence/patterns.md`, `intelligence/calibration.md` |

### 3.2 All Documents

#### Configurations
- `configurations/timeout_hierarchy.md` — SAGE T1-T5 timeout levels
- `configurations/loading_configurations.md` — Loading strategies and layers
- `configurations/runtime_settings.md` — Environment and runtime config

#### Conventions
- `conventions/naming.md` — Naming conventions
- `conventions/code_patterns.md` — Code patterns (DI, EventBus, etc.)
- `conventions/file_structure.md` — File and directory organization

#### Decisions (ADRs)
- `decisions/ADR-0001-architecture.md` — Three-layer architecture
- `decisions/ADR-0002-sage-protocol.md` — SAGE protocol design
- `decisions/ADR-0003-timeout-hierarchy.md` — Timeout hierarchy
- `decisions/ADR-0004-dependency-injection.md` — DI container
- `decisions/ADR-0005-event-bus.md` — Event bus
- `decisions/ADR-0006-protocol-first.md` — Protocol-first design
- `decisions/ADR-0007-configuration.md` — Configuration management
- `decisions/ADR-0008-plugin-system.md` — Plugin system

#### Intelligence
- `intelligence/patterns.md` — AI interaction patterns
- `intelligence/optimizations.md` — Project optimizations
- `intelligence/calibration.md` — Autonomy calibration

---

## 4. Usage Guide

### 4.1 For New Contributors

1. Start with `conventions/naming.md` and `conventions/file_structure.md`
2. Read key ADRs: ADR-0001 (architecture), ADR-0002 (SAGE protocol)
3. Review `intelligence/patterns.md` for AI collaboration

### 4.2 For AI Assistants

1. Check `intelligence/calibration.md` for autonomy levels
2. Follow patterns in `intelligence/patterns.md`
3. Use optimizations from `intelligence/optimizations.md`
4. Reference conventions when generating code

### 4.3 For Configuration

1. Timeout settings: `configurations/timeout_hierarchy.md`
2. Loading behavior: `configurations/loading_configurations.md`
3. Runtime/environment: `configurations/runtime_settings.md`

---

## Related

- `content/` — Generic, reusable knowledge
- `.junie/guidelines.md` — AI collaboration guidelines
- `docs/design/` — Design documents
- `README.md` — Project overview

---

*Part of SAGE Knowledge Base - Project Context*
