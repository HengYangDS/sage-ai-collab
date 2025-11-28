"""
SAGE Knowledge Base - Main Entry Point.

Enables running the package as a module:
    python -m sage [command] [options]

This is equivalent to running the CLI directly:
    sage [command] [options]

Version: 0.1.0
"""

from sage.services.cli import main

if __name__ == "__main__":
    main()
