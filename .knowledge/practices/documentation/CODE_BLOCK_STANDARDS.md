# Code Block Standards

> Single source of truth for code blocks, quote blocks, and callout standards

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Design Principles](#2-design-principles)
- [3. Code Blocks](#3-code-blocks)
- [4. Language Identifiers](#4-language-identifiers)
- [5. Code Content Guidelines](#5-code-content-guidelines)
- [6. Quote Blocks](#6-quote-blocks)
- [7. Callout Blocks](#7-callout-blocks)
- [8. Inline Code](#8-inline-code)
- [9. Anti-Patterns](#9-anti-patterns)
- [10. Troubleshooting](#10-troubleshooting)

---

## 1. Overview

| Element         | Purpose                          | Token Impact |
|-----------------|----------------------------------|--------------|
| **Code Block**  | Display code, commands, output   | High         |
| **Quote Block** | Highlight important information  | Medium       |
| **Callout**     | Draw attention to warnings/notes | Medium       |
| **Inline Code** | Reference code elements in text  | Low          |

### 1.1 Element Selection Guide

| Content Type      | Recommended Element            |
|-------------------|--------------------------------|
| Executable code   | Code block with language       |
| Terminal commands | Code block with `bash`/`shell` |
| Config files      | Code block with `yaml`/`json`  |
| API responses     | Code block with `json`         |
| File paths        | Inline code                    |
| Variable names    | Inline code                    |
| Important notes   | Quote block or callout         |
| Warnings          | Callout block                  |

---

## 2. Design Principles

Apply 信达雅 (Xin-Da-Ya) philosophy to code documentation.

**Priority**: 信 → 达 → 雅 (Faithfulness → Clarity → Elegance)

### 2.1 信 (Faithfulness) — Correct Code

| Checkpoint       | Requirement                         |
|------------------|-------------------------------------|
| **Correctness**  | Code must be syntactically valid    |
| **Completeness** | Include necessary context (imports) |
| **Testability**  | Examples should be runnable         |
| **Currency**     | Code matches current API/syntax     |

### 2.2 达 (Clarity) — Clear Purpose

| Checkpoint       | Requirement                  |
|------------------|------------------------------|
| **Purpose**      | Clear what code demonstrates |
| **Comments**     | Explain non-obvious logic    |
| **Structure**    | Logical organization         |
| **Highlighting** | Correct language for syntax  |

### 2.3 雅 (Elegance) — Minimal Examples

| Checkpoint      | Requirement                |
|-----------------|----------------------------|
| **Minimalism**  | Show only what's necessary |
| **Readability** | Consistent formatting      |
| **Focus**       | One concept per example    |
| **Length**      | Appropriate size           |

### 2.4 Design Checklist

Before finalizing code blocks:

1. **信**: Does the code actually work?
2. **达**: Will readers understand what it does?
3. **雅**: Is this the minimal example needed?

---

## 3. Code Blocks

### 3.1 Size Guidelines

| Metric    | Recommended | Maximum   |
|-----------|-------------|-----------|
| Lines     | 5-25        | 50        |
| Width     | 80 chars    | 100 chars |
| Functions | 1-2         | 3         |
| Concepts  | 1           | 2         |

### 3.2 Code Block Types

| Type           | Use Case              | Language ID            |
|----------------|-----------------------|------------------------|
| Source code    | Implementation        | `python`, `javascript` |
| Shell commands | Terminal instructions | `bash`, `shell`        |
| Configuration  | Config files          | `yaml`, `json`, `toml` |
| Output         | Command output        | `text`, `console`      |
| Data           | Data structures       | `json`, `xml`          |
| Diff           | Code changes          | `diff`                 |

---

## 4. Language Identifiers

### 4.1 Common Languages

| Category      | Languages              | Identifiers                            |
|---------------|------------------------|----------------------------------------|
| **Systems**   | C, C++, Rust, Go       | `c`, `cpp`, `rust`, `go`               |
| **Scripting** | Python, Ruby           | `python`, `ruby`                       |
| **Web**       | JavaScript, TypeScript | `js`, `ts`, `javascript`, `typescript` |
| **Data**      | SQL, JSON, YAML        | `sql`, `json`, `yaml`                  |
| **Shell**     | Bash, PowerShell       | `bash`, `powershell`                   |
| **Config**    | TOML, INI              | `toml`, `ini`                          |
| **Docs**      | Markdown               | `markdown`, `md`                       |

### 4.2 Special Identifiers

| Use Case       | Identifier | Notes             |
|----------------|------------|-------------------|
| Diff/patch     | `diff`     | Shows +/-         |
| Console output | `console`  | Commands + output |
| Plain text     | `text`     | No highlighting   |
| Mermaid        | `mermaid`  | Diagrams          |

### 4.3 Diff Example

```diff
- old_function()  # Removed
+ new_function()  # Added
  unchanged_line()
```
### 4.4 Console Example

```console
$ python --version
Python 3.11.0
$ pip install requests
Successfully installed requests-2.28.0
```
---

## 5. Code Content Guidelines

### 5.1 Example Structure

**Recommended pattern**:

1. Brief description of what code does
2. Code block with language
3. Output comment or explanation

```python
# Calculate sum of list
result = sum([1, 2, 3, 4, 5])
print(result)  # Output: 15
```
### 5.2 Comment Guidelines

| Comment Type | When to Use          | Example                 |
|--------------|----------------------|-------------------------|
| **Purpose**  | Start of example     | `# Calculate user age`  |
| **Output**   | After print/return   | `# Output: 42`          |
| **Warning**  | Non-obvious gotchas  | `# Note: Blocks thread` |
| **Step**     | Multi-step processes | `# Step 1: Initialize`  |

### 5.3 Input/Output Convention

Always show expected output:

```python
# Input
data = [1, 2, 3, 4, 5]

# Processing
result = sum(data)

# Output
print(result)  # Output: 15
```
### 5.4 Error Examples

Show error handling:

```python
# ❌ This raises an error
try:
    result = 1 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")  # Output: Error: division by zero
```
### 5.5 Multi-File Examples

Use headers for multi-file:

**`config.yaml`**:

```yaml
database:
  host: localhost
  port: 5432
```
**`app.py`**:

```python
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)
```
---

## 6. Quote Blocks

### 6.1 Quote Block Types

| Type           | Purpose         | Example                  |
|----------------|-----------------|--------------------------|
| **Definition** | Define terms    | `> **Term**: Definition` |
| **Note**       | Additional info | `> **Note**: Detail`     |
| **Citation**   | External quotes | `> "Quote" — Author`     |
| **Summary**    | Key takeaways   | `> **Summary**: Points`  |

### 6.2 Common Patterns

| Pattern              | Syntax                                         | Notes                    |
|----------------------|------------------------------------------------|--------------------------|
| Document purpose     | `> Single-line purpose statement`              | After `# Title`          |
| Nested quote         | `> > Level 2 nested`                           | Use sparingly, max 2     |
| Quote with author    | `> "Quote text"` + `>` + `> — Author`          | Blank `>` line before    |

---

## 7. Callout Blocks

### 7.1 Standard Types

| Type          | Purpose                | Icon |
|---------------|------------------------|------|
| **Note**      | Additional information | ℹ️   |
| **Tip**       | Helpful suggestion     | 💡   |
| **Warning**   | Caution required       | ⚠️   |
| **Danger**    | Critical warning       | 🚫   |
| **Important** | Must-know info         | ❗    |

### 7.2 Syntax Options

| Type      | GitHub/GitLab Syntax | Alternative (fallback)    |
|-----------|----------------------|---------------------------|
| Note      | `> [!NOTE]`          | `> **Note**: ...`         |
| Tip       | `> [!TIP]`           | `> **💡 Tip**: ...`       |
| Warning   | `> [!WARNING]`       | `> **⚠️ Warning**: ...`   |
| Caution   | `> [!CAUTION]`       | `> **⚠️ Caution**: ...`   |
| Important | `> [!IMPORTANT]`     | `> **Important**: ...`    |

### 7.3 Best Practices

| Guideline     | Recommendation            |
|---------------|---------------------------|
| **Frequency** | Max 2-3 per section       |
| **Length**    | 1-3 sentences             |
| **Placement** | Before relevant content   |
| **Selection** | Match severity to content |

---

## 8. Inline Code

### 8.1 When to Use

| Use Case       | Example                   |
|----------------|---------------------------|
| Variable names | The `user_id` parameter   |
| Function names | Call `getData()`          |
| File names     | Edit `config.yaml`        |
| Command names  | Run `npm install`         |
| Code snippets  | Returns `true` or `false` |
| Key names      | Press `Ctrl+C`            |
| Values         | Set to `null`             |

### 8.2 When NOT to Use

| Avoid         | Use Instead                       |
|---------------|-----------------------------------|
| Emphasis      | **bold** or *italic*              |
| Product names | Plain text (Python, not `Python`) |
| Concept names | Plain text (REST API)             |
| URLs          | Markdown links                    |

### 8.3 Special Cases

| Situation          | Solution                               | Example                    |
|--------------------|----------------------------------------|----------------------------|
| Include backticks  | Use double backticks with spaces       | ``` `` `code` `` ```       |
| Long expression    | Use code block instead                 | Avoid `long...expression`  |
| Multiple elements  | Separate with commas or use code block | `a`, `b`, `c` or code block |

---

## 9. Anti-Patterns

### 9.1 Code Block Anti-Patterns

| Anti-Pattern   | Problem         | Solution                 |
|----------------|-----------------|--------------------------|
| No language ID | No highlighting | Always specify           |
| Too long       | Overwhelming    | Break into smaller       |
| Incomplete     | Missing imports | Include all needed       |
| Untested       | May have errors | Test all examples        |
| Over-commented | Distracting     | Comment non-obvious only |

### 9.2 Quote Block Anti-Patterns

| Anti-Pattern    | Problem           | Solution              |
|-----------------|-------------------|-----------------------|
| Overuse         | Diminished impact | Reserve for important |
| Too long        | Lost emphasis     | 1-3 sentences         |
| Nested too deep | Hard to read      | Max 2 levels          |
| No purpose      | Confusion         | Indicate why quoted   |

### 9.3 Inline Code Anti-Patterns

| Anti-Pattern     | Problem           | Solution            |
|------------------|-------------------|---------------------|
| Overuse          | Visual noise      | Only for code       |
| Product names    | Incorrect styling | Plain text          |
| Long expressions | Hard to read      | Use code block      |
| Formatting abuse | Confusing         | Use proper emphasis |

---

## 10. Troubleshooting

### 10.1 Common Issues

| Issue                  | Cause               | Fix                  |
|------------------------|---------------------|----------------------|
| No syntax highlighting | Missing language ID | Add identifier       |
| Code runs off screen   | Lines too long      | Wrap or shorten      |
| Backticks showing      | Unclosed fences     | Check matching ```   |
| Quote not formatting   | Missing `>`         | Add `>` to all lines |

### 10.2 Escaping Code Fences

To show code fences in documentation, wrap with 4+ backticks: `` ````` `` wraps `` ```` `` wraps `` ``` ``.

### 10.3 Validation Checklist

| Element     | Check                                                            |
|-------------|------------------------------------------------------------------|
| Code Block  | Language ID specified, code valid, examples runnable             |
| Quote Block | Every line starts with `>`, purpose clear, content concise       |
| Inline Code | Used only for code elements, backticks properly closed           |

---

## Related

- `.knowledge/practices/documentation/INDEX.md` — Documentation practices index
- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Document format standards
- `.knowledge/practices/documentation/DIAGRAM_STANDARDS.md` — Diagram standards
- `.knowledge/practices/documentation/TABLE_STANDARDS.md` — Table standards
- `.knowledge/guidelines/DOCUMENTATION.md` — Documentation guidelines

---

*AI Collaboration Knowledge Base*
