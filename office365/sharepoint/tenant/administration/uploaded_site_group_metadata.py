from __future__ import annotations

from office365.runtime.client_value import ClientValue


class UploadedSiteGroupMetadata(ClientValue):
    groupName: str | None = None
    siteCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.UploadedSiteGroupMetadata"
