from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AnnouncementAction(ClientValue):
    Type: Optional[str] = None
    value: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.Experience.AnnouncementAction"
