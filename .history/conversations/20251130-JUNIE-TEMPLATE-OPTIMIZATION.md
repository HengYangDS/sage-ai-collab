# Junie Template System Optimization

> **Date**: 2025-11-30
> **Type**: Optimization & Knowledge Capture
> **Status**: Completed

---

## Summary

Comprehensive optimization of the `.junie/` thin layer template system across multiple iterations, culminating in a
clean separation between generic (reusable) and project-specific content.

---

## Optimization Journey

### Phase 1: Initial Review & Analysis

**Identified Issues**:

- `GUIDELINES.md` contained both generic and project-specific content
- No clear separation between reusable and customizable files
- MCP config had hardcoded paths

**Initial Structure**:

```
.junie/
├── GUIDELINES.md    (mixed content)
└── mcp/
    └── mcp.json     (hardcoded paths)
```

### Phase 2: Content Extraction & Generalization

**Actions**:

1. Extracted project variables into `project.yaml`
2. Created `config.yaml` for Junie settings
3. Created `QUICKREF.md` for quick reference
4. Optimized MCP config with environment variables

**Intermediate Structure**:

```
.junie/
├── GUIDELINES.md
├── config.yaml
├── QUICKREF.md
├── project.yaml
├── PROJECT-GUIDELINES.md
└── mcp/
    └── mcp.json
```

### Phase 3: Directory Reorganization (Final)

**Goal**: Clear physical separation of generic vs project-specific files.

**Final Structure**:

```
.junie/
├── GUIDELINES.md           # 🔄 Main entry point
├── README.md               # 🔄 Directory documentation
│
├── generic/                # 🔄 Reusable settings
│   ├── config.yaml         # Junie settings
│   └── QUICKREF.md         # Quick reference card
│
├── mcp/                    # 🔄 MCP configuration
│   └── mcp.json            # MCP servers definition
│
├── configuration/          # 🔄 Configuration guides
│   ├── README.md
│   ├── 01-introduction.EN.md
│   ├── 02-action-allowlist.EN.md
│   ├── 03-mcp-integration.EN.md
│   ├── 04-future-vision.EN.md
│   └── 05-appendix.EN.md
│
└── project/                # 📌 Project-specific (customize)
    ├── config.yaml         # Project variables
    └── QUICKREF.md         # Project quick reference
```

---

## Key Decisions

| Decision                          | Rationale                                |
|-----------------------------------|------------------------------------------|
| `GUIDELINES.md` at root           | Main entry point, Junie reads this first |
| `generic/` subdirectory           | Clear grouping of reusable settings      |
| `project/` subdirectory           | Isolates customization needs             |
| `configuration/` at root          | MCP requirement for config path          |
| No project names in generic files | Ensures true reusability                 |

---

## Lessons Learned

### 1. Thin Layer Principle

Keep `.junie/` minimal—delegate detailed knowledge to `.context/` and `.knowledge/`.

### 2. Variable Centralization

All project-specific values in one file (`project/config.yaml`) prevents duplication and inconsistency.

### 3. Physical Separation > Comments

Putting generic and project files in separate directories is clearer than just marking them with comments.

### 4. Iterative Refinement

Three phases of optimization were needed to reach the optimal structure. Initial designs rarely capture all
requirements.

### 5. Cross-Reference Consistency

When restructuring, update ALL references (GUIDELINES.md, README.md, index files, knowledge docs).

---

## File Classification Guide

### Generic Files (🔄) — Copy without changes

| File                  | Purpose                 | Lines  |
|-----------------------|-------------------------|--------|
| `GUIDELINES.md`       | AI collaboration rules  | ~243   |
| `README.md`           | Directory documentation | ~100   |
| `generic/config.yaml` | Junie settings          | ~104   |
| `generic/QUICKREF.md` | Quick reference         | ~98    |
| `mcp/mcp.json`        | MCP servers             | ~72    |
| `configuration/*.md`  | Configuration guides    | varies |

### Project Files (📌) — Must customize

| File                  | Purpose           | Customization           |
|-----------------------|-------------------|-------------------------|
| `project/config.yaml` | Project variables | Name, stack, commands   |
| `project/QUICKREF.md` | Project reference | Paths, tips, philosophy |

---

## Artifacts Created

### Knowledge Documents

- `.knowledge/practices/ai_collaboration/JUNIE_CONFIGURATION_TEMPLATE.md` — Comprehensive template guide

### Session Records

- This file — Optimization journey and lessons learned

### Updated Files

- `.knowledge/practices/INDEX.md` — Added template reference
- `.context/INDEX.md` — Updated if needed

---

## Reusability Checklist

For new projects, copy `.junie/` and:

1. ☐ Edit `project/config.yaml` with project info
2. ☐ Edit `project/QUICKREF.md` with project specifics
3. ☐ Keep all other files unchanged
4. ☐ Optionally create `.context/` for project knowledge
5. ☐ Optionally create `.history/` for session tracking

---

## Related

- `2025-11-30-KNOWLEDGE-REORGANIZATION.md` — Main session record (this is Iteration 9)
- `.knowledge/practices/ai_collaboration/JUNIE_CONFIGURATION_TEMPLATE.md` — Full template documentation
- `.junie/GUIDELINES.md` — Main entry point
- `.context/INDEX.md` — Project context navigation

---

*Session record for SAGE Knowledge Base — 2025-11-30*
*AI Collaboration Knowledge Base*
