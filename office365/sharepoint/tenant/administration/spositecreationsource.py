from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SPOSiteCreationSource(ClientValue):
    DisplayName: str | None = None
    Id: str | None = None
    Name: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOSiteCreationSource"
