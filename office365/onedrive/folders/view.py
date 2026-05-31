from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class FolderView(ClientValue):
    """The FolderView resource provides or sets recommendations on the user-experience of a folder."""

    sortBy: str | None = None
    sortOrder: str | None = None
    viewType: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FolderView"
