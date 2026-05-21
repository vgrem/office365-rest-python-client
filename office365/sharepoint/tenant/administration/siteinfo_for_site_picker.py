from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SiteInfoForSitePicker(ClientValue):
    Error: str | None = None
    SiteId: str | None = None
    SiteName: str | None = None
    Url: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteInfoForSitePicker"
