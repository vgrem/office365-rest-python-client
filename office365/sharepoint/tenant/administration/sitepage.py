from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPSitePage(ClientValue):

    def __init__(
        self,
        created_by: str = None,
        created_date_time: datetime = None,
        last_modified_date_time: datetime = None,
        name: str = None,
        title: str = None,
        unique_id: UUID = None,
    ):
        self.CreatedBy = created_by
        self.CreatedDateTime = created_date_time
        self.LastModifiedDateTime = last_modified_date_time
        self.Name = name
        self.Title = title
        self.UniqueId = unique_id

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPSitePage"
