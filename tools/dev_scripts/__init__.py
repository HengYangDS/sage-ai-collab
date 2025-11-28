"""
Development Scripts - Dev-only utilities for project setup and maintenance.

This module provides development utilities that are NOT imported at runtime.
They are only used during development setup and maintenance tasks.

Scripts:
- setup_dev.py: Development environment setup

Usage:
    # From command line
    python -m tools.dev_scripts.setup_dev

    # Or import when needed (dev only)
    from tools.dev_scripts.setup_dev import setup_development_environment

Author: SAGE AI Collab Team
Version: 0.1.0
"""

__all__ = [
    "setup_dev",
]
