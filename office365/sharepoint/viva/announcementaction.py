from typing import Optional

from office365.runtime.client_value import ClientValue


class AnnouncementAction(ClientValue):
    Type: Optional[str] = None
    value: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.Experience.AnnouncementAction"
