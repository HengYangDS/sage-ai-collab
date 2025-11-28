# AI Collaboration Knowledge Base - Navigation Index

> **Load Priority**: Always Load (~100 tokens)  
> **Purpose**: Quick navigation to all knowledge layers

---

## 🎯 Quick Start

| Need              | Go To                                                                        |
|-------------------|------------------------------------------------------------------------------|
| Core principles   | [01_core/principles.md](01_core/principles.md)                               |
| Quick reference   | [01_core/quick_reference.md](01_core/quick_reference.md)                     |
| Quick start guide | [02_guidelines/00_quick_start.md](02_guidelines/00_quick_start.md)           |
| Code standards    | [02_guidelines/02_code_style.md](02_guidelines/02_code_style.md)             |
| AI collaboration  | [02_guidelines/06_ai_collaboration.md](02_guidelines/06_ai_collaboration.md) |
| Python practices  | [02_guidelines/05_python.md](02_guidelines/05_python.md)                     |

---

## 📚 Knowledge Layers

### L0: Navigation (This File)

- Always loaded (~100 tokens)
- Entry point for all knowledge

### L1: Core Principles (`01_core/`)

| File                 | Content                                  | Tokens |
|----------------------|------------------------------------------|--------|
| `principles.md`      | Xin-Da-Ya philosophy, core values        | ~200   |
| `quick_reference.md` | 5 critical questions, autonomy quick ref | ~150   |
| `defaults.md`        | Default behaviors and calibration        | ~100   |

### L2: Guidelines (`02_guidelines/`)

| File                     | Content                                      | Tokens |
|--------------------------|----------------------------------------------|--------|
| `00_quick_start.md`      | 3-minute primer                              | ~60    |
| `01_planning_design.md`  | Planning + Architecture + SOLID              | ~150   |
| `02_code_style.md`       | Code style, naming, formatting               | ~200   |
| `03_engineering.md`      | Config, Testing, Performance, Change Control | ~250   |
| `04_documentation.md`    | Docs, comments, changelog, ADR               | ~150   |
| `05_python.md`           | Python + Type hints + Decorators + Async     | ~180   |
| `06_ai_collaboration.md` | Autonomy levels, execution modes             | ~300   |
| `07_cognitive.md`        | 5 questions, expert committee, biases        | ~200   |
| `08_quality.md`          | Quality metrics, review, testing strategy    | ~150   |
| `09_success.md`          | Xin-Da-Ya mapping, Shu-Fa-Dao                | ~150   |

### L3: Frameworks (`03_frameworks/`)

| Directory    | File                  | Content                                 |
|--------------|-----------------------|-----------------------------------------|
| `autonomy/`  | `levels.md`           | L1-L6 detailed definitions, calibration |
| `cognitive/` | `expert_committee.md` | Multi-expert analysis, scoring          |
| `timeout/`   | `hierarchy.md`        | 5-level timeout, fallback strategy      |

### L4: Practices (`04_practices/`)

| Directory           | File          | Content                                         |
|---------------------|---------------|-------------------------------------------------|
| `ai_collaboration/` | `workflow.md` | Daily workflow, handoff, reporting              |
| `engineering/`      | `patterns.md` | Repository, Service, Factory, Strategy patterns |

### L5: Tools (`05_tools/`)

| File                  | Content                          |
|-----------------------|----------------------------------|
| `timeout_manager.py`  | Timeout hierarchy implementation |
| `plugins/base.py`     | Plugin base class                |
| `plugins/registry.py` | Plugin registration system       |

### L6: Templates (`06_templates/`)

| File               | Content                                                  |
|--------------------|----------------------------------------------------------|
| `project_setup.md` | Thin layer config, pyproject.toml, README, Docker, CI/CD |

### L7: Scenarios (`07_scenarios/`)

| Directory         | File         | Content                                         |
|-------------------|--------------|-------------------------------------------------|
| `python_backend/` | `context.md` | FastAPI patterns, testing, autonomy calibration |

---

## 🔧 CLI Commands

```bash
# Core operations
aikb get                    # Get core principles
aikb get --layer 2          # Get guidelines layer
aikb guidelines code_style  # Get specific guideline

# Search
aikb search "autonomy"      # Search all knowledge
aikb search "pattern" -t 3  # Search with context

# Server
aikb serve                  # Start MCP server
aikb serve --port 8080      # Custom port

# Info
aikb info                   # Show KB structure
aikb version                # Show version
```

---

## ⏱️ Timeout Guarantees

| Level | Operation    | Timeout | Fallback        |
|-------|--------------|---------|-----------------|
| L0    | Cache lookup | 100ms   | Level 1         |
| L1    | File read    | 500ms   | Partial content |
| L2    | Layer load   | 2s      | Core only       |
| L3    | Full load    | 5s      | Emergency       |
| L4    | Emergency    | 10s     | Embedded        |

**Rule**: Always return something, never hang.

---

## 🎚️ Autonomy Quick Reference

```
L1: Minimal (0-20%)      ← Execute only explicit tasks, ask before every decision
L2: Low (20-40%)         ← Execute well-defined tasks, ask on implementation choices
L3: Medium (40-60%)      ← Complete tasks independently, ask for architectural changes
L4: Medium-High (60-80%) ← Proactive project partner, multi-task initiatives [DEFAULT]
L5: High (80-95%)        ← Strategic decisions, refactor architecture proactively
L6: Full (95-100%)       ← Autonomous agent, rarely recommended
```

---

## 📊 Statistics

| Metric              | Value  |
|---------------------|--------|
| Total Files         | 25+    |
| Guidelines Chapters | 10     |
| Framework Docs      | 3      |
| Practice Guides     | 2      |
| Templates           | 1      |
| Scenarios           | 1      |
| Total Lines         | ~4,000 |

---

*Version: 2.1.0 | Score: 100/100 | Experts: 24*
