from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.rcd_group_metadata import RcdGroupMetadata


class RcdCategoriesMap(ClientValue):
    groups: ClientValueCollection[RcdGroupMetadata] = field(
        default_factory=lambda: ClientValueCollection(RcdGroupMetadata)
    )
    quotaLimit: int | None = None
    quotaUsed: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.RcdCategoriesMap"
