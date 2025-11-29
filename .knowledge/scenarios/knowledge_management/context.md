# Knowledge Management Scenario Context

> Pre-configured context for knowledge management system development

---

## Table of Contents

- [1. Scenario Profile](#1-scenario-profile)
- [2. Relevant Knowledge](#2-relevant-knowledge)
- [3. Project Structure](#3-project-structure)
- [4. Knowledge Architecture](#4-knowledge-architecture)
- [5. Content Patterns](#5-content-patterns)
- [6. Common Tasks](#6-common-tasks)
- [7. Autonomy Calibration](#7-autonomy-calibration)
- [8. Quick Commands](#8-quick-commands)

---

## 1. Scenario Profile

```yaml
scenario: knowledge_management
languages: [ markdown, yaml, python ]
tools: [ sage, mkdocs, sphinx, obsidian ]
focus: [ content-organization, taxonomy, search, ai-integration ]
autonomy_default: L3
```

---

## 2. Relevant Knowledge

| Priority      | Files                                                                                                                                                                                    |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Auto-Load** | `core/principles.md` · `.knowledge/references/knowledge_quick_ref.md`                                                                                                                    |
| **On-Demand** | `practices/documentation/knowledge_organization.md` · `frameworks/design/` · `practices/documentation/documentation_standards.md` · `practices/ai_collaboration/knowledge_extraction.md` |

---

## 3. Project Structure

| Directory     | Purpose                      |
|---------------|------------------------------|
| `.knowledge/` | Generic, reusable knowledge  |
| `.context/`   | Project-specific knowledge   |
| `docs/`       | User-facing documentation    |
| `config/`     | Configuration files          |
| `.history/`   | Session history and handoffs |
| `templates/`  | Document templates           |
| `schemas/`    | Content validation schemas   |

---

## 4. Knowledge Architecture

### 4.1 Layer Model

```
┌─────────────────────────────────────┐
│           Core Layer                │  ← Fundamental concepts
│    (Principles, Concepts)           │     Always loaded first
├─────────────────────────────────────┤
│         Guidelines Layer            │  ← Standards & rules
│    (Standards, Conventions)         │     High priority
├─────────────────────────────────────┤
│        Frameworks Layer             │  ← Patterns & structures
│    (Patterns, Architectures)        │     Medium priority
├─────────────────────────────────────┤
│         Practices Layer             │  ← Implementation guides
│    (How-tos, Workflows)             │     On-demand loading
└─────────────────────────────────────┘
```

### 4.2 Content Types

| Type          | Purpose                     | Format                            |
|---------------|-----------------------------|-----------------------------------|
| **Principle** | Fundamental truth or belief | Declarative statement             |
| **Concept**   | Abstract idea or notion     | Definition + examples             |
| **Guideline** | Recommended practice        | Rule + rationale                  |
| **Pattern**   | Reusable solution           | Problem → Solution → Consequences |
| **Practice**  | Step-by-step guide          | Procedure + tips                  |
| **Reference** | Lookup information          | Tables, lists                     |

### 4.3 Metadata Schema

```yaml
# Standard frontmatter
---
title: Document Title
layer: core | guidelines | frameworks | practices
tags: [ tag1, tag2, tag3 ]
priority: 1-5
auto_load: true | false
tokens: ~500
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: Name or AI
---
```

---

## 5. Content Patterns

### 5.1 Document Template

```markdown
# Title

> One-line description

---

## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)

---

## Section 1

### 1.1 Subsection

Content...

---

## Related

- Related doc 1
- Related doc 2

---

*Part of [Knowledge Base Name]*
```

### 5.2 Index Pattern

<!-- Example template - replace placeholder links with actual document paths -->

```markdown
# Category Index

> Navigation for [category] knowledge

---

## Quick Links

| Document | Purpose | Tokens |
|----------|---------|--------|
| [Doc 1](#) | Description | ~200 |  <!-- Replace # with actual path -->
| [Doc 2](#) | Description | ~300 |  <!-- Replace # with actual path -->

---

## By Topic

### Topic A

- Document 1
- Document 2

### Topic B

- Document 3

---

*Index for [Knowledge Base Name]*
```

### 5.3 Cross-Reference Pattern

```markdown
## References

### Internal

- `.knowledge/core/principles.md` — Core principles
- `.knowledge/practices/workflow.md` — Implementation guide

### External

- [External Resource](https://example.com) — Description

### Related Decisions

- ADR-0001: Architecture decision
```

---

## 6. Common Tasks

| Task                        | Steps                                                        |
|-----------------------------|--------------------------------------------------------------|
| **Add knowledge content**   | Choose layer → Create file → Add metadata → Link in index    |
| **Reorganize structure**    | Analyze current → Plan changes → Update links → Verify       |
| **Create taxonomy**         | Identify concepts → Define hierarchy → Apply tags → Document |
| **Improve discoverability** | Add metadata → Create indexes → Enhance cross-refs           |
| **Integrate with AI**       | Define context → Configure loading → Test retrieval          |
| **Quality audit**           | Check completeness → Verify links → Validate format          |

### 6.1 Adding New Knowledge

```bash
# 1. Create content file
touch .knowledge/practices/new_topic/guide.md

# 2. Add content with metadata
# (Use standard template)

# 3. Update layer index
# Edit .knowledge/practices/index.md

# 4. Verify integration
sage search "new topic"
```

### 6.2 Knowledge Extraction Workflow

```
1. Source Identification
   └── Identify knowledge source (docs, code, conversations)

2. Content Extraction
   └── Extract key information
   └── Identify patterns and principles

3. Structuring
   └── Choose appropriate layer
   └── Apply document template
   └── Add metadata

4. Integration
   └── Link to related content
   └── Update indexes
   └── Verify searchability

5. Validation
   └── Review for accuracy
   └── Check for completeness
   └── Test AI retrieval
```

---

## 7. Autonomy Calibration

| Task Type              | Level | Notes                 |
|------------------------|-------|-----------------------|
| Fix typos in content   | L5    | Low risk, routine     |
| Add new content file   | L3-L4 | Follow templates      |
| Reorganize structure   | L2-L3 | May affect navigation |
| Change taxonomy        | L2    | Cross-cutting impact  |
| Modify metadata schema | L1-L2 | Affects all content   |
| Update core principles | L1    | Fundamental changes   |
| Create new layer       | L1    | Architecture decision |

---

## 8. Quick Commands

| Category       | Commands                                                |
|----------------|---------------------------------------------------------|
| **Search**     | `sage search "query"` · `grep -r "pattern" .knowledge/` |
| **Validate**   | `sage validate --all` · `markdownlint .knowledge/`      |
| **Index**      | `sage index --rebuild` · `find content -name "*.md"`    |
| **Statistics** | `sage info --layers` · `wc -l .knowledge/**/*.md`       |

---

## Best Practices

### Content Organization

| Practice                    | Description                    |
|-----------------------------|--------------------------------|
| **Single Responsibility**   | Each document covers one topic |
| **Appropriate Granularity** | Not too broad, not too narrow  |
| **Consistent Naming**       | Follow naming conventions      |
| **Rich Metadata**           | Enable discovery and filtering |
| **Cross-References**        | Connect related content        |

### Knowledge Quality

| Dimension           | Criteria                      |
|---------------------|-------------------------------|
| **Accuracy**        | Factually correct, up-to-date |
| **Completeness**    | Covers topic adequately       |
| **Clarity**         | Easy to understand            |
| **Consistency**     | Follows standards             |
| **Discoverability** | Easy to find                  |

### AI Integration

| Aspect                | Consideration                          |
|-----------------------|----------------------------------------|
| **Token Budget**      | Estimate and document token count      |
| **Loading Priority**  | Set appropriate auto_load flags        |
| **Context Relevance** | Tag content for scenario-based loading |
| **Chunking**          | Structure for partial retrieval        |

---

## Related

- `.knowledge/practices/documentation/knowledge_organization.md` — Organization patterns
- `.knowledge/practices/documentation/documentation_standards.md` — Documentation standards (SSOT)
- `.knowledge/practices/ai_collaboration/knowledge_capture.md` — Extraction techniques
- `.knowledge/frameworks/design/index.md` — Design patterns

---

*Part of SAGE Knowledge Base*
