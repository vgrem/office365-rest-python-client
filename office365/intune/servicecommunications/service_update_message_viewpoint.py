from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ServiceUpdateMessageViewpoint(ClientValue):
    isArchived: bool | None = None
    isFavorited: bool | None = None
    isRead: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ServiceUpdateMessageViewpoint"
