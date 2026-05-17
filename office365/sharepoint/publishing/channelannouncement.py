from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.announcements.author import AnnouncementAuthor
from office365.sharepoint.publishing.calltoaction import CallToAction
from office365.sharepoint.publishing.icon import Icon


class ChannelAnnouncement(ClientValue):
    def __init__(
        self,
        author: AnnouncementAuthor = AnnouncementAuthor(),
        call_to_action: CallToAction = CallToAction(),
        channel_name: Optional[str] = None,
        icon: Icon = Icon(),
        id_: Optional[int] = None,
        is_read: Optional[bool] = None,
        message: Optional[str] = None,
        publish_start_date: Optional[str] = None,
        title: Optional[str] = None,
    ):
        self.Author = author
        self.CallToAction = call_to_action
        self.ChannelName = channel_name
        self.Icon = icon
        self.ID = id_
        self.IsRead = is_read
        self.Message = message
        self.PublishStartDate = publish_start_date
        self.Title = title

    @property
    def entity_type_name(self):
        return "SP.Publishing.ChannelAnnouncement"
