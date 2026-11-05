from __future__ import annotations

from office365.runtime.client_value import ClientValue


class VirtualEventExternalInformation(ClientValue):
    applicationId: str | None = None
    externalEventId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VirtualEventExternalInformation"
