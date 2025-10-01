from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.announcementauthor import AnnouncementAuthor
from office365.sharepoint.publishing.calltoaction import CallToAction
from office365.sharepoint.publishing.icon import Icon


class ChannelAnnouncement(ClientValue):

    def __init__(
        self,
        author: AnnouncementAuthor = AnnouncementAuthor(),
        call_to_action: CallToAction = CallToAction(),
        channel_name: str = None,
        icon: Icon = Icon(),
        id_: int = None,
        is_read: bool = None,
        message: str = None,
        publish_start_date: str = None,
        title: str = None,
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
