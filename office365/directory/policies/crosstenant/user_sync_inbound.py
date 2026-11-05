from __future__ import annotations

from office365.runtime.client_value import ClientValue


class CrossTenantUserSyncInbound(ClientValue):
    isSyncAllowed: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantUserSyncInbound"
