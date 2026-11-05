from __future__ import annotations

from office365.runtime.client_value import ClientValue


class HyperlinkOrPictureColumn(ClientValue):
    """Represents a hyperlink or picture column in SharePoint."""

    isPicture: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.HyperlinkOrPictureColumn"
