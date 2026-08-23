from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.catalog_management_group import CatalogManagementGroup


class CatalogManagementCategory(ClientValue):
    categoryColumnName: str | None = None
    categoryDisplayName: str | None = None
    categoryName: str | None = None
    categoryType: str | None = None
    groups: ClientValueCollection[CatalogManagementGroup] = field(
        default_factory=lambda: ClientValueCollection(CatalogManagementGroup)
    )

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.CatalogManagementCategory"
