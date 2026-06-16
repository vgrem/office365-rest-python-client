from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ExtendedAttributeSettings(ClientValue):
    attributeNumber: int | None = None
    description: str | None = None
    displayName: str | None = None
    isScanPending: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.ExtendedAttributeSettings"
