from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SPOTenantWebTemplate(ClientValue):
    CompatibilityLevel: int | None = None
    Description: str | None = None
    DisplayCategory: str | None = None
    Id: int | None = None
    Lcid: int | None = None
    Name: str | None = None
    Title: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOTenantWebTemplate"
