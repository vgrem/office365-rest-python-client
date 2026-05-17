from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class SPOSitePropertiesEnumerableFilter(ClientValue):
    def __init__(
        self,
        archived_by: Optional[str] = None,
        archived_time: Optional[datetime] = None,
        archive_status: Optional[str] = None,
        filter_: Optional[str] = None,
        group_id_defined: Optional[int] = None,
        include_detail: Optional[bool] = None,
        include_personal_site: Optional[int] = None,
        include_system_user_site: Optional[bool] = None,
        is_authoritative: Optional[bool] = None,
        start_index: Optional[str] = None,
        template: Optional[str] = None,
    ):
        self.ArchivedBy = archived_by
        self.ArchivedTime = archived_time
        self.ArchiveStatus = archive_status
        self.Filter = filter_
        self.GroupIdDefined = group_id_defined
        self.IncludeDetail = include_detail
        self.IncludePersonalSite = include_personal_site
        self.IncludeSystemUserSite = include_system_user_site
        self.IsAuthoritative = is_authoritative
        self.StartIndex = start_index
        self.Template = template

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOSitePropertiesEnumerableFilter"
