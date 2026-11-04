from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SitePropertiesEnumerableFilter(ClientValue):
    """Args:
    _filter (str):
    start_index (str):
    include_detail (bool):
    include_personal_site (int):
    group_id_defined (int):
    template (str):
    """

    Filter: str | None = None
    StartIndex: str | None = None
    IncludeDetail: bool | None = None
    IncludePersonalSite: int | None = None
    GroupIdDefined: int | None = None
    Template: str | None = None
    ArchivedBy: str | None = None
    ArchivedTime: str | None = None
    ArchiveStatus: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOSitePropertiesEnumerableFilter"
