from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.property import Property


class ExtendedPropertyMap(ClientValue):
    createdDate: datetime | None = field(default_factory=lambda: datetime.min)
    lastUpdatedTimeUtc: datetime | None = field(default_factory=lambda: datetime.min)
    properties: ClientValueCollection[Property] = field(default_factory=lambda: ClientValueCollection(Property))

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.ExtendedPropertyMap"
