from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPORestrictedContentDiscoverabilitySiteDetails(ClientValue):
    LastModified: datetime | None = None
    SiteOwnerEmail: str | None = None
    SiteTitle: str | None = None
    SiteUrl: str | None = None
    TimeCreated: datetime | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPORestrictedContentDiscoverabilitySiteDetails"
