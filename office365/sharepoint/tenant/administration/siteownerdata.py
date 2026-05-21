from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SiteOwnerData(ClientValue):
    department: str | None = None
    jobTitle: str | None = None
    preferredLanguage: str | None = None
    userPrincipalName: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.SiteOwnerData"
