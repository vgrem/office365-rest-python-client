from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ContentTypeOrder(ClientValue):
    """The contentTypeOrder resource specifies in which order the Content Type will appear in the selection UI."""

    default: bool | None = None
    position: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ContentTypeOrder"
