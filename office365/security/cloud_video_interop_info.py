from __future__ import annotations

from office365.runtime.client_value import ClientValue


class CloudVideoInteropInfo(ClientValue):
    moreInfoWebUrl: str | None = None
    tenantKey: str | None = None
    videoTeleconferenceId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudVideoInteropInfo"
