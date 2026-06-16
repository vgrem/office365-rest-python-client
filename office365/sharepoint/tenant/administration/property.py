from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.propertyvalue import PropertyValue


class Property(ClientValue):
    propertyType: int | None = None
    values: ClientValueCollection[PropertyValue] = field(default_factory=lambda: ClientValueCollection(PropertyValue))

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.Property"
