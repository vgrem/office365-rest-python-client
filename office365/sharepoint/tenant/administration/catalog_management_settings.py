from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.extended_attribute_settings import ExtendedAttributeSettings
from office365.sharepoint.tenant.administration.value_display_name_settings import ValueDisplayNameSettings


class CatalogManagementSettings(ClientValue):
    departmentDisplayName: str | None = None
    extendedAttributes: ClientValueCollection[ExtendedAttributeSettings] = field(
        default_factory=lambda: ClientValueCollection(ExtendedAttributeSettings)
    )
    informationBarriersSegmentDisplayName: str | None = None
    localeDisplayName: str | None = None
    preferredDataLocationDisplayName: str | None = None
    userTypeDisplayName: str | None = None
    valueDisplayNames: ClientValueCollection[ValueDisplayNameSettings] = field(
        default_factory=lambda: ClientValueCollection(ValueDisplayNameSettings)
    )

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.CatalogManagementSettings"
