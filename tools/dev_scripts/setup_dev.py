"""
Development Environment Setup Script.

This script sets up the development environment for SAGE Knowledge Base.

Features:
- Install development dependencies
- Setup pre-commit hooks
- Create the necessary directories
- Verify configuration files

Usage:
    python -m tools.dev_scripts.setup_dev
    python -m tools.dev_scripts.setup_dev --skip-hooks
    python -m tools.dev_scripts.setup_dev --verify-only

Author: SAGE AI Collab Team
Version: 0.1.0
"""

import argparse
import subprocess
import sys
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    print(f"  Running: {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def install_dependencies(dev: bool = True) -> bool:
    """Install project dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        if dev:
            result = run_command(
                [sys.executable, "-m", "pip", "install", "-e", ".[dev]"]
            )
        else:
            result = run_command([sys.executable, "-m", "pip", "install", "-e", "."])
        print("  ✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Failed to install dependencies: {e.stderr}")
        return False


def setup_pre_commit() -> bool:
    """Setup pre-commit hooks."""
    print("\n🪝 Setting up pre-commit hooks...")
    project_root = get_project_root()
    pre_commit_config = project_root / ".pre-commit-config.yaml"

    if not pre_commit_config.exists():
        print("  ⚠️ .pre-commit-config.yaml not found, skipping hooks setup")
        return True

    try:
        run_command(["pre-commit", "install"])
        print("  ✅ Pre-commit hooks installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Failed to setup pre-commit: {e.stderr}")
        return False
    except FileNotFoundError:
        print("  ⚠️ pre-commit not found, install with: pip install pre-commit")
        return False


def create_directories() -> bool:
    """Create necessary project directories."""
    print("\n📁 Creating directories...")
    project_root = get_project_root()

    directories = [
        project_root / "tests" / "fixtures" / "sample_content",
        project_root / "tests" / "fixtures" / "mock_responses",
        project_root / "tests" / "fixtures" / "configs",
        project_root / "tests" / "unit" / "core",
        project_root / "tests" / "unit" / "services",
        project_root / "tests" / "integration",
        project_root / "tests" / "performance" / "benchmarks",
        project_root / ".history" / "current",
        project_root / ".history" / "conversations",
        project_root / ".history" / "handoffs",
    ]

    for directory in directories:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  Created: {directory.relative_to(project_root)}")
        else:
            print(f"  Exists: {directory.relative_to(project_root)}")

    print("  ✅ Directories created")
    return True


def verify_config_files() -> bool:
    """Verify required configuration files exist."""
    print("\n📄 Verifying configuration files...")
    project_root = get_project_root()

    required_files = [
        ("pyproject.toml", True),
        ("README.md", True),
        (".gitignore", True),
        ("sage.yaml", False),  # Optional - will be created
        ("index.md", False),  # Optional - will be created
    ]

    all_present = True
    for filename, required in required_files:
        filepath = project_root / filename
        if filepath.exists():
            print(f"  ✅ {filename}")
        elif required:
            print(f"  ❌ {filename} (required)")
            all_present = False
        else:
            print(f"  ⚠️ {filename} (optional, not found)")

    return all_present


def verify_imports() -> bool:
    """Verify that package imports work correctly."""
    print("\n🔍 Verifying package imports...")
    try:
        from sage import KnowledgeLoader, Layer

        print("  ✅ sage.KnowledgeLoader")

        from sage.core.loader import LoadResult

        print("  ✅ sage.core.loader.LoadResult")

        from sage.services.cli import app

        print("  ✅ sage.services.cli.app")

        from sage.capabilities import QualityAnalyzer, HealthMonitor

        print("  ✅ sage.capabilities")

        print("  ✅ All imports successful")
        return True
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False


def setup_development_environment(
    skip_hooks: bool = False,
    verify_only: bool = False,
) -> bool:
    """
    Setup the complete development environment.

    Args:
        skip_hooks: Skip pre-commit hooks setup
        verify_only: Only verify, don't install anything

    Returns:
        True if setup was successful
    """
    print("=" * 60)
    print("🚀 SAGE Knowledge Base - Development Setup")
    print("=" * 60)

    success = True

    if verify_only:
        print("\n[Verify Only Mode]")
        success &= verify_config_files()
        success &= verify_imports()
    else:
        success &= install_dependencies(dev=True)
        success &= create_directories()
        if not skip_hooks:
            success &= setup_pre_commit()
        success &= verify_config_files()
        success &= verify_imports()

    print("\n" + "=" * 60)
    if success:
        print("✅ Development environment setup complete!")
    else:
        print("⚠️ Setup completed with warnings - check messages above")
    print("=" * 60)

    return success


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Setup SAGE Knowledge Base development environment"
    )
    parser.add_argument(
        "--skip-hooks",
        action="store_true",
        help="Skip pre-commit hooks installation",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify setup, don't install anything",
    )

    args = parser.parse_args()

    success = setup_development_environment(
        skip_hooks=args.skip_hooks,
        verify_only=args.verify_only,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
