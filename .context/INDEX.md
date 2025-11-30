---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---
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
|:----------------|:-------------------------------------|:---------|
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
| `PROJECT_OVERVIEW.md` | Project introduction, architecture, key concepts |

### 2.1 Policies

Project-specific policy documentation:

| Document                    | Description                                   |
|:----------------------------|:----------------------------------------------|
| `TIMEOUT_HIERARCHY.md`      | T1-T5 timeout levels and fallback strategies  |
| `LOADING_CONFIGURATIONS.md` | Knowledge loading strategies and layer config |
| `RUNTIME_SETTINGS.md`       | Environment variables, logging, services      |
| `MEMORY_SETTINGS.md`        | Memory persistence and caching configuration  |
| `PLUGIN_SETTINGS.md`        | Plugin system settings and extension points   |
| `SERVICE_SETTINGS.md`       | Service layer configuration (CLI, MCP, API)   |

### 2.2 Conventions

Project-specific rules and standards:

| Document            | Description                              |
|:--------------------|:-----------------------------------------|
| `NAMING.md`         | Naming conventions for all code elements |
| `CODE_PATTERNS.md`  | DI, EventBus, timeout, async patterns    |
| `FILE_STRUCTURE.md` | Directory layout, module organization    |

### 2.3 Decisions

Architecture Decision Records (ADRs) documenting significant technical decisions.

**ADR Format**: All ADRs follow the standard ADR template structure:

- **Status** → **Context** → **Decision** → **Alternatives Considered** → **Consequences** → **Implementation** → *
  *Related**

This format is an industry-standard pattern for documenting architecture decisions, providing consistent structure for
decision rationale and traceability.

| ADR      | Title                           | Status   |
|:---------|:--------------------------------|:---------|
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

| Subdirectory    | Purpose                       | Files |
|:----------------|:------------------------------|:------|
| `calibration/`  | Autonomy levels and patterns  | 2     |
| `learning/`     | Cases, lessons, pitfalls      | 3     |
| `optimization/` | Performance and optimizations | 2     |
| `automation/`   | Session automation planning   | 1     |

#### Files by Subdirectory

**calibration/** — Autonomy and patterns:

| Document         | Description                                   |
|:-----------------|:----------------------------------------------|
| `CALIBRATION.md` | Autonomy level calibration (L1-L6)            |
| `PATTERNS.md`    | Successful interaction patterns and templates |

**learning/** — Cases and lessons:

| Document             | Description                            |
|:---------------------|:---------------------------------------|
| `CASES.md`           | Case studies and real-world examples   |
| `LESSONS_LEARNED.md` | Key learnings from project development |
| `COMMON_PITFALLS.md` | Common mistakes and how to avoid them  |

**optimization/** — Performance:

| Document                | Description                          |
|:------------------------|:-------------------------------------|
| `OPTIMIZATIONS.md`      | Code generation preferences, testing |
| `PERFORMANCE_TUNING.md` | Performance optimization strategies  |

**automation/** — Session management:

| Document                             | Description                                   |
|:-------------------------------------|:----------------------------------------------|
| `SESSION_AUTOMATION_REQUIREMENTS.md` | Long-term automation plan for session history |

---

## 3. Quick Access

### 3.1 By Topic

| Topic                | Documents                                                                         |
|:---------------------|:----------------------------------------------------------------------------------|
| **Getting Started**  | `overview/PROJECT_OVERVIEW.md`, `conventions/NAMING.md`                           |
| **Architecture**     | `decisions/ADR-0001-ARCHITECTURE.md`, `decisions/ADR-0002-SAGE-PROTOCOL.md`       |
| **Configuration**    | `policies/RUNTIME_SETTINGS.md`, `policies/LOADING_CONFIGURATIONS.md`              |
| **Timeouts**         | `policies/TIMEOUT_HIERARCHY.md`, `decisions/ADR-0003-TIMEOUT-HIERARCHY.md`        |
| **DI & Events**      | `decisions/ADR-0004-DEPENDENCY-INJECTION.md`, `decisions/ADR-0005-EVENT-BUS.md`   |
| **AI Collaboration** | `intelligence/calibration/CALIBRATION.md`, `intelligence/calibration/PATTERNS.md` |

### 3.2 All Documents

#### Overview

- `overview/PROJECT_OVERVIEW.md` — Project introduction and quick start

#### Policies

- `policies/TIMEOUT_HIERARCHY.md` — SAGE T1-T5 timeout levels
- `policies/LOADING_CONFIGURATIONS.md` — Loading strategies and layers
- `policies/RUNTIME_SETTINGS.md` — Environment and runtime config
- `policies/MEMORY_SETTINGS.md` — Memory persistence and caching
- `policies/PLUGIN_SETTINGS.md` — Plugin system settings
- `policies/SERVICE_SETTINGS.md` — Service layer configuration

#### Conventions

- `conventions/NAMING.md` — Naming conventions
- `conventions/CODE_PATTERNS.md` — Code patterns (DI, EventBus, etc.)
- `conventions/FILE_STRUCTURE.md` — File and directory organization

#### Decisions (ADRs)

- `decisions/ADR-0001-ARCHITECTURE.md` — Three-layer architecture
- `decisions/ADR-0002-SAGE-PROTOCOL.md` — SAGE protocol design
- `decisions/ADR-0003-TIMEOUT-HIERARCHY.md` — Timeout hierarchy
- `decisions/ADR-0004-DEPENDENCY-INJECTION.md` — DI container
- `decisions/ADR-0005-EVENT-BUS.md` — Event bus
- `decisions/ADR-0006-PROTOCOL-FIRST.md` — Protocol-first design
- `decisions/ADR-0007-CONFIGURATION.md` — Configuration management
- `decisions/ADR-0008-PLUGIN-SYSTEM.md` — Plugin system

#### Intelligence

**calibration/**

- `intelligence/calibration/CALIBRATION.md` — Autonomy calibration (L1-L6)
- `intelligence/calibration/PATTERNS.md` — AI interaction patterns

**learning/**

- `intelligence/learning/CASES.md` — Case studies and examples
- `intelligence/learning/LESSONS_LEARNED.md` — Key project learnings
- `intelligence/learning/COMMON_PITFALLS.md` — Common mistakes to avoid

**optimization/**

- `intelligence/optimization/OPTIMIZATIONS.md` — Project optimizations
- `intelligence/optimization/PERFORMANCE_TUNING.md` — Performance optimization

**automation/**

- `intelligence/automation/SESSION_AUTOMATION_REQUIREMENTS.md` — Session history automation

---

## 4. Usage Guide

### 4.1 For New Contributors

1. Start with `overview/PROJECT_OVERVIEW.md` for quick introduction
2. Read `conventions/NAMING.md` and `conventions/FILE_STRUCTURE.md`
3. Review key ADRs: ADR-0001 (architecture), ADR-0002 (SAGE protocol)

### 4.2 For AI Assistants

1. Check `intelligence/calibration/CALIBRATION.md` for autonomy levels
2. Follow patterns in `intelligence/calibration/PATTERNS.md`
3. Use optimizations from `intelligence/optimization/OPTIMIZATIONS.md`
4. Learn from `intelligence/learning/` (cases, lessons, pitfalls)

### 4.3 For Policies

1. Timeout settings: `policies/TIMEOUT_HIERARCHY.md`
2. Loading behavior: `policies/LOADING_CONFIGURATIONS.md`
3. Runtime/environment: `policies/RUNTIME_SETTINGS.md`

---

## Related

- `.knowledge/` — Generic, reusable knowledge
- `.junie/GUIDELINES.md` — AI collaboration guidelines
- `docs/design/` — Design documents
- `README.md` — Project overview

---

*Part of SAGE Knowledge Base - Project Context*
