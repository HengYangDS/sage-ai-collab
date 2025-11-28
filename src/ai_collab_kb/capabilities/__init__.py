"""
Runtime Capabilities Module.

This module provides runtime capabilities that can be exposed via MCP/API services.
These are distinct from dev-only tools in the tools/ directory.

Capabilities include:
- analyzers: Quality, content, structure analysis
- checkers: Link validation
- monitors: Health monitoring

Usage:
    from ai_collab_kb.capabilities.analyzers import QualityAnalyzer
    from ai_collab_kb.capabilities.checkers import LinkChecker
    from ai_collab_kb.capabilities.monitors import HealthMonitor

MCP Tools exposed:
    - analyze_quality: QualityAnalyzer.analyze_file()
    - analyze_content: ContentAnalyzer.analyze()
    - check_structure: StructureChecker.check()
    - check_links: LinkChecker.check()
    - get_health: HealthMonitor.get_status()
"""

from ai_collab_kb.capabilities.analyzers import (
    ContentAnalyzer,
    ContentMetrics,
    QualityAnalyzer,
    QualityScore,
    StructureChecker,
    StructureReport,
)
from ai_collab_kb.capabilities.checkers import (
    LinkChecker,
)
from ai_collab_kb.capabilities.monitors import (
    HealthMonitor,
)

__all__ = [
    # Analyzers
    "QualityAnalyzer",
    "QualityScore",
    "ContentAnalyzer",
    "ContentMetrics",
    "StructureChecker",
    "StructureReport",
    # Checkers
    "LinkChecker",
    # Monitors
    "HealthMonitor",
]
