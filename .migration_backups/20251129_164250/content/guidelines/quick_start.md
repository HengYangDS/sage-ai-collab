# Quick Start Guide

> **Load Time**: Always available (~60 tokens)  
> **Purpose**: Get productive in 3 minutes

---

## 🚀 30-Second Summary

**AI Collaboration KB** provides knowledge for human-AI collaboration:

1. **Core Principles** (01_core/) - Always loaded, ~500 tokens
2. **Guidelines** (02_guidelines/) - 10 chapters, load on demand
3. **Frameworks** (03_frameworks/) - Deep theory for complex tasks
4. **Tools** (05_tools/) - CLI, MCP server, plugins

---

## ⚡ Quick Commands

```bash
# Get core principles
sage get

# Get specific guidelines
sage guidelines code_style
sage guidelines ai_collaboration

# Search knowledge
sage search "autonomy levels"

# Start MCP server
sage serve
```

---

## 🎯 Core Philosophy

### Xin-Da-Ya (信达雅)

- **信 (Xin)**: Faithfulness - accurate, reliable
- **达 (Da)**: Clarity - clear, maintainable
- **雅 (Ya)**: Elegance - refined, balanced

### 5 Critical Questions

1. What am I assuming?
2. What could go wrong?
3. Is there a simpler way?
4. What will future maintainers need?
5. How does this fit the bigger picture?

---

## 🎚️ Autonomy Levels (Quick Ref)

| Level | Name                 | When to Use                               |
|-------|----------------------|-------------------------------------------|
| L1    | Minimal (0-20%)      | Critical/unfamiliar tasks, onboarding     |
| L2    | Low (20-40%)         | New project phases, learning codebase     |
| L3    | Medium (40-60%)      | Routine development, clear guidelines     |
| L4    | Medium-High (60-80%) | Mature collaboration, proactive partner ⭐ |
| L5    | High (80-95%)        | Strategic partnership, trusted systems    |
| L6    | Full (95-100%)       | Autonomous agent (rarely recommended)     |

**Default**: Start at L4 for mature collaboration, L2-L3 for new projects.

---

## 📚 Guidelines Overview (10 Chapters)

| #  | Chapter           | Focus                        |
|----|-------------------|------------------------------|
| 00 | Quick Start       | This guide                   |
| 01 | Planning & Design | Architecture, modularity     |
| 02 | Code Style        | Formatting, naming           |
| 03 | Engineering       | Config, testing, performance |
| 04 | Documentation     | Standards, templates         |
| 05 | Python            | Python-specific practices    |
| 06 | AI Collaboration  | Human-AI interaction         |
| 07 | Cognitive         | Enhancement frameworks       |
| 08 | Quality           | Quality assurance            |
| 09 | Success           | Philosophy mapping           |

---

## ⏱️ Timeout Guarantees

| Operation | Timeout | Fallback  |
|-----------|---------|-----------|
| Cache     | 100ms   | Embedded  |
| File      | 500ms   | Partial   |
| Layer     | 2s      | Core only |
| Full      | 5s      | Emergency |

**Rule**: Always returns something, never hangs.

---

## 🔗 Next Steps

1. **Explore**: `sage info` - See full KB structure
2. **Search**: `sage search "<topic>"` - Find specific content
3. **Deep Dive**: `sage framework autonomy` - Load frameworks

---

*Version 0.1.0 | Score: 100/100 | 24 Experts*
