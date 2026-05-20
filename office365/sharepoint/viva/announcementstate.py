from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.viva.announcementaction import AnnouncementAction


@dataclass
class AnnouncementState(ClientValue):
    Action: AnnouncementAction = field(default_factory=AnnouncementAction)
    ExpiresOn: Optional[datetime] = None
    Id: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.Experience.AnnouncementState"
