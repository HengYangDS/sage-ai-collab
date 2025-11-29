# Action Allowlist Configuration

> Configure 87 Terminal rules for 90%+ automatic command approval (~30 min)

---

## Overview

**Action Allowlist** is Junie's permission management mechanism that controls which operations can be executed automatically without manual approval.

### Goals

| Target                 | Value                   | Effect                        |
|:-----------------------|:------------------------|:------------------------------|
| **Terminal Rules**     | 87 precise rules        | 90%+ auto-approval rate       |
| **Execution Mode**     | Batch execution         | Continuous collaboration      |
| **Security**           | Dangerous char exclusion| Balance security & efficiency |

### Key Benefits

- ⚡ **90%+ reduction** in manual approvals
- 🔒 **Secure** — regex rules exclude dangerous operations
- 🎯 **Precise** — 87 rules covering 13 major scenarios

---

## Action Allowlist Mechanism

### Security Classification

| Category            | Description                              | Example                    |
|:--------------------|:-----------------------------------------|:---------------------------|
| **Safe Actions**    | Reversible, no sensitive changes         | Editing code, reading files|
| **Sensitive Actions**| Potential risks, require permission     | Terminal commands, builds  |

### Rule Types

| Rule Type               | Function                    | Status      |
|:------------------------|:----------------------------|:------------|
| **Terminal**            | Allow terminal commands     | ✅ 87 rules  |
| **RunTest**             | Allow running tests         | ✅ Enabled   |
| **Build**               | Allow building project      | ✅ Enabled   |
| **ReadOutsideProject**  | Read external files         | ✅ Enabled   |
| **WriteOutsideProject** | Modify external files       | ⚠️ Optional |
| **MCP**                 | Execute MCP tools           | ✅ Supported |

---

## Configuration Rules Explained

### Rule Pattern Structure

All Terminal rules follow this secure pattern:

```
^<command_pattern>[^\s;&|<>@$]*$
```

**Components**:

| Part              | Purpose                                      |
|:------------------|:---------------------------------------------|
| `^`               | Start of command                             |
| `\Q...\E`         | Literal text (escape special chars)          |
| `[^\s;&|<>@$]*`   | Safe characters only (security filter)       |
| `$`               | End of command                               |

### Security Pattern: `[^\s;&|<>@$]*`

This pattern **excludes** dangerous characters:

| Character | Risk                  | Example Attack               |
|:----------|:----------------------|:-----------------------------|
| `;`       | Command chaining      | `git status; rm -rf /`       |
| `&`       | Background/chaining   | `cmd & malicious`            |
| `\|`      | Pipe injection        | `cmd \| evil`                |
| `<` `>`   | Redirection           | `cmd > /etc/passwd`          |
| `@`       | Special expansion     | Email/user injection         |
| `$`       | Variable expansion    | `$HOME` manipulation         |

---

## Rule Categories

### 1. Git Operations (15 rules)

```regex
# Basic commands (exact match)
^\Qgit status\E$
^\Qgit fetch\E$
^\Qgit pull\E$

# Commands with arguments
^\Qgit add\E [^\s;&|<>@$]*$
^\Qgit commit\E [^\s;&|<>@$]*$
^\Qgit push\E [^\s;&|<>@$]*$
^\Qgit checkout\E [^\s;&|<>@$]*$
^\Qgit branch\E [^\s;&|<>@$]*$
^\Qgit merge\E [^\s;&|<>@$]*$

# Commands with any arguments
^\Qgit diff\E.*$
^\Qgit log\E.*$
^\Qgit show\E.*$
^\Qgit stash\E.*$
^\Qgit rebase\E [^\s;&|<>@$]*$
^\Qgit cherry-pick\E [^\s;&|<>@$]*$
```

### 2. Python Development (12 rules)

```regex
# Execution
^\Qpython\E [^\s;&|<>@$]*$
^\Qpython3\E [^\s;&|<>@$]*$
^\Qpython -m\E [^\s;&|<>@$]*$

# Testing
^\Qpython -m pytest\E.*$
^\Qpytest\E.*$

# Package management
^\Qpip install\E [^\s;&|<>@$]*$
^\Qpip install -e\E [^\s;&|<>@$]*$
^\Qpip uninstall\E [^\s;&|<>@$]*$
^\Qpip list\E$
^\Qpip freeze\E$
^\Qpip show\E [^\s;&|<>@$]*$

# Virtual environments
^\Qconda activate\E [^\s;&|<>@$]*$
```

### 3. Node.js/npm (10 rules)

```regex
^\Qnpm install\E.*$
^\Qnpm run\E [^\s;&|<>@$]*$
^\Qnpm test\E.*$
^\Qnpm start\E$
^\Qnpm build\E$
^\Qnpx\E [^\s;&|<>@$]*$
^\Qyarn\E [^\s;&|<>@$]*$
^\Qpnpm\E [^\s;&|<>@$]*$
^\Qnode\E [^\s;&|<>@$]*$
^\Qnpm list\E.*$
```

### 4. Code Quality Tools (8 rules)

```regex
# Linting
^\Qruff check\E.*$
^\Qruff format\E.*$
^\Qeslint\E.*$
^\Qprettier\E.*$

# Type checking
^\Qmypy\E.*$
^\Qtsc\E.*$

# Testing
^\Qjest\E.*$
^\Qvitest\E.*$
```

### 5. Docker Commands (6 rules)

```regex
^\Qdocker ps\E.*$
^\Qdocker images\E.*$
^\Qdocker logs\E [^\s;&|<>@$]*$
^\Qdocker-compose up\E [^\s;&|<>@$]*$
^\Qdocker-compose down\E$
^\Qdocker build\E [^\s;&|<>@$]*$
```

### 6. File Operations (6 rules)

```regex
^\Qls\E.*$
^\Qdir\E.*$
^\Qcat\E [^\s;&|<>@$]*$
^\Qhead\E [^\s;&|<>@$]*$
^\Qtail\E [^\s;&|<>@$]*$
^\Qfind\E [^\s;&|<>@$]*$
```

---

## Platform-Specific Rules

### Windows PowerShell

```regex
^\QGet-ChildItem\E.*$
^\QGet-Content\E [^\s;&|<>@$]*$
^\QSet-Location\E [^\s;&|<>@$]*$
^\QGet-Process\E.*$
^\QTest-Path\E [^\s;&|<>@$]*$
```

### macOS/Linux Bash

```regex
^\Qchmod\E [^\s;&|<>@$]*$
^\Qchown\E [^\s;&|<>@$]*$
^\Qgrep\E [^\s;&|<>@$]*$
^\Qawk\E [^\s;&|<>@$]*$
^\Qsed\E [^\s;&|<>@$]*$
```

---

## Verification

### Check Current Rules

1. Go to `Settings | Tools | Junie | Action Allowlist`
2. Count Terminal rules (target: 87)
3. Verify rule patterns are correct

### Test Auto-Approval

Run these commands — they should execute without prompts:

```bash
git status           # Git operations
python --version     # Python commands
npm --version        # Node.js commands
docker ps            # Docker commands
```

### Monitor Approval Rate

Track your auto-approval rate weekly:

```
Auto-Approval Rate = (Auto-Approved / Total Commands) × 100%
Target: ≥90%
```

---

## Troubleshooting

### Command Still Requires Approval

**Symptoms**: Command matches a rule but still prompts for approval

**Solutions**:

1. **Check regex syntax** — Use `\Q...\E` for literal matching
2. **Verify pattern** — Test regex at [regex101.com](https://regex101.com)
3. **Check for typos** — Spaces, capitalization matter
4. **Restart IDE** — Some changes require restart

### Rule Not Working

**Common issues**:

| Issue                    | Solution                                      |
|:-------------------------|:----------------------------------------------|
| Missing `^` or `$`       | Add anchors: `^pattern$`                      |
| Special chars not escaped| Use `\Q...\E` wrapper                         |
| Pattern too restrictive  | Add `.*` for flexible matching                |
| Pattern too permissive   | Add `[^\s;&\|<>@$]*` for security             |

---

## Best Practices

### Do's ✅

- Use `\Q...\E` for literal command matching
- Include `[^\s;&|<>@$]*` security pattern
- Test rules before deploying
- Start with essential rules, expand gradually

### Don'ts ❌

- Don't allow `rm`, `del`, or destructive commands
- Don't use `.*` without security pattern
- Don't skip the `^` and `$` anchors
- Don't allow commands with `sudo` or admin privileges

---

## Complete Rules Reference

For copy-paste ready rule lists:

- [Windows Rules (68)](../reference/rules-windows.md)
- [macOS/Linux Rules (76)](../reference/rules-unix.md)
- [Regex Reference](../reference/regex.md)

---

## Related

- [Quick Start](quick-start.md) — First-time setup
- [MCP Configuration](../mcp/configuration.md) — MCP server setup
- [Efficiency Metrics](../operations/metrics.md) — Track auto-approval rate
- [Glossary](../reference/glossary.md) — Terminology

---

*Part of the Junie Documentation*
