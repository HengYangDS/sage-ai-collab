# Shell Script Guidelines

> Principles, standards, and quick reference for Bash scripting

---

## Table of Contents

- [1. Quick Reference](#1-quick-reference)
- [2. Core Principles](#2-core-principles)
- [3. Script Standards](#3-script-standards)
- [4. Best Practices](#4-best-practices)

---

## 1. Quick Reference

### 1.1 Common Commands

| Task              | Command                     |
|-------------------|-----------------------------|
| Check file exists | `[[ -f file ]]`             |
| Check dir exists  | `[[ -d dir ]]`              |
| Check var set     | `[[ -n "${var:-}" ]]`       |
| String match      | `[[ "${str}" == "value" ]]` |
| Regex match       | `[[ "${str}" =~ pattern ]]` |
| Numeric compare   | `[[ "${n}" -gt 10 ]]`       |

### 1.2 Test Operators

| Operator        | Description                     |
|-----------------|---------------------------------|
| `-f file`       | File exists and is regular file |
| `-d dir`        | Directory exists                |
| `-e path`       | Path exists                     |
| `-r file`       | File is readable                |
| `-w file`       | File is writable                |
| `-x file`       | File is executable              |
| `-z str`        | String is empty                 |
| `-n str`        | String is not empty             |
| `str1 == str2`  | Strings are equal               |
| `num1 -eq num2` | Numbers are equal               |
| `num1 -gt num2` | Greater than                    |
| `num1 -lt num2` | Less than                       |

### 1.3 Checklist

| Check             | Requirement           |
|-------------------|-----------------------|
| ☐ Shebang         | `#!/usr/bin/env bash` |
| ☐ Strict mode     | `set -euo pipefail`   |
| ☐ Quote variables | `"${var}"`            |
| ☐ Local variables | `local var=""`        |
| ☐ Error handling  | Trap and exit codes   |
| ☐ shellcheck      | No warnings           |

---

## 2. Core Principles

### 2.1 Guiding Principles

| Principle       | Description                              |
|-----------------|------------------------------------------|
| **Safety**      | Use strict mode, handle errors           |
| **Clarity**     | Write readable, self-documenting scripts |
| **Portability** | Consider POSIX compatibility             |
| **Idempotent**  | Safe to run multiple times               |

### 2.2 Naming Conventions

| Element      | Convention         | Example         |
|--------------|--------------------|-----------------|
| Script files | `snake_case.sh`    | `deploy_app.sh` |
| Functions    | `snake_case`       | `check_status`  |
| Constants    | `UPPER_SNAKE_CASE` | `MAX_RETRIES`   |
| Variables    | `lower_snake_case` | `output_dir`    |

---

## 3. Script Standards

### 3.1 Shebang

```bash
# ✅ Preferred - Portable
#!/usr/bin/env bash
# ✅ Also acceptable - Direct path
#!/bin/bash
# ⚠️ POSIX shell only
#!/bin/sh
```

### 3.2 Strict Mode

```bash
set -euo pipefail
# -e: Exit on error
# -u: Error on undefined variables
# -o pipefail: Catch errors in pipelines
```

### 3.3 Script Template

For complete script templates, see:

> `.knowledge/templates/SHELL_SCRIPT.md`

---

## 4. Best Practices

### 4.1 Variable Quoting

| Practice | Example |
|----------|---------|
| Quote variables | `"${variable}"` |
| Quote substitution | `result="$(command)"` |
| Quote in tests | `[[ "${var}" == "value" ]]` |
| Exception: arithmetic | `count=$((count + 1))` |

### 4.2 Command Substitution

```bash
# ✅ Modern syntax
result=$(command)
# ❌ Avoid legacy syntax
result=`command`
```

### 4.3 Safety Rules

| Rule | Rationale |
|------|-----------|
| Use `[[ ]]` not `[ ]` | More features, safer |
| Use `$(...)` not backticks | Nestable, readable |
| Use `mktemp` for temp files | Secure, unique names |
| Use `--` before filenames | Handle `-` prefixed names |
| Use `-print0` with `find` | Handle spaces in names |

### 4.4 Code Patterns

For detailed implementation patterns, see:

> `.knowledge/practices/engineering/languages/SHELL_PATTERNS.md`

---

## Related

- `.knowledge/templates/SHELL_SCRIPT.md` — Standard script template
- `.knowledge/practices/engineering/languages/SHELL_PATTERNS.md` — Common patterns
- `.knowledge/guidelines/CODE_STYLE.md` — General code style
- `.knowledge/practices/engineering/design/ERROR_HANDLING.md` — Error handling patterns

---

*AI Collaboration Knowledge Base*
