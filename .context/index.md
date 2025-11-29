# Project Context Navigation

> Project-specific knowledge base for SAGE Knowledge Base

---

## Table of Contents

- [1. Directory Structure](#1-directory-structure)
- [2. Content Categories](#2-content-categories)
- [3. Quick Access](#3-quick-access)
- [4. Usage Guide](#4-usage-guide)

---

## 1. Directory Structure

| Directory       | Purpose                              | Contents |
|:-----------------|:--------------------------------------|:---------|
| `overview/`     | Project introduction and quick start | 1 file   |
| `policies/`     | Project-specific policies            | 6 files  |
| `conventions/`  | Project-specific coding conventions  | 3 files  |
| `decisions/`    | Architecture Decision Records (ADRs) | 8 files  |
| `intelligence/` | AI collaboration (4 subdirectories)  | 8 files  |

---

## 2. Content Categories

### 2.0 Overview

Quick introduction to the project:

| Document              | Description                                      |
|:----------------------|:-------------------------------------------------|
| `project_overview.md` | Project introduction, architecture, key concepts |

### 2.1 Policies

Project-specific policy documentation:

| Document                    | Description                                   |
|:-----------------------------|:-----------------------------------------------|
| `timeout_hierarchy.md`      | T1-T5 timeout levels and fallback strategies  |
| `loading_configurations.md` | Knowledge loading strategies and layer config |
| `runtime_settings.md`       | Environment variables, logging, services      |
| `memory_settings.md`        | Memory persistence and caching configuration  |
| `plugin_settings.md`        | Plugin system settings and extension points   |
| `service_settings.md`       | Service layer configuration (CLI, MCP, API)   |

### 2.2 Conventions

Project-specific rules and standards:

| Document            | Description                              |
|:---------------------|:------------------------------------------|
| `naming.md`         | Naming conventions for all code elements |
| `code_patterns.md`  | DI, EventBus, timeout, async patterns    |
| `file_structure.md` | Directory layout, module organization    |

### 2.3 Decisions

Architecture Decision Records (ADRs) documenting significant technical decisions.

**ADR Format**: All ADRs follow the standard ADR template structure:
- **Status** → **Context** → **Decision** → **Alternatives Considered** → **Consequences** → **Implementation** → **Related**

This format is an industry-standard pattern for documenting architecture decisions, providing consistent structure for decision rationale and traceability.

| ADR      | Title                           | Status   |
|:----------|:---------------------------------|:----------|
| ADR-0001 | Three-Layer Architecture        | Accepted |
| ADR-0002 | SAGE Protocol Design            | Accepted |
| ADR-0003 | Timeout Hierarchy Design        | Accepted |
| ADR-0004 | Dependency Injection Container  | Accepted |
| ADR-0005 | Event Bus Architecture          | Accepted |
| ADR-0006 | Protocol-First Interface Design | Accepted |
| ADR-0007 | Configuration Management        | Accepted |
| ADR-0008 | Plugin System Design            | Accepted |

### 2.4 Intelligence

AI collaboration patterns, learned behaviors, and project-specific calibration data.

**Purpose**: This directory contains knowledge that helps AI assistants collaborate effectively with the project:
- **Calibration**: Autonomy levels and decision boundaries for this project
- **Patterns**: Successful interaction templates and workflows
- **Learning**: Cases, lessons, and pitfalls from actual development
- **Optimization**: Performance tuning and efficiency improvements

#### Subdirectory Structure

| Subdirectory    | Purpose                        | Files |
|:----------------|:-------------------------------|:------|
| `calibration/`  | Autonomy levels and patterns   | 2     |
| `learning/`     | Cases, lessons, pitfalls       | 3     |
| `optimization/` | Performance and optimizations  | 2     |
| `automation/`   | Session automation planning    | 1     |

#### Files by Subdirectory

**calibration/** — Autonomy and patterns:

| Document          | Description                                   |
|:------------------|:----------------------------------------------|
| `calibration.md`  | Autonomy level calibration (L1-L6)            |
| `patterns.md`     | Successful interaction patterns and templates |

**learning/** — Cases and lessons:

| Document             | Description                           |
|:---------------------|:--------------------------------------|
| `cases.md`           | Case studies and real-world examples  |
| `lessons_learned.md` | Key learnings from project development|
| `common_pitfalls.md` | Common mistakes and how to avoid them |

**optimization/** — Performance:

| Document              | Description                                   |
|:----------------------|:----------------------------------------------|
| `optimizations.md`    | Code generation preferences, testing          |
| `performance_tuning.md` | Performance optimization strategies         |

**automation/** — Session management:

| Document                             | Description                               |
|:-------------------------------------|:------------------------------------------|
| `session_automation_requirements.md` | Long-term automation plan for session history |

---

## 3. Quick Access

### 3.1 By Topic

| Topic                | Documents                                                                            |
|:----------------------|:-------------------------------------------------------------------------------------|
| **Getting Started**  | `overview/project_overview.md`, `conventions/naming.md`                              |
| **Architecture**     | `decisions/ADR-0001-architecture.md`, `decisions/ADR-0002-sage-protocol.md`          |
| **Configuration**    | `policies/runtime_settings.md`, `policies/loading_configurations.md`                 |
| **Timeouts**         | `policies/timeout_hierarchy.md`, `decisions/ADR-0003-timeout-hierarchy.md`           |
| **DI & Events**      | `decisions/ADR-0004-dependency-injection.md`, `decisions/ADR-0005-event-bus.md`      |
| **AI Collaboration** | `intelligence/calibration/calibration.md`, `intelligence/calibration/patterns.md`   |

### 3.2 All Documents

#### Overview

- `overview/project_overview.md` — Project introduction and quick start

#### Policies

- `policies/timeout_hierarchy.md` — SAGE T1-T5 timeout levels
- `policies/loading_configurations.md` — Loading strategies and layers
- `policies/runtime_settings.md` — Environment and runtime config
- `policies/memory_settings.md` — Memory persistence and caching
- `policies/plugin_settings.md` — Plugin system settings
- `policies/service_settings.md` — Service layer configuration

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

**calibration/**
- `intelligence/calibration/calibration.md` — Autonomy calibration (L1-L6)
- `intelligence/calibration/patterns.md` — AI interaction patterns

**learning/**
- `intelligence/learning/cases.md` — Case studies and examples
- `intelligence/learning/lessons_learned.md` — Key project learnings
- `intelligence/learning/common_pitfalls.md` — Common mistakes to avoid

**optimization/**
- `intelligence/optimization/optimizations.md` — Project optimizations
- `intelligence/optimization/performance_tuning.md` — Performance optimization

**automation/**
- `intelligence/automation/session_automation_requirements.md` — Session history automation

---

## 4. Usage Guide

### 4.1 For New Contributors

1. Start with `overview/project_overview.md` for quick introduction
2. Read `conventions/naming.md` and `conventions/file_structure.md`
3. Review key ADRs: ADR-0001 (architecture), ADR-0002 (SAGE protocol)

### 4.2 For AI Assistants

1. Check `intelligence/calibration/calibration.md` for autonomy levels
2. Follow patterns in `intelligence/calibration/patterns.md`
3. Use optimizations from `intelligence/optimization/optimizations.md`
4. Learn from `intelligence/learning/` (cases, lessons, pitfalls)

### 4.3 For Policies

1. Timeout settings: `policies/timeout_hierarchy.md`
2. Loading behavior: `policies/loading_configurations.md`
3. Runtime/environment: `policies/runtime_settings.md`

---

## Related

- `.knowledge/` — Generic, reusable knowledge
- `.junie/guidelines.md` — AI collaboration guidelines
- `docs/design/` — Design documents
- `README.md` — Project overview

---

*Part of SAGE Knowledge Base - Project Context*
