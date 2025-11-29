#!/usr/bin/env python3
"""SAGE Architecture Checker.

Validates that code follows the three-layer architecture rules:
- Core layer: Cannot import from services or capabilities
- Services layer: Cannot import from capabilities
- Capabilities layer: Can import from any layer

Uses AST static analysis - no external dependencies required.
"""

import ast
import sys
from pathlib import Path

# Architecture layer rules
# Key: layer path prefix, Value: dict with forbidden imports
LAYER_RULES = {
    "src/sage/core": {
        "forbidden": ["sage.services", "sage.capabilities"],
        "description": "Core layer",
    },
    "src/sage/services": {
        "forbidden": ["sage.capabilities"],
        "description": "Services layer",
    },
    "src/sage/capabilities": {
        "forbidden": [],
        "description": "Capabilities layer",
    },
}


def get_layer(file_path: Path) -> str | None:
    """Determine which layer a file belongs to."""
    path_str = str(file_path).replace("\\", "/")

    for layer_path in LAYER_RULES:
        if layer_path in path_str:
            return layer_path

    return None


def extract_imports(file_path: Path) -> list[str]:
    """Extract all import statements from a Python file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content)
    except SyntaxError:
        return []
    except Exception:
        return []

    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return imports


def check_file(file_path: Path) -> list[str]:
    """Check a single file for architecture violations."""
    errors = []

    # Determine layer
    layer = get_layer(file_path)
    if not layer:
        return []  # Not in a monitored layer

    rules = LAYER_RULES[layer]
    forbidden = rules["forbidden"]

    if not forbidden:
        return []  # No restrictions for this layer

    # Extract imports
    imports = extract_imports(file_path)

    # Check for violations
    for imp in imports:
        for forbidden_prefix in forbidden:
            if imp.startswith(forbidden_prefix):
                errors.append(
                    f"{file_path}: {rules['description']} cannot import '{imp}' "
                    f"(forbidden: {forbidden_prefix})"
                )

    return errors


def get_python_files() -> list[Path]:
    """Get all Python files in the source directory."""
    src_path = Path("src/sage")

    if not src_path.exists():
        return []

    return list(src_path.rglob("*.py"))


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Check SAGE architecture rules")
    parser.add_argument("files", nargs="*", help="Specific files to check")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # Get files to check
    if args.files:
        files = [Path(f) for f in args.files if f.endswith(".py")]
    else:
        files = get_python_files()

    if args.verbose:
        print(f"Checking architecture in {len(files)} files...")
        print("\nLayer rules:")
        for layer, rules in LAYER_RULES.items():
            if rules["forbidden"]:
                print(f"  {rules['description']} ({layer}):")
                print(f"    Cannot import: {', '.join(rules['forbidden'])}")

    # Check all files
    all_errors = []
    for file_path in files:
        errors = check_file(file_path)
        all_errors.extend(errors)

    # Report results
    if all_errors:
        print("\n❌ Architecture violations found:")
        for error in all_errors:
            print(f"  {error}")
        return 1
    else:
        if args.verbose:
            print(f"\n✅ All {len(files)} files follow architecture rules")
        return 0


if __name__ == "__main__":
    sys.exit(main())
