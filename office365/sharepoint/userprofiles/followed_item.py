from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class FollowedItem(ClientValue):
    """The FollowItem method is reserved for server-to-server use only. The server sets the specified item to be
    followed by the current user. This method cannot be called from the client.

    :param int FileType:
    """

    FileType: Optional[int] = None
    Data: Optional[dict] = None
    FileTypeProgid: Optional[str] = None
    Flags: Optional[str] = None
    GroupId: Optional[str] = None
    HasFeed: Optional[bool] = None
    Hidden: Optional[bool] = None
    IconUrl: Optional[str] = None
    ItemId: Optional[int] = None
    ItemType: Optional[int] = None
    ListId: Optional[str] = None
    ParentUrl: Optional[str] = None
    Pinned: Optional[int] = None
    ServerUrlProgid: Optional[str] = None
    SiteId: Optional[str] = None
    Subtype: Optional[int] = None
    Title: Optional[str] = None
    UniqueId: Optional[str] = None
    Url: Optional[str] = None
    WebId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.FollowedItem"
