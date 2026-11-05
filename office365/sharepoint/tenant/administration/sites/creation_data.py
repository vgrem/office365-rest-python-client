from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SiteCreationData(ClientValue):
    Count: int | None = None
    SiteCreationSourceGuid: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteCreationData"
