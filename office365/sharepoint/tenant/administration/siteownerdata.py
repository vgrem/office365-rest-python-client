from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SiteOwnerData(ClientValue):
    department: str | None = None
    jobTitle: str | None = None
    preferredLanguage: str | None = None
    userPrincipalName: str | None = None
    extensionAttribute1: str | None = None
    extensionAttribute10: str | None = None
    extensionAttribute11: str | None = None
    extensionAttribute12: str | None = None
    extensionAttribute13: str | None = None
    extensionAttribute14: str | None = None
    extensionAttribute15: str | None = None
    extensionAttribute2: str | None = None
    extensionAttribute3: str | None = None
    extensionAttribute4: str | None = None
    extensionAttribute5: str | None = None
    extensionAttribute6: str | None = None
    extensionAttribute7: str | None = None
    extensionAttribute8: str | None = None
    extensionAttribute9: str | None = None
    preferredDataLocation: str | None = None
    userType: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.SiteOwnerData"
