"""Base contract for documentation providers (docstring injection)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from generator.builders.type import TypeBuilder


class DocumentationProvider(ABC):
    """Enriches a type builder with docstrings before the file is written."""

    @abstractmethod
    def build_documentation(self, type_builder: TypeBuilder) -> None:
        """Inject descriptions into ``type_builder``."""
