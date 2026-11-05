from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ContentTypeInfo(ClientValue):
    """
    The contentTypeInfo resource indicates the SharePoint content type of an item.
    """

    id: str | None = None
    name: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ContentTypeInfo"
