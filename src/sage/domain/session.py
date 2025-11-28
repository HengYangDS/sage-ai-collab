"""
Session Domain Models.

Business domain models for collaboration sessions and interactions.
These models track AI-human collaboration state and history.

Version: 0.1.0
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class SessionStatus(str, Enum):
    """Status of a collaboration session."""

    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class InteractionType(str, Enum):
    """Type of interaction in a session."""

    QUERY = "query"  # User query
    RESPONSE = "response"  # AI response
    COMMAND = "command"  # CLI/MCP command
    FEEDBACK = "feedback"  # User feedback
    CHECKPOINT = "checkpoint"  # Session checkpoint
    HANDOFF = "handoff"  # Task handoff


class AutonomyLevel(int, Enum):
    """AI autonomy level for the session."""

    L1_MINIMAL = 1  # Wait for explicit approval
    L2_SUGGEST = 2  # Suggest and wait
    L3_INFORM = 3  # Inform then proceed
    L4_AUTONOMOUS = 4  # Proceed with logs
    L5_FULL = 5  # Full autonomy
    L6_EXPERT = 6  # Expert committee mode


@dataclass
class Interaction:
    """
    A single interaction in a collaboration session.

    Attributes:
        id: Unique interaction identifier
        type: Type of interaction
        timestamp: When the interaction occurred
        content: Interaction content
        tokens: Token count for the interaction
        metadata: Additional interaction data
    """

    id: str
    type: InteractionType
    timestamp: datetime = field(default_factory=datetime.now)
    content: str = ""
    tokens: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SessionContext:
    """
    Context information for a session.

    Tracks the current state and configuration of a collaboration session.

    Attributes:
        task: Current task description
        autonomy_level: Current autonomy level
        loaded_layers: Currently loaded knowledge layers
        active_frameworks: Active decision frameworks
        custom: Custom context data
    """

    task: str = ""
    autonomy_level: AutonomyLevel = AutonomyLevel.L3_INFORM
    loaded_layers: list[str] = field(default_factory=list)
    active_frameworks: list[str] = field(default_factory=list)
    custom: dict[str, Any] = field(default_factory=dict)


@dataclass
class CollaborationSession:
    """
    A collaboration session between AI and human.

    Tracks the full lifecycle of an AI-human collaboration including
    interactions, context, and metrics.

    Attributes:
        session_id: Unique session identifier
        created_at: Session creation timestamp
        updated_at: Last update timestamp
        status: Current session status
        context: Session context
        interactions: List of interactions
        metrics: Session metrics
        checkpoints: Session checkpoints for recovery
    """

    session_id: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    status: SessionStatus = SessionStatus.ACTIVE
    context: SessionContext = field(default_factory=SessionContext)
    interactions: list[Interaction] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    checkpoints: list[str] = field(default_factory=list)

    def add_interaction(self, interaction: Interaction) -> None:
        """Add an interaction to the session."""
        self.interactions.append(interaction)
        self.updated_at = datetime.now()

        # Update metrics
        self.metrics["interaction_count"] = len(self.interactions)
        self.metrics["total_tokens"] = sum(i.tokens for i in self.interactions)

    def pause(self) -> None:
        """Pause the session."""
        self.status = SessionStatus.PAUSED
        self.updated_at = datetime.now()

    def resume(self) -> None:
        """Resume a paused session."""
        if self.status == SessionStatus.PAUSED:
            self.status = SessionStatus.ACTIVE
            self.updated_at = datetime.now()

    def complete(self) -> None:
        """Mark session as completed."""
        self.status = SessionStatus.COMPLETED
        self.updated_at = datetime.now()
        self.metrics["completed_at"] = datetime.now().isoformat()

    def abandon(self) -> None:
        """Mark session as abandoned."""
        self.status = SessionStatus.ABANDONED
        self.updated_at = datetime.now()

    @property
    def duration_seconds(self) -> float:
        """Calculate session duration in seconds."""
        return (self.updated_at - self.created_at).total_seconds()

    @property
    def is_active(self) -> bool:
        """Check if session is active."""
        return self.status == SessionStatus.ACTIVE

    def to_dict(self) -> dict[str, Any]:
        """Convert session to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "status": self.status.value,
            "context": {
                "task": self.context.task,
                "autonomy_level": self.context.autonomy_level.value,
                "loaded_layers": self.context.loaded_layers,
                "active_frameworks": self.context.active_frameworks,
                "custom": self.context.custom,
            },
            "interaction_count": len(self.interactions),
            "metrics": self.metrics,
            "checkpoints": self.checkpoints,
        }


@dataclass
class HandoffPackage:
    """
    Package for handing off a task between sessions or agents.

    Contains all necessary context for seamless task continuation.

    Attributes:
        handoff_id: Unique handoff identifier
        source_session_id: Original session ID
        target_session_id: Target session ID (if known)
        timestamp: Handoff creation timestamp
        task_summary: Summary of the current task
        context_snapshot: Snapshot of session context
        pending_actions: Actions that need to be completed
        recommendations: Recommendations for the receiving agent
        metadata: Additional handoff data
    """

    handoff_id: str
    source_session_id: str
    target_session_id: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    task_summary: str = ""
    context_snapshot: dict[str, Any] = field(default_factory=dict)
    pending_actions: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert handoff to dictionary for serialization."""
        return {
            "handoff_id": self.handoff_id,
            "source_session_id": self.source_session_id,
            "target_session_id": self.target_session_id,
            "timestamp": self.timestamp.isoformat(),
            "task_summary": self.task_summary,
            "context_snapshot": self.context_snapshot,
            "pending_actions": self.pending_actions,
            "recommendations": self.recommendations,
            "metadata": self.metadata,
        }

    @classmethod
    def from_session(
        cls,
        session: CollaborationSession,
        handoff_id: str,
        task_summary: str = "",
    ) -> "HandoffPackage":
        """Create a handoff package from a session."""
        return cls(
            handoff_id=handoff_id,
            source_session_id=session.session_id,
            task_summary=task_summary or session.context.task,
            context_snapshot=session.to_dict(),
            metadata={"original_status": session.status.value},
        )
