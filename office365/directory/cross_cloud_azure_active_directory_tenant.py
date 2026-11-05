from __future__ import annotations

from office365.runtime.client_value import ClientValue


class CrossCloudAzureActiveDirectoryTenant(ClientValue):
    cloudInstance: str | None = None
    displayName: str | None = None
    tenantId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossCloudAzureActiveDirectoryTenant"
