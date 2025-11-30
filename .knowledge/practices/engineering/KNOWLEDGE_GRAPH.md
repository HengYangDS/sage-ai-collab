# Knowledge Graph Guide

> Building and using knowledge graphs for content analysis and visualization

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Getting Started](#2-getting-started)
- [3. Graph Structure](#3-graph-structure)
- [4. Building Graphs](#4-building-graphs)
- [5. Analysis & Queries](#5-analysis--queries)
- [6. Visualization](#6-visualization)
- [7. Best Practices](#7-best-practices)
- [8. Use Cases](#8-use-cases)

---

## 1. Overview

### 1.1 What is a Knowledge Graph?

A knowledge graph represents relationships between knowledge base content:

- **Nodes**: Files, concepts, tags, categories
- **Edges**: Links, references, relationships
- **Properties**: Metadata, content, statistics

### 1.2 Benefits

| Benefit                  | Description                        |
|--------------------------|------------------------------------|
| **Discover connections** | Find related content automatically |
| **Identify gaps**        | Spot missing documentation         |
| **Analyze structure**    | Understand KB organization         |
| **Optimize navigation**  | Improve content findability        |
| **Validate links**       | Detect broken references           |

### 1.3 Graph Types

| Type              | Nodes     | Edges               | Use Case               |
|-------------------|-----------|---------------------|------------------------|
| **File Graph**    | Files     | Links between files | Navigation analysis    |
| **Concept Graph** | Concepts  | Semantic relations  | Topic modeling         |
| **Tag Graph**     | Tags      | Co-occurrence       | Classification         |
| **Full Graph**    | All types | All relations       | Comprehensive analysis |

---

## 2. Getting Started

### 2.1 Quick Start

```bash
# Via CLI
sage graph build --path .knowledge/

# Via MCP tool
build_knowledge_graph(path="content")
```
### 2.2 Output Location

All graph outputs are saved to `.outputs/` directory:

```bash
# Build with output file
sage graph build --output graph.json

# File saved to: .outputs/graph.json
```
### 2.3 Basic Usage

```python
from tools.knowledge_graph.knowledge_graph_builder import KnowledgeGraphBuilder
from pathlib import Path

# Create builder
builder = KnowledgeGraphBuilder(kb_path=Path("content"))

# Build graph
graph = builder.build_from_directory()

# Get statistics
stats = builder.get_statistics()
print(f"Nodes: {stats['total_nodes']}")
print(f"Edges: {stats['total_edges']}")

# Export to JSON
builder.export_to_json(Path(".outputs/graph.json"))
```
---

## 3. Graph Structure

### 3.1 Node Types

| Type        | Description         | Properties          |
|-------------|---------------------|---------------------|
| `FILE`      | Markdown/YAML files | path, title, tokens |
| `DIRECTORY` | Folders             | path, file_count    |
| `CONCEPT`   | Extracted concepts  | name, frequency     |
| `TAG`       | Document tags       | name, count         |
| `CATEGORY`  | Content categories  | name, description   |

### 3.2 Edge Types

| Type          | Description             | Example            |
|---------------|-------------------------|--------------------|
| `LINKS_TO`    | File links to file      | `A.md → B.md`      |
| `CONTAINS`    | Directory contains file | `docs/ → A.md`     |
| `REFERENCES`  | File references concept | `A.md → "timeout"` |
| `TAGGED_WITH` | File has tag            | `A.md → "guide"`   |
| `RELATED_TO`  | Semantic similarity     | `A.md ↔ B.md`      |

### 3.3 Data Model

```python
from dataclasses import dataclass
from enum import Enum

class NodeType(Enum):
    FILE = "file"
    DIRECTORY = "directory"
    CONCEPT = "concept"
    TAG = "tag"

class EdgeType(Enum):
    LINKS_TO = "links_to"
    CONTAINS = "contains"
    REFERENCES = "references"
    TAGGED_WITH = "tagged_with"

@dataclass
class KnowledgeNode:
    id: str
    name: str
    node_type: NodeType
    properties: dict
    tokens: int = 0

@dataclass
class KnowledgeEdge:
    source: str
    target: str
    edge_type: EdgeType
    weight: float = 1.0
```
---

## 4. Building Graphs

### 4.1 Full Graph Build

```python
builder = KnowledgeGraphBuilder(kb_path=Path("content"))

# Build with all options
graph = builder.build_from_directory(
    include_content=True,  # Include file content in nodes
    extract_concepts=True,  # Extract concepts from text
    extract_tags=True,  # Extract tags from frontmatter
)
```
### 4.2 Incremental Build

```python
# Build only changed files
graph = builder.build_incremental(
    since=last_build_time,
    changed_files=[".knowledge/new_file.md"]
)
```
### 4.3 Filtered Build

```python
# Build specific directories
graph = builder.build_from_directory(
    include_patterns=[".knowledge/core/**", ".knowledge/guidelines/**"],
    exclude_patterns=["**/_*", "**/archive/**"]
)
```
### 4.4 MCP Tool Usage

```python
# Via MCP tool
result = await build_knowledge_graph(
    path="content",
    include_content=False,
    output_file="analysis.json"  # Saved to .outputs/analysis.json
)

print(f"Nodes: {result['result']['total_nodes']}")
print(f"Edges: {result['result']['total_edges']}")
```
---

## 5. Analysis & Queries

### 5.1 Basic Statistics

```python
stats = builder.get_statistics()

# Output:
# {
#     "total_nodes": 150,
#     "total_edges": 320,
#     "total_tokens": 45000,
#     "nodes_by_type": {"file": 80, "concept": 50, "tag": 20},
#     "edges_by_type": {"links_to": 200, "references": 100, "tagged_with": 20}
# }
```
### 5.2 Find Related Content

```python
# Get subgraph for a specific file
file_graph = builder.get_file_graph(".knowledge/core/PRINCIPLES.md")

# Find files linked from this file
outgoing = [
    edge.target for edge in file_graph.edges
    if edge.edge_type == EdgeType.LINKS_TO
]

# Find files linking to this file
incoming = [
    edge.source for edge in graph.edges
    if edge.target == file_id and edge.edge_type == EdgeType.LINKS_TO
]
```
### 5.3 Identify Orphan Files

```python
def find_orphans(graph):
    """Find files with no incoming links."""
    linked_files = set()
    all_files = set()

    for node in graph.nodes.values():
        if node.node_type == NodeType.FILE:
            all_files.add(node.id)

    for edge in graph.edges:
        if edge.edge_type == EdgeType.LINKS_TO:
            linked_files.add(edge.target)

    return all_files - linked_files
```
### 5.4 Find Broken Links

```python
def find_broken_links(graph):
    """Find edges pointing to non-existent nodes."""
    broken = []
    node_ids = set(graph.nodes.keys())

    for edge in graph.edges:
        if edge.target not in node_ids:
            broken.append(
                {
                    "source": edge.source,
                    "target": edge.target,
                    "type"  : edge.edge_type.value
                }
            )

    return broken
```
### 5.5 Centrality Analysis

```python
def calculate_centrality(graph):
    """Calculate node importance by connection count."""
    centrality = {}

    for node_id in graph.nodes:
        incoming = sum(1 for e in graph.edges if e.target == node_id)
        outgoing = sum(1 for e in graph.edges if e.source == node_id)
        centrality[node_id] = incoming + outgoing

    # Sort by centrality
    return sorted(centrality.items(), key=lambda x: x[1], reverse=True)
```
---

## 6. Visualization

### 6.1 Export Formats

| Format  | Use Case          | Tool       |
|---------|-------------------|------------|
| JSON    | Data exchange     | Any        |
| GraphML | Graph tools       | Gephi, yEd |
| DOT     | Graphviz          | Graphviz   |
| D3 JSON | Web visualization | D3.js      |

### 6.2 JSON Export

```python
# Export to JSON
builder.export_to_json(Path(".outputs/graph.json"))

# JSON structure:
# {
#     "nodes": [
#         {"id": "...", "name": "...", "type": "file", ...}
#     ],
#     "edges": [
#         {"source": "...", "target": "...", "type": "links_to", ...}
#     ],
#     "metadata": {
#         "created": "2025-11-29T22:00:00",
#         "total_nodes": 150,
#         "total_edges": 320
#     }
# }
```
### 6.3 Visualization Tools

**Graphviz (DOT format)**:

```python
def export_to_dot(graph, output_path):
    lines = ["digraph KnowledgeGraph {"]
    lines.append('  rankdir=LR;')

    for node in graph.nodes.values():
        shape = "box" if node.node_type == NodeType.FILE else "ellipse"
        lines.append(f'  "{node.id}" [label="{node.name}" shape={shape}];')

    for edge in graph.edges:
        lines.append(f'  "{edge.source}" -> "{edge.target}";')

    lines.append("}")

    Path(output_path).write_text("\n".join(lines))
```
**D3.js Format**:

```python
def export_to_d3(graph, output_path):
    d3_data = {
        "nodes": [
            {"id": n.id, "name": n.name, "group": n.node_type.value}
            for n in graph.nodes.values()
        ],
        "links": [
            {"source": e.source, "target": e.target, "value": e.weight}
            for e in graph.edges
        ]
    }

    with open(output_path, "w") as f:
        json.dump(d3_data, f, indent=2)
```
---

## 7. Best Practices

### 7.1 Performance Tips

| Tip                     | Description                           |
|-------------------------|---------------------------------------|
| **Limit scope**         | Build graphs for specific directories |
| **Exclude large files** | Skip files over token limit           |
| **Cache results**       | Reuse graphs when content unchanged   |
| **Incremental builds**  | Only process changed files            |

### 7.2 Graph Maintenance

```python
# Regular maintenance script
def maintain_graph():
    builder = KnowledgeGraphBuilder(kb_path=Path("content"))
    graph = builder.build_from_directory()

    # Check for issues
    orphans = find_orphans(graph)
    broken = find_broken_links(graph)

    if orphans:
        print(f"Warning: {len(orphans)} orphan files found")

    if broken:
        print(f"Error: {len(broken)} broken links found")

    # Export for review
    builder.export_to_json(Path(".outputs/maintenance_graph.json"))
```
### 7.3 Content Organization

| Practice                    | Benefit                     |
|-----------------------------|-----------------------------|
| **Use consistent naming**   | Better concept extraction   |
| **Add frontmatter tags**    | Improved classification     |
| **Maintain internal links** | Stronger graph connectivity |
| **Group related content**   | Clearer structure           |

---

## 8. Use Cases

### 8.1 Documentation Audit

```python
# Audit knowledge base completeness
def audit_documentation():
    builder = KnowledgeGraphBuilder(kb_path=Path("content"))
    graph = builder.build_from_directory()
    stats = builder.get_statistics()

    report = {
        "total_files"    : stats["nodes_by_type"].get("file", 0),
        "total_concepts" : stats["nodes_by_type"].get("concept", 0),
        "orphan_files"   : len(find_orphans(graph)),
        "broken_links"   : len(find_broken_links(graph)),
        "avg_connections": stats["total_edges"] / max(stats["total_nodes"], 1)
    }

    return report
```
### 8.2 Content Recommendations

```python
# Find related content for a file
def recommend_related(file_path, graph, top_n=5):
    file_id = f"file:{file_path}"

    # Get concepts from this file
    file_concepts = set()
    for edge in graph.edges:
        if edge.source == file_id and edge.edge_type == EdgeType.REFERENCES:
            file_concepts.add(edge.target)

    # Find files with similar concepts
    similarity = {}
    for edge in graph.edges:
        if (edge.edge_type == EdgeType.REFERENCES and
            edge.target in file_concepts and
            edge.source != file_id):
            similarity[edge.source] = similarity.get(edge.source, 0) + 1

    # Return top N
    return sorted(similarity.items(), key=lambda x: x[1], reverse=True)[:top_n]
```
### 8.3 Knowledge Gap Analysis

```python
# Identify topics needing more documentation
def find_knowledge_gaps(graph, min_coverage=3):
    concept_coverage = {}

    for edge in graph.edges:
        if edge.edge_type == EdgeType.REFERENCES:
            concept = edge.target
            concept_coverage[concept] = concept_coverage.get(concept, 0) + 1

    # Find under-documented concepts
    gaps = [
        concept for concept, count in concept_coverage.items()
        if count < min_coverage
    ]

    return gaps
```
### 8.4 Navigation Optimization

```python
# Suggest new links to improve navigation
def suggest_links(graph, threshold=0.5):
    suggestions = []
    file_nodes = [n for n in graph.nodes.values() if n.node_type == NodeType.FILE]

    for file1 in file_nodes:
        for file2 in file_nodes:
            if file1.id == file2.id:
                continue

            # Calculate similarity based on shared concepts
            concepts1 = get_file_concepts(file1.id, graph)
            concepts2 = get_file_concepts(file2.id, graph)

            if concepts1 and concepts2:
                similarity = len(concepts1 & concepts2) / len(concepts1 | concepts2)

                if similarity >= threshold:
                    # Check if link exists
                    link_exists = any(
                        e.source == file1.id and e.target == file2.id
                        for e in graph.edges if e.edge_type == EdgeType.LINKS_TO
                    )

                    if not link_exists:
                        suggestions.append(
                            {
                                "from"      : file1.name,
                                "to"        : file2.name,
                                "similarity": similarity
                            }
                        )

    return suggestions
```
---

## Quick Reference

### CLI Commands

```bash
sage graph build                    # Build full graph
sage graph build --path .knowledge/    # Build specific path
sage graph build --output g.json    # Export to file
sage graph stats                    # Show statistics
sage graph check                    # Check for issues
```
### MCP Tool

```python
# Build graph
result = await build_knowledge_graph(
    path="content",
    include_content=False,
    output_file="graph.json"
)

# Result structure
{
    "success": True,
    "result" : {
        "total_nodes"  : 150,
        "total_edges"  : 320,
        "total_tokens" : 45000,
        "nodes_by_type": {...},
        "edges_by_type": {...}
    }
}
```
---

## Related

- `tools/knowledge_graph/` — Graph builder implementation
- `docs/guides/MCP_TOOLS.md` — MCP tools reference
- `.knowledge/practices/documentation/KNOWLEDGE_ORGANIZATION.md` — Content organization
- `.outputs/` — Graph output directory

---

*AI Collaboration Knowledge Base*
