# Shell Script Guidelines

> Best practices for Bash and shell scripting

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Script Structure](#2-script-structure)
- [3. Variables](#3-variables)
- [4. Control Flow](#4-control-flow)
- [5. Functions](#5-functions)
- [6. Error Handling](#6-error-handling)
- [7. Best Practices](#7-best-practices)
- [8. Common Patterns](#8-common-patterns)

---

## 1. Overview

### 1.1 Core Principles

| Principle       | Description                              |
|-----------------|------------------------------------------|
| **Safety**      | Use strict mode, handle errors           |
| **Clarity**     | Write readable, self-documenting scripts |
| **Portability** | Consider POSIX compatibility             |
| **Idempotent**  | Safe to run multiple times               |

### 1.2 File Conventions

| Element      | Convention         | Example         |
|--------------|--------------------|-----------------|
| Script files | `snake_case.sh`    | `deploy_app.sh` |
| Functions    | `snake_case`       | `check_status`  |
| Constants    | `UPPER_SNAKE_CASE` | `MAX_RETRIES`   |
| Variables    | `lower_snake_case` | `output_dir`    |

---

## 2. Script Structure

### 2.1 Standard Template

```bash
#!/usr/bin/env bash
#
# Script: script_name.sh
# Description: Brief description of what this script does
# Usage: ./script_name.sh [options] <arguments>
#
# Author: Your Name
# Date: 2024-01-01

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

log_info() { log "INFO" "$@"; }
log_warn() { log "WARN" "$@"; }
log_error() { log "ERROR" "$@"; }

cleanup() {
    # Cleanup code here
    log_info "Cleaning up..."
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
            *)
                break
                ;;
        esac
    done
    
    # Main logic here
    log_info "Starting ${SCRIPT_NAME}"
}

main "$@"
```
### 2.2 Shebang Lines

```bash
# ✅ Preferred - Portable
#!/usr/bin/env bash

# ✅ Also acceptable - Direct path
#!/bin/bash

# ⚠️ POSIX shell only
#!/bin/sh
```
### 2.3 Strict Mode

```bash
# Enable strict mode
set -euo pipefail

# -e: Exit on error
# -u: Error on undefined variables
# -o pipefail: Catch errors in pipelines

# Optional: Debug mode
set -x  # Print commands as they execute
```
---

## 3. Variables

### 3.1 Variable Declaration

```bash
# ✅ Good - Quoted variables
name="John Doe"
path="/path/with spaces/file.txt"

# ✅ Good - Use braces for clarity
echo "Hello, ${name}!"
echo "${path}/subdir"

# ✅ Good - Readonly for constants
readonly MAX_RETRIES=3
readonly CONFIG_FILE="/etc/app/config.yaml"

# ✅ Good - Local variables in functions
my_function() {
    local result=""
    local count=0
    # ...
}
```
### 3.2 Default Values

```bash
# Default value if unset
name="${NAME:-default_name}"

# Default value if unset or empty
name="${NAME:-}"

# Assign default if unset
: "${NAME:=default_name}"

# Error if unset
name="${NAME:?'NAME is required'}"
```
### 3.3 Arrays

```bash
# Declare array
declare -a files=("file1.txt" "file2.txt" "file3.txt")

# Add to array
files+=("file4.txt")

# Access elements
echo "${files[0]}"       # First element
echo "${files[@]}"       # All elements
echo "${#files[@]}"      # Array length

# Iterate
for file in "${files[@]}"; do
    echo "Processing: ${file}"
done

# Associative array (Bash 4+)
declare -A config
config[host]="localhost"
config[port]="8080"
echo "${config[host]}:${config[port]}"
```
---

## 4. Control Flow

### 4.1 Conditionals

```bash
# ✅ Good - Use [[ ]] for tests
if [[ -f "${file}" ]]; then
    echo "File exists"
elif [[ -d "${file}" ]]; then
    echo "Is a directory"
else
    echo "Does not exist"
fi

# String comparisons
if [[ "${name}" == "admin" ]]; then
    echo "Admin user"
fi

if [[ "${name}" =~ ^[A-Z] ]]; then
    echo "Starts with uppercase"
fi

# Numeric comparisons
if [[ "${count}" -gt 10 ]]; then
    echo "Count is greater than 10"
fi

# Combining conditions
if [[ -f "${file}" && -r "${file}" ]]; then
    echo "File exists and is readable"
fi
```
### 4.2 Test Operators

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

### 4.3 Loops

```bash
# For loop with list
for item in apple banana cherry; do
    echo "Fruit: ${item}"
done

# For loop with array
for file in "${files[@]}"; do
    process "${file}"
done

# For loop with range
for i in {1..10}; do
    echo "Number: ${i}"
done

# C-style for loop
for ((i=0; i<10; i++)); do
    echo "Index: ${i}"
done

# While loop
while read -r line; do
    echo "Line: ${line}"
done < input.txt

# While with condition
count=0
while [[ "${count}" -lt 10 ]]; do
    ((count++))
done
```
### 4.4 Case Statement

```bash
case "${command}" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        stop_service
        start_service
        ;;
    status|info)
        show_status
        ;;
    *)
        echo "Unknown command: ${command}"
        exit 1
        ;;
esac
```
---

## 5. Functions

### 5.1 Function Definition

```bash
# ✅ Good - Standard function
process_file() {
    local file="$1"
    local output="$2"
    
    if [[ ! -f "${file}" ]]; then
        log_error "File not found: ${file}"
        return 1
    fi
    
    # Process file...
    cat "${file}" > "${output}"
    return 0
}

# Usage
if process_file "input.txt" "output.txt"; then
    echo "Success"
else
    echo "Failed"
fi
```
### 5.2 Return Values

```bash
# Return status code
check_status() {
    if [[ -f "/tmp/healthy" ]]; then
        return 0  # Success
    else
        return 1  # Failure
    fi
}

# Capture output
get_version() {
    echo "1.0.0"
}
version=$(get_version)

# Return multiple values via global
get_dimensions() {
    RESULT_WIDTH=1920
    RESULT_HEIGHT=1080
}
get_dimensions
echo "Width: ${RESULT_WIDTH}, Height: ${RESULT_HEIGHT}"
```
### 5.3 Arguments

```bash
process_args() {
    local positional=()
    local verbose=false
    local output=""
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -v|--verbose)
                verbose=true
                shift
                ;;
            -o|--output)
                output="$2"
                shift 2
                ;;
            --)
                shift
                positional+=("$@")
                break
                ;;
            -*)
                echo "Unknown option: $1" >&2
                return 1
                ;;
            *)
                positional+=("$1")
                shift
                ;;
        esac
    done
    
    # Restore positional arguments
    set -- "${positional[@]}"
    
    echo "Verbose: ${verbose}"
    echo "Output: ${output}"
    echo "Args: $*"
}
```
---

## 6. Error Handling

### 6.1 Exit Codes

```bash
# Standard exit codes
readonly EXIT_SUCCESS=0
readonly EXIT_ERROR=1
readonly EXIT_USAGE=2

# Exit on error
if ! command_that_might_fail; then
    log_error "Command failed"
    exit "${EXIT_ERROR}"
fi

# Check last command
some_command
if [[ $? -ne 0 ]]; then
    log_error "Command failed with status: $?"
fi
```
### 6.2 Trap for Cleanup

```bash
# Cleanup on exit
cleanup() {
    local exit_code=$?
    
    # Remove temp files
    if [[ -n "${TEMP_DIR:-}" && -d "${TEMP_DIR}" ]]; then
        rm -rf "${TEMP_DIR}"
    fi
    
    # Restore state
    if [[ -n "${ORIGINAL_DIR:-}" ]]; then
        cd "${ORIGINAL_DIR}"
    fi
    
    exit "${exit_code}"
}

trap cleanup EXIT INT TERM

# Now safe to create temp resources
TEMP_DIR=$(mktemp -d)
ORIGINAL_DIR=$(pwd)
```
### 6.3 Error Messages

```bash
# ✅ Good - Informative error messages
die() {
    local message="$1"
    local code="${2:-1}"
    
    log_error "${message}"
    exit "${code}"
}

# Usage
[[ -f "${config_file}" ]] || die "Config file not found: ${config_file}"
[[ -n "${API_KEY:-}" ]] || die "API_KEY environment variable is required"
```
---

## 7. Best Practices

### 7.1 Quoting

```bash
# ✅ Always quote variables
echo "${variable}"
cp "${source}" "${destination}"

# ✅ Quote command substitution
result="$(some_command)"

# ✅ Quote in conditionals
if [[ "${var}" == "value" ]]; then

# ⚠️ Exception: Arithmetic
count=$((count + 1))
```
### 7.2 Command Substitution

```bash
# ✅ Good - Modern syntax
result=$(command)
files=$(ls -la)

# ❌ Avoid - Legacy syntax
result=`command`

# ✅ Good - Nested substitution
result=$(command1 "$(command2)")
```
### 7.3 Safe Temporary Files

```bash
# ✅ Good - Use mktemp
temp_file=$(mktemp)
temp_dir=$(mktemp -d)

# Clean up with trap
trap 'rm -f "${temp_file}"' EXIT

# ❌ Bad - Predictable names
temp_file="/tmp/myapp_temp"
```
### 7.4 Safe File Operations

```bash
# ✅ Good - Check before operations
if [[ -f "${file}" ]]; then
    rm "${file}"
fi

# ✅ Good - Use -- for files starting with -
rm -- "${file}"
cat -- "${file}"

# ✅ Good - Handle spaces in filenames
while IFS= read -r -d '' file; do
    process "${file}"
done < <(find . -type f -print0)
```
---

## 8. Common Patterns

### 8.1 Script Self-Location

```bash
# Get script directory (handles symlinks)
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"

# Or simpler version
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
```
### 8.2 Configuration Loading

```bash
# Load config file
load_config() {
    local config_file="${1:-config.sh}"
    
    if [[ -f "${config_file}" ]]; then
        # shellcheck source=/dev/null
        source "${config_file}"
    else
        log_warn "Config file not found: ${config_file}"
    fi
}
```
### 8.3 Logging

```bash
# Colored logging
log() {
    local level="$1"
    shift
    local color=""
    local reset="\033[0m"
    
    case "${level}" in
        INFO)  color="\033[32m" ;;  # Green
        WARN)  color="\033[33m" ;;  # Yellow
        ERROR) color="\033[31m" ;;  # Red
        DEBUG) color="\033[36m" ;;  # Cyan
    esac
    
    echo -e "${color}[${level}]${reset} $*" >&2
}
```
### 8.4 Retry Pattern

```bash
retry() {
    local max_attempts="${1:-3}"
    local delay="${2:-1}"
    shift 2
    local cmd=("$@")
    
    local attempt=1
    while [[ "${attempt}" -le "${max_attempts}" ]]; do
        if "${cmd[@]}"; then
            return 0
        fi
        
        log_warn "Attempt ${attempt}/${max_attempts} failed, retrying in ${delay}s..."
        sleep "${delay}"
        ((attempt++))
    done
    
    log_error "All ${max_attempts} attempts failed"
    return 1
}

# Usage
retry 3 5 curl -f "https://api.example.com/health"
```
### 8.5 Progress Indicator

```bash
spinner() {
    local pid="$1"
    local delay=0.1
    local spinstr='|/-\'
    
    while ps -p "${pid}" > /dev/null 2>&1; do
        local temp=${spinstr#?}
        printf " [%c]  " "${spinstr}"
        spinstr=${temp}${spinstr%"$temp"}
        sleep "${delay}"
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# Usage
long_running_command &
spinner $!
```
---

## Quick Reference

### Common Commands

| Task              | Command                     |
|-------------------|-----------------------------|
| Check file exists | `[[ -f file ]]`             |
| Check dir exists  | `[[ -d dir ]]`              |
| Check var set     | `[[ -n "${var:-}" ]]`       |
| String match      | `[[ "${str}" == "value" ]]` |
| Regex match       | `[[ "${str}" =~ pattern ]]` |
| Numeric compare   | `[[ "${n}" -gt 10 ]]`       |

### Checklist

| Check             | Description           |
|-------------------|-----------------------|
| ☐ Shebang         | `#!/usr/bin/env bash` |
| ☐ Strict mode     | `set -euo pipefail`   |
| ☐ Quote variables | `"${var}"`            |
| ☐ Local variables | `local var=""`        |
| ☐ Error handling  | Trap and exit codes   |
| ☐ shellcheck      | No warnings           |

---

## Related

- `.knowledge/guidelines/CODE_STYLE.md` — General code style
- `.knowledge/practices/engineering/ERROR_HANDLING.md` — Error handling patterns

---

*AI Collaboration Knowledge Base*
