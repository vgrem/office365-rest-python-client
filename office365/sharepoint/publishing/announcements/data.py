from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.calltoaction import CallToAction
from office365.sharepoint.publishing.icon import Icon


class AnnouncementsData(ClientValue):
    def __init__(
        self,
        call_to_action: CallToAction = CallToAction(),
        dismissable: bool = None,
        expires_on: datetime = None,
        icon: Icon = Icon(),
        id_: str = None,
        message: str = None,
        publish_start_date: datetime = None,
        title: str = None,
    ):
        self.CallToAction = call_to_action
        self.Dismissable = dismissable
        self.ExpiresOn = expires_on
        self.Icon = icon
        self.ID = id_
        self.Message = message
        self.PublishStartDate = publish_start_date
        self.Title = title

    @property
    def entity_type_name(self):
        return "SP.Publishing.AnnouncementsData"
