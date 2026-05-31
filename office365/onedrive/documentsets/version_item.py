from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class DocumentSetVersionItem(ClientValue):
    """
    Represents an item that is a part of a captured documentSetVersion.
    """

    itemId: str | None = None
    title: str | None = None
    versionId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DocumentSetVersionItem"
