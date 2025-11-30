# Shell Script Patterns

> Common patterns and practices for Bash scripting

---

## Table of Contents

- [1. Variable Patterns](#1-variable-patterns)
- [2. Control Flow Patterns](#2-control-flow-patterns)
- [3. Function Patterns](#3-function-patterns)
- [4. Error Handling Patterns](#4-error-handling-patterns)
- [5. Utility Patterns](#5-utility-patterns)

---

## 1. Variable Patterns

### 1.1 Declaration & Defaults

```bash
# Quoted variables
name="John Doe"
path="/path/with spaces/file.txt"

# Default values
name="${NAME:-default_name}"      # Default if unset
name="${NAME:?'NAME required'}"   # Error if unset

# Constants
readonly MAX_RETRIES=3
readonly CONFIG_FILE="/etc/app/config.yaml"

# Local in functions
my_function() {
    local result=""
    local count=0
}
```

### 1.2 Arrays

```bash
# Indexed array
declare -a files=("file1.txt" "file2.txt")
files+=("file3.txt")              # Append
echo "${files[0]}"                # First element
echo "${#files[@]}"               # Length

# Iterate
for file in "${files[@]}"; do
    process "${file}"
done

# Associative array (Bash 4+)
declare -A config
config[host]="localhost"
config[port]="8080"
```

---

## 2. Control Flow Patterns

### 2.1 Conditionals

```bash
# File tests
if [[ -f "${file}" ]]; then
    echo "File exists"
elif [[ -d "${file}" ]]; then
    echo "Is directory"
fi

# String comparison
[[ "${name}" == "admin" ]] && echo "Admin user"
[[ "${name}" =~ ^[A-Z] ]] && echo "Starts uppercase"

# Numeric comparison
[[ "${count}" -gt 10 ]] && echo "Greater than 10"

# Combined conditions
[[ -f "${file}" && -r "${file}" ]] && cat "${file}"
```

### 2.2 Loops

```bash
# For with list
for item in apple banana cherry; do
    echo "${item}"
done

# For with range
for i in {1..10}; do
    echo "${i}"
done

# While read file
while IFS= read -r line; do
    echo "${line}"
done < input.txt

# While with condition
count=0
while [[ "${count}" -lt 10 ]]; do
    ((count++))
done
```

### 2.3 Case Statement

```bash
case "${command}" in
    start)
        start_service
        ;;
    stop|kill)
        stop_service
        ;;
    *)
        echo "Unknown: ${command}" >&2
        exit 1
        ;;
esac
```

---

## 3. Function Patterns

### 3.1 Basic Function

```bash
process_file() {
    local file="$1"
    local output="${2:-/dev/stdout}"
    
    [[ -f "${file}" ]] || return 1
    cat "${file}" > "${output}"
}

# Usage
if process_file "input.txt" "output.txt"; then
    echo "Success"
fi
```

### 3.2 Return Values

```bash
# Status code
check_health() {
    [[ -f "/tmp/healthy" ]] && return 0 || return 1
}

# Output capture
get_version() {
    echo "1.0.0"
}
version=$(get_version)

# Multiple values via globals
get_dimensions() {
    RESULT_WIDTH=1920
    RESULT_HEIGHT=1080
}
```

### 3.3 Argument Parsing

```bash
parse_args() {
    local positional=()
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -v|--verbose) VERBOSE=true; shift ;;
            -o|--output)  OUTPUT="$2"; shift 2 ;;
            --)           shift; positional+=("$@"); break ;;
            -*)           echo "Unknown: $1" >&2; return 1 ;;
            *)            positional+=("$1"); shift ;;
        esac
    done
    
    set -- "${positional[@]}"
}
```

---

## 4. Error Handling Patterns

### 4.1 Exit Codes

```bash
readonly EXIT_SUCCESS=0
readonly EXIT_ERROR=1
readonly EXIT_USAGE=2

# Check command result
if ! command_that_might_fail; then
    log_error "Command failed"
    exit "${EXIT_ERROR}"
fi
```

### 4.2 Trap & Cleanup

```bash
cleanup() {
    local exit_code=$?
    [[ -d "${TEMP_DIR:-}" ]] && rm -rf "${TEMP_DIR}"
    exit "${exit_code}"
}

trap cleanup EXIT INT TERM

# Safe to create temp resources
TEMP_DIR=$(mktemp -d)
```

### 4.3 Die Function

```bash
die() {
    echo "ERROR: $1" >&2
    exit "${2:-1}"
}

# Guard clauses
[[ -f "${config}" ]] || die "Config not found: ${config}"
[[ -n "${API_KEY:-}" ]] || die "API_KEY required"
```

---

## 5. Utility Patterns

### 5.1 Colored Logging

```bash
log() {
    local level="$1"; shift
    local color reset="\033[0m"
    
    case "${level}" in
        INFO)  color="\033[32m" ;;  # Green
        WARN)  color="\033[33m" ;;  # Yellow
        ERROR) color="\033[31m" ;;  # Red
    esac
    
    echo -e "${color}[${level}]${reset} $*" >&2
}
```

### 5.2 Retry Pattern

```bash
retry() {
    local max="${1:-3}" delay="${2:-1}"; shift 2
    local attempt=1
    
    while [[ "${attempt}" -le "${max}" ]]; do
        if "$@"; then return 0; fi
        echo "Attempt ${attempt}/${max} failed, retry in ${delay}s..." >&2
        sleep "${delay}"
        ((attempt++))
    done
    return 1
}

# Usage
retry 3 5 curl -f "https://api.example.com/health"
```

### 5.3 Progress Spinner

```bash
spinner() {
    local pid="$1" spin='|/-\'
    
    while kill -0 "${pid}" 2>/dev/null; do
        printf " [%c] " "${spin:0:1}"
        spin="${spin:1}${spin:0:1}"
        sleep 0.1
        printf "\b\b\b\b\b"
    done
}

# Usage
long_command & spinner $!
```

### 5.4 Config Loading

```bash
load_config() {
    local config="${1:-config.sh}"
    
    if [[ -f "${config}" ]]; then
        # shellcheck source=/dev/null
        source "${config}"
    else
        echo "Config not found: ${config}" >&2
    fi
}
```

### 5.5 Safe File Operations

```bash
# Handle filenames with spaces
while IFS= read -r -d '' file; do
    process "${file}"
done < <(find . -type f -print0)

# Handle files starting with dash
rm -- "${file}"
cat -- "${file}"
```

---

## Related

- `.knowledge/guidelines/SHELL.md` — Shell script guidelines
- `.knowledge/templates/SHELL_SCRIPT.md` — Standard script template
- `.knowledge/practices/engineering/ERROR_HANDLING.md` — General error handling

---

*AI Collaboration Knowledge Base*
