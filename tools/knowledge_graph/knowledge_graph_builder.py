"""
Knowledge Graph Builder - Build and visualize knowledge relationships.

This module provides:
- KnowledgeNode: Represents a knowledge entity
- KnowledgeEdge: Represents a relationship between entities
- KnowledgeGraph: Graph structure for knowledge base
- KnowledgeGraphBuilder: Build graph from knowledge base

Author: SAGE AI Collab Team
Version: 2.0.0
"""

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class NodeType(Enum):
    """Types of knowledge nodes."""

    FILE = "file"
    DIRECTORY = "directory"
    HEADING = "heading"
    CONCEPT = "concept"
    TAG = "tag"


class EdgeType(Enum):
    """Types of relationships between nodes."""

    CONTAINS = "contains"  # Directory contains file
    LINKS_TO = "links_to"  # File links to another
    REFERENCES = "references"  # Concept references another
    TAGGED_WITH = "tagged_with"  # File tagged with concept
    PARENT_OF = "parent_of"  # Heading hierarchy
    RELATED_TO = "related_to"  # General relationship


@dataclass
class KnowledgeNode:
    """Represents a node in the knowledge graph."""

    id: str
    name: str
    node_type: NodeType
    path: str = ""
    level: int = 0  # For headings
    tokens: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.node_type.value,
            "path": self.path,
            "level": self.level,
            "tokens": self.tokens,
            "metadata": self.metadata,
        }


@dataclass
class KnowledgeEdge:
    """Represents an edge in the knowledge graph."""

    source: str  # Node ID
    target: str  # Node ID
    edge_type: EdgeType
    weight: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "source": self.source,
            "target": self.target,
            "type": self.edge_type.value,
            "weight": self.weight,
            "metadata": self.metadata,
        }


@dataclass
class KnowledgeGraph:
    """Knowledge graph structure."""

    nodes: dict[str, KnowledgeNode] = field(default_factory=dict)
    edges: list[KnowledgeEdge] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_node(self, node: KnowledgeNode) -> None:
        """Add a node to the graph."""
        self.nodes[node.id] = node

    def add_edge(self, edge: KnowledgeEdge) -> None:
        """Add an edge to the graph."""
        self.edges.append(edge)

    def get_node(self, node_id: str) -> KnowledgeNode | None:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def get_neighbors(self, node_id: str) -> list[str]:
        """Get all neighbor node IDs."""
        neighbors = []
        for edge in self.edges:
            if edge.source == node_id:
                neighbors.append(edge.target)
            elif edge.target == node_id:
                neighbors.append(edge.source)
        return neighbors

    def get_edges_for_node(self, node_id: str) -> list[KnowledgeEdge]:
        """Get all edges connected to a node."""
        return [e for e in self.edges if e.source == node_id or e.target == node_id]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
            "metadata": self.metadata,
            "stats": {
                "node_count": len(self.nodes),
                "edge_count": len(self.edges),
                "node_types": self._count_by_type(),
            },
        }

    def _count_by_type(self) -> dict[str, int]:
        """Count nodes by type."""
        counts = {}
        for node in self.nodes.values():
            type_name = node.node_type.value
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


class KnowledgeGraphBuilder:
    """
    Build knowledge graph from knowledge base.

    Features:
    - Extract file structure as nodes
    - Extract headings from markdown files
    - Extract links between files
    - Extract concepts and tags
    - Build relationships
    """

    # Patterns
    MD_HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
    MD_LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
    MD_TAG_PATTERN = re.compile(r"#(\w+)")
    CONCEPT_PATTERN = re.compile(r"\*\*([^*]+)\*\*")  # Bold text as concepts

    def __init__(self, kb_path: Path | None = None):
        """
        Initialize graph builder.

        Args:
            kb_path: Path to knowledge base root
        """
        self.kb_path = kb_path or Path(__file__).parent.parent.parent
        self.graph = KnowledgeGraph()
        self._file_nodes: dict[str, str] = {}  # path -> node_id

    def _generate_id(self, prefix: str, name: str) -> str:
        """Generate a unique ID for a node."""
        safe_name = re.sub(r"[^\w]", "_", name.lower())
        return f"{prefix}_{safe_name}"

    def _estimate_tokens(self, content: str) -> int:
        """Estimate token count for content."""
        return len(content) // 4

    def build_from_directory(self, include_content: bool = True) -> KnowledgeGraph:
        """
        Build graph from directory structure.

        Args:
            include_content: Whether to parse file contents

        Returns:
            KnowledgeGraph
        """
        self.graph = KnowledgeGraph()
        self._file_nodes.clear()

        # Add root node
        root_node = KnowledgeNode(
            id="root",
            name=self.kb_path.name,
            node_type=NodeType.DIRECTORY,
            path=str(self.kb_path),
        )
        self.graph.add_node(root_node)

        # Walk directory tree
        self._walk_directory(self.kb_path, "root", include_content)

        # Add metadata
        self.graph.metadata = {
            "built_at": datetime.now().isoformat(),
            "kb_path": str(self.kb_path),
            "include_content": include_content,
        }

        return self.graph

    def _walk_directory(
        self,
        dir_path: Path,
        parent_id: str,
        include_content: bool,
    ) -> None:
        """Recursively walk directory and build nodes."""
        try:
            for item in sorted(dir_path.iterdir()):
                # Skip hidden and special directories
                if item.name.startswith(".") or item.name == "__pycache__":
                    continue

                rel_path = str(item.relative_to(self.kb_path))

                if item.is_dir():
                    # Add directory node
                    node_id = self._generate_id("dir", rel_path)
                    node = KnowledgeNode(
                        id=node_id,
                        name=item.name,
                        node_type=NodeType.DIRECTORY,
                        path=rel_path,
                    )
                    self.graph.add_node(node)
                    self.graph.add_edge(
                        KnowledgeEdge(
                            source=parent_id,
                            target=node_id,
                            edge_type=EdgeType.CONTAINS,
                        )
                    )

                    # Recurse
                    self._walk_directory(item, node_id, include_content)

                elif item.is_file() and item.suffix == ".md":
                    # Add file node
                    node_id = self._generate_id("file", rel_path)
                    self._file_nodes[rel_path] = node_id

                    content = ""
                    tokens = 0
                    if include_content:
                        try:
                            content = item.read_text(encoding="utf-8")
                            tokens = self._estimate_tokens(content)
                        except Exception as e:
                            logger.warning(f"Error reading {item}: {e}")

                    node = KnowledgeNode(
                        id=node_id,
                        name=item.stem,
                        node_type=NodeType.FILE,
                        path=rel_path,
                        tokens=tokens,
                    )
                    self.graph.add_node(node)
                    self.graph.add_edge(
                        KnowledgeEdge(
                            source=parent_id,
                            target=node_id,
                            edge_type=EdgeType.CONTAINS,
                        )
                    )

                    # Parse content for headings and links
                    if content:
                        self._parse_file_content(node_id, rel_path, content)

        except PermissionError:
            logger.warning(f"Permission denied: {dir_path}")

    def _parse_file_content(
        self,
        file_node_id: str,
        file_path: str,
        content: str,
    ) -> None:
        """Parse file content for headings, links, and concepts."""
        # Extract headings
        prev_heading_id = file_node_id
        prev_level = 0

        for match in self.MD_HEADING_PATTERN.finditer(content):
            level = len(match.group(1))
            heading_text = match.group(2).strip()

            heading_id = self._generate_id(f"h{level}", f"{file_path}_{heading_text}")

            heading_node = KnowledgeNode(
                id=heading_id,
                name=heading_text,
                node_type=NodeType.HEADING,
                path=file_path,
                level=level,
            )
            self.graph.add_node(heading_node)

            # Link to parent (file or higher-level heading)
            if level == 1 or level <= prev_level:
                self.graph.add_edge(
                    KnowledgeEdge(
                        source=file_node_id,
                        target=heading_id,
                        edge_type=EdgeType.CONTAINS,
                    )
                )
            else:
                self.graph.add_edge(
                    KnowledgeEdge(
                        source=prev_heading_id,
                        target=heading_id,
                        edge_type=EdgeType.PARENT_OF,
                    )
                )

            prev_heading_id = heading_id
            prev_level = level

        # Extract links
        for match in self.MD_LINK_PATTERN.finditer(content):
            link_text = match.group(1)
            link_target = match.group(2)

            # Only process internal links
            if not link_target.startswith(("http://", "https://", "#")):
                # Resolve relative path
                target_path = self._resolve_link_path(file_path, link_target)
                target_node_id = self._file_nodes.get(target_path)

                if target_node_id:
                    self.graph.add_edge(
                        KnowledgeEdge(
                            source=file_node_id,
                            target=target_node_id,
                            edge_type=EdgeType.LINKS_TO,
                            metadata={"link_text": link_text},
                        )
                    )

        # Extract concepts (bold text)
        concepts_found = set()
        for match in self.CONCEPT_PATTERN.finditer(content):
            concept = match.group(1).strip()
            if len(concept) > 2 and concept not in concepts_found:
                concepts_found.add(concept)

                concept_id = self._generate_id("concept", concept)

                # Add concept node if not exists
                if concept_id not in self.graph.nodes:
                    self.graph.add_node(
                        KnowledgeNode(
                            id=concept_id,
                            name=concept,
                            node_type=NodeType.CONCEPT,
                        )
                    )

                self.graph.add_edge(
                    KnowledgeEdge(
                        source=file_node_id,
                        target=concept_id,
                        edge_type=EdgeType.REFERENCES,
                    )
                )

    def _resolve_link_path(self, source_path: str, link_target: str) -> str:
        """Resolve a relative link path."""
        # Remove anchor
        link_target = link_target.split("#")[0]
        if not link_target:
            return source_path

        source_dir = Path(source_path).parent
        resolved = (source_dir / link_target).resolve()

        try:
            return str(resolved.relative_to(self.kb_path.resolve())).replace("\\", "/")
        except ValueError:
            return link_target

    def get_file_graph(self, file_path: str) -> KnowledgeGraph:
        """
        Get a subgraph for a specific file.

        Args:
            file_path: Relative path to the file

        Returns:
            KnowledgeGraph containing the file and its relationships
        """
        if not self.graph.nodes:
            self.build_from_directory()

        node_id = self._file_nodes.get(file_path)
        if not node_id:
            return KnowledgeGraph()

        # Get all connected nodes
        connected = {node_id}
        for edge in self.graph.edges:
            if edge.source == node_id:
                connected.add(edge.target)
            elif edge.target == node_id:
                connected.add(edge.source)

        # Build subgraph
        subgraph = KnowledgeGraph()
        for nid in connected:
            node = self.graph.get_node(nid)
            if node:
                subgraph.add_node(node)

        for edge in self.graph.edges:
            if edge.source in connected and edge.target in connected:
                subgraph.add_edge(edge)

        return subgraph

    def get_statistics(self) -> dict[str, Any]:
        """Get graph statistics."""
        if not self.graph.nodes:
            self.build_from_directory()

        # Count by type
        type_counts = {}
        total_tokens = 0
        for node in self.graph.nodes.values():
            type_name = node.node_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
            total_tokens += node.tokens

        # Count edges by type
        edge_counts = {}
        for edge in self.graph.edges:
            type_name = edge.edge_type.value
            edge_counts[type_name] = edge_counts.get(type_name, 0) + 1

        return {
            "total_nodes": len(self.graph.nodes),
            "total_edges": len(self.graph.edges),
            "total_tokens": total_tokens,
            "nodes_by_type": type_counts,
            "edges_by_type": edge_counts,
        }

    def export_to_json(self, output_path: Path) -> None:
        """Export graph to JSON file."""
        if not self.graph.nodes:
            self.build_from_directory()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(self.graph.to_json())

        logger.info(f"Graph exported to {output_path}")


# Convenience function
def build_knowledge_graph(kb_path: Path | None = None) -> KnowledgeGraph:
    """Quick function to build knowledge graph."""
    builder = KnowledgeGraphBuilder(kb_path=kb_path)
    return builder.build_from_directory()
