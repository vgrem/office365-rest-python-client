from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.uploaded_site_group_metadata import UploadedSiteGroupMetadata


class UploadedSiteCategoryMetadata(ClientValue):
    description: str | None = None
    displayName: str | None = None
    groups: ClientValueCollection[UploadedSiteGroupMetadata] = field(
        default_factory=lambda: ClientValueCollection(UploadedSiteGroupMetadata)
    )
    id: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.UploadedSiteCategoryMetadata"
