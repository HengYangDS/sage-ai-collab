
# macOS/Linux Terminal Rules

> Complete rule list for Bash/Zsh (76 Rules)

---

## Table of Contents

1. [Quick Setup](#1-quick-setup)
2. [Cross-Platform Rules](#2-cross-platform-rules-57-rules)
3. [Unix-Specific Rules](#3-unix-specific-rules-19-rules)
4. [All Rules](#4-all-rules-copy-paste-block)
5. [Summary](#5-summary)
6. [Related](#6-related)

---

## 1. Quick Setup

1. Open `Settings | Tools | Junie | Action Allowlist`
2. Copy rules from below
3. Add each rule as a Terminal rule
4. Click "Apply"

---

## 2. Cross-Platform Rules (57 Rules)

These rules work on all platforms.

### Git Operations (15 rules)

```text
^\Qgit status\E$
^\Qgit fetch\E$
^\Qgit pull\E$
^\Qgit add\E [^\s;&|<>@$]*$
^\Qgit commit\E [^\s;&|<>@$]*$
^\Qgit push\E [^\s;&|<>@$]*$
^\Qgit checkout\E [^\s;&|<>@$]*$
^\Qgit branch\E [^\s;&|<>@$]*$
^\Qgit merge\E [^\s;&|<>@$]*$
^\Qgit diff\E.*$
^\Qgit log\E.*$
^\Qgit show\E.*$
^\Qgit stash\E.*$
^\Qgit rebase\E [^\s;&|<>@$]*$
^\Qgit cherry-pick\E [^\s;&|<>@$]*$
```

### Python Development (12 rules)

```text
^\Qpython\E [^\s;&|<>@$]*$
^\Qpython3\E [^\s;&|<>@$]*$
^\Qpython -m\E [^\s;&|<>@$]*$
^\Qpython -m pytest\E.*$
^\Qpytest\E.*$
^\Qpip install\E [^\s;&|<>@$]*$
^\Qpip install -e\E [^\s;&|<>@$]*$
^\Qpip uninstall\E [^\s;&|<>@$]*$
^\Qpip list\E$
^\Qpip freeze\E$
^\Qpip show\E [^\s;&|<>@$]*$
^\Qconda activate\E [^\s;&|<>@$]*$
```

### Node.js/npm (10 rules)

```text
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

### Code Quality Tools (8 rules)

```text
^\Qruff check\E.*$
^\Qruff format\E.*$
^\Qeslint\E.*$
^\Qprettier\E.*$
^\Qmypy\E.*$
^\Qtsc\E.*$
^\Qjest\E.*$
^\Qvitest\E.*$
```

### Docker Commands (6 rules)

```text
^\Qdocker ps\E.*$
^\Qdocker images\E.*$
^\Qdocker logs\E [^\s;&|<>@$]*$
^\Qdocker-compose up\E [^\s;&|<>@$]*$
^\Qdocker-compose down\E$
^\Qdocker build\E [^\s;&|<>@$]*$
```

### File/Directory Operations (6 rules)

```text
^\Qls\E.*$
^\Qdir\E.*$
^\Qcat\E [^\s;&|<>@$]*$
^\Qhead\E [^\s;&|<>@$]*$
^\Qtail\E [^\s;&|<>@$]*$
^\Qfind\E [^\s;&|<>@$]*$
```

---

## 3. Unix-Specific Rules (19 Rules)

These rules are for macOS and Linux Bash/Zsh.

### File Operations (8 rules)

```text
^\Qchmod\E [^\s;&|<>@$]*$
^\Qchown\E [^\s;&|<>@$]*$
^\Qcp\E [^\s;&|<>@$]*$
^\Qmv\E [^\s;&|<>@$]*$
^\Qmkdir\E [^\s;&|<>@$]*$
^\Qtouch\E [^\s;&|<>@$]*$
^\Qln\E [^\s;&|<>@$]*$
^\Qreadlink\E [^\s;&|<>@$]*$
```

### Text Processing (6 rules)

```text
^\Qgrep\E [^\s;&|<>@$]*$
^\Qawk\E [^\s;&|<>@$]*$
^\Qsed\E [^\s;&|<>@$]*$
^\Qsort\E [^\s;&|<>@$]*$
^\Quniq\E [^\s;&|<>@$]*$
^\Qwc\E [^\s;&|<>@$]*$
```

### System Information (5 rules)

```text
^\Qpwd\E$
^\Qwhoami\E$
^\Qwhich\E [^\s;&|<>@$]*$
^\Qenv\E$
^\Qecho\E [^\s;&|<>@$]*$
```

---

## 4. All Rules (Copy-Paste Block)

Copy this entire block for quick setup:

```text
^\Qgit status\E$
^\Qgit fetch\E$
^\Qgit pull\E$
^\Qgit add\E [^\s;&|<>@$]*$
^\Qgit commit\E [^\s;&|<>@$]*$
^\Qgit push\E [^\s;&|<>@$]*$
^\Qgit checkout\E [^\s;&|<>@$]*$
^\Qgit branch\E [^\s;&|<>@$]*$
^\Qgit merge\E [^\s;&|<>@$]*$
^\Qgit diff\E.*$
^\Qgit log\E.*$
^\Qgit show\E.*$
^\Qgit stash\E.*$
^\Qgit rebase\E [^\s;&|<>@$]*$
^\Qgit cherry-pick\E [^\s;&|<>@$]*$
^\Qpython\E [^\s;&|<>@$]*$
^\Qpython3\E [^\s;&|<>@$]*$
^\Qpython -m\E [^\s;&|<>@$]*$
^\Qpython -m pytest\E.*$
^\Qpytest\E.*$
^\Qpip install\E [^\s;&|<>@$]*$
^\Qpip install -e\E [^\s;&|<>@$]*$
^\Qpip uninstall\E [^\s;&|<>@$]*$
^\Qpip list\E$
^\Qpip freeze\E$
^\Qpip show\E [^\s;&|<>@$]*$
^\Qconda activate\E [^\s;&|<>@$]*$
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
^\Qruff check\E.*$
^\Qruff format\E.*$
^\Qeslint\E.*$
^\Qprettier\E.*$
^\Qmypy\E.*$
^\Qtsc\E.*$
^\Qjest\E.*$
^\Qvitest\E.*$
^\Qdocker ps\E.*$
^\Qdocker images\E.*$
^\Qdocker logs\E [^\s;&|<>@$]*$
^\Qdocker-compose up\E [^\s;&|<>@$]*$
^\Qdocker-compose down\E$
^\Qdocker build\E [^\s;&|<>@$]*$
^\Qls\E.*$
^\Qdir\E.*$
^\Qcat\E [^\s;&|<>@$]*$
^\Qhead\E [^\s;&|<>@$]*$
^\Qtail\E [^\s;&|<>@$]*$
^\Qfind\E [^\s;&|<>@$]*$
^\Qchmod\E [^\s;&|<>@$]*$
^\Qchown\E [^\s;&|<>@$]*$
^\Qcp\E [^\s;&|<>@$]*$
^\Qmv\E [^\s;&|<>@$]*$
^\Qmkdir\E [^\s;&|<>@$]*$
^\Qtouch\E [^\s;&|<>@$]*$
^\Qln\E [^\s;&|<>@$]*$
^\Qreadlink\E [^\s;&|<>@$]*$
^\Qgrep\E [^\s;&|<>@$]*$
^\Qawk\E [^\s;&|<>@$]*$
^\Qsed\E [^\s;&|<>@$]*$
^\Qsort\E [^\s;&|<>@$]*$
^\Quniq\E [^\s;&|<>@$]*$
^\Qwc\E [^\s;&|<>@$]*$
^\Qpwd\E$
^\Qwhoami\E$
^\Qwhich\E [^\s;&|<>@$]*$
^\Qenv\E$
^\Qecho\E [^\s;&|<>@$]*$
```

---

## 5. Summary

| Category       | Count  |
|:---------------|:-------|
| Cross-Platform | 57     |
| Unix-Specific  | 19     |
| **Total**      | **76** |

---

## 6. Related

- [Windows Rules](RULES_WINDOWS.md) — Windows/PowerShell rules
- [Regex Reference](regex.md) — Pattern syntax
- [Action Allowlist](../guides/ACTION_ALLOWLIST.md) — Configuration guide

---

*AI Collaboration Knowledge Base*
