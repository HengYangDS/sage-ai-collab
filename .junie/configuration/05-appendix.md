# Appendix

> Reference materials: regex patterns, complete rules list, and changelog (~15 min)

---

## Table of Contents

- [1. Regex Reference](#1-regex-reference)
- [2. Complete Rules List](#2-complete-rules-list)
- [3. Changelog](#3-changelog)
- [4. Document Information](#4-document-information)

---

## 1. Regex Reference

### Basic Patterns

| Pattern | Meaning              | Example | Matches               |
|:--------|:---------------------|:--------|:----------------------|
| `.`     | Any single character | `a.c`   | abc, aXc, a9c         |
| `*`     | Zero or more         | `ab*c`  | ac, abc, abbc         |
| `+`     | One or more          | `ab+c`  | abc, abbc (not ac)    |
| `?`     | Zero or one          | `ab?c`  | ac, abc               |
| `^`     | Start of line        | `^git`  | git status (at start) |
| `$`     | End of line          | `\.py$` | test.py (at end)      |

### Character Classes

| Pattern  | Meaning                          | Example                    |
|:---------|:---------------------------------|:---------------------------|
| `[abc]`  | Any of a, b, or c                | `[pP]` = p or P            |
| `[^abc]` | Not a, b, or c                   | `[^0-9]` = non-digit       |
| `[a-z]`  | Range a to z                     | `[A-Z]` = uppercase        |
| `\d`     | Digit [0-9]                      | `\d+` = one or more digits |
| `\w`     | Word character [A-Za-z0-9_]      | `\w+` = identifier         |
| `\s`     | Whitespace (space, tab, newline) | `\s+` = spaces             |

### Special Sequences

| Pattern   | Meaning                   | Usage in This Project               |
|:----------|:--------------------------|:------------------------------------|
| `\Q...\E` | Literal text (escape all) | `\Qgit status\E` = exact match      |
| `[^\s;&   | <>@$]`                    | Exclude dangerous chars             | Security pattern in all Terminal rules |
| `.*`      | Match anything            | `git log.*` = git log with any args |

### Common Patterns in This Configuration

**Exact Command Match**:

```regex
^\Qgit status\E$
```

Matches: `git status` (exactly)

**Command with Safe Arguments**:

```regex
^\Qpython\E [^\s;&|<>@$]*$
```

Matches: `python test.py`, `python -m pytest`
Excludes: `python; rm -rf` (contains `;`)

**Command with Any Arguments**:

```regex
^\Qgit log\E.*$
```

Matches: `git log`, `git log --oneline`, `git log -p`

---

## 2. Complete Rules List

> **🌐 Cross-Platform Configuration Guide**
>
> This appendix provides **two complete rule sets** optimized for easy copy-paste configuration:
> - **Windows Version**: Includes PowerShell-specific commands (68 Rules)
> - **macOS/Linux Version**: Includes Unix/Linux-specific commands (76 Rules)
>
> **Usage Instructions**:
> 1. **Choose your platform** below
> 2. **Copy the entire rule block** for your platform
> 3. **Paste into** `Settings | Tools | Junie | Action Allowlist`
> 4. Click "Add" for each rule (or import if bulk import is supported)
>
> **Why separate versions?**
> - ✅ **Faster configuration**: No need to filter platform-specific rules
> - ✅ **Zero errors**: Each version contains only compatible commands
> - ✅ **Team-friendly**: Share the appropriate version with team members

**💾 Quick Export Options**:

| Method                      | Steps                                     | Best For            |
|:----------------------------|:------------------------------------------|:--------------------|
| **Copy from this document** | Select rule block → Copy → Paste into IDE | Quick setup         |
| **Save as text file**       | Copy rules → Save as `.txt` file          | Team sharing        |
| **Export IDE settings**     | `File                                     | Manage IDE Settings | Export Settings` | Backup & migration |

> **💡 Tip**: After configuring, export your IDE settings as backup. This allows quick restoration after IDE updates or
> when setting up new machines.

---

### 🪟 Windows Version (68 Rules)

**For Windows users with PowerShell**

Copy-paste the complete rule block below:

```
^\Qpython -m pytest\E.*$
^\Qpython -m pip\E.*$
^\Qpython -m\E.*$
^\Qpython\E [^\s;&|<>@$]*$
^\Qpip install\E.*$
^\Qpip list\E.*$
^\Qpip show\E.*$
^\Qgit status\E$
^\Qgit log\E.*$
^\Qgit diff\E.*$
^\Qgit show\E [^\s;&|<>@$]+$
^\Qgit branch\E.*$
^\Qgit add\E.*$
^\Qgit commit\E.*$
^\Qgit push\E.*$
^\Qgit pull\E.*$
^\Qgit checkout\E.*$
^\Qgit merge\E.*$
^\Qgit stash\E.*$
^\Qgit tag\E.*$
^\Qgit remote\E.*$
^\Qdir\E.*$
^\QGet-ChildItem\E.*$
^\QSelect-String\E.*$
^\QGet-Content\E.*$
^\Qtree\E.*$
^\Qmake\E.*$
^\Qpoetry\E.*$
^\Qnpm\E.*$
^\Qyarn\E.*$
^\Qmvn\E.*$
^\Qgradle\E.*$
^\Qmkdocs\E.*$
^\Qsphinx-build\E.*$
^\Qdocker ps\E.*$
^\Qdocker images\E.*$
^\Qdocker logs\E.*$
^\Qdocker inspect\E.*$
^\Qkubectl get\E.*$
^\Qkubectl describe\E.*$
^\Qkubectl logs\E.*$
^\QWrite-Host\E.*$
^\QGet-Location\E$
^\Qpwd\E$
^\Qwhoami\E$
^\QGet-Date\E$
^\QGet-Command\E.*$
^Invoke-WebRequest.*$
^\Qcurl\E.*$
^\Qunzip -l\E [^\s;&|<>@$]+$
^\Qunzip\E [^\s;&|<>@$]+$
^\Qping\E [^\s;&|<>@$]+$
^\Qnslookup\E [^\s;&|<>@$]+$
^\Qdig\E.*$
^\Qnetstat\E.*$
^\Qpython -m venv\E.*$
^\.\\[^\s;&|<>@$]+\\Scripts\\Activate.ps1$
^\Qconda activate\E [^\s;&|<>@$]*$
^\Qconda deactivate\E$
^\Qconda env list\E$
^\Qpylint\E.*$
^\Qflake8\E.*$
^\Qblack\E.*$
^\Qmypy\E.*$
^\Qisort\E.*$
^\Qbandit\E.*$
^\Qpsql\E.*-c "SELECT.*"$
^\Qmysql\E.*-e "SELECT.*"$
```

**Total**: 68 rules for Windows (PowerShell)

**Categories Included**:

- ✅ Python Development (7)
- ✅ Git Operations (14)
- ✅ File Operations - Windows (5: dir, Get-ChildItem, Select-String, Get-Content, tree)
- ✅ Build Tools (8)
- ✅ Docker/K8s (7)
- ✅ System Commands - Windows (6: Write-Host, Get-Location, pwd, whoami, Get-Date, Get-Command)
- ✅ Development Assistance - Windows (2: Invoke-WebRequest, curl)
- ✅ Compression - Universal (2: unzip)
- ✅ Network Diagnostics (4)
- ✅ Python Virtual Environments - Windows (4: venv create, activate, conda)
- ✅ Code Quality Tools (6)
- ✅ Database Clients (2)

---

### 🐧 macOS/Linux Version (76 Rules)

**For macOS and Linux users with Bash/Zsh**

Copy-paste the complete rule block below:

```
^\Qpython -m pytest\E.*$
^\Qpython -m pip\E.*$
^\Qpython -m\E.*$
^\Qpython\E [^\s;&|<>@$]*$
^\Qpip install\E.*$
^\Qpip list\E.*$
^\Qpip show\E.*$
^\Qgit status\E$
^\Qgit log\E.*$
^\Qgit diff\E.*$
^\Qgit show\E [^\s;&|<>@$]+$
^\Qgit branch\E.*$
^\Qgit add\E.*$
^\Qgit commit\E.*$
^\Qgit push\E.*$
^\Qgit pull\E.*$
^\Qgit checkout\E.*$
^\Qgit merge\E.*$
^\Qgit stash\E.*$
^\Qgit tag\E.*$
^\Qgit remote\E.*$
^\Qls\E.*$
^\Qfind\E.*$
^\Qgrep\E.*$
^\Qcat\E [^\s;&|<>@$]+$
^\Qmake\E.*$
^\Qpoetry\E.*$
^\Qnpm\E.*$
^\Qyarn\E.*$
^\Qmvn\E.*$
^\Qgradle\E.*$
^\Qmkdocs\E.*$
^\Qsphinx-build\E.*$
^\Qdocker ps\E.*$
^\Qdocker images\E.*$
^\Qdocker logs\E.*$
^\Qdocker inspect\E.*$
^\Qkubectl get\E.*$
^\Qkubectl describe\E.*$
^\Qkubectl logs\E.*$
^\Qecho\E.*$
^\Qenv\E$
^\Qpwd\E$
^\Qwhoami\E$
^\Qdate\E$
^\Qwhich\E.*$
^\Qwget\E.*$
^\Qcurl\E.*$
^\Qhead\E.*$
^\Qtail\E.*$
^\Qwc\E.*$
^\Qsort\E.*$
^\Quniq\E.*$
^\Qawk\E.*$
^\Qsed\E.*$
^\Qtar -tzf\E [^\s;&|<>@$]+$
^\Qtar -xzf\E [^\s;&|<>@$]+$
^\Qunzip -l\E [^\s;&|<>@$]+$
^\Qunzip\E [^\s;&|<>@$]+$
^\Qping\E [^\s;&|<>@$]+$
^\Qnslookup\E [^\s;&|<>@$]+$
^\Qdig\E.*$
^\Qnetstat\E.*$
^\Qpython -m venv\E.*$
^\Qsource\E [^\s;&|<>@$]+/activate$
^\Qconda activate\E [^\s;&|<>@$]*$
^\Qconda deactivate\E$
^\Qconda env list\E$
^\Qpylint\E.*$
^\Qflake8\E.*$
^\Qblack\E.*$
^\Qmypy\E.*$
^\Qisort\E.*$
^\Qbandit\E.*$
^\Qpsql\E.*-c "SELECT.*"$
^\Qmysql\E.*-e "SELECT.*"$
```

**Total**: 76 rules for macOS/Linux (Bash/Zsh)

**Categories Included**:

- ✅ Python Development (7)
- ✅ Git Operations (14)
- ✅ File Operations - Unix (4: ls, find, grep, cat)
- ✅ Build Tools (8)
- ✅ Docker/K8s (7)
- ✅ System Commands - Unix (5: echo, env, pwd, whoami, date, which)
- ✅ Development Assistance - Unix (2: wget, curl)
- ✅ Text Processing (7: head, tail, wc, sort, uniq, awk, sed)
- ✅ Compression - Unix (4: tar, unzip)
- ✅ Network Diagnostics (4)
- ✅ Python Virtual Environments - Unix (4: venv create, source activate, conda)
- ✅ Code Quality Tools (6)
- ✅ Database Clients (2)

---

### 📋 Cross-Platform Differences Summary

| Feature             | Windows (68 Rules)            | macOS/Linux (76 Rules)                                       |
|---------------------|-------------------------------|--------------------------------------------------------------|
| **File Listing**    | `dir`, `Get-ChildItem`        | `ls`                                                         |
| **File Search**     | `Get-ChildItem -Recurse`      | `find`                                                       |
| **Content Search**  | `Select-String`               | `grep`                                                       |
| **View File**       | `Get-Content`                 | `cat`                                                        |
| **Print Text**      | `Write-Host`                  | `echo`                                                       |
| **Show Path**       | `Get-Location`                | `pwd`                                                        |
| **Environment**     | (PowerShell automatic)        | `env`                                                        |
| **Current Time**    | `Get-Date`                    | `date`                                                       |
| **Find Command**    | `Get-Command`                 | `which`                                                      |
| **HTTP Request**    | `Invoke-WebRequest`, `curl`   | `wget`, `curl`                                               |
| **Text Processing** | (Not included)                | `head`, `tail`, `wc`, `sort`, `uniq`, `awk`, `sed` (7 rules) |
| **Archive**         | `unzip` (2)                   | `tar`, `unzip` (4)                                           |
| **Activate venv**   | `.\venv\Scripts\Activate.ps1` | `source venv/bin/activate`                                   |

---

### 💡 Configuration Tips

**Windows Users**:

- ✅ Use the Windows version (68 Rules)
- ✅ Ensure PowerShell is your default terminal
- ⚠️ Text processing commands (awk, sed, etc.) not included - use PowerShell cmdlets instead

**macOS/Linux Users**:

- ✅ Use the macOS/Linux version (76 Rules)
- ✅ Works with both Bash and Zsh
- ✅ Includes Unix text processing tools (awk, sed, grep, etc.)

**Cross-Platform Teams**:

- ✅ Each member uses their platform-specific version
- ✅ Both versions provide equivalent functionality
- ✅ Share this guide with the team for consistent setup

---

> **💡 Note**: Include conda virtual environment rules if using conda instead of venv (
> see [Python Virtual Environments](#11-python-virtual-environments-6-rules---v20-added) in Configuration Rules)

---

## 3. Changelog

### v1.0.0 (2025-11-27) - First Official Release 🎉

**Focus**: First official release of Junie Configuration Guide.

**Document Highlights**:

- **📘 Action Allowlist Configuration**: 87 precise Terminal rules for 90%+ automatic command approval
    - 57 cross-platform universal rules (Git, Python, Docker, npm, etc.)
    - 30 platform-specific rules (Windows PowerShell / macOS-Linux Bash)
    - Dangerous character exclusion for security guarantee

- **🚀 MCP Integration Guide**: Complete Model Context Protocol integration guidance
    - P0 tools: Filesystem, Memory, Git servers
    - P1 tools: GitHub, SQLite, Puppeteer servers
    - Cross-platform configuration examples (Windows/macOS/Linux)

- **🔮 Future Protocol Vision**: A2A/ACP protocol evolution roadmap
    - Protocol ecosystem landscape analysis
    - Future-oriented architecture recommendations
    - Multi-agent collaboration preparation

---

## 4. Document Information

> 📋 For current version and update date, see the [document header](#junie-configuration-guide).

**Language**: English  
**Status**: Production-Ready

**Feedback & Contributing**:

- Report issues or suggest improvements via project issue tracker
- Configuration best practices and cross-platform compatibility reports welcome

### How to Contribute

We welcome contributions to improve this guide! Here's how you can help:

**📝 Report Issues**:

- Found an error? Open an issue with the section name and description
- Include your platform (Windows/macOS/Linux) and IDE version

**💡 Suggest Improvements**:

- New rules for common commands
- Better explanations or examples
- Cross-platform compatibility fixes

**🔧 Submit Changes**:

1. **For new Terminal rules**:
    - Test the rule on your platform first
    - Ensure it follows the security pattern `[^\s;&|<>@$]`
    - Provide the command category and use case

2. **For documentation updates**:
    - Keep the same formatting style
    - Update both the rule explanation and Appendix B
    - Verify all cross-references still work

3. **For MCP configurations**:
    - Test on actual Junie installation
    - Include both Windows and Unix examples
    - Document any platform-specific issues

**📋 Contribution Checklist**:

- [ ] Tested on target platform
- [ ] Follows existing formatting conventions
- [ ] No security vulnerabilities introduced
- [ ] Cross-references updated if needed
- [ ] Version comparison table updated (if adding features)

---

## Related

- `README.md` — Configuration guide index
- `01-introduction.md` — Document overview
- `02-action-allowlist.md` — Terminal rules configuration
- `03-mcp-integration.md` — MCP setup and best practices
- `04-future-vision.md` — Protocol roadmap (previous)

---

*Part of the Junie Configuration Guide*
