from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class CustomSitePropertyData(ClientValue):
    property1: str | None = None
    property10: str | None = None
    property11: str | None = None
    property12: str | None = None
    property13: str | None = None
    property14: str | None = None
    property15: str | None = None
    property16: str | None = None
    property17: str | None = None
    property18: str | None = None
    property19: str | None = None
    property2: str | None = None
    property20: str | None = None
    property3: str | None = None
    property4: str | None = None
    property5: str | None = None
    property6: str | None = None
    property7: str | None = None
    property8: str | None = None
    property9: str | None = None
    siteId: UUID | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.CustomSitePropertyData"
