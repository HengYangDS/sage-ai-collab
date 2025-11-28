"""
Migration Toolkit - Safe migration with backup and rollback support.

This module provides:
- MigrationStep: Individual migration step definition
- MigrationPlan: Complete migration plan
- MigrationResult: Result of a migration
- MigrationToolkit: Execute migrations safely.

Author: SAGE AI Collab Team
Version: 2.0.0
"""

import json
import logging
import shutil
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class MigrationStatus(Enum):
    """Status of a migration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class StepType(Enum):
    """Types of migration steps."""

    CREATE_DIR = "create_dir"
    MOVE_FILE = "move_file"
    COPY_FILE = "copy_file"
    DELETE_FILE = "delete_file"
    RENAME = "rename"
    TRANSFORM = "transform"  # Custom transformation
    CUSTOM = "custom"


@dataclass
class MigrationStep:
    """Individual migration step."""

    step_type: StepType
    source: str = ""
    target: str = ""
    description: str = ""
    transform_func: Callable[[str], str] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary (excluding transform_func)."""
        return {
            "step_type": self.step_type.value,
            "source": self.source,
            "target": self.target,
            "description": self.description,
            "metadata": self.metadata,
        }


@dataclass
class StepResult:
    """Result of executing a migration step."""

    step: MigrationStep
    success: bool
    message: str = ""
    backup_path: str = ""
    duration_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "step": self.step.to_dict(),
            "success": self.success,
            "message": self.message,
            "backup_path": self.backup_path,
            "duration_ms": round(self.duration_ms, 2),
        }


@dataclass
class MigrationPlan:
    """Complete migration plan."""

    name: str
    version: str
    steps: list[MigrationStep]
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "steps": [s.to_dict() for s in self.steps],
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


@dataclass
class MigrationResult:
    """Result of a complete migration."""

    plan: MigrationPlan
    status: MigrationStatus
    step_results: list[StepResult]
    backup_dir: str = ""
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
    error: str = ""

    @property
    def duration_ms(self) -> float:
        """Total duration in milliseconds."""
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds() * 1000
        return 0.0

    @property
    def success_rate(self) -> float:
        """Percentage of successful steps."""
        if not self.step_results:
            return 0.0
        successful = sum(1 for r in self.step_results if r.success)
        return (successful / len(self.step_results)) * 100

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "plan": self.plan.to_dict(),
            "status": self.status.value,
            "step_results": [r.to_dict() for r in self.step_results],
            "backup_dir": self.backup_dir,
            "started_at": self.started_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "duration_ms": round(self.duration_ms, 2),
            "success_rate": round(self.success_rate, 2),
            "error": self.error,
        }


class MigrationToolkit:
    """
    Safe migration toolkit with backup and rollback support.

    Features:
    - Automatic backup before migration
    - Step-by-step execution with logging
    - Rollback on failure
    - Dry run mode
    - Migration history
    """

    def __init__(
        self,
        kb_path: Path | None = None,
        backup_dir: Path | None = None,
    ):
        """
        Initialize migration toolkit.

        Args:
            kb_path: Path to knowledge base root
            backup_dir: Directory for backups (default: .migration_backups)
        """
        self.kb_path = kb_path or Path(__file__).parent.parent
        self.backup_dir = backup_dir or self.kb_path / ".migration_backups"
        self._history: list[MigrationResult] = []

    def create_backup(self, name: str = "") -> Path:
        """
        Create a backup of the current state.

        Args:
            name: Optional backup name

        Returns:
            Path to backup directory
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{name}_{timestamp}" if name else timestamp
        backup_path = self.backup_dir / backup_name

        backup_path.mkdir(parents=True, exist_ok=True)

        # Copy content directory
        content_src = self.kb_path / "content"
        if content_src.exists():
            shutil.copytree(
                content_src,
                backup_path / "content",
                dirs_exist_ok=True,
            )

        # Copy config files
        for config_file in ["aikb.yaml", "index.md"]:
            src = self.kb_path / config_file
            if src.exists():
                shutil.copy2(src, backup_path / config_file)

        logger.info(f"Backup created: {backup_path}")
        return backup_path

    def restore_backup(self, backup_path: Path) -> bool:
        """
        Restore from a backup.

        Args:
            backup_path: Path to backup directory

        Returns:
            True if restore successful
        """
        try:
            # Restore content directory
            content_backup = backup_path / "content"
            content_dest = self.kb_path / "content"

            if content_backup.exists():
                if content_dest.exists():
                    shutil.rmtree(content_dest)
                shutil.copytree(content_backup, content_dest)

            # Restore config files
            for config_file in ["aikb.yaml", "index.md"]:
                src = backup_path / config_file
                if src.exists():
                    shutil.copy2(src, self.kb_path / config_file)

            logger.info(f"Restored from backup: {backup_path}")
            return True

        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False

    def execute_step(
        self,
        step: MigrationStep,
        dry_run: bool = False,
    ) -> StepResult:
        """
        Execute a single migration step.

        Args:
            step: The step to execute
            dry_run: If True, only simulate the step

        Returns:
            StepResult
        """
        import time

        start_time = time.monotonic()
        backup_path = ""

        try:
            source_path = self.kb_path / step.source if step.source else None
            target_path = self.kb_path / step.target if step.target else None

            if dry_run:
                return StepResult(
                    step=step,
                    success=True,
                    message=f"[DRY RUN] Would execute: {step.description or step.step_type.value}",
                    duration_ms=(time.monotonic() - start_time) * 1000,
                )

            if step.step_type == StepType.CREATE_DIR:
                if target_path:
                    target_path.mkdir(parents=True, exist_ok=True)
                    message = f"Created directory: {step.target}"
                else:
                    raise ValueError("Target required for CREATE_DIR")

            elif step.step_type == StepType.MOVE_FILE:
                if source_path and target_path:
                    if source_path.exists():
                        # Backup before move
                        if source_path.is_file():
                            backup_path = str(self._backup_file(source_path))
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(source_path), str(target_path))
                        message = f"Moved: {step.source} -> {step.target}"
                    else:
                        message = f"Source not found (skipped): {step.source}"
                else:
                    raise ValueError("Source and target required for MOVE_FILE")

            elif step.step_type == StepType.COPY_FILE:
                if source_path and target_path:
                    if source_path.exists():
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        if source_path.is_dir():
                            shutil.copytree(
                                source_path, target_path, dirs_exist_ok=True
                            )
                        else:
                            shutil.copy2(source_path, target_path)
                        message = f"Copied: {step.source} -> {step.target}"
                    else:
                        message = f"Source not found (skipped): {step.source}"
                else:
                    raise ValueError("Source and target required for COPY_FILE")

            elif step.step_type == StepType.DELETE_FILE:
                if source_path and source_path.exists():
                    # Backup before delete
                    backup_path = str(self._backup_file(source_path))
                    if source_path.is_dir():
                        shutil.rmtree(source_path)
                    else:
                        source_path.unlink()
                    message = f"Deleted: {step.source}"
                else:
                    message = f"File not found (skipped): {step.source}"

            elif step.step_type == StepType.RENAME:
                if source_path and target_path:
                    if source_path.exists():
                        backup_path = str(self._backup_file(source_path))
                        source_path.rename(target_path)
                        message = f"Renamed: {step.source} -> {step.target}"
                    else:
                        message = f"Source not found (skipped): {step.source}"
                else:
                    raise ValueError("Source and target required for RENAME")

            elif step.step_type == StepType.TRANSFORM:
                if source_path and source_path.exists() and step.transform_func:
                    backup_path = str(self._backup_file(source_path))
                    content = source_path.read_text(encoding="utf-8")
                    transformed = step.transform_func(content)
                    dest = target_path or source_path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_text(transformed, encoding="utf-8")
                    message = f"Transformed: {step.source}"
                else:
                    message = f"Transform skipped: {step.source}"

            elif step.step_type == StepType.CUSTOM:
                message = f"Custom step: {step.description}"

            else:
                message = f"Unknown step type: {step.step_type}"

            return StepResult(
                step=step,
                success=True,
                message=message,
                backup_path=backup_path,
                duration_ms=(time.monotonic() - start_time) * 1000,
            )

        except Exception as e:
            return StepResult(
                step=step,
                success=False,
                message=f"Error: {e}",
                backup_path=backup_path,
                duration_ms=(time.monotonic() - start_time) * 1000,
            )

    def _backup_file(self, path: Path) -> Path:
        """Create a backup of a single file or directory."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{path.name}_{timestamp}"
        backup_path = self.backup_dir / "files" / backup_name

        backup_path.parent.mkdir(parents=True, exist_ok=True)

        if path.is_dir():
            shutil.copytree(path, backup_path)
        else:
            shutil.copy2(path, backup_path)

        return backup_path

    def execute_plan(
        self,
        plan: MigrationPlan,
        dry_run: bool = False,
        stop_on_error: bool = True,
    ) -> MigrationResult:
        """
        Execute a complete migration plan.

        Args:
            plan: The migration plan to execute
            dry_run: If True, only simulate the migration
            stop_on_error: If True, stop on first error

        Returns:
            MigrationResult
        """
        result = MigrationResult(
            plan=plan,
            status=MigrationStatus.IN_PROGRESS,
            step_results=[],
        )

        # Create full backup before migration
        if not dry_run:
            try:
                backup_path = self.create_backup(plan.name)
                result.backup_dir = str(backup_path)
            except Exception as e:
                result.status = MigrationStatus.FAILED
                result.error = f"Backup failed: {e}"
                result.completed_at = datetime.now()
                return result

        # Execute steps
        for step in plan.steps:
            step_result = self.execute_step(step, dry_run=dry_run)
            result.step_results.append(step_result)

            if not step_result.success and stop_on_error:
                result.status = MigrationStatus.FAILED
                result.error = f"Step failed: {step_result.message}"

                # Rollback on failure
                if not dry_run and result.backup_dir:
                    logger.warning("Migration failed, initiating rollback...")
                    if self.restore_backup(Path(result.backup_dir)):
                        result.status = MigrationStatus.ROLLED_BACK
                        result.error += " (rolled back)"

                break

        if result.status == MigrationStatus.IN_PROGRESS:
            result.status = MigrationStatus.COMPLETED

        result.completed_at = datetime.now()
        self._history.append(result)

        return result

    def rollback_last(self) -> bool:
        """
        Rollback the last migration.

        Returns:
            True if rollback successful
        """
        if not self._history:
            logger.warning("No migration history to rollback")
            return False

        last = self._history[-1]
        if last.backup_dir:
            return self.restore_backup(Path(last.backup_dir))

        logger.warning("Last migration has no backup")
        return False

    def get_history(self) -> list[MigrationResult]:
        """Get migration history."""
        return self._history.copy()

    def list_backups(self) -> list[dict[str, Any]]:
        """List all available backups."""
        backups = []

        if self.backup_dir.exists():
            for item in sorted(self.backup_dir.iterdir(), reverse=True):
                if item.is_dir() and not item.name.startswith("."):
                    backups.append(
                        {
                            "name": item.name,
                            "path": str(item),
                            "created": datetime.fromtimestamp(
                                item.stat().st_ctime
                            ).isoformat(),
                        }
                    )

        return backups

    def cleanup_backups(self, keep_last: int = 5) -> int:
        """
        Clean up old backups, keeping the most recent ones.

        Args:
            keep_last: Number of recent backups to keep

        Returns:
            Number of backups removed
        """
        backups = self.list_backups()
        removed = 0

        if len(backups) > keep_last:
            for backup in backups[keep_last:]:
                try:
                    shutil.rmtree(backup["path"])
                    removed += 1
                except Exception as e:
                    logger.warning(f"Failed to remove backup {backup['name']}: {e}")

        return removed


# Convenience functions
def create_migration_plan(
    name: str,
    version: str,
    steps: list[dict[str, Any]],
    description: str = "",
) -> MigrationPlan:
    """Create a migration plan from step definitions."""
    migration_steps = []

    for step_def in steps:
        step = MigrationStep(
            step_type=StepType(step_def.get("type", "custom")),
            source=step_def.get("source", ""),
            target=step_def.get("target", ""),
            description=step_def.get("description", ""),
        )
        migration_steps.append(step)

    return MigrationPlan(
        name=name,
        version=version,
        steps=migration_steps,
        description=description,
    )


def migrate(
    plan: MigrationPlan,
    kb_path: Path | None = None,
    dry_run: bool = False,
) -> MigrationResult:
    """Quick function to execute a migration."""
    toolkit = MigrationToolkit(kb_path=kb_path)
    return toolkit.execute_plan(plan, dry_run=dry_run)
