from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.announcements.author import AnnouncementAuthor
from office365.sharepoint.publishing.calltoaction import CallToAction as _CallToAction
from office365.sharepoint.publishing.icon import Icon as _Icon


@dataclass
class ChannelAnnouncement(ClientValue):
    Author: AnnouncementAuthor = field(default_factory=lambda: AnnouncementAuthor())
    CallToAction: _CallToAction = field(default_factory=lambda: _CallToAction())
    ChannelName: Optional[str] = None
    Icon: _Icon = field(default_factory=lambda: _Icon())
    ID: Optional[int] = None
    IsRead: Optional[bool] = None
    Message: Optional[str] = None
    PublishStartDate: Optional[str] = None
    Title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.ChannelAnnouncement"
