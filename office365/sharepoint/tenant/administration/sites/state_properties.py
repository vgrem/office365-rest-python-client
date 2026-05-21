from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SiteStateProperties(ClientValue):
    GroupSiteRelationship: int | None = None
    IsArchived: bool | None = None
    IsSiteOnHold: bool | None = None
    LockState: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteStateProperties"
