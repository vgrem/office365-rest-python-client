from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ImageInfo(ClientValue):
    addImageQuery: bool | None = None
    alternateText: str | None = None
    alternativeText: str | None = None
    iconUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ImageInfo"
