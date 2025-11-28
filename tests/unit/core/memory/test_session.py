"""Unit tests for Session Continuity.

Tests cover:
- SessionStatus enum
- SessionState dataclass
- HandoffPackage dataclass
- SessionContinuity service
"""

import tempfile
from pathlib import Path

import pytest

from sage.core.memory.session import (
    HandoffPackage,
    SessionContinuity,
    SessionState,
    SessionStatus,
)
from sage.core.memory.store import MemoryStore, MemoryType
from sage.core.memory.token_budget import TokenBudget, TokenBudgetConfig


class TestSessionStatus:
    """Tests for SessionStatus enum."""

    def test_status_values_exist(self):
        """Test all expected statuses exist."""
        assert SessionStatus.ACTIVE == "active"
        assert SessionStatus.PAUSED == "paused"
        assert SessionStatus.COMPLETED == "completed"
        assert SessionStatus.HANDED_OFF == "handed_off"
        assert SessionStatus.FAILED == "failed"

    def test_status_count(self):
        """Test correct number of statuses."""
        assert len(SessionStatus) == 5


class TestSessionState:
    """Tests for SessionState dataclass."""

    def test_create_session_state(self):
        """Test creating a session state."""
        state = SessionState(
            session_id="test-session",
            current_objective="Test objective",
        )
        assert state.session_id == "test-session"
        assert state.current_objective == "Test objective"
        assert state.status == SessionStatus.ACTIVE
        assert state.completed_steps == []
        assert state.pending_steps == []
        assert state.progress_percentage == 0.0

    def test_session_state_to_dict(self):
        """Test serializing session state."""
        state = SessionState(
            session_id="test-session",
            current_objective="Objective",
            completed_steps=["Step 1"],
            pending_steps=["Step 2", "Step 3"],
        )
        data = state.to_dict()

        assert data["session_id"] == "test-session"
        assert data["status"] == "active"
        assert data["completed_steps"] == ["Step 1"]
        assert data["pending_steps"] == ["Step 2", "Step 3"]
        assert "created_at" in data
        assert "updated_at" in data

    def test_session_state_from_dict(self):
        """Test deserializing session state."""
        data = {
            "session_id": "test-session",
            "task_id": None,
            "status": "completed",
            "created_at": "2025-01-01T12:00:00",
            "updated_at": "2025-01-01T13:00:00",
            "current_objective": "Objective",
            "completed_steps": ["Step 1", "Step 2"],
            "pending_steps": [],
            "progress_percentage": 100.0,
            "last_action": "Finished",
            "last_result": "Success",
            "key_decisions": [],
            "important_context": [],
            "total_tokens_used": 5000,
            "metadata": {},
        }
        state = SessionState.from_dict(data)

        assert state.session_id == "test-session"
        assert state.status == SessionStatus.COMPLETED
        assert state.progress_percentage == 100.0

    def test_calculate_progress(self):
        """Test progress calculation."""
        state = SessionState(
            session_id="test",
            completed_steps=["A", "B"],
            pending_steps=["C", "D"],
        )
        progress = state.calculate_progress()
        assert progress == 0.5  # 2 of 4 completed

    def test_calculate_progress_empty(self):
        """Test progress calculation with no steps."""
        state = SessionState(session_id="test")
        progress = state.calculate_progress()
        assert progress == 0.0

    def test_calculate_progress_all_complete(self):
        """Test progress calculation when all complete."""
        state = SessionState(
            session_id="test",
            completed_steps=["A", "B", "C"],
            pending_steps=[],
        )
        progress = state.calculate_progress()
        assert progress == 1.0


class TestHandoffPackage:
    """Tests for HandoffPackage dataclass."""

    @pytest.fixture
    def sample_state(self):
        """Create a sample session state."""
        return SessionState(
            session_id="handoff-session",
            current_objective="Complete feature X",
            completed_steps=["Design", "Implement"],
            pending_steps=["Test", "Deploy"],
            progress_percentage=50.0,
            last_action="Implemented core logic",
            last_result="All tests passing",
        )

    def test_create_handoff_package(self, sample_state):
        """Test creating a handoff package."""
        package = HandoffPackage(
            session_state=sample_state,
            summary="Working on feature X",
            key_context=[],
            decisions=[],
            continuation_prompt="",
            token_count=5000,
        )
        assert package.session_state.session_id == "handoff-session"
        assert package.summary == "Working on feature X"
        assert package.token_count == 5000

    def test_to_prompt(self, sample_state):
        """Test generating continuation prompt."""
        package = HandoffPackage(
            session_state=sample_state,
            summary="Working on feature X implementation",
            key_context=[],
            decisions=[],
            continuation_prompt="",
            token_count=5000,
        )
        prompt = package.to_prompt()

        assert "Session Continuation" in prompt
        assert "Working on feature X implementation" in prompt
        assert "Complete feature X" in prompt
        assert "✓ Design" in prompt
        assert "✓ Implement" in prompt
        assert "Test" in prompt
        assert "Deploy" in prompt
        assert "50%" in prompt

    def test_to_prompt_with_decisions(self, sample_state):
        """Test prompt includes decisions."""
        # Create mock decision entry
        class MockEntry:
            content = "Use Protocol-based interfaces"

        package = HandoffPackage(
            session_state=sample_state,
            summary="Summary",
            key_context=[],
            decisions=[MockEntry()],
            continuation_prompt="",
            token_count=5000,
        )
        prompt = package.to_prompt()

        assert "Protocol-based interfaces" in prompt

    def test_to_dict(self, sample_state):
        """Test converting package to dictionary."""
        package = HandoffPackage(
            session_state=sample_state,
            summary="Summary",
            key_context=[],
            decisions=[],
            continuation_prompt="Continue here",
            token_count=5000,
        )
        data = package.to_dict()

        assert "session_state" in data
        assert data["summary"] == "Summary"
        assert data["token_count"] == 5000


class TestSessionContinuity:
    """Tests for SessionContinuity service."""

    @pytest.fixture
    def temp_store(self):
        """Create a temporary memory store."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = MemoryStore(base_path=Path(tmpdir), auto_save=False)
            yield store

    @pytest.fixture
    def continuity(self, temp_store):
        """Create a session continuity service."""
        return SessionContinuity(temp_store)

    @pytest.fixture
    def continuity_with_budget(self, temp_store):
        """Create a session continuity with token budget."""
        config = TokenBudgetConfig(max_tokens=10000, reserved_tokens=1000)
        budget = TokenBudget(temp_store, config)
        return SessionContinuity(temp_store, budget)

    # Session Lifecycle Tests

    def test_start_session(self, continuity):
        """Test starting a new session."""
        session = continuity.start_session(
            objective="Test objective",
            steps=["Step 1", "Step 2"],
        )

        assert session.session_id is not None
        assert session.current_objective == "Test objective"
        assert session.pending_steps == ["Step 1", "Step 2"]
        assert session.status == SessionStatus.ACTIVE

    def test_current_session_property(self, continuity):
        """Test accessing current session."""
        assert continuity.current_session is None

        continuity.start_session(objective="Test")
        assert continuity.current_session is not None

    def test_start_session_with_metadata(self, continuity):
        """Test starting session with metadata."""
        session = continuity.start_session(
            objective="Test",
            task_id="task-123",
            metadata={"key": "value"},
        )

        assert session.task_id == "task-123"
        assert session.metadata == {"key": "value"}

    def test_end_session(self, continuity):
        """Test ending a session."""
        continuity.start_session(objective="Test")
        session = continuity.end_session(
            status=SessionStatus.COMPLETED,
            final_result="Success",
        )

        assert session.status == SessionStatus.COMPLETED
        assert session.last_result == "Success"
        assert continuity.current_session is None

    def test_end_session_no_active(self, continuity):
        """Test ending when no active session."""
        result = continuity.end_session()
        assert result is None

    # Progress Tracking Tests

    def test_update_progress_completed_step(self, continuity):
        """Test marking a step as completed."""
        continuity.start_session(
            objective="Test",
            steps=["Step 1", "Step 2"],
        )
        session = continuity.update_progress(completed_step="Step 1")

        assert "Step 1" in session.completed_steps
        assert "Step 1" not in session.pending_steps
        assert session.progress_percentage == 50.0

    def test_update_progress_last_action(self, continuity):
        """Test updating last action."""
        continuity.start_session(objective="Test")
        session = continuity.update_progress(
            last_action="Did something",
            last_result="It worked",
        )

        assert session.last_action == "Did something"
        assert session.last_result == "It worked"

    def test_update_progress_decision(self, continuity, temp_store):
        """Test recording a decision."""
        continuity.start_session(objective="Test")
        session = continuity.update_progress(
            decision="Use pattern X",
        )

        assert len(session.key_decisions) == 1
        # Verify decision was stored
        decisions = temp_store.get_by_type(MemoryType.DECISION)
        assert len(decisions) == 1
        assert decisions[0].content == "Use pattern X"

    def test_update_progress_context(self, continuity, temp_store):
        """Test recording important context."""
        continuity.start_session(objective="Test")
        session = continuity.update_progress(
            context="Important context info",
        )

        assert len(session.important_context) == 1
        # Verify context was stored
        contexts = temp_store.get_by_type(MemoryType.CONTEXT)
        assert len(contexts) >= 1

    def test_update_progress_no_session(self, continuity):
        """Test updating when no active session."""
        result = continuity.update_progress(last_action="Something")
        assert result is None

    def test_add_step(self, continuity):
        """Test adding a new step."""
        continuity.start_session(
            objective="Test",
            steps=["Step 1"],
        )
        session = continuity.add_step("Step 2")

        assert "Step 2" in session.pending_steps

    def test_add_step_no_duplicate(self, continuity):
        """Test adding step doesn't create duplicates."""
        continuity.start_session(
            objective="Test",
            steps=["Step 1"],
        )
        continuity.add_step("Step 1")
        session = continuity.current_session

        assert session.pending_steps.count("Step 1") == 1

    # Checkpoint Tests

    def test_create_checkpoint(self, continuity):
        """Test creating a checkpoint."""
        continuity.start_session(
            objective="Test",
            steps=["Step 1"],
        )
        continuity.update_progress(completed_step="Step 1")

        checkpoint_id = continuity.create_checkpoint()
        assert checkpoint_id is not None
        assert checkpoint_id.startswith("cp_")

    def test_create_checkpoint_custom_id(self, continuity):
        """Test creating checkpoint with custom ID."""
        continuity.start_session(objective="Test")
        checkpoint_id = continuity.create_checkpoint("my-checkpoint")
        assert checkpoint_id == "my-checkpoint"

    def test_create_checkpoint_no_session(self, continuity):
        """Test checkpoint fails without active session."""
        with pytest.raises(RuntimeError, match="No active session"):
            continuity.create_checkpoint()

    def test_resume_from_checkpoint(self, continuity, temp_store):
        """Test resuming from a checkpoint."""
        # Start session and create checkpoint
        session1 = continuity.start_session(
            objective="Original objective",
            steps=["Step 1", "Step 2"],
        )
        continuity.update_progress(completed_step="Step 1")
        checkpoint_id = continuity.create_checkpoint()

        # End session
        continuity.end_session()

        # Resume from checkpoint
        session2 = continuity.start_session(
            objective="Continue work",
            resume_from=checkpoint_id,
        )

        assert session2.status == SessionStatus.ACTIVE
        assert session2.current_objective == "Continue work"

    # Handoff Tests

    def test_prepare_handoff(self, continuity):
        """Test preparing a handoff package."""
        continuity.start_session(
            objective="Test objective",
            steps=["Step 1", "Step 2"],
        )
        continuity.update_progress(completed_step="Step 1")

        handoff = continuity.prepare_handoff()

        assert handoff.session_state.session_id is not None
        assert handoff.summary is not None
        assert "Test objective" in handoff.continuation_prompt
        assert handoff.session_state.status == SessionStatus.HANDED_OFF

    def test_prepare_handoff_with_decisions(self, continuity):
        """Test handoff includes decisions."""
        continuity.start_session(objective="Test")
        continuity.update_progress(decision="Important decision")

        handoff = continuity.prepare_handoff()

        assert len(handoff.decisions) == 1

    def test_prepare_handoff_custom_summary(self, continuity):
        """Test handoff with custom summary."""
        continuity.start_session(objective="Test")

        handoff = continuity.prepare_handoff(summary="Custom summary")

        assert handoff.summary == "Custom summary"

    def test_prepare_handoff_no_session(self, continuity):
        """Test handoff fails without active session."""
        with pytest.raises(RuntimeError, match="No active session"):
            continuity.prepare_handoff()

    # Token Tracking Tests

    def test_token_tracking_with_budget(self, continuity_with_budget, temp_store):
        """Test session tracks token usage."""
        continuity_with_budget.start_session(objective="Test")

        # Add some tokens via store
        temp_store.add(
            type=MemoryType.CONTEXT,
            content="Test",
            tokens=1000,
            session_id=continuity_with_budget.current_session.session_id,
        )

        continuity_with_budget.update_progress(last_action="Updated")
        session = continuity_with_budget.current_session

        assert session.total_tokens_used > 0

    # Summary Tests

    def test_get_session_summary(self, continuity):
        """Test getting session summary."""
        continuity.start_session(
            objective="Test objective",
            steps=["Step 1", "Step 2"],
        )
        continuity.update_progress(completed_step="Step 1")

        summary = continuity.get_session_summary()

        assert "Session Summary" in summary
        assert "Test objective" in summary
        assert "50%" in summary

    def test_get_session_summary_no_session(self, continuity):
        """Test summary returns None without session."""
        result = continuity.get_session_summary()
        assert result is None


class TestSessionContinuityIntegration:
    """Integration tests for session continuity workflow."""

    @pytest.fixture
    def temp_store(self):
        """Create a temporary memory store."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = MemoryStore(base_path=Path(tmpdir), auto_save=True)
            yield store

    def test_full_session_workflow(self, temp_store):
        """Test complete session workflow."""
        config = TokenBudgetConfig(max_tokens=10000, reserved_tokens=1000)
        budget = TokenBudget(temp_store, config)
        continuity = SessionContinuity(temp_store, budget)

        # 1. Start session
        session = continuity.start_session(
            objective="Implement feature X",
            steps=["Design", "Implement", "Test"],
        )
        assert session.status == SessionStatus.ACTIVE
        assert session.progress_percentage == 0.0

        # 2. Complete first step with decision
        continuity.update_progress(
            completed_step="Design",
            last_action="Created design document",
            decision="Use Protocol-based interfaces",
        )
        assert session.progress_percentage == pytest.approx(33.3, rel=0.1)

        # 3. Complete second step
        continuity.update_progress(
            completed_step="Implement",
            last_action="Implemented core logic",
            context="Uses async/await patterns",
        )
        assert session.progress_percentage == pytest.approx(66.6, rel=0.1)

        # 4. Create checkpoint before handoff
        checkpoint_id = continuity.create_checkpoint()
        assert checkpoint_id is not None

        # 5. Prepare handoff
        handoff = continuity.prepare_handoff()
        assert "Design" in handoff.continuation_prompt
        assert "Implement" in handoff.continuation_prompt
        assert len(handoff.decisions) == 1
        assert session.status == SessionStatus.HANDED_OFF

    def test_checkpoint_restore_workflow(self, temp_store):
        """Test checkpoint and restore workflow."""
        continuity = SessionContinuity(temp_store)

        # Create and progress session
        continuity.start_session(
            objective="Original task",
            steps=["A", "B", "C"],
        )
        continuity.update_progress(completed_step="A")
        continuity.update_progress(decision="Decision 1")

        # Create checkpoint
        checkpoint_id = continuity.create_checkpoint()

        # End original session
        continuity.end_session()

        # Start new session from checkpoint
        new_session = continuity.start_session(
            objective="Continue task",
            resume_from=checkpoint_id,
        )

        assert new_session.status == SessionStatus.ACTIVE
        assert new_session.current_objective == "Continue task"
