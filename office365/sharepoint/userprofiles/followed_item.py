from office365.runtime.client_value import ClientValue


class FollowedItem(ClientValue):
    """The FollowItem method is reserved for server-to-server use only. The server sets the specified item to be
    followed by the current user. This method cannot be called from the client."""

    def __init__(
        self,
        file_type=None,
        data: dict = None,
        file_type_progid: str = None,
        flags: str = None,
        group_id: str = None,
        has_feed: bool = None,
        hidden: bool = None,
        icon_url: str = None,
        item_id: int = None,
        item_type: int = None,
        list_id: str = None,
        parent_url: str = None,
        pinned: int = None,
        server_url_progid: str = None,
        site_id: str = None,
        subtype: int = None,
        title: str = None,
        unique_id: str = None,
        url: str = None,
        web_id: str = None,
    ):
        """
        :param int file_type:
        """
        self.FileType = file_type
        self.Data = data
        self.FileTypeProgid = file_type_progid
        self.Flags = flags
        self.GroupId = group_id
        self.HasFeed = has_feed
        self.Hidden = hidden
        self.IconUrl = icon_url
        self.ItemId = item_id
        self.ItemType = item_type
        self.ListId = list_id
        self.ParentUrl = parent_url
        self.Pinned = pinned
        self.ServerUrlProgid = server_url_progid
        self.SiteId = site_id
        self.Subtype = subtype
        self.Title = title
        self.UniqueId = unique_id
        self.Url = url
        self.WebId = web_id

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.FollowedItem"
