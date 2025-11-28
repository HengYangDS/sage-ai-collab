"""
Knowledge Domain Models.

Business domain models for knowledge assets and knowledge cycles.
These models represent the core concepts in the knowledge management domain.

Version: 0.1.0
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class KnowledgeLayer(str, Enum):
    """Knowledge layer classification following L0-L4 hierarchy."""

    L0_INDEX = "index"  # Navigation index (~100 tokens)
    L1_CORE = "core"  # Core principles (~500 tokens)
    L2_GUIDELINES = "guidelines"  # Engineering guidelines (~1,200 tokens)
    L3_FRAMEWORKS = "frameworks"  # Deep frameworks (~2,000 tokens)
    L4_PRACTICES = "practices"  # Best practices (~1,500 tokens)


class ContentType(str, Enum):
    """Type of knowledge content."""

    PRINCIPLE = "principle"
    GUIDELINE = "guideline"
    FRAMEWORK = "framework"
    PRACTICE = "practice"
    TEMPLATE = "template"
    SCENARIO = "scenario"
    REFERENCE = "reference"


class AssetStatus(str, Enum):
    """Status of a knowledge asset."""

    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


@dataclass
class KnowledgeMetadata:
    """Metadata for a knowledge asset."""

    title: str
    version: str = "0.1.0"
    author: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    custom: dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeAsset:
    """
    A knowledge asset in the knowledge base.

    Represents a single unit of knowledge content with its metadata,
    classification, and relationships to other assets.

    Attributes:
        id: Unique identifier for the asset
        path: File path relative to knowledge base root
        layer: Knowledge layer (L0-L4)
        content_type: Type of content
        content: Raw content string
        metadata: Asset metadata
        status: Current status
        tokens: Estimated token count
        checksum: Content checksum for change detection
    """

    id: str
    path: Path
    layer: KnowledgeLayer
    content_type: ContentType
    content: str
    metadata: KnowledgeMetadata = field(default_factory=lambda: KnowledgeMetadata(title="Untitled"))
    status: AssetStatus = AssetStatus.APPROVED
    tokens: int = 0
    checksum: str | None = None

    def __post_init__(self) -> None:
        """Calculate tokens if not provided."""
        if self.tokens == 0 and self.content:
            # Rough estimate: ~4 chars per token
            self.tokens = len(self.content) // 4

    @property
    def is_loadable(self) -> bool:
        """Check if asset can be loaded (not deprecated/archived)."""
        return self.status in (AssetStatus.DRAFT, AssetStatus.REVIEW, AssetStatus.APPROVED)


@dataclass
class KnowledgeCycle:
    """
    A knowledge lifecycle cycle tracking SAGE operations.

    Tracks the full cycle of Source -> Analyze -> Generate -> Evolve
    for audit and optimization purposes.

    Attributes:
        cycle_id: Unique cycle identifier
        started_at: Cycle start timestamp
        completed_at: Cycle completion timestamp
        source_result: Result from Source stage
        analyze_result: Result from Analyze stage
        generate_result: Result from Generate stage
        evolve_result: Result from Evolve stage
        status: Current cycle status
        metrics: Performance metrics for the cycle
    """

    cycle_id: str
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
    source_result: dict[str, Any] | None = None
    analyze_result: dict[str, Any] | None = None
    generate_result: dict[str, Any] | None = None
    evolve_result: dict[str, Any] | None = None
    status: str = "in_progress"  # in_progress | completed | failed
    metrics: dict[str, Any] = field(default_factory=dict)

    def complete(self) -> None:
        """Mark cycle as completed."""
        self.completed_at = datetime.now()
        self.status = "completed"

    def fail(self, error: str) -> None:
        """Mark cycle as failed."""
        self.completed_at = datetime.now()
        self.status = "failed"
        self.metrics["error"] = error

    @property
    def duration_ms(self) -> int | None:
        """Calculate cycle duration in milliseconds."""
        if self.completed_at is None:
            return None
        delta = self.completed_at - self.started_at
        return int(delta.total_seconds() * 1000)


@dataclass
class KnowledgeIndex:
    """
    Index of all knowledge assets.

    Provides fast lookup and navigation of knowledge assets.

    Attributes:
        assets: Dictionary of asset_id -> KnowledgeAsset
        by_layer: Assets grouped by layer
        by_type: Assets grouped by content type
        total_tokens: Total tokens across all assets
        last_updated: Last index update timestamp
    """

    assets: dict[str, KnowledgeAsset] = field(default_factory=dict)
    by_layer: dict[KnowledgeLayer, list[str]] = field(default_factory=dict)
    by_type: dict[ContentType, list[str]] = field(default_factory=dict)
    total_tokens: int = 0
    last_updated: datetime = field(default_factory=datetime.now)

    def add_asset(self, asset: KnowledgeAsset) -> None:
        """Add an asset to the index."""
        self.assets[asset.id] = asset
        self.total_tokens += asset.tokens

        # Index by layer
        if asset.layer not in self.by_layer:
            self.by_layer[asset.layer] = []
        self.by_layer[asset.layer].append(asset.id)

        # Index by type
        if asset.content_type not in self.by_type:
            self.by_type[asset.content_type] = []
        self.by_type[asset.content_type].append(asset.id)

        self.last_updated = datetime.now()

    def remove_asset(self, asset_id: str) -> KnowledgeAsset | None:
        """Remove an asset from the index."""
        if asset_id not in self.assets:
            return None

        asset = self.assets.pop(asset_id)
        self.total_tokens -= asset.tokens

        # Remove from layer index
        if asset.layer in self.by_layer:
            self.by_layer[asset.layer] = [
                aid for aid in self.by_layer[asset.layer] if aid != asset_id
            ]

        # Remove from type index
        if asset.content_type in self.by_type:
            self.by_type[asset.content_type] = [
                aid for aid in self.by_type[asset.content_type] if aid != asset_id
            ]

        self.last_updated = datetime.now()
        return asset

    def get_by_layer(self, layer: KnowledgeLayer) -> list[KnowledgeAsset]:
        """Get all assets in a layer."""
        asset_ids = self.by_layer.get(layer, [])
        return [self.assets[aid] for aid in asset_ids if aid in self.assets]
