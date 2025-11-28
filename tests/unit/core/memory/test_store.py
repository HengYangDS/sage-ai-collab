"""Unit tests for MemoryStore.

Tests cover:
- CRUD operations (add, get, update, delete)
- Query operations with filters
- Checkpoint operations (create, restore, list)
- Pruning operations
- Index management
"""

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from sage.core.memory.store import (
    MemoryEntry,
    MemoryPriority,
    MemoryStore,
    MemoryType,
)


class TestMemoryType:
    """Tests for MemoryType enum."""

    def test_memory_types_exist(self):
        """Test all expected memory types exist."""
        assert MemoryType.CONVERSATION == "conversation"
        assert MemoryType.DECISION == "decision"
        assert MemoryType.CONTEXT == "context"
        assert MemoryType.SUMMARY == "summary"
        assert MemoryType.CHECKPOINT == "checkpoint"
        assert MemoryType.ARTIFACT == "artifact"

    def test_memory_type_count(self):
        """Test correct number of memory types."""
        assert len(MemoryType) == 6


class TestMemoryPriority:
    """Tests for MemoryPriority enum."""

    def test_memory_priorities_exist(self):
        """Test all expected priorities exist with correct values."""
        assert MemoryPriority.EPHEMERAL == 10
        assert MemoryPriority.LOW == 30
        assert MemoryPriority.NORMAL == 50
        assert MemoryPriority.HIGH == 70
        assert MemoryPriority.CRITICAL == 90
        assert MemoryPriority.PERMANENT == 100

    def test_priority_ordering(self):
        """Test priorities are correctly ordered."""
        priorities = [
            MemoryPriority.EPHEMERAL,
            MemoryPriority.LOW,
            MemoryPriority.NORMAL,
            MemoryPriority.HIGH,
            MemoryPriority.CRITICAL,
            MemoryPriority.PERMANENT,
        ]
        for i in range(len(priorities) - 1):
            assert priorities[i].value < priorities[i + 1].value


class TestMemoryEntry:
    """Tests for MemoryEntry dataclass."""

    def test_create_entry(self):
        """Test creating a memory entry."""
        entry = MemoryEntry(
            id="test-id",
            type=MemoryType.CONTEXT,
            content="Test content",
        )
        assert entry.id == "test-id"
        assert entry.type == MemoryType.CONTEXT
        assert entry.content == "Test content"
        assert entry.priority == MemoryPriority.NORMAL
        assert entry.tokens == 0
        assert entry.tags == []
        assert entry.metadata == {}

    def test_entry_to_dict(self):
        """Test serializing entry to dictionary."""
        entry = MemoryEntry(
            id="test-id",
            type=MemoryType.DECISION,
            content="Important decision",
            priority=MemoryPriority.HIGH,
            tokens=100,
            tags=["important"],
        )
        data = entry.to_dict()

        assert data["id"] == "test-id"
        assert data["type"] == "decision"
        assert data["priority"] == 70
        assert data["tokens"] == 100
        assert data["tags"] == ["important"]
        assert "created_at" in data
        assert "updated_at" in data

    def test_entry_from_dict(self):
        """Test deserializing entry from dictionary."""
        data = {
            "id": "test-id",
            "type": "context",
            "content": "Test content",
            "priority": 50,
            "tokens": 50,
            "created_at": "2025-01-01T12:00:00",
            "updated_at": "2025-01-01T12:00:00",
            "session_id": None,
            "task_id": None,
            "tags": [],
            "metadata": {},
            "is_summarized": False,
            "summary_of": [],
        }
        entry = MemoryEntry.from_dict(data)

        assert entry.id == "test-id"
        assert entry.type == MemoryType.CONTEXT
        assert entry.priority == MemoryPriority.NORMAL
        assert entry.tokens == 50

    def test_entry_roundtrip(self):
        """Test entry survives serialization roundtrip."""
        original = MemoryEntry(
            id="roundtrip-test",
            type=MemoryType.ARTIFACT,
            content="Artifact content",
            priority=MemoryPriority.CRITICAL,
            tokens=200,
            tags=["artifact", "important"],
            metadata={"key": "value"},
        )
        data = original.to_dict()
        restored = MemoryEntry.from_dict(data)

        assert restored.id == original.id
        assert restored.type == original.type
        assert restored.content == original.content
        assert restored.priority == original.priority
        assert restored.tokens == original.tokens
        assert restored.tags == original.tags
        assert restored.metadata == original.metadata


class TestMemoryStore:
    """Tests for MemoryStore class."""

    @pytest.fixture
    def temp_store(self):
        """Create a temporary memory store."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = MemoryStore(base_path=Path(tmpdir), auto_save=False)
            yield store

    @pytest.fixture
    def store_with_data(self, temp_store):
        """Create a store with some test data."""
        temp_store.add(
            type=MemoryType.CONTEXT,
            content="Context 1",
            session_id="session-1",
            tags=["tag1"],
        )
        temp_store.add(
            type=MemoryType.DECISION,
            content="Decision 1",
            priority=MemoryPriority.HIGH,
            session_id="session-1",
            tags=["tag1", "tag2"],
        )
        temp_store.add(
            type=MemoryType.CONTEXT,
            content="Context 2",
            session_id="session-2",
            tags=["tag2"],
        )
        return temp_store

    # CRUD Tests

    def test_add_entry(self, temp_store):
        """Test adding a memory entry."""
        entry = temp_store.add(
            type=MemoryType.CONTEXT,
            content="Test content",
            tokens=50,
        )

        assert entry.id is not None
        assert entry.type == MemoryType.CONTEXT
        assert entry.content == "Test content"
        assert entry.tokens == 50

    def test_get_entry(self, temp_store):
        """Test retrieving an entry by ID."""
        added = temp_store.add(
            type=MemoryType.DECISION,
            content="Important",
        )

        retrieved = temp_store.get(added.id)
        assert retrieved is not None
        assert retrieved.id == added.id
        assert retrieved.content == "Important"

    def test_get_nonexistent_entry(self, temp_store):
        """Test getting a non-existent entry returns None."""
        result = temp_store.get("nonexistent-id")
        assert result is None

    def test_update_entry(self, temp_store):
        """Test updating an entry."""
        entry = temp_store.add(
            type=MemoryType.CONTEXT,
            content="Original",
        )

        updated = temp_store.update(
            entry.id,
            content="Updated",
            priority=MemoryPriority.HIGH,
        )

        assert updated is not None
        assert updated.content == "Updated"
        assert updated.priority == MemoryPriority.HIGH
        assert updated.updated_at > entry.created_at

    def test_update_nonexistent_entry(self, temp_store):
        """Test updating non-existent entry returns None."""
        result = temp_store.update("nonexistent", content="new")
        assert result is None

    def test_delete_entry(self, temp_store):
        """Test deleting an entry."""
        entry = temp_store.add(
            type=MemoryType.CONTEXT,
            content="To delete",
        )

        assert temp_store.delete(entry.id) is True
        assert temp_store.get(entry.id) is None

    def test_delete_nonexistent_entry(self, temp_store):
        """Test deleting non-existent entry returns False."""
        result = temp_store.delete("nonexistent")
        assert result is False

    # Query Tests

    def test_query_by_session(self, store_with_data):
        """Test querying by session ID."""
        results = store_with_data.query(session_id="session-1")
        assert len(results) == 2

    def test_query_by_type(self, store_with_data):
        """Test querying by memory type."""
        results = store_with_data.query(type=MemoryType.CONTEXT)
        assert len(results) == 2

    def test_query_by_tags(self, store_with_data):
        """Test querying by tags."""
        results = store_with_data.query(tags=["tag1"])
        assert len(results) == 2

        results = store_with_data.query(tags=["tag2"])
        assert len(results) == 2

    def test_query_by_priority(self, store_with_data):
        """Test querying by priority range."""
        results = store_with_data.query(min_priority=MemoryPriority.HIGH)
        assert len(results) == 1
        assert results[0].priority == MemoryPriority.HIGH

    def test_query_with_limit(self, store_with_data):
        """Test querying with limit."""
        results = store_with_data.query(limit=1)
        assert len(results) == 1

    def test_query_ordering(self, store_with_data):
        """Test query result ordering."""
        results = store_with_data.query(order_by="priority", descending=True)
        priorities = [r.priority.value for r in results]
        assert priorities == sorted(priorities, reverse=True)

    def test_get_by_session(self, store_with_data):
        """Test get_by_session helper."""
        results = store_with_data.get_by_session("session-1")
        assert len(results) == 2

    def test_get_by_type(self, store_with_data):
        """Test get_by_type helper."""
        results = store_with_data.get_by_type(MemoryType.DECISION)
        assert len(results) == 1

    def test_get_by_tags(self, store_with_data):
        """Test get_by_tags helper."""
        results = store_with_data.get_by_tags(["tag1"])
        assert len(results) == 2

    # Checkpoint Tests

    def test_create_checkpoint(self, store_with_data):
        """Test creating a checkpoint."""
        checkpoint_id = store_with_data.create_checkpoint("session-1")
        assert checkpoint_id is not None
        assert checkpoint_id.startswith("cp_")

    def test_list_checkpoints(self, store_with_data):
        """Test listing checkpoints."""
        store_with_data.create_checkpoint("session-1", checkpoint_id="cp-session-1")
        store_with_data.create_checkpoint("session-2", checkpoint_id="cp-session-2")

        checkpoints = store_with_data.list_checkpoints()
        assert len(checkpoints) == 2

    def test_restore_checkpoint(self, temp_store):
        """Test restoring from checkpoint."""
        # Add some data
        temp_store.add(
            type=MemoryType.CONTEXT,
            content="To checkpoint",
            session_id="test-session",
        )

        # Create checkpoint
        checkpoint_id = temp_store.create_checkpoint("test-session")

        # Clear and restore
        temp_store.clear()
        restored = temp_store.restore_checkpoint(checkpoint_id)

        assert len(restored) == 1
        assert restored[0].content == "To checkpoint"

    def test_restore_nonexistent_checkpoint(self, temp_store):
        """Test restoring non-existent checkpoint raises error."""
        with pytest.raises(FileNotFoundError):
            temp_store.restore_checkpoint("nonexistent-checkpoint")

    # Pruning Tests

    def test_prune_by_priority(self, store_with_data):
        """Test pruning low-priority entries."""
        # Add some low-priority entries
        store_with_data.add(
            type=MemoryType.CONTEXT,
            content="Ephemeral",
            priority=MemoryPriority.EPHEMERAL,
        )

        pruned = store_with_data.prune(max_priority=MemoryPriority.EPHEMERAL)
        assert pruned == 1

    def test_prune_by_session(self, store_with_data):
        """Test pruning entries from specific session."""
        store_with_data.add(
            type=MemoryType.CONTEXT,
            content="Low priority",
            priority=MemoryPriority.LOW,
            session_id="session-1",
        )

        pruned = store_with_data.prune(
            max_priority=MemoryPriority.LOW,
            session_id="session-1",
        )
        assert pruned >= 1

    # Token Counting Tests

    def test_get_total_tokens(self, temp_store):
        """Test getting total token count."""
        temp_store.add(type=MemoryType.CONTEXT, content="A", tokens=100)
        temp_store.add(type=MemoryType.CONTEXT, content="B", tokens=200)

        total = temp_store.get_total_tokens()
        assert total == 300

    def test_get_total_tokens_by_session(self, temp_store):
        """Test getting token count for specific session."""
        temp_store.add(
            type=MemoryType.CONTEXT,
            content="A",
            tokens=100,
            session_id="s1",
        )
        temp_store.add(
            type=MemoryType.CONTEXT,
            content="B",
            tokens=200,
            session_id="s2",
        )

        total = temp_store.get_total_tokens("s1")
        assert total == 100

    # Clear Tests

    def test_clear_all(self, store_with_data):
        """Test clearing all entries."""
        count = store_with_data.clear()
        assert count == 3
        assert len(store_with_data.query()) == 0

    def test_clear_by_session(self, store_with_data):
        """Test clearing entries for specific session."""
        count = store_with_data.clear("session-1")
        assert count == 2
        assert len(store_with_data.query(session_id="session-1")) == 0
        assert len(store_with_data.query(session_id="session-2")) == 1


class TestMemoryStorePersistence:
    """Tests for MemoryStore file persistence."""

    def test_persistence_roundtrip(self):
        """Test data survives save/load cycle."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)

            # Create store and add data
            store1 = MemoryStore(base_path=path, auto_save=True)
            store1.add(
                type=MemoryType.DECISION,
                content="Persistent decision",
                session_id="persist-session",
                tokens=100,
            )

            # Create new store instance pointing to same location
            store2 = MemoryStore(base_path=path, auto_save=True)

            # Manually load the session
            store2._load_session("persist-session")

            results = store2.query(session_id="persist-session")
            assert len(results) == 1
            assert results[0].content == "Persistent decision"

    def test_directory_structure_created(self):
        """Test that directory structure is created on init."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "memory"
            MemoryStore(base_path=path)

            assert (path / "sessions").exists()
            assert (path / "summaries").exists()
            assert (path / "checkpoints").exists()
