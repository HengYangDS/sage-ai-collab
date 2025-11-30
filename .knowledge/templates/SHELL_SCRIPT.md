# Shell Script Template

> Standard Bash script template with best practices

---

## Table of Contents

- [1. Usage](#1-usage)
- [2. Template](#2-template)
- [3. Customization](#3-customization)

---

## 1. Usage

### Quick Start

```bash
# Copy template to new script
cp template.sh my_script.sh
# Make executable
chmod +x my_script.sh
# Run
./my_script.sh --help
```

### When to Use

| Scenario | Recommendation |
|----------|----------------|
| Simple one-liner | No template needed |
| Quick automation | Minimal template |
| Production script | Full template |
| Shared tooling | Full template + tests |

---

## 2. Template

```bash
#!/usr/bin/env bash
#
# Script: script_name.sh
# Description: Brief description of what this script does
# Usage: ./script_name.sh [options] <arguments>
#
set -euo pipefail
IFS=$'\n\t'
# =============================================================================
# Constants
# =============================================================================
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
# =============================================================================
# Configuration
# =============================================================================
LOG_LEVEL="${LOG_LEVEL:-INFO}"
OUTPUT_DIR="${OUTPUT_DIR:-./output}"
# =============================================================================
# Functions
# =============================================================================
usage() {
    cat << EOF
Usage: ${SCRIPT_NAME} [options] <argument>
Description:
    Brief description of what the script does.
Options:
    -h, --help      Show this help message
    -v, --verbose   Enable verbose output
    -d, --dry-run   Show what would be done
Arguments:
    argument        Description of the argument
Examples:
    ${SCRIPT_NAME} --verbose input.txt
    ${SCRIPT_NAME} -d /path/to/dir
EOF
}
log() {
    local level="$1"
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [${level}] $*" >&2
}
log_info()  { log "INFO" "$@"; }
log_warn()  { log "WARN" "$@"; }
log_error() { log "ERROR" "$@"; }
die() {
    log_error "$1"
    exit "${2:-1}"
}
cleanup() {
    log_info "Cleaning up..."
    # Add cleanup code here
}
# =============================================================================
# Main
# =============================================================================
main() {
    trap cleanup EXIT
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                usage
                exit 0
                ;;
            -v|--verbose)
                LOG_LEVEL="DEBUG"
                shift
                ;;
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            *)
                break
                ;;
        esac
    done
    
    # Validate arguments
    [[ $# -ge 1 ]] || { usage; die "Missing required argument"; }
    
    # Main logic here
    log_info "Starting ${SCRIPT_NAME}"
}
main "$@"
```

---

## 3. Customization

### Minimal Version

For simple scripts, use this reduced template:

```bash
#!/usr/bin/env bash
set -euo pipefail
die() { echo "ERROR: $1" >&2; exit 1; }
main() {
    [[ $# -ge 1 ]] || die "Usage: $0 <argument>"
    
    # Your code here
    echo "Processing: $1"
}
main "$@"
```

### Adding Features

| Feature | Add to Template |
|---------|-----------------|
| Color output | Add color codes to `log()` |
| Config file | Add `load_config()` function |
| Retry logic | Add `retry()` function |
| Progress | Add `spinner()` function |

> See `.knowledge/practices/engineering/languages/SHELL_PATTERNS.md` for implementations.

---

## Related

- `.knowledge/guidelines/SHELL.md` — Shell script guidelines
- `.knowledge/practices/engineering/languages/SHELL_PATTERNS.md` — Common patterns

---

*AI Collaboration Knowledge Base*
