from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPOSitePropertiesEnumerableFilter(ClientValue):
    ArchivedBy: str | None = None
    ArchivedTime: datetime | None = None
    ArchiveStatus: str | None = None
    Filter: str | None = None
    GroupIdDefined: int | None = None
    IncludeDetail: bool | None = None
    IncludePersonalSite: int | None = None
    IncludeSystemUserSite: bool | None = None
    IsAuthoritative: bool | None = None
    StartIndex: str | None = None
    Template: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOSitePropertiesEnumerableFilter"
