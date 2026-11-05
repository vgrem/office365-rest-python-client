from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SpecialFolder(ClientValue):
    """The SpecialFolder resource groups special folder-related data items into a single structure."""

    name: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SpecialFolder"
