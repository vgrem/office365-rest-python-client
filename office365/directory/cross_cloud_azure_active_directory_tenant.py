from __future__ import annotations

from office365.directory.identitygovernance.entitlementmanagement.identity_source import IdentitySource


class CrossCloudAzureActiveDirectoryTenant(IdentitySource):
    cloudInstance: str | None = None
    displayName: str | None = None
    tenantId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossCloudAzureActiveDirectoryTenant"
