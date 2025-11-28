"""
SAGE Core Layer.

Core infrastructure components:
- KnowledgeLoader: Knowledge loading with timeout protection
- Layer: Knowledge layer enumeration
- DI: Dependency Injection container with lifetime management
"""

from .loader import KnowledgeLoader, Layer
from .di import (
    DIContainer,
    DIScope,
    Lifetime,
    get_container,
    TypeRegistry,
    get_registry,
)

__all__ = [
    # Loader
    "KnowledgeLoader",
    "Layer",
    # DI Container
    "DIContainer",
    "DIScope",
    "Lifetime",
    "get_container",
    "TypeRegistry",
    "get_registry",
]
