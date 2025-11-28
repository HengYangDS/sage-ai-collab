"""
SAGE Core Layer.

Core infrastructure components:
- KnowledgeLoader: Knowledge loading with timeout protection
- Layer: Knowledge layer enumeration
"""

from .loader import KnowledgeLoader, Layer

__all__ = ["KnowledgeLoader", "Layer"]
