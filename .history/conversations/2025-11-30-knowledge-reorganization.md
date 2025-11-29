# Knowledge Reorganization - 2025-11-30

## Context

User requested analysis and execution of knowledge reorganization across the project's knowledge directories (`.context`, `content`, `docs`, `.history`), addressing four key questions:
1. What generic knowledge in `.context` should be moved to `content`
2. What project-specific knowledge in `content` should be moved to `.context`
3. What knowledge in `docs` should be consolidated
4. Why `.history` documents haven't been updated

## Key Decisions

### Decision 1: Generic Knowledge Migration (.context → content)

**Rationale**: `.context/intelligence/` contained reusable patterns mixed with project-specific data

**Actions**:
- Created `content/practices/engineering/common_pitfalls.md` (539 lines) - generic pitfalls guide
- Created `content/practices/ai_collaboration/interaction_patterns.md` (283 lines) - generic AI patterns
- Updated `.context/intelligence/common_pitfalls.md` to slim reference (88 lines) with SAGE-specific pitfalls only
- Updated `.context/intelligence/patterns.md` to slim reference (100 lines) with SAGE-specific calibration data only
- Kept `optimizations.md` and `performance_tuning.md` in `.context/` (SAGE-specific conventions)

### Decision 2: Project-Specific Content Migration (content → docs)

**Rationale**: `content/references/` contained SAGE-specific API documentation that doesn't belong in distributable content

**Actions**:
- Moved `content/references/mcp_api.md` → `docs/api/mcp_quick_ref.md`
- Moved `content/references/plugin_api.md` → `docs/api/plugin_quick_ref.md`
- Updated `docs/api/index.md` with new Quick References section

### Decision 3: Cross-References Between Design Docs and ADRs

**Rationale**: Design documents should reference their corresponding Architecture Decision Records

**Actions**:
- Updated `docs/design/01-architecture.md` with ADR references (0001, 0004, 0005, 0006)
- Updated `docs/design/02-sage-protocol.md` with ADR-0002 reference
- Updated `docs/design/04-timeout-loading.md` with ADR-0003 and timeout policy references

### Decision 4: Session History Activation

**Rationale**: `.history/` only contained example templates, no actual records were being created

**Actions**:
- Added Session History Management section to `.junie/guidelines.md` with:
  - Record type table
  - Session end checklist
  - Naming conventions
- Created `.history/_session-end-checklist.md` (143 lines) - detailed checklist template
- Created `.context/intelligence/session_automation_requirements.md` (247 lines) - long-term automation plan

## Outcomes

### Files Created
- `content/practices/engineering/common_pitfalls.md`
- `content/practices/ai_collaboration/interaction_patterns.md`
- `.history/_session-end-checklist.md`
- `.context/intelligence/session_automation_requirements.md`
- `.history/conversations/2025-11-30-knowledge-reorganization.md` (this file)

### Files Modified
- `.context/intelligence/common_pitfalls.md` (reduced from 541 to 88 lines)
- `.context/intelligence/patterns.md` (reduced from 277 to 100 lines)
- `docs/api/index.md` (added Quick References section)
- `docs/design/01-architecture.md` (added ADR references)
- `docs/design/02-sage-protocol.md` (added ADR reference)
- `docs/design/04-timeout-loading.md` (added ADR and policy references)
- `.junie/guidelines.md` (added Session History Management section)

### Files Moved
- `content/references/mcp_api.md` → `docs/api/mcp_quick_ref.md`
- `content/references/plugin_api.md` → `docs/api/plugin_quick_ref.md`

## Session Continuation: Configuration Verification

### Question 5: Configuration File Adjustments

**Analysis performed on configuration files:**

| Config File | Status | Notes |
|------------|--------|-------|
| `config/knowledge/content.yaml` | ✓ Valid | `references` directory still valid (2 files remain) |
| `config/knowledge/triggers.yaml` | ✓ Valid | No references to moved files |
| `config/knowledge/loading.yaml` | ✓ Valid | `always` list files exist |
| `config/sage.yaml` | ✓ Valid | Abstract paths, no direct file refs |

**Configuration Status**: All configuration files use abstract directory references (`content/references/`) rather than specific file paths. The `content/references/` directory still exists with `knowledge_quick_ref.md` and `performance_checklist.md`, so no configuration changes were needed.

### Broken Reference Fixes

**Found and fixed broken references to moved files:**

| File | Old Reference | New Reference |
|------|---------------|---------------|
| `content/scenarios/mcp_integration/context.md` | `content/references/mcp_api.md` | `docs/api/mcp_quick_ref.md` |
| `content/scenarios/plugin_development/context.md` | `content/references/plugin_api.md` | `docs/api/plugin_quick_ref.md` |

**Ignored references (historical/temporary):**
- `.history/conversations/2025-11-30-knowledge-reorganization.md` - Historical record
- `.outputs/*.py` - Temporary analysis scripts

---

## Learnings

1. **Knowledge Classification Principle**: 
   - `.context/` = Project-specific (ADRs, conventions, calibration data)
   - `content/` = Generic, distributable (patterns, practices, frameworks)
   - `docs/` = User-facing documentation (guides, API references)

2. **Session History Gap**: The `.history/` system was well-designed but lacked integration with AI collaboration workflows. Short-term solution is explicit instructions; long-term solution is automation via hooks and plugins.

3. **Cross-Reference Value**: Linking design docs to ADRs improves traceability and helps understand "why" behind designs.

## References

- `.junie/guidelines.md` — Updated AI collaboration guidelines
- `.history/index.md` — Session history structure
- `.context/intelligence/session_automation_requirements.md` — Automation roadmap
- `content/practices/ai_collaboration/interaction_patterns.md` — Generic AI patterns

---

## Session Continuation 2: Deep Optimization Iteration

### Context

User requested another iteration of knowledge reorganization optimization following the principles of high cohesion, low coupling, and reducing information redundancy.

### Decision 5: Further Intelligence File Refactoring

**Rationale**: `optimizations.md` (489 lines) and `performance_tuning.md` (391 lines) still contained significant generic content mixed with SAGE-specific data.

**Actions**:
- Refactored `.context/intelligence/optimizations.md`: 489 → 201 lines
  - Extracted generic code patterns to reference `content/practices/engineering/`
  - Kept SAGE-specific: import organization, test coverage goals, loading optimizations, common patterns (singleton, config, events), project shortcuts
- Refactored `.context/intelligence/performance_tuning.md`: 391 → 149 lines
  - Extracted generic performance patterns to reference `content/frameworks/performance/`
  - Kept SAGE-specific: performance goals with actual measurements, benchmarks (P50/P95/P99), monitoring thresholds, tuning checklist

### Decision 6: Index File Updates

**Rationale**: Index files needed updates to reflect reorganized content

**Actions**:
- Updated `.context/index.md`:
  - Added `session_automation_requirements.md` to intelligence section
  - Updated file count from 7 to 8
- Updated `content/index.md`:
  - Added References layer (2 files: `knowledge_quick_ref.md`, `performance_checklist.md`)
  - Updated total file count from ~114 to ~116
  - Added References section to Complete File List
- Updated `docs/index.md`:
  - Updated API file count from 4 to 6
  - Added `mcp_quick_ref.md` and `plugin_quick_ref.md` to API table

### Validation Results

**Cross-reference validation**:
- All references to old paths (`content/references/mcp_api.md`, `content/references/plugin_api.md`) only in historical/temporary files
- All new references in refactored files point to existing files:
  - `content/practices/engineering/patterns.md` ✓
  - `content/practices/engineering/testing_strategy.md` ✓
  - `content/frameworks/performance/optimization_strategies.md` ✓
  - `content/frameworks/performance/caching_patterns.md` ✓
  - `content/frameworks/performance/profiling_guide.md` ✓

**Session history status**:
- System is active: This conversation record exists as proof
- Templates still available for reference (prefixed with `_example-`)

### Summary of All Optimizations

| File | Before | After | Reduction |
|------|--------|-------|-----------|
| `.context/intelligence/common_pitfalls.md` | 541 | 88 | 84% |
| `.context/intelligence/patterns.md` | 277 | 100 | 64% |
| `.context/intelligence/optimizations.md` | 489 | 201 | 59% |
| `.context/intelligence/performance_tuning.md` | 391 | 149 | 62% |
| **Total** | **1698** | **538** | **68%** |

### Learnings (Iteration 2)

1. **Reference Pattern**: Slimmed `.context/intelligence/` files now follow consistent pattern:
   - Generic References table at top
   - SAGE-specific content only in body
   - Related section pointing to both generic and project-specific docs

2. **Index Maintenance**: After reorganization, all three index files (`.context/`, `content/`, `docs/`) need updates for file counts and listings.

3. **Validation Importance**: Cross-reference validation ensures no broken links after moves/refactors.

---

## Session Continuation 3: Rules Solidification

### Context

User requested "固化规则性的东西和知识" (Solidify rules and knowledge) - consolidating the rule-based patterns established during optimization sessions into permanent, referenceable guidelines.

### Decision 7: Guidelines Enhancement

**Rationale**: The `.junie/guidelines.md` was missing key rules established during recent optimization work.

**Actions**:
- Added new "📝 Documentation Standards" section with:
  - Document Format Rules table (header, TOC, sections, related, footer)
  - Knowledge Placement Rules table (where content types belong)
  - Index Maintenance Rules (steps after file changes)
- Added "Documentation Standards" reference to References section

### Rules Solidified

| Rule Category | Location | Content |
|---------------|----------|---------|
| **Document Format** | `.junie/guidelines.md` | Header, TOC, sections, related, footer rules |
| **Knowledge Placement** | `.junie/guidelines.md` | `.context/` vs `content/` vs `docs/` vs `.history/` |
| **Index Maintenance** | `.junie/guidelines.md` | Update counts, listings, cross-refs after changes |
| **Full Standards** | `DOCUMENTATION_STANDARDS.md` | Complete SSOT for documentation |

### Learnings (Iteration 3)

1. **Rule Consolidation**: Guidelines file should be the single entry point for all project rules, with references to detailed documents for specifics.

2. **Progressive Disclosure**: Keep guidelines concise with tables; link to full documentation for details.

3. **SSOT Pattern**: Rules established during sessions should be captured in permanent documentation, not just conversation records.

---

## Session Continuation 4: Token Efficiency Optimization

### Context

User requested deep optimization focusing on:
1. Identifying knowledge/norms that should be consolidated into `content/` as generic standards
2. Making `.junie/guidelines.md` reference generic standards instead of duplicating
3. Deep restructuring based on token efficiency and role clarity
4. Solidifying rules into appropriate locations

### Decision 8: Guidelines Deduplication

**Rationale**: `.junie/guidelines.md` contained duplicated content that exists in generic standards files.

**Actions**:
- Refactored Coding Standards section: 25 lines → 8 lines
  - Added references to `content/guidelines/python.md` and `.context/conventions/naming.md`
  - Kept quick summary for immediate reference
- Condensed Session History Management: 25 lines → 6 lines
  - Added reference to `.history/index.md` and `.history/_session-end-checklist.md`
- Condensed Expert Committee Pattern: 8 lines → 5 lines
  - Added reference to `content/frameworks/cognitive/expert_committee.md`
- Added reference to Timeout Hierarchy section
  - Linked to `.context/policies/timeout_hierarchy.md`

### Decision 9: Convention File Optimization

**Rationale**: `.context/conventions/naming.md` duplicated generic Python naming conventions.

**Actions**:
- Refactored `.context/conventions/naming.md`: 306 → 271 lines (12% reduction)
  - Replaced detailed Python conventions (sections 1-2) with reference to `content/guidelines/python.md`
  - Kept SAGE-specific principles and quick reference summary
  - Renumbered all sections (7 sections total now)

### Summary of Session 4 Optimizations

| File | Before | After | Reduction |
|------|--------|-------|-----------|
| `.junie/guidelines.md` (Coding Standards) | 25 lines | 8 lines | 68% |
| `.junie/guidelines.md` (Session History) | 25 lines | 6 lines | 76% |
| `.junie/guidelines.md` (Expert Committee) | 8 lines | 5 lines | 38% |
| `.context/conventions/naming.md` | 306 lines | 271 lines | 12% |

### Cumulative Optimization Results (All Sessions)

| Category | Files | Total Reduction |
|----------|-------|-----------------|
| `.context/intelligence/` | 4 files | 68% (1698 → 538 lines) |
| `.context/conventions/` | 1 file | 12% (306 → 271 lines) |
| `.junie/guidelines.md` | 1 file | ~20% in key sections |

### Learnings (Iteration 4)

1. **Reference-First Pattern**: Guidelines and convention files should reference generic standards rather than duplicating content, keeping only project-specific customizations and quick summaries inline.

2. **Token Efficiency Principle**: Each file should have a clear role - either be the source of truth for generic content (in `content/`) or reference it (in `.context/` and `.junie/`).

3. **Quick Summary Value**: Even when referencing external files, keeping a 2-3 line quick summary provides immediate value without context-switching.

4. **Audit Methodology**: Systematic audit of all directories (`.junie/`, `.context/`, `content/`, `docs/`) reveals duplication patterns that can be systematically addressed.

---

## Session Continuation 5: Session History Management Consolidation

### Context

User asked "session history management 难道不应该沉淀到 content?" (Shouldn't session history management be consolidated into content?) - questioning whether the session management practices in `.history/` should be generic reusable knowledge in `content/`.

### Analysis

**Found existing structure**:
- `content/practices/ai_collaboration/session_management.md` (321 lines) — Full session management practices ✓
- `content/templates/` — Session templates (conversation_record, session_state, task_handoff) ✓
- `.history/_session-end-checklist.md` (143 lines) — Workflow checklist with templates

**Issue identified**: `.history/_session-end-checklist.md` contained generic content (quality checks, cleanup actions, decision guide) that overlapped with but wasn't fully covered by `session_management.md`.

### Decision 10: Create Generic Session Checklist

**Rationale**: The checklist workflow pattern is generic and reusable across projects, separate from session management theory.

**Actions**:
- Created `content/practices/ai_collaboration/session_checklist.md` (159 lines)
  - Session Start checklist
  - During Session checklist  
  - Pre-Completion checks (work verification, quality, code review)
  - Session End checklist (documentation, cleanup, handoff)
  - Decision Guide (when to create which records)
  - Quick Reference Card

- Refactored `.history/_session-end-checklist.md`: 143 → 72 lines (50% reduction)
  - Now references generic checklist
  - Keeps only SAGE-specific additions (timeout levels, EventBus, DI)
  - Includes project paths and template locations

- Updated `content/practices/index.md`: Added session_checklist.md (7 → 8 files in AI Collaboration)

- Updated `.junie/guidelines.md` Session History section:
  - Now references generic checklist in `content/`
  - References project-specific checklist in `.history/`
  - Points to templates in `content/templates/`

### Knowledge Structure Clarified

| Content Type | Location | Example |
|--------------|----------|---------|
| **Generic practices** | `content/practices/ai_collaboration/` | `session_management.md`, `session_checklist.md` |
| **Generic templates** | `content/templates/` | `conversation_record.md`, `task_handoff.md` |
| **Project-specific config** | `.history/` | `_session-end-checklist.md` (SAGE additions) |
| **Instance data** | `.history/` | Actual conversation records, handoffs |

### Files Changed

| File | Action | Lines |
|------|--------|-------|
| `content/practices/ai_collaboration/session_checklist.md` | Created | 159 |
| `.history/_session-end-checklist.md` | Refactored | 143 → 72 |
| `content/practices/index.md` | Updated | +1 line |
| `.junie/guidelines.md` | Updated | ~4 lines |

### Learnings (Iteration 5)

1. **Checklist vs Practice**: Checklists (quick reference workflow) are distinct from practices (comprehensive guidance). Both are generic and belong in `content/`.

2. **Three-Layer Pattern for Session Management**:
   - Practices (`content/practices/`) — Theory and comprehensive guidance
   - Templates (`content/templates/`) — Document structure blueprints
   - Checklists (`content/practices/`) — Quick-reference workflows

3. **Instance vs Pattern**: `.history/` stores instance data (actual records) while `content/` stores patterns (how to create records).

---

## Session Continuation 6: Validation Audit

### Context

User requested to continue the optimization work. This iteration performed a comprehensive validation audit to verify all previous optimizations are complete and properly implemented.

### Audit Results

#### `.context/conventions/` Audit

| File | Status | Notes |
|------|--------|-------|
| `code_patterns.md` | ✓ Appropriate | SAGE-specific DI, EventBus, timeout patterns |
| `file_structure.md` | ✓ Appropriate | SAGE-specific directory layout and rules |
| `naming.md` | ✓ Optimized | References generic Python conventions |

#### `.context/policies/` Audit

| File | Status | Notes |
|------|--------|-------|
| `timeout_hierarchy.md` | ✓ Appropriate | SAGE T1-T5 levels, refs generic patterns |
| `loading_configurations.md` | ✓ Appropriate | SAGE-specific loading strategies |
| `memory_settings.md` | ✓ Appropriate | SAGE-specific cache/memory config |
| `plugin_settings.md` | ✓ Appropriate | SAGE plugin configuration |
| `runtime_settings.md` | ✓ Appropriate | SAGE runtime environment |
| `service_settings.md` | ✓ Appropriate | SAGE service layer config |

#### Cross-Reference Validation

- ✓ No broken references to old paths (`content/references/mcp_api.md`, `content/references/plugin_api.md`)
- ✓ All scenario context files updated with new paths
- ✓ Index files accurate

#### Directory Content Audit

| Directory | Status | Notes |
|-----------|--------|-------|
| `content/references/` | ✓ 2 files | Generic: `knowledge_quick_ref.md`, `performance_checklist.md` |
| `docs/guides/` | ✓ 9 files | User-facing SAGE documentation |
| `docs/api/` | ✓ 6 files | Includes migrated quick refs |

### Validation Summary

**All optimizations verified complete:**

1. **Knowledge Placement** — All content in appropriate directories
   - Generic → `content/`
   - Project-specific → `.context/`
   - User documentation → `docs/`
   - Session records → `.history/`

2. **Reference Pattern** — Project-specific files reference generic standards
   - `.context/intelligence/` files reference `content/practices/`
   - `.context/policies/timeout_hierarchy.md` references `content/frameworks/resilience/`
   - `.junie/guidelines.md` references all relevant generic standards

3. **No Remaining Issues** — Audit found no further optimization opportunities

### Final Statistics (All Sessions)

| Category | Optimization |
|----------|--------------|
| `.context/intelligence/` | 68% reduction (1698 → 538 lines) |
| `.context/conventions/naming.md` | 12% reduction |
| `.junie/guidelines.md` | ~20% reduction in key sections |
| `.history/_session-end-checklist.md` | 50% reduction |
| Files migrated | 2 (mcp_api, plugin_api) |
| Files created | 3 (interaction_patterns, common_pitfalls, session_checklist) |
| Cross-references fixed | 4 |

---

## Session Continuation 7: Session History Automation

### Context

User asked "上述流程如何能更自动化触发" (How can the above workflow be triggered more automatically) - requesting automation for the session history management workflow established in previous sessions.

### Analysis

**Current State**:
- Session automation requirements documented in `.context/intelligence/session_automation_requirements.md`
- No MCP tools implemented for session management
- No CLI commands for sessions
- Manual workflow only

**Options Evaluated**:
- **A**: Instruction enhancement only (no code)
- **B**: MCP tools implementation
- **C**: CLI commands implementation
- **D**: Hybrid approach (recommended) — Instructions + MCP tools

User selected **Option D: Hybrid Approach**.

### Decision 11: Implement Session Automation Tools

**Rationale**: MCP tools provide programmatic automation that AI can call automatically based on trigger rules, while enhanced instructions ensure consistent behavior.

**Actions**:

1. **Implemented 3 MCP Tools** in `src/sage/services/mcp_server.py`:

| Tool | Purpose | Parameters |
|------|---------|------------|
| `session_start` | Create session state file | `task`, `description`, `autonomy_level` |
| `session_end` | End session, create record | `summary`, `next_steps`, `record_type` |
| `session_status` | Check active sessions | (none) |

2. **Updated `list_tools()`** to include `session_tools` category

3. **Updated server startup message** to list session tools

4. **Added trigger rules** to `.junie/guidelines.md`:
   - Session Automation section with tool descriptions
   - Automatic trigger rules table (6 conditions)
   - Usage examples

### Implementation Details

**Tool Behavior**:
- `session_start`: Creates `.history/current/session-YYYYMMDD-HHMM.md` with task state template
- `session_end`: 
  - Auto-detects record type (conversation vs handoff) based on `next_steps`
  - Creates record in `.history/conversations/` or `.history/handoffs/`
  - Removes session state file after completion
- `session_status`: Returns active sessions and recent records

**Trigger Rules Added**:

| Trigger | Action |
|---------|--------|
| Complex task begins | `session_status()` → `session_start()` |
| Work completed | `session_end(summary)` |
| Work interrupted | `session_end(summary, next_steps="...")` |
| Resuming work | `session_status()` |

### Files Changed

| File | Action | Changes |
|------|--------|---------|
| `src/sage/services/mcp_server.py` | Modified | +329 lines (3 tools + category) |
| `.junie/guidelines.md` | Modified | +36 lines (automation section) |

### Learnings (Iteration 7)

1. **Tool-Based Automation**: MCP tools provide a middle ground between manual workflows and full automation - AI can call them based on rules without requiring complex event systems.

2. **Auto-Detection Pattern**: The `session_end` tool's auto-detection of record type (based on whether `next_steps` is provided) reduces decision burden while maintaining flexibility.

3. **Incremental Automation**: Phase 1 (semi-automated with tools) can be implemented quickly; full automation (Phase 2-3 with EventBus integration) can be added later.

---

*Session Duration: ~20 minutes (Iteration 7)*
*Total Session Duration: ~155 minutes*
*Part of SAGE Knowledge Base - Session History*
