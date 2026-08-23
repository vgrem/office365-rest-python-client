from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.catalog_management_category import CatalogManagementCategory


class CatalogManagementSchema(ClientValue):
    categories: ClientValueCollection[CatalogManagementCategory] = field(
        default_factory=lambda: ClientValueCollection(CatalogManagementCategory)
    )

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.CatalogManagementSchema"
