from datetime import datetime

from office365.runtime.client_value import ClientValue


class SPOSitePropertiesEnumerableFilter(ClientValue):

    def __init__(
        self,
        archived_by: str = None,
        archived_time: datetime = None,
        archive_status: str = None,
        filter_: str = None,
        group_id_defined: int = None,
        include_detail: bool = None,
        include_personal_site: int = None,
        include_system_user_site: bool = None,
        is_authoritative: bool = None,
        start_index: str = None,
        template: str = None,
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
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOSitePropertiesEnumerableFilter"
