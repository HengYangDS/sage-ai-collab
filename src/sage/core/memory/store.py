"""Memory store for cross-task persistence.

This module provides persistent memory storage with priority-based retention
and query capabilities for the SAGE Knowledge Base.

Version: 0.1.0
"""

from __future__ import annotations

import json
import logging
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional

try:
    from platformdirs import user_data_dir
except ImportError:
    # Fallback if platformdirs not installed
    def user_data_dir(appname: str, appauthor: str | None = None) -> str:
        """Fallback user data directory."""
        import os
        if os.name == "nt":
            return str(Path.home() / "AppData" / "Local" / appname)
        elif os.name == "darwin":
            return str(Path.home() / "Library" / "Application Support" / appname)
        else:
            return str(Path.home() / ".local" / "share" / appname)

logger = logging.getLogger(__name__)


class MemoryType(str, Enum):
    """Types of memory entries.

    Each type represents a different category of information that can be
    stored and retrieved from the memory system.
    """

    CONVERSATION = "conversation"  # Chat history
    DECISION = "decision"  # Important decisions made
    CONTEXT = "context"  # Task context
    SUMMARY = "summary"  # Consolidated summaries
    CHECKPOINT = "checkpoint"  # Session checkpoints
    ARTIFACT = "artifact"  # Generated artifacts


class MemoryPriority(int, Enum):
    """Memory retention priority (higher = more important).

    Priority levels determine which memories are retained when token
    budgets are exceeded and pruning is required.
    """

    EPHEMERAL = 10  # Can be discarded first
    LOW = 30  # Nice to have
    NORMAL = 50  # Standard importance
    HIGH = 70  # Should be retained
    CRITICAL = 90  # Must be retained
    PERMANENT = 100  # Never discard


@dataclass
class MemoryEntry:
    """A single memory entry.

    Represents a unit of information stored in the memory system with
    associated metadata for retrieval, prioritization, and lifecycle
    management.
    """

    id: str
    type: MemoryType
    content: str
    priority: MemoryPriority = MemoryPriority.NORMAL
    tokens: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    session_id: Optional[str] = None
    task_id: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    # For summarization tracking
    is_summarized: bool = False
    summary_of: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert entry to dictionary for serialization."""
        data = asdict(self)
        data["type"] = self.type.value
        data["priority"] = self.priority.value
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MemoryEntry:
        """Create entry from dictionary."""
        data = data.copy()
        data["type"] = MemoryType(data["type"])
        data["priority"] = MemoryPriority(data["priority"])
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return cls(**data)


class MemoryStore:
    """Persistent memory store with file backend.

    Provides CRUD operations, querying, and checkpoint support for
    cross-task memory persistence.

    Storage structure:
        ~/.local/share/sage/memory/
        ├── index.json           # Memory index
        ├── sessions/
        │   └── {session_id}.json
        ├── summaries/
        │   └── {date}.json
        └── checkpoints/
            └── {checkpoint_id}.json
    """

    def __init__(
        self,
        base_path: Optional[Path] = None,
        auto_save: bool = True,
    ) -> None:
        """Initialize the memory store.

        Args:
            base_path: Custom storage path. Defaults to platformdirs location.
            auto_save: Whether to auto-save after modifications.
        """
        if base_path is None:
            base_path = Path(user_data_dir("sage")) / "memory"

        self._base_path = base_path
        self._auto_save = auto_save
        self._entries: dict[str, MemoryEntry] = {}
        self._index: dict[str, dict[str, list[str]]] = {
            "by_session": {},
            "by_type": {},
            "by_tag": {},
        }

        # Ensure directories exist
        self._ensure_directories()

        # Load existing data
        self._load_index()

    def _ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        directories = [
            self._base_path,
            self._base_path / "sessions",
            self._base_path / "summaries",
            self._base_path / "checkpoints",
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def _load_index(self) -> None:
        """Load memory index from disk."""
        index_path = self._base_path / "index.json"
        if index_path.exists():
            try:
                with open(index_path, "r", encoding="utf-8") as f:
                    self._index = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                logger.warning(f"Failed to load memory index: {e}")
                self._index = {"by_session": {}, "by_type": {}, "by_tag": {}}

    def _save_index(self) -> None:
        """Save memory index to disk."""
        index_path = self._base_path / "index.json"
        try:
            with open(index_path, "w", encoding="utf-8") as f:
                json.dump(self._index, f, indent=2)
        except OSError as e:
            logger.error(f"Failed to save memory index: {e}")

    def _get_session_path(self, session_id: str) -> Path:
        """Get path for session file."""
        return self._base_path / "sessions" / f"{session_id}.json"

    def _load_session(self, session_id: str) -> None:
        """Load entries for a session from disk."""
        session_path = self._get_session_path(session_id)
        if session_path.exists():
            try:
                with open(session_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for entry_data in data.get("entries", []):
                        entry = MemoryEntry.from_dict(entry_data)
                        self._entries[entry.id] = entry
            except (json.JSONDecodeError, OSError) as e:
                logger.warning(f"Failed to load session {session_id}: {e}")

    def _save_session(self, session_id: str) -> None:
        """Save entries for a session to disk."""
        session_path = self._get_session_path(session_id)
        entries = [
            e.to_dict()
            for e in self._entries.values()
            if e.session_id == session_id
        ]
        try:
            with open(session_path, "w", encoding="utf-8") as f:
                json.dump({"session_id": session_id, "entries": entries}, f, indent=2)
        except OSError as e:
            logger.error(f"Failed to save session {session_id}: {e}")

    def _update_index(self, entry: MemoryEntry, remove: bool = False) -> None:
        """Update index for an entry."""
        # Session index
        if entry.session_id:
            if entry.session_id not in self._index["by_session"]:
                self._index["by_session"][entry.session_id] = []
            session_ids = self._index["by_session"][entry.session_id]
            if remove:
                if entry.id in session_ids:
                    session_ids.remove(entry.id)
            elif entry.id not in session_ids:
                session_ids.append(entry.id)

        # Type index
        type_key = entry.type.value
        if type_key not in self._index["by_type"]:
            self._index["by_type"][type_key] = []
        type_ids = self._index["by_type"][type_key]
        if remove:
            if entry.id in type_ids:
                type_ids.remove(entry.id)
        elif entry.id not in type_ids:
            type_ids.append(entry.id)

        # Tag index
        for tag in entry.tags:
            if tag not in self._index["by_tag"]:
                self._index["by_tag"][tag] = []
            tag_ids = self._index["by_tag"][tag]
            if remove:
                if entry.id in tag_ids:
                    tag_ids.remove(entry.id)
            elif entry.id not in tag_ids:
                tag_ids.append(entry.id)

    # CRUD Operations

    def add(
        self,
        type: MemoryType,
        content: str,
        *,
        priority: MemoryPriority = MemoryPriority.NORMAL,
        tokens: int = 0,
        session_id: Optional[str] = None,
        task_id: Optional[str] = None,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> MemoryEntry:
        """Add a new memory entry.

        Args:
            type: Type of memory entry.
            content: Content to store.
            priority: Retention priority.
            tokens: Token count for content.
            session_id: Associated session ID.
            task_id: Associated task ID.
            tags: Tags for categorization.
            metadata: Additional metadata.

        Returns:
            The created memory entry.
        """
        entry = MemoryEntry(
            id=str(uuid.uuid4()),
            type=type,
            content=content,
            priority=priority,
            tokens=tokens,
            session_id=session_id,
            task_id=task_id,
            tags=tags or [],
            metadata=metadata or {},
        )

        self._entries[entry.id] = entry
        self._update_index(entry)

        if self._auto_save:
            if session_id:
                self._save_session(session_id)
            self._save_index()

        logger.debug(f"Added memory entry: {entry.id} ({entry.type.value})")
        return entry

    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """Get a memory entry by ID.

        Args:
            entry_id: The entry ID.

        Returns:
            The memory entry, or None if not found.
        """
        return self._entries.get(entry_id)

    def update(
        self,
        entry_id: str,
        *,
        content: Optional[str] = None,
        priority: Optional[MemoryPriority] = None,
        tokens: Optional[int] = None,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> Optional[MemoryEntry]:
        """Update a memory entry.

        Args:
            entry_id: The entry ID to update.
            content: New content (if provided).
            priority: New priority (if provided).
            tokens: New token count (if provided).
            tags: New tags (if provided).
            metadata: Additional metadata to merge.

        Returns:
            The updated entry, or None if not found.
        """
        entry = self._entries.get(entry_id)
        if entry is None:
            return None

        # Remove old index entries for tags
        old_tags = entry.tags.copy()

        if content is not None:
            entry.content = content
        if priority is not None:
            entry.priority = priority
        if tokens is not None:
            entry.tokens = tokens
        if tags is not None:
            entry.tags = tags
        if metadata is not None:
            entry.metadata.update(metadata)

        entry.updated_at = datetime.now()

        # Update tag index if tags changed
        if tags is not None and tags != old_tags:
            for tag in old_tags:
                if tag in self._index["by_tag"]:
                    if entry.id in self._index["by_tag"][tag]:
                        self._index["by_tag"][tag].remove(entry.id)
            for tag in tags:
                if tag not in self._index["by_tag"]:
                    self._index["by_tag"][tag] = []
                if entry.id not in self._index["by_tag"][tag]:
                    self._index["by_tag"][tag].append(entry.id)

        if self._auto_save:
            if entry.session_id:
                self._save_session(entry.session_id)
            self._save_index()

        logger.debug(f"Updated memory entry: {entry.id}")
        return entry

    def delete(self, entry_id: str) -> bool:
        """Delete a memory entry.

        Args:
            entry_id: The entry ID to delete.

        Returns:
            True if deleted, False if not found.
        """
        entry = self._entries.get(entry_id)
        if entry is None:
            return False

        session_id = entry.session_id
        self._update_index(entry, remove=True)
        del self._entries[entry_id]

        if self._auto_save:
            if session_id:
                self._save_session(session_id)
            self._save_index()

        logger.debug(f"Deleted memory entry: {entry_id}")
        return True

    # Query Operations

    def query(
        self,
        *,
        session_id: Optional[str] = None,
        type: Optional[MemoryType] = None,
        tags: Optional[list[str]] = None,
        min_priority: Optional[MemoryPriority] = None,
        max_priority: Optional[MemoryPriority] = None,
        limit: Optional[int] = None,
        order_by: str = "created_at",
        descending: bool = True,
    ) -> list[MemoryEntry]:
        """Query memory entries with filters.

        Args:
            session_id: Filter by session ID.
            type: Filter by memory type.
            tags: Filter by tags (any match).
            min_priority: Minimum priority filter.
            max_priority: Maximum priority filter.
            limit: Maximum number of results.
            order_by: Field to order by (created_at, updated_at, priority).
            descending: Whether to sort descending.

        Returns:
            List of matching memory entries.
        """
        # Start with all entries or filtered by index
        if session_id:
            if session_id not in self._index["by_session"]:
                self._load_session(session_id)
            entry_ids = set(self._index["by_session"].get(session_id, []))
            entries = [self._entries[eid] for eid in entry_ids if eid in self._entries]
        else:
            entries = list(self._entries.values())

        # Apply filters
        if type is not None:
            entries = [e for e in entries if e.type == type]

        if tags:
            entries = [e for e in entries if any(t in e.tags for t in tags)]

        if min_priority is not None:
            entries = [e for e in entries if e.priority.value >= min_priority.value]

        if max_priority is not None:
            entries = [e for e in entries if e.priority.value <= max_priority.value]

        # Sort
        if order_by == "priority":
            entries.sort(key=lambda e: e.priority.value, reverse=descending)
        elif order_by == "updated_at":
            entries.sort(key=lambda e: e.updated_at, reverse=descending)
        else:  # created_at
            entries.sort(key=lambda e: e.created_at, reverse=descending)

        # Limit
        if limit is not None:
            entries = entries[:limit]

        return entries

    def get_by_session(self, session_id: str) -> list[MemoryEntry]:
        """Get all entries for a session.

        Args:
            session_id: The session ID.

        Returns:
            List of memory entries for the session.
        """
        return self.query(session_id=session_id)

    def get_by_type(self, type: MemoryType) -> list[MemoryEntry]:
        """Get all entries of a specific type.

        Args:
            type: The memory type.

        Returns:
            List of memory entries of the specified type.
        """
        return self.query(type=type)

    def get_by_tags(self, tags: list[str]) -> list[MemoryEntry]:
        """Get entries matching any of the specified tags.

        Args:
            tags: List of tags to match.

        Returns:
            List of matching memory entries.
        """
        return self.query(tags=tags)

    # Checkpoint Operations

    def create_checkpoint(
        self,
        session_id: str,
        checkpoint_id: Optional[str] = None,
    ) -> str:
        """Create a checkpoint of session memory.

        Args:
            session_id: The session to checkpoint.
            checkpoint_id: Optional custom checkpoint ID.

        Returns:
            The checkpoint ID.
        """
        if checkpoint_id is None:
            checkpoint_id = f"cp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{session_id[:8]}"

        entries = self.get_by_session(session_id)
        checkpoint_data = {
            "checkpoint_id": checkpoint_id,
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "entries": [e.to_dict() for e in entries],
        }

        checkpoint_path = self._base_path / "checkpoints" / f"{checkpoint_id}.json"
        try:
            with open(checkpoint_path, "w", encoding="utf-8") as f:
                json.dump(checkpoint_data, f, indent=2)
            logger.info(f"Created checkpoint: {checkpoint_id}")
        except OSError as e:
            logger.error(f"Failed to create checkpoint: {e}")
            raise

        return checkpoint_id

    def restore_checkpoint(self, checkpoint_id: str) -> list[MemoryEntry]:
        """Restore memory from a checkpoint.

        Args:
            checkpoint_id: The checkpoint ID to restore.

        Returns:
            List of restored memory entries.
        """
        checkpoint_path = self._base_path / "checkpoints" / f"{checkpoint_id}.json"
        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_id}")

        try:
            with open(checkpoint_path, "r", encoding="utf-8") as f:
                checkpoint_data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Failed to load checkpoint: {e}")
            raise

        entries = []
        for entry_data in checkpoint_data.get("entries", []):
            entry = MemoryEntry.from_dict(entry_data)
            self._entries[entry.id] = entry
            self._update_index(entry)
            entries.append(entry)

        if self._auto_save:
            self._save_index()

        logger.info(f"Restored checkpoint: {checkpoint_id} ({len(entries)} entries)")
        return entries

    def list_checkpoints(self) -> list[dict[str, Any]]:
        """List all available checkpoints.

        Returns:
            List of checkpoint metadata.
        """
        checkpoints = []
        checkpoint_dir = self._base_path / "checkpoints"

        for checkpoint_file in checkpoint_dir.glob("*.json"):
            try:
                with open(checkpoint_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    checkpoints.append({
                        "checkpoint_id": data.get("checkpoint_id"),
                        "session_id": data.get("session_id"),
                        "created_at": data.get("created_at"),
                        "entry_count": len(data.get("entries", [])),
                    })
            except (json.JSONDecodeError, OSError):
                continue

        return sorted(checkpoints, key=lambda c: c.get("created_at", ""), reverse=True)

    # Pruning Operations

    def prune(
        self,
        *,
        max_priority: MemoryPriority = MemoryPriority.LOW,
        older_than: Optional[datetime] = None,
        session_id: Optional[str] = None,
    ) -> int:
        """Prune low-priority entries.

        Args:
            max_priority: Maximum priority to prune (inclusive).
            older_than: Only prune entries older than this datetime.
            session_id: Only prune from specific session.

        Returns:
            Number of entries pruned.
        """
        entries_to_prune = self.query(
            session_id=session_id,
            max_priority=max_priority,
        )

        if older_than:
            entries_to_prune = [e for e in entries_to_prune if e.created_at < older_than]

        pruned_count = 0
        for entry in entries_to_prune:
            if self.delete(entry.id):
                pruned_count += 1

        logger.info(f"Pruned {pruned_count} memory entries")
        return pruned_count

    def get_total_tokens(self, session_id: Optional[str] = None) -> int:
        """Get total token count.

        Args:
            session_id: Optional session to count tokens for.

        Returns:
            Total token count.
        """
        entries = self.query(session_id=session_id) if session_id else list(self._entries.values())
        return sum(e.tokens for e in entries)

    def clear(self, session_id: Optional[str] = None) -> int:
        """Clear all entries or entries for a specific session.

        Args:
            session_id: Optional session to clear.

        Returns:
            Number of entries cleared.
        """
        if session_id:
            entries = self.get_by_session(session_id)
            for entry in entries:
                self.delete(entry.id)
            return len(entries)
        else:
            count = len(self._entries)
            self._entries.clear()
            self._index = {"by_session": {}, "by_type": {}, "by_tag": {}}
            if self._auto_save:
                self._save_index()
            return count
