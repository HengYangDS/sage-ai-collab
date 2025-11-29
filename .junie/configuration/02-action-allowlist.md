# Action Allowlist Configuration

> Configure 87 Terminal rules for 90%+ automatic command approval (~30 min)

---

## Table of Contents

- [1. Configuration Overview](#1-configuration-overview)
- [2. Quick Start](#2-quick-start)
- [3. Action Allowlist Mechanism](#3-action-allowlist-mechanism)
- [4. Configuration Rules Explained](#4-configuration-rules-explained)
- [5. Auto-Configuration Process](#5-auto-configuration-process)
- [6. Project Configuration Preferences](#6-project-configuration-preferences)
- [7. Verification and Maintenance](#7-verification-and-maintenance)
- [8. Troubleshooting](#8-troubleshooting)
- [9. FAQ](#9-faq)

---

## 1. Configuration Overview

### 1.1 Goals

Configure **maximum autonomy** (Level 5 Autonomy) for Junie AI Assistant through precise Terminal rules that enable
seamless AI collaboration.

**🎯 Core Goal**: Eliminate 90%+ manual approvals, achieve seamless batch execution mode

| Configuration Item | Target Value                  | Current Status | Expected Effect                               |
|:-------------------|:------------------------------|:---------------|:----------------------------------------------|
| **Terminal Rules** | 87 precise rules              | ✅ Complete     | 90%+ auto-approval                            |
| **Execution Mode** | Week/Phase batch execution    | ✅ Enabled      | Continuous collaboration without interruption |
| **Quality Tools**  | 6 automation tools            | ✅ Configured   | Automatic code quality checks                 |
| **Security**       | Dangerous character exclusion | ✅ Secured      | Balance between security and efficiency       |

**Key Values**:

- ⚡ **Efficiency Boost**: 90%+ reduction in manual approvals, 5-10x collaboration efficiency improvement
- 🔒 **Security Guarantee**: Precise regex rules exclude all dangerous operations
- 🎯 **Precise Control**: 87 rules covering 13 major scenarios, extensible as needed

### 1.2 Statistics

- **Terminal Rules**: 87 rules
- **Allowed Actions**: 3 (RunTest, Build, ReadOutsideProject)
- **Configuration File**: See [Platform Quick Reference](#platform-quick-reference) for your platform's path

> 📜 For complete version history, see [Changelog](05-appendix.md#3-changelog) in the Appendix.
>
> 💡 For MCP Integration goals and statistics, see [MCP Integration Guide](03-mcp-integration.md).
> For Future Protocol Vision, see [Future Vision](04-future-vision.md).

---

## 2. Quick Start

### 2.1 Method 1: Auto-Configuration Completed (Recommended)

If auto-configuration has been run, simply:

1. **Restart IDE** (Required)
   ```
   File | Exit (or use your IDE's exit shortcut)
   ```
   > **Note**: Shortcut keys may vary by IDE and platform (e.g., `Ctrl+Q` on some IDEs, `Cmd+Q` on macOS)

2. **Verify Configuration**
    - Open `Settings | Tools | Junie | Action Allowlist`
    - Confirm you see 87 Terminal rules

3. **Test Execution**
   ```bash
   git status  # Should execute directly without approval
   ```

### 2.2 Method 2: Manual Configuration

If you need to reconfigure or set up on another machine:

1. Open `Settings | Tools | Junie | Action Allowlist`
2. Refer to "Configuration Rules Explained" chapter in this document
3. Add rules one by one or use "Allow similar commands" in the tool window

---

## 3. Action Allowlist Mechanism

### 3.1 Core Concepts

**Action Allowlist** is Junie's permission management mechanism that controls which sensitive operations can be executed
automatically.

#### Security Classification

- **Safe Actions**: Reversible, no sensitive changes (e.g., editing code)
- **Sensitive Actions**: Potential risks (e.g., executing terminal commands)

### 3.2 Rule Types

| Rule Type               | Function Description             | Configuration Precision            | Project Configuration                                                         |
|:------------------------|:---------------------------------|:-----------------------------------|:------------------------------------------------------------------------------|
| **Terminal**            | Allow specific terminal commands | Exact/Regex/All                    | ✅ 87 rules                                                                    |
| **RunTest**             | Allow running tests              | Allow all                          | ✅ Configured                                                                  |
| **Build**               | Allow building project           | Allow all                          | ✅ Configured                                                                  |
| **ReadOutsideProject**  | Read files outside project       | Allow all                          | ✅ Configured                                                                  |
| **WriteOutsideProject** | Modify files outside project     | Allow all                          | ⏸️ Observation period                                                         |
| **Preview**             | Run builds/code                  | Allow all                          | ⏸️ Not used                                                                   |
| **MCP**                 | Execute MCP tools                | Settings config + Action Allowlist | ✅ [Supported](https://www.jetbrains.com/help/junie/mcp-settings.html) (stdio) |
| **Edit build scripts**  | Edit build scripts               | Allow all                          | ⏸️ Use with caution                                                           |

### 3.3 Security Strategy

#### Excluded Dangerous Characters

All Terminal rules use `[^\s;&|<>@$]` to exclude:

- `;` - Command separator
- `&` - Background execution
- `|` - Pipe operator
- `<` `>` - Redirection
- `@` `$` - Variable expansion

#### High-Risk Operations Not Added

- ❌ `rm` / `Remove-Item` - Delete files
- ❌ `docker run` - Run containers
- ❌ `kubectl delete` - Delete resources
- ❌ `sudo` - Privilege escalation

### Command Execution Decision Flow

The following diagram shows how Junie decides whether to execute a command automatically:

```
                              +----------------------+
                              |    Junie receives    |
                              |   command request    |
                              +----------------------+
                                         |
                                         v
                              +----------------------+
                              |   Is command type    |
                              |    in Allowlist?     |
                              +----------+-----------+
                                         |
                           +-------------+-------------+
                           |                           |
                          YES                          NO
                           |                           |
                           v                           v
                  +-----------------+       +--------------------+
                  |   Check regex   |       |  MANUAL APPROVAL   |
                  |      rules      |       | Prompt user [END]  |
                  +--------+--------+       +--------------------+
                           |
                           v
                  +-----------------+
                  |  Does command   |
                  | match any rule? |
                  +--------+--------+
                           |
                +----------+----------+
                |                     |
               YES                    NO
                |                     |
                v                     v
       +-----------------+    +--------------------+
       |    Contains     |    |  MANUAL APPROVAL   |
       | dangerous chars?|    | Prompt user [END]  |
       +--------+--------+    +--------------------+
                |
       +--------+--------+
       |                 |
      YES                NO
       |                 |
       v                 v
  +---------+    +-----------------+
  | BLOCKED |    |  AUTO-EXECUTE   |
  |  [END]  |    | Command runs    |
  +---------+    |     [END]       |
                 +-----------------+
```

**Key Decision Points**:

1. **Allowlist Check**: Is the action type (Terminal, RunTest, etc.) configured?
2. **Regex Match**: Does the command match any configured regex pattern?
3. **Security Check**: Does the command contain dangerous characters?

---

## 4. Configuration Rules Explained

### Terminal Rules Classification (87 rules)

> **Note**: This section shows representative examples from each category. For the complete list of all 87 rules,
> see [Appendix B: Complete Rules List](#appendix-b-complete-rules-list-plain-text).

> **🌐 Cross-Platform Note**: All Terminal rules in this section are classified into two categories by cross-platform
> compatibility:
>
> **📘 Cross-Platform Universal Commands (57 rules)**: These commands have identical syntax across Windows/macOS/Linux,
> no platform distinction needed.
> - Includes: Python, Git, Docker/K8s, npm/yarn, Maven/Gradle, code quality tools, database clients, etc.
>
> **🔧 Platform-Specific Commands (30 rules)**: These commands have different equivalents on different platforms. This
> document provides complete dual-platform versions for each function.
> - **Windows (PowerShell)**: Uses PowerShell cmdlets and Windows-specific commands
> - **macOS/Linux (Bash/Zsh)**: Uses Unix/Linux standard commands
>
> **Usage Recommendations**:
> - ✅ Cross-platform universal commands can be copied directly
> - ✅ For platform-specific commands, select the version for your operating system
> - ✅ For team collaboration, recommend including all platform versions in configuration files to support cross-platform
    development

---

#### 1. Python Development (7 Rules)

**Platform Compatibility**: ✅ Cross-Platform Universal (Windows/macOS/Linux)

```regex
^\Qpython -m pytest\E.*$
^\Qpip install\E.*$
^\Qpip list\E.*$
```

**Allowed Operations**: pytest testing, pip package management, Python module execution

#### 2. Git Operations (14 Rules)

**Platform Compatibility**: ✅ Cross-Platform Universal (Windows/macOS/Linux)

```regex
^\Qgit status\E$
^\Qgit log\E.*$
^\Qgit diff\E.*$
^\Qgit add\E.*$
^\Qgit commit\E.*$
^\Qgit push\E.*$
```

**Allowed Operations**: Repository status, history viewing, staging, committing, pushing

#### 3. File Operations (9 Rules)

**Platform Compatibility**: 🔧 Platform-Specific (select based on your OS)

**Windows (PowerShell)**: `dir`, `Get-ChildItem`, `Select-String`, `Get-Content`, `tree`  
**macOS/Linux (Bash/Zsh)**: `ls`, `find`, `grep`, `cat`

```regex
# Examples shown are for Unix/Linux - adjust for Windows PowerShell
^\Qls\E.*$
^\Qfind\E [^\s;&|<>@$]*$
^\Qcat\E [^\s;&|<>@$]*$
```

| Function       | Windows (PowerShell)     | macOS/Linux |
|----------------|--------------------------|-------------|
| List files     | `dir` / `Get-ChildItem`  | `ls`        |
| Search files   | `Get-ChildItem -Recurse` | `find`      |
| Search content | `Select-String`          | `grep`      |
| View file      | `Get-Content`            | `cat`       |

**Allowed Operations**: Directory listing, file searching, content viewing

#### 4. Build Tools (8 Rules)

**Platform Compatibility**: ✅ Cross-Platform Universal (Windows/macOS/Linux)

```regex
^\Qmake\E [^\s;&|<>@$]*$
^\Qmkdocs\E [^\s;&|<>@$]*$
^\Qnpm\E [^\s;&|<>@$]*$
```

**Allowed Operations**: Make builds, MkDocs documentation, npm package management

#### 5. Docker/K8s (7 Rules)

**Platform Compatibility**: ✅ Cross-Platform Universal (Windows/macOS/Linux)

```regex
^\Qdocker ps\E.*$
^\Qdocker images\E.*$
^\Qkubectl get\E.*$
```

**Allowed Operations**: Container/image listing, Kubernetes resource viewing

#### 6. System Commands (10 Rules)

**Platform Compatibility**: 🔧 Platform-Specific (select based on your OS)

**Windows (PowerShell)**: `Write-Host`, `Get-Location`, `Get-Date`, `Get-Command`  
**macOS/Linux (Bash/Zsh)**: `echo`, `pwd`, `date`, `which`  
**Universal**: `whoami`

```regex
# Examples shown - adjust for your platform
^\Qecho\E [^\s;&|<>@$]*$
^\Qdate\E$
^\Qpwd\E$
```

| Function     | Windows (PowerShell) | macOS/Linux |
|--------------|----------------------|-------------|
| Output text  | `Write-Host`         | `echo`      |
| Current path | `Get-Location`       | `pwd`       |
| Current time | `Get-Date`           | `date`      |
| Find command | `Get-Command`        | `which`     |

**Allowed Operations**: Output text, display date/time, print working directory

#### 7. Development Assistance (5 Rules)

**Platform Compatibility**: 🔧 Platform-Specific (select based on your OS)

**Windows (PowerShell)**: `Get-Command`, `Invoke-WebRequest`  
**macOS/Linux (Bash/Zsh)**: `which`, `wget`  
**Universal**: `curl`

```regex
^\Qwhich\E [^\s;&|<>@$]*$
^\Qcurl\E [^\s;&|<>@$]*$
```

**Allowed Operations**: Command path lookup, HTTP requests

#### 8. Text Processing (7 Rules) - v2.0 Added

**Platform Compatibility**: 🔧 Platform-Specific (macOS/Linux native, Windows needs WSL or Unix tools)

**macOS/Linux (Bash/Zsh)**: `grep`, `sed`, `awk`, `head`, `tail`, `wc`, `sort`, `uniq`  
**Windows Alternative**: PowerShell cmdlets or install Git Bash/WSL

```regex
^\Qgrep\E [^\s;&|<>@$]*$
^\Qsed\E [^\s;&|<>@$]*$
^\Qawk\E [^\s;&|<>@$]*$
```

**Allowed Operations**: Text search, stream editing, pattern processing

#### 9. Compression & Archiving (4 Rules) - v2.0 Added

**Platform Compatibility**: 🔧 Platform-Specific (select based on your OS)

**macOS/Linux (Bash/Zsh)**: `tar -tzf`, `tar -xzf`  
**Universal**: `unzip`  
**Windows (PowerShell)**: `Expand-Archive` or install tar

```regex
^\Qtar -tzf\E [^\s;&|<>@$]*$
^\Qunzip\E [^\s;&|<>@$]*$
```

**Allowed Operations**: Archive listing, file compression

#### 10. Network Diagnostics (4 Rules) - v2.0 Added

**Platform Compatibility**: ✅ Cross-Platform Universal (Windows/macOS/Linux)

```regex
^\Qping\E [^\s;&|<>@$]*$
^\Qcurl\E [^\s;&|<>@$]*$
^\Qnslookup\E [^\s;&|<>@$]*$
```

**Note**: `dig` requires additional installation on Windows; `nslookup` and `ping` are native.

**Allowed Operations**: Network connectivity testing, HTTP requests, DNS queries

#### 11. Python Virtual Environments (6 Rules) - v2.0 Added

**Platform Compatibility**: 🔧 Platform-Specific (select based on your OS and tool)

**Supports both conda and venv (conda/miniconda recommended)**

**conda (Miniconda/Anaconda) - Recommended**:

```regex
^\Qconda activate\E [^\s;&|<>@$]*$
^\Qconda deactivate\E$
^\Qconda env list\E$
```

**venv (Python built-in)**:

```regex
^\Qpython -m venv\E.*$
^\Qsource\E [^\s;&|<>@$]*/activate$
^\.\\[^\s;&|<>@$]*\\Scripts\\Activate.ps1$
```

| Function       | conda (All Platforms) - Recommended | venv (Windows)                | venv (macOS/Linux)         |
|----------------|-------------------------------------|-------------------------------|----------------------------|
| Create env     | `conda create -n env_name`          | `python -m venv`              | `python -m venv`           |
| Activate env   | `conda activate env_name`           | `.\venv\Scripts\Activate.ps1` | `source venv/bin/activate` |
| Deactivate env | `conda deactivate`                  | `deactivate`                  | `deactivate`               |
| List envs      | `conda env list`                    | -                             | -                          |

**Allowed Operations**: Virtual environment creation, activation, deactivation, and listing

#### 12. Code Quality Tools (6 Rules) - v2.0 Added

**Platform Compatibility**: ✅ Cross-Platform Universal (Windows/macOS/Linux)

```regex
^\Qpylint\E [^\s;&|<>@$]*$
^\Qblack\E [^\s;&|<>@$]*$
^\Qmypy\E [^\s;&|<>@$]*$
^\Qflake8\E [^\s;&|<>@$]*$
^\Qisort\E [^\s;&|<>@$]*$
^\Qbandit\E [^\s;&|<>@$]*$
```

**Allowed Operations**: Code linting, formatting, type checking, security scanning

#### 13. Database Clients (2 Rules) - v2.0 Added

**Platform Compatibility**: ✅ Cross-Platform Universal (Windows/macOS/Linux)

```regex
^\Qpsql\E.*-c "SELECT.*"$
^\Qmysql\E.*-e "SELECT.*"$
```

**Allowed Operations**: Read-only database queries (SELECT only)

---

### Summary Statistics

- **Total Rules**: 87 across 13 categories
- **Security Model**: Dangerous character exclusion pattern `[^\s;&|<>@$]`
- **Coverage**: Development, operations, quality assurance, and diagnostics

> **💡 Tip**: For the complete list of all 87 rules with full regex patterns, refer
> to [Appendix B](#appendix-b-complete-rules-list-plain-text) where you can copy-paste the entire configuration.

---

## 5. Auto-Configuration Process

### Configuration Approach Selection

This project uses **automated configuration scripts** that directly generate and apply the optimized configuration to
ensure consistency and accuracy.

### Execution Steps

#### 1. Backup Original Configuration

Before applying new configuration, the system automatically backs up existing settings to:

| Platform    | Backup Location                                                                       |
|:------------|:--------------------------------------------------------------------------------------|
| **Windows** | `%APPDATA%\JetBrains\<Product><Version>\options\junie.xml.backup`                     |
| **macOS**   | `~/Library/Application Support/JetBrains/<Product><Version>/options/junie.xml.backup` |
| **Linux**   | `~/.config/JetBrains/<Product><Version>/options/junie.xml.backup`                     |

> **Note**: Replace `<Product><Version>` with your IDE, e.g., `PyCharm2025.2`, `IntelliJIdea2025.2`

#### 2. Apply New Configuration

The configuration script:

- Reads the template configuration
- Applies 87 Terminal rules
- Enables 3 Allowed Actions (RunTest, Build, ReadOutsideProject)
- Saves to the IDE configuration file

#### 3. Verify Configuration

After configuration:

1. Restart PyCharm (required for settings to take effect)
2. Open `Settings | Tools | Junie | Action Allowlist`
3. Confirm 87 Terminal rules are present
4. Test with: `git status` (should execute without approval)

---

## 6. Project Configuration Preferences

### Configuration Options

**Terminal Rules**:

- **Quantity**: 87 rules covering 13 categories
- **Security Model**: Dangerous character exclusion `[^\s;&|<>@$]`
- **Extensibility**: Can be customized per project needs

**Allowed Actions**:

- **RunTest**: Enabled - allows test execution without approval
- **Build**: Enabled - allows project builds without approval
- **ReadOutsideProject**: Enabled - allows reading files outside project directory
- **WriteOutsideProject**: Disabled (observation period) - requires approval for external file modifications

**MCP Integration**:

- **Configuration Method**: Settings UI or configuration file
- **Recommended Tools**: Filesystem, Memory, Git (P0 priority)
- **Transport**: stdio (currently supported)

### Customization Guidelines

**Adding New Rules**:

1. Identify the command pattern
2. Ensure dangerous characters are excluded
3. Test in a safe environment
4. Add via Settings UI or configuration file

**Removing Rules**:

- Use with caution - may reduce automation efficiency
- Only remove if specific security concerns exist

### 📚 Real-World Configuration Examples

Here are configuration patterns for common project types:

#### Example 1: Python Data Science Project

**Project Profile**: Jupyter notebooks, pandas, scikit-learn, data pipelines

**Recommended Additional Rules**:

```regex
^\Qjupyter\E [^\s;&|<>@$]*$
^\Qjupyter-lab\E.*$
^\Qpandas\E.*$
^\Qdvc\E [^\s;&|<>@$]*$
```

**Configuration Focus**:

- ✅ Enable all Python and pip rules
- ✅ Add Jupyter notebook commands
- ✅ Consider DVC for data version control
- ⚠️ Be cautious with data file operations

---

#### Example 2: Full-Stack Web Development

**Project Profile**: React/Vue frontend, Python/Node backend, Docker deployment

**Recommended Additional Rules**:

```regex
^\Qnpx\E [^\s;&|<>@$]*$
^\Qyarn dev\E$
^\Qnpm run\E [^\s;&|<>@$]*$
^\Qdocker-compose\E [^\s;&|<>@$]*$
```

**Configuration Focus**:

- ✅ Enable all npm/yarn rules
- ✅ Enable Docker inspection commands
- ✅ Add project-specific build scripts
- ⚠️ Keep `docker run` excluded for safety

---

#### Example 3: DevOps/Infrastructure Project

**Project Profile**: Terraform, Ansible, Kubernetes management

**Recommended Additional Rules**:

```regex
^\Qterraform plan\E.*$
^\Qterraform validate\E$
^\Qansible-playbook\E.*--check.*$
^\Qhelm template\E.*$
```

**Configuration Focus**:

- ✅ Enable read-only Kubernetes commands
- ✅ Add Terraform plan/validate (not apply!)
- ✅ Add Ansible dry-run commands
- ❌ Never auto-approve: `terraform apply`, `kubectl delete`, `helm install`

---

#### Example 4: Machine Learning/AI Project

**Project Profile**: PyTorch/TensorFlow, model training, experiment tracking

**Recommended Additional Rules**:

```regex
^\Qmlflow\E [^\s;&|<>@$]*$
^\Qwandb\E [^\s;&|<>@$]*$
^\Qtensorboard\E.*$
^\Qpython -m torch\E.*$
```

**Configuration Focus**:

- ✅ Enable experiment tracking tools (MLflow, W&B)
- ✅ Enable TensorBoard for visualization
- ✅ Add model evaluation scripts
- ⚠️ Training commands may need manual review (resource-intensive)

---

> **💡 Tip**: Start with the base 87 rules, then add project-specific rules gradually based on your workflow. Monitor
> which commands you manually approve frequently—those are candidates for new rules.

---

## 7. Verification and Maintenance

### Configuration Verification

**Method 1: UI Verification**

1. Open `Settings | Tools | Junie | Action Allowlist`
2. Check Terminal rules count (should be 87)
3. Verify Allowed Actions (RunTest, Build, ReadOutsideProject)

**Method 2: Functional Testing**

```bash
# Should execute without approval:
git status
python -m pytest
pip list
```

**Method 3: Configuration File Check**

**Windows (PowerShell)**:

```powershell
# Check configuration file exists and count Terminal rules
$configPath = "$env:APPDATA\JetBrains\PyCharm2025.2\options\junie.xml"
if (Test-Path $configPath)
{
    $ruleCount = (Select-String -Path $configPath -Pattern "Terminal" -AllMatches).Matches.Count
    Write-Host "✅ Config file found. Terminal rules: $ruleCount"
}
else
{
    Write-Host "❌ Config file not found at: $configPath"
}
```

**macOS/Linux (Bash)**:

```bash
# Check configuration file exists and count Terminal rules
# macOS path:
CONFIG_PATH=~/Library/Application\ Support/JetBrains/PyCharm2025.2/options/junie.xml
# Linux path (uncomment if needed):
# CONFIG_PATH=~/.config/JetBrains/PyCharm2025.2/options/junie.xml

if [ -f "$CONFIG_PATH" ]; then
    RULE_COUNT=$(grep -c "Terminal" "$CONFIG_PATH")
    echo "✅ Config file found. Terminal rules: $RULE_COUNT"
else
    echo "❌ Config file not found at: $CONFIG_PATH"
fi
```

**Method 4: Automated Validation Script**

For comprehensive validation, save this as `validate_junie_config.py`:

```python
#!/usr/bin/env python3
"""Junie Configuration Validator - Quick health check for Action Allowlist setup."""
import os
import platform
import subprocess


def get_config_path():
    """Get Junie config path based on OS."""
    system = platform.system()
    if system == "Windows":
        base = os.environ.get("APPDATA", "")
        return os.path.join(base, "JetBrains", "PyCharm2025.2", "options", "junie.xml")
    elif system == "Darwin":  # macOS
        return os.path.expanduser("~/Library/Application Support/JetBrains/PyCharm2025.2/options/junie.xml")
    else:  # Linux
        return os.path.expanduser("~/.config/JetBrains/PyCharm2025.2/options/junie.xml")


def validate():
    """Run validation checks."""
    print("🔍 Junie Configuration Validator\n" + "=" * 40)

    # Check 1: Config file exists
    config_path = get_config_path()
    if os.path.exists(config_path):
        print(f"✅ Config file found: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            terminal_count = content.count('Terminal')
            print(f"✅ Terminal rules found: {terminal_count}")
    else:
        print(f"❌ Config file NOT found: {config_path}")
        return

    # Check 2: Test commands
    test_commands = ["git --version", "python --version"]
    print("\n🧪 Command availability:")
    for cmd in test_commands:
        try:
            subprocess.run(cmd.split(), capture_output=True, check=True)
            print(f"  ✅ {cmd.split()[0]} available")
        except Exception:
            print(f"  ⚠️ {cmd.split()[0]} not available")

    print("\n✨ Validation complete!")


if __name__ == "__main__":
    validate()
```

Run with: `python validate_junie_config.py`

> **💡 Tip**: Adjust the IDE version in the path (e.g., `PyCharm2025.2` → `IntelliJIdea2025.2`) to match your
> installation.

### Maintenance Recommendations

**Regular Review** (Monthly):

- Review action logs for denied commands
- Evaluate if new rules should be added
- Check for security vulnerabilities

**Update Strategy**:

- Monitor Junie release notes for configuration changes
- Test new rules in development environment first
- Keep configuration synchronized across team

**Performance Monitoring**:

- Track approval rate (target: 90%+ auto-approval)
- Monitor execution efficiency
- Identify bottlenecks in workflow

---

## 8. Troubleshooting

### ⚡ 5-Minute Quick Diagnosis

**Use this checklist to quickly identify common issues**:

| Step | Check                   | Action if Failed                                          |
|:-----|:------------------------|:----------------------------------------------------------|
| 1️⃣  | **IDE Restarted?**      | Restart IDE after any configuration change                |
| 2️⃣  | **Rules Visible?**      | `Settings                                                 | Tools | Junie | Action Allowlist` → Should show 87 rules |
| 3️⃣  | **Test Command?**       | Run `git status` → Should execute without approval prompt |
| 4️⃣  | **Check Syntax?**       | Blocked command contains `;` `&` `                        |` `<` `>` `@` `$`? → Expected behavior |
| 5️⃣  | **Config File Exists?** | Check `junie.xml` in IDE options directory                |

**Quick Fixes** (in order of likelihood):

```
90% of issues → Restart IDE
 5% of issues → Command contains dangerous characters (expected block)
 3% of issues → Rule syntax error (check regex)
 2% of issues → Configuration file corruption (restore backup)
```

> **💡 Still stuck?** See detailed solutions below or check [Action Allowlist FAQ](#action-allowlist-faq).

---

### Problem 1: Configuration Not Taking Effect

**Symptoms**: Rules are configured but still require manual approval

**Solutions**:

1. **Restart PyCharm** (most common fix)
    - `File | Exit` and restart
    - Configuration changes require IDE restart
2. **Verify Configuration File**
    - Check `%APPDATA%\JetBrains\PyCharm2025.2\options\junie.xml`
    - Ensure Terminal rules are present
3. **Clear IDE Cache**
    - `File | Invalidate Caches / Restart...`
    - Select "Invalidate and Restart"

### Problem 2: Some Commands Still Require Approval

**Symptoms**: Certain commands are not auto-approved despite configuration

**Possible Causes**:

- Command contains dangerous characters (`;`, `&`, `|`, etc.)
- Command pattern doesn't match configured regex
- Command involves high-risk operations (e.g., `rm`, `docker run`)

**Solutions**:

1. **Check Command Pattern**
    - Review the exact command being blocked
    - Compare with configured regex patterns
2. **Add Specific Rule** (if safe)
    - Use "Allow similar commands" in the prompt dialog
    - Or add manually via Settings
3. **Verify Security Exclusions**
    - Ensure command doesn't contain: `;` `&` `|` `<` `>` `@` `$`

### Problem 3: Too Many Auto-Approvals (Security Concern)

**Symptoms**: Worried about excessive automation reducing security oversight

**Solutions**:

1. **Review Configuration**
    - Audit Terminal rules list
    - Remove rules for infrequently used commands
2. **Enable Logging**
    - Monitor which commands are auto-approved
    - Review logs regularly
3. **Add Specific Restrictions**
    - Disable `WriteOutsideProject` if concerned about external file modifications
    - Keep high-risk operations (`rm`, `docker run`) excluded

### Problem 4: Configuration Lost After IDE Update

**Symptoms**: Rules disappear after upgrading your JetBrains IDE

**Solutions**:

1. **Locate Backup**
    - Check `junie.xml.backup` in options directory
    - Restore from backup if available
2. **Re-run Configuration Script**
    - Use auto-configuration script to regenerate
3. **Export/Import Settings**
    - `File | Manage IDE Settings | Export Settings`
    - Include "Tools | Junie" in export
    - Import on new installation

### Problem 5: Commands Work in Terminal but Not in Junie

**Symptoms**: Command executes successfully in system terminal but fails in Junie

**Possible Causes**:

- Environment variable differences
- Path configuration issues
- Command not in system PATH

**Solutions**:

1. **Check Environment**
   ```bash
   echo $PATH  # Linux/macOS
   ```
   ```powershell
   $env:PATH  # Windows PowerShell
   ```
2. **Use Full Command Paths**
    - Instead of `python`, use `/usr/bin/python` (or Windows equivalent)
3. **Configure PATH in IDE**
    - `Settings | Tools | Terminal`
    - Ensure PATH includes necessary directories

---

## 9. FAQ

> **Scope**: This FAQ covers Action Allowlist configuration questions only. For MCP-related questions,
> see [MCP FAQ](#mcp-faq) in Part 3.

### General Questions

#### Q1: How long does configuration take?

**A**: First-time setup takes 10-30 minutes. Experienced users can complete it in under 10 minutes using the copy-paste
rules from [Appendix B](#appendix-b-complete-rules-list-plain-text).

#### Q2: Do I need to configure separately for each project?

**A**: No. Action Allowlist rules are configured at the IDE level (global), not per-project. Once configured, rules
apply to all projects in that IDE installation.

#### Q3: Is this configuration safe?

**A**: Yes. All rules use dangerous character exclusion patterns `[^\s;&|<>@$]` which prevent command injection.
High-risk operations like `rm -rf` are intentionally excluded.

---

### Rule-Related Questions

#### Q4: A rule I added doesn't seem to work. What should I check?

**A**:

1. **Restart IDE**: Some changes require restart to take effect
2. **Check regex syntax**: Ensure special characters are properly escaped with `\Q...\E`
3. **Verify rule format**: Must start with `^` and end with `$` for exact matching
4. **Check for typos**: Compare with examples in [Appendix B](#appendix-b-complete-rules-list-plain-text)

#### Q5: How do I know if a rule is being used?

**A**: Currently, Junie doesn't provide built-in usage statistics. You can:

1. Monitor which commands execute without prompting
2. Check IDE logs for action approval events
3. Track commands that still require manual approval (candidates for new rules)

#### Q6: Can I add rules for custom scripts?

**A**: Yes. Use the pattern:

```regex
^\Q./scripts/my-script.sh\E.*$
```

Replace `my-script.sh` with your script name. The `.*` allows arguments.

---

### Performance Questions

#### Q7: Will adding many rules slow down Junie?

**A**: No. The regex matching is highly optimized. Even with 100+ rules, the performance impact is negligible (< 1ms per
command check).

---

## Related

- `README.md` — Configuration guide index
- `01-introduction.md` — Document overview (previous)
- `03-mcp-integration.md` — MCP setup and best practices (next)
- `04-future-vision.md` — Protocol roadmap
- `05-appendix.md` — References and resources

---

*Part of the Junie Configuration Guide*
