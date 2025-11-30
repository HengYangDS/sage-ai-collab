# Technical Cases Repository

> Collection of problem-solving cases and lessons learned

---

## Table of Contents

- [Overview](#overview)
- [Case Index](#case-index)
- [Case Categories Reference](#case-categories-reference)
- [How to Add New Cases](#how-to-add-new-cases)

---

## Overview

This document records technical cases encountered during project development. Each case follows the structure defined in
`.knowledge/templates/CASE_STUDY.md`.

---

## Case Index

| ID                  | Title                                 | Category      | Date       | Status     |
|:--------------------|:--------------------------------------|:--------------|:-----------|:-----------|
| CASE-2025-11-30-001 | Root directory output file prevention | Convention    | 2025-11-30 | Resolved   |
| CASE-2025-11-29-001 | Output files in wrong directory       | Bug Fix       | 2025-11-29 | Resolved   |
| CASE-2025-11-29-002 | Knowledge consolidation initiative    | Documentation | 2025-11-29 | Resolved   |
| CASE-2025-11-29-003 | Layer terminology standardization     | Architecture  | 2025-11-29 | Resolved   |
| CASE-2025-11-29-004 | Configuration context refactoring     | Architecture  | 2025-11-29 | Resolved   |
| CASE-2025-11-29-005 | Test coverage gap analysis            | Engineering   | 2025-11-29 | Identified |

---

## CASE-2025-11-29-001

### Summary

| Field          | Value                                   |
|:---------------|:----------------------------------------|
| **Case ID**    | CASE-2025-11-29-001                     |
| **Title**      | Output files created in wrong directory |
| **Date**       | 2025-11-29                              |
| **Category**   | Bug Fix                                 |
| **Difficulty** | Simple                                  |
| **Time Spent** | 15 minutes                              |
| **Status**     | Resolved                                |

### Problem Description

The `build_knowledge_graph` MCP tool was creating output files (e.g., `test_graph.json`) in the current working
directory or user-specified path instead of the designated `.outputs/` directory.

**Expected Behavior**: Output files should be saved to `.outputs/` directory.

**Actual Behavior**: Files were saved to the path provided by the user directly.

### Root Cause

The `build_knowledge_graph` function in `mcp_server.py` directly used the `output_file` parameter without normalizing
the path to the `.outputs/` directory.

```python
# Original code
if output_file:
    builder.export_to_json(Path(output_file))
```

### Solution

Modified `src/sage/services/mcp_server.py` to:

1. Create `.outputs/` directory if it doesn't exist
2. Extract only the filename from user-provided path
3. Construct output path as `.outputs/{filename}`

```python
# Fixed code
if output_file:
    project_root = Path(__file__).parent.parent.parent.parent
    outputs_dir = project_root / ".outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    output_filename = Path(output_file).name
    output_path = outputs_dir / output_filename
    builder.export_to_json(output_path)
```

### Verification

- Ran unit tests: `pytest tests/unit/services/test_mcp_server.py::TestKnowledgeGraphTool -v`
- Verified `test_graph.json` was created in `.outputs/` directory

### Lessons Learned

| Takeaway                            | Action                                   |
|:------------------------------------|:-----------------------------------------|
| Output paths should be normalized   | Always use designated output directories |
| Create directories programmatically | Use `mkdir(parents=True, exist_ok=True)` |
| Document output locations           | Update docstrings with file locations    |

### Tags

`bug-fix` `mcp-tools` `file-output` `path-normalization`

---

## CASE-2025-11-29-002

### Summary

| Field          | Value                              |
|:---------------|:-----------------------------------|
| **Case ID**    | CASE-2025-11-29-002                |
| **Title**      | Knowledge consolidation initiative |
| **Date**       | 2025-11-29                         |
| **Category**   | Documentation                      |
| **Difficulty** | Medium                             |
| **Time Spent** | ~60 minutes                        |
| **Status**     | Resolved                           |

### Problem Description

User requested analysis of knowledge gaps in the SAGE Knowledge Base and implementation of recommended improvements.

**Request**: "What knowledge can be consolidated or supplemented"

### Analysis Results

After analyzing the project structure, identified the following areas for improvement:

| Category        | Gap                                  | Priority |
|:----------------|:-------------------------------------|:---------|
| Troubleshooting | No dedicated troubleshooting guide   | High     |
| Integration     | No integration patterns document     | High     |
| Security        | No security practices document       | Medium   |
| Migration       | No version migration guide           | Medium   |
| FAQ             | No FAQ document                      | Medium   |
| Configuration   | No comprehensive config guide        | Medium   |
| Tools           | No MCP tools guide                   | Medium   |
| Tools           | No Knowledge Graph guide             | Medium   |
| Cases           | No case study template or repository | Medium   |

### Solution

Created 10 new documentation files:

| File                                                  | Lines     | Purpose               |
|:------------------------------------------------------|:----------|:----------------------|
| `.knowledge/practices/engineering/TROUBLESHOOTING.md` | 451       | Troubleshooting guide |
| `.knowledge/frameworks/patterns/INTEGRATION.md`       | 574       | Integration patterns  |
| `.knowledge/practices/engineering/SECURITY.md`        | 592       | Security practices    |
| `docs/guides/MIGRATION.md`                            | 477       | Version migration     |
| `docs/guides/FAQ.md`                                  | 472       | FAQ                   |
| `.knowledge/templates/CASE_STUDY.md`                  | 231       | Case study template   |
| `docs/guides/CONFIGURATION.md`                        | 756       | Configuration guide   |
| `.knowledge/practices/engineering/KNOWLEDGE_GRAPH.md` | 562       | Knowledge graph guide |
| `docs/guides/MCP_TOOLS.md`                            | 861       | MCP tools guide       |
| `.context/intelligence/CASES.md`                      | This file | Cases repository      |

**Total**: ~5,000 lines of documentation added

### Lessons Learned

| Takeaway                                     | Action                                         |
|:---------------------------------------------|:-----------------------------------------------|
| Regular knowledge audits are valuable        | Schedule periodic KB reviews                   |
| Documentation gaps accumulate                | Address gaps proactively                       |
| Templates accelerate documentation           | Create templates for common doc types          |
| Case studies capture institutional knowledge | Record significant problem-solving experiences |

### Tags

`documentation` `knowledge-management` `knowledge-gaps` `best-practices`

---

## Case Categories Reference

| Category      | Description               |
|:--------------|:--------------------------|
| Bug Fix       | Fixing incorrect behavior |
| Performance   | Optimization issues       |
| Architecture  | Design-level issues       |
| Integration   | External system issues    |
| Configuration | Config-related issues     |
| Security      | Security vulnerabilities  |
| Documentation | Doc-related improvements  |

---

## CASE-2025-11-29-003

### Summary

| Field          | Value                             |
|:---------------|:----------------------------------|
| **Case ID**    | CASE-2025-11-29-003               |
| **Title**      | Layer terminology standardization |
| **Date**       | 2025-11-29                        |
| **Category**   | Architecture                      |
| **Difficulty** | Simple                            |
| **Time Spent** | 20 minutes                        |
| **Status**     | Resolved                          |

### Problem Description

Inconsistent terminology between documentation and codebase regarding the third architectural layer.

**Documentation**: `.junie/GUIDELINES.md` referred to "Core → Services → Tools"
**Codebase**: `src/sage/capabilities/` and README referred to "Capabilities Layer"

### Root Cause

Historical evolution of terminology without synchronization across all documentation files.

### Solution

Updated `.junie/GUIDELINES.md` Architecture Rules section:

- Changed "Tools" to "Capabilities" in the Three-Layer Model description
- Aligned with codebase directory structure and README

### Verification

- Grep search confirmed no remaining "Tools Layer" references in architecture documentation
- Cross-referenced with `src/sage/` directory structure

### Lessons Learned

| Takeaway                             | Action                                      |
|:-------------------------------------|:--------------------------------------------|
| Terminology drift occurs naturally   | Periodic terminology audits needed          |
| Single source of truth               | Code structure should drive doc terminology |
| Expert committee reviews catch drift | Use Level 5 reviews for consistency         |

### Tags

`architecture` `documentation` `terminology` `consistency`

---

## CASE-2025-11-29-004

### Summary

| Field          | Value                             |
|:---------------|:----------------------------------|
| **Case ID**    | CASE-2025-11-29-004               |
| **Title**      | Configuration context refactoring |
| **Date**       | 2025-11-29                        |
| **Category**   | Architecture                      |
| **Difficulty** | Medium                            |
| **Time Spent** | 45 minutes                        |
| **Status**     | Resolved                          |

### Problem Description

Semantic confusion between `.context/configurations/` (governance policies) and `config/` (runtime configuration).

**Issue**: Both directories dealt with "configuration" but served different purposes:

- `.context/configurations/`: Policy documents about how things should be configured
- `config/`: Actual runtime YAML configuration files

### Root Cause

Original naming didn't distinguish between "policy/governance" and "runtime settings".

### Solution

1. Renamed `.context/configurations/` to `.context/policies/`
2. Updated 16 files with cross-references:
    - `.context/INDEX.md` (comprehensive update)
    - `.junie/GUIDELINES.md`
    - `config/INDEX.md`
    - ADRs (ADR-0003, ADR-0007)
    - Content files in frameworks and practices
    - Intelligence documents

### Verification

- Verified all links work after rename
- Confirmed no broken references via grep search
- Directory structure reflects semantic intent

### Lessons Learned

| Takeaway                             | Action                                              |
|:-------------------------------------|:----------------------------------------------------|
| Names should reflect purpose         | Use "policies" for governance, "config" for runtime |
| Refactoring requires thorough search | Use grep to find all references before renaming     |
| Document the distinction             | Add clear descriptions in index files               |

### Tags

`architecture` `refactoring` `naming` `semantic-clarity`

---

## CASE-2025-11-29-005

### Summary

| Field          | Value                      |
|:---------------|:---------------------------|
| **Case ID**    | CASE-2025-11-29-005        |
| **Title**      | Test coverage gap analysis |
| **Date**       | 2025-11-29                 |
| **Category**   | Engineering                |
| **Difficulty** | Large                      |
| **Time Spent** | Ongoing                    |
| **Status**     | Identified                 |

### Problem Description

Level 5 Expert Committee identified significant asymmetry between source code implementation and test coverage.

### Analysis

| Source Module             | Implementation Files | Test Files | Gap    |
|:--------------------------|:---------------------|:-----------|:-------|
| `capabilities/analyzers/` | 3                    | 0          | 3      |
| `capabilities/checkers/`  | 1                    | 0          | 1      |
| `capabilities/monitors/`  | 1                    | 0          | 1      |
| `core/di/`                | 2                    | 0          | 2      |
| `core/events/`            | 4                    | 0          | 4      |
| `core/logging/`           | 3                    | 0          | 3      |
| `core/memory/`            | 3                    | 0          | 3      |
| **Total**                 | **17**               | **0**      | **17** |

### Root Cause

- Rapid initial development prioritized functionality over test coverage
- Test directory structure created but not populated
- No CI enforcement of coverage thresholds

### Proposed Solution

1. Create skeleton test files for all modules
2. Start with `core/` modules (foundational)
3. Add basic smoke tests for each class
4. Implement CI coverage gate (e.g., 60% minimum)

### Current Status

Identified and documented. Implementation planned as Phase 4 of optimization initiative.

### Tags

`testing` `coverage` `technical-debt` `engineering-practice`

---

## CASE-2025-11-30-001

### Summary

| Field          | Value                                 |
|:---------------|:--------------------------------------|
| **Case ID**    | CASE-2025-11-30-001                   |
| **Title**      | Root directory output file prevention |
| **Date**       | 2025-11-30                            |
| **Category**   | Convention                            |
| **Difficulty** | Simple                                |
| **Time Spent** | 30 minutes                            |
| **Status**     | Resolved                              |

### Problem Description

User discovered `.output.txt` file generated in project root directory instead of the designated `.outputs/` directory.
This was caused by external tools (MCP, Terminal) generating temporary output files without respecting project
conventions.

**Expected Behavior**: All output files should be generated in `.outputs/` directory.

**Actual Behavior**: Files like `.output.txt` were created in project root.

### Root Cause

1. External tools (MCP Desktop Commander, Terminal commands) may generate output files in the current working directory
   by default
2. No systematic documentation existed to guide tool usage regarding output file locations
3. `.gitignore` did not cover root-level output files as a safety measure

### Solution

Implemented a three-part systematic prevention:

**1. Updated `.gitignore`** (safety net):

```gitignore
# Root-level temporary output files (generated by external tools like MCP)
# These should be placed in .outputs/ instead
.output.txt
*.output.txt
output.txt
```

**2. Updated `.context/conventions/FILE_STRUCTURE.md`** (documentation):

- Added Section 1.4 "Output File Convention"
- Documented correct vs incorrect file locations
- Explained why this matters (4 reasons)
- Provided guidance for external tools

**3. Recorded case study** (knowledge capture):

- Added this case to `.context/intelligence/CASES.md`
- Ensures future reference and learning

### Verification

- Confirmed `.gitignore` rules added
- Confirmed documentation updated with clear conventions
- Verified `.outputs/` directory exists with `.gitkeep`

### Lessons Learned

| Takeaway                     | Action                                                      |
|:-----------------------------|:------------------------------------------------------------|
| External tools need guidance | Document output conventions explicitly                      |
| Defense in depth             | Use .gitignore as safety net + documentation                |
| Systematic prevention        | Don't just fix, establish conventions to prevent recurrence |
| Knowledge capture            | Record cases for future reference                           |

### Prevention Measures

For future development:

1. **When using external tools**: Always specify `.outputs/` as the output directory
2. **When creating new tools**: Default output path should be `.outputs/`
3. **Code review**: Check for hardcoded output paths in root directory

### Tags

`convention` `file-structure` `output-files` `prevention` `documentation`

---

## How to Add New Cases

1. Copy the case template structure from this file or `.knowledge/templates/CASE_STUDY.md`
2. Fill in all sections with details
3. Add entry to the Case Index table at the top
4. Add relevant tags for searchability
5. Update this file via PR or direct edit

---

## Related

- `.knowledge/templates/CASE_STUDY.md` — Case study template
- `.context/intelligence/calibration/PATTERNS.md` — Learned patterns
- `.context/intelligence/optimization/OPTIMIZATIONS.md` — Optimization history
- `.knowledge/practices/engineering/TROUBLESHOOTING.md` — Troubleshooting guide

---

*AI Collaboration Knowledge Base*
