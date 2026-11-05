from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ExternalTokenBasedSapIagConnectionInfo(ClientValue):
    accessTokenUrl: str | None = None
    clientId: str | None = None
    keyVaultName: str | None = None
    resourceGroup: str | None = None
    secretName: str | None = None
    subscriptionId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ExternalTokenBasedSapIagConnectionInfo"
