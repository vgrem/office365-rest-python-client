from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPOFileArchivePolicySiteInfo(ClientValue):
    PolicyId: UUID | None = None
    SiteId: UUID | None = None
    SiteUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOFileArchivePolicySiteInfo"
