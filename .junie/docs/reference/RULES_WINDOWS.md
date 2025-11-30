
# Windows Terminal Rules

> Complete rule list for Windows PowerShell (68 Rules)

---

## Table of Contents

1. [Quick Setup](#1-quick-setup)
2. [Cross-Platform Rules](#2-cross-platform-rules-57-rules)
3. [Windows-Specific Rules](#3-windows-specific-rules-11-rules)
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

## 3. Windows-Specific Rules (11 Rules)

These rules are for Windows PowerShell.

### PowerShell Commands (11 rules)

```text
^\QGet-ChildItem\E.*$
^\QGet-Content\E [^\s;&|<>@$]*$
^\QSet-Location\E [^\s;&|<>@$]*$
^\QGet-Process\E.*$
^\QTest-Path\E [^\s;&|<>@$]*$
^\QNew-Item\E [^\s;&|<>@$]*$
^\QRemove-Item\E [^\s;&|<>@$]*$
^\QCopy-Item\E [^\s;&|<>@$]*$
^\QMove-Item\E [^\s;&|<>@$]*$
^\QGet-Location\E$
^\QSet-ExecutionPolicy\E [^\s;&|<>@$]*$
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
^\QGet-ChildItem\E.*$
^\QGet-Content\E [^\s;&|<>@$]*$
^\QSet-Location\E [^\s;&|<>@$]*$
^\QGet-Process\E.*$
^\QTest-Path\E [^\s;&|<>@$]*$
^\QNew-Item\E [^\s;&|<>@$]*$
^\QRemove-Item\E [^\s;&|<>@$]*$
^\QCopy-Item\E [^\s;&|<>@$]*$
^\QMove-Item\E [^\s;&|<>@$]*$
^\QGet-Location\E$
^\QSet-ExecutionPolicy\E [^\s;&|<>@$]*$
```

---

## 5. Summary

| Category         | Count  |
|:-----------------|:-------|
| Cross-Platform   | 57     |
| Windows-Specific | 11     |
| **Total**        | **68** |

---

## 6. Related

- [Unix Rules](RULES_UNIX.md) — macOS/Linux rules
- [Regex Reference](regex.md) — Pattern syntax
- [Action Allowlist](../guides/ACTION_ALLOWLIST.md) — Configuration guide

---

*AI Collaboration Knowledge Base*
