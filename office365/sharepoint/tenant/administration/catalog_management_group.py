from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class CatalogManagementGroup(ClientValue):
    groupDisplayName: str | None = None
    groupId: UUID | None = None
    groupName: str | None = None
    siteCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.CatalogManagementGroup"
