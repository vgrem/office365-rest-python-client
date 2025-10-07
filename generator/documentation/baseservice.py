from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from generator.builders.type_builder import TypeBuilder


class BaseDocumentationService(ABC):
    """Abstract base class for documentation services"""

    def __init__(self):
        self._documentation_cache = {}

    @abstractmethod
    def build_documentation(self, type_builder: TypeBuilder):
        """Build documentation for the given type builder"""
        pass
