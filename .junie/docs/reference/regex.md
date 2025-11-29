# Regex Reference

> Regular expression patterns for Terminal rules (~10 min reference)

---

## Basic Patterns

| Pattern | Meaning              | Example | Matches               |
|:--------|:---------------------|:--------|:----------------------|
| `.`     | Any single character | `a.c`   | abc, aXc, a9c         |
| `*`     | Zero or more         | `ab*c`  | ac, abc, abbc         |
| `+`     | One or more          | `ab+c`  | abc, abbc (not ac)    |
| `?`     | Zero or one          | `ab?c`  | ac, abc               |
| `^`     | Start of line        | `^git`  | git status (at start) |
| `$`     | End of line          | `\.py$` | test.py (at end)      |

---

## Character Classes

| Pattern  | Meaning                          | Example                    |
|:---------|:---------------------------------|:---------------------------|
| `[abc]`  | Any of a, b, or c                | `[pP]` = p or P            |
| `[^abc]` | Not a, b, or c                   | `[^0-9]` = non-digit       |
| `[a-z]`  | Range a to z                     | `[A-Z]` = uppercase        |
| `\d`     | Digit [0-9]                      | `\d+` = one or more digits |
| `\w`     | Word character [A-Za-z0-9_]      | `\w+` = identifier         |
| `\s`     | Whitespace (space, tab, newline) | `\s+` = spaces             |

---

## Special Sequences

| Pattern   | Meaning                   | Usage                               |
|:----------|:--------------------------|:------------------------------------|
| `\Q...\E` | Literal text (escape all) | `\Qgit status\E` = exact match      |
| `.*`      | Match anything            | `git log.*` = git log with any args |

---

## Security Pattern

### `[^\s;&|<>@$]*`

This is the **critical security pattern** used in all Terminal rules. It matches any character EXCEPT dangerous ones.

**Characters Excluded**:

| Character | Risk                  | Example Attack             |
|:----------|:----------------------|:---------------------------|
| `\s`      | Space (word boundary) | Prevents command splitting |
| `;`       | Command chaining      | `git status; rm -rf /`     |
| `&`       | Background/chaining   | `cmd & malicious`          |
| `\|`      | Pipe injection        | `cmd \| evil`              |
| `<`       | Input redirection     | `cmd < /etc/passwd`        |
| `>`       | Output redirection    | `cmd > /etc/passwd`        |
| `@`       | Special expansion     | Email/user injection       |
| `$`       | Variable expansion    | `$HOME` manipulation       |

**Usage**:

```regex
^\Qcommand\E [^\s;&|<>@$]*$
```

---

## Common Patterns

### Exact Command Match

Matches command with no arguments:

```regex
^\Qgit status\E$
```

**Matches**: `git status` (exactly)
**Does NOT match**: `git status -s`, `git statusx`

### Command with Safe Arguments

Allows arguments but excludes dangerous characters:

```regex
^\Qpython\E [^\s;&|<>@$]*$
```

**Matches**: `python test.py`, `python -m pytest`
**Does NOT match**: `python; rm -rf /`, `python | cat`

### Command with Any Arguments

Allows any arguments (use with caution):

```regex
^\Qgit log\E.*$
```

**Matches**: `git log`, `git log --oneline`, `git log -p`
**Caution**: Less secure, use only for safe commands

### Optional Subcommand

Allows command with optional parts:

```regex
^\Qgit\E (status|diff|log).*$
```

**Matches**: `git status`, `git diff`, `git log --oneline`

---

## Pattern Templates

### Template 1: Exact Match

```regex
^\Q<command>\E$
```

Use for: Commands that should never have arguments

### Template 2: Safe Arguments

```regex
^\Q<command>\E [^\s;&|<>@$]*$
```

Use for: Commands that need arguments but must be secure

### Template 3: Any Arguments

```regex
^\Q<command>\E.*$
```

Use for: Safe commands where any argument is acceptable

### Template 4: Specific Subcommands

```regex
^\Q<command>\E (<sub1>|<sub2>|<sub3>).*$
```

Use for: Commands with specific allowed subcommands

---

## Examples by Category

### Git Commands

```regex
# Exact match (no args)
^\Qgit status\E$
^\Qgit fetch\E$

# Safe arguments
^\Qgit add\E [^\s;&|<>@$]*$
^\Qgit commit\E [^\s;&|<>@$]*$
^\Qgit push\E [^\s;&|<>@$]*$

# Any arguments (safe commands)
^\Qgit diff\E.*$
^\Qgit log\E.*$
```

### Python Commands

```regex
# Safe arguments
^\Qpython\E [^\s;&|<>@$]*$
^\Qpython3\E [^\s;&|<>@$]*$
^\Qpip install\E [^\s;&|<>@$]*$

# Any arguments (test commands)
^\Qpython -m pytest\E.*$
^\Qpytest\E.*$
```

### Node.js Commands

```regex
# Safe arguments
^\Qnpm run\E [^\s;&|<>@$]*$
^\Qnpx\E [^\s;&|<>@$]*$
^\Qnode\E [^\s;&|<>@$]*$

# Any arguments
^\Qnpm install\E.*$
^\Qnpm test\E.*$
```

---

## Testing Patterns

### Online Tools

- **regex101.com** — Test patterns with explanation
- **regexr.com** — Visual regex tester

### Test Procedure

1. Go to regex101.com
2. Select "Java 8" flavor (Junie uses Java regex)
3. Enter your pattern
4. Test with various inputs
5. Verify matches and non-matches

### Test Cases Template

```
Pattern: ^\Qgit add\E [^\s;&|<>@$]*$

Should MATCH:
✓ git add .
✓ git add file.txt
✓ git add src/main.py

Should NOT MATCH:
✗ git add; rm -rf /
✗ git add | cat
✗ git add > output.txt
✗ git add $HOME
```

---

## Common Mistakes

| Mistake                    | Problem                       | Fix                          |
|:---------------------------|:------------------------------|:-----------------------------|
| Missing `^`                | Matches anywhere in command   | Add `^` at start             |
| Missing `$`                | Matches partial commands      | Add `$` at end               |
| Using `.*` without caution | Allows dangerous characters   | Use `[^\s;&\|<>@$]*` instead |
| Not escaping special chars | Pattern doesn't match literal | Use `\Q...\E` wrapper        |
| Forgetting space           | Pattern too restrictive       | Add space before `[^...]`    |

---

## Best Practices

### Do's ✅

1. **Always use anchors** — `^` at start, `$` at end
2. **Use `\Q...\E`** for literal command text
3. **Include security pattern** — `[^\s;&|<>@$]*`
4. **Test thoroughly** before deploying
5. **Start restrictive**, loosen only if needed

### Don'ts ❌

1. **Don't use bare `.*`** without security consideration
2. **Don't allow** `rm`, `del`, destructive commands
3. **Don't skip** the security character exclusion
4. **Don't allow** `sudo` or admin commands
5. **Don't copy** patterns without understanding them

---

## Related

- [Action Allowlist](../guides/action-allowlist.md) — Configuration guide
- [Windows Rules](rules-windows.md) — Complete Windows rule list
- [Unix Rules](rules-unix.md) — Complete macOS/Linux rule list
- [Glossary](glossary.md) — Terminology

---

*Part of the Junie Configuration Template System*
