from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.viva.announcementaction import AnnouncementAction


class AnnouncementState(ClientValue):

    def __init__(
        self,
        action: AnnouncementAction = AnnouncementAction(),
        expires_on: datetime = None,
        id_: str = None,
    ):
        self.Action = action
        self.ExpiresOn = expires_on
        self.Id = id_

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.Experience.AnnouncementState"
