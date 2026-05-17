from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPSitePage(ClientValue):
    def __init__(
        self,
        created_by: Optional[str] = None,
        created_date_time: Optional[datetime] = None,
        last_modified_date_time: Optional[datetime] = None,
        name: Optional[str] = None,
        title: Optional[str] = None,
        unique_id: Optional[UUID] = None,
    ):
        self.CreatedBy = created_by
        self.CreatedDateTime = created_date_time
        self.LastModifiedDateTime = last_modified_date_time
        self.Name = name
        self.Title = title
        self.UniqueId = unique_id

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPSitePage"
