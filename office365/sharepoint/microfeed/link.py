from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.microfeed.linkaction import MicrofeedLinkAction


class MicrofeedLink(ClientValue):
    def __init__(
        self,
        click_action: MicrofeedLinkAction = MicrofeedLinkAction(),
        content_uri: Optional[str] = None,
        description: Optional[str] = None,
        height: Optional[int] = None,
        href: Optional[str] = None,
        length: Optional[int] = None,
        link_type: Optional[int] = None,
        name: Optional[str] = None,
        preview_height: Optional[int] = None,
        preview_picture_url: Optional[str] = None,
        preview_width: Optional[int] = None,
        status: Optional[int] = None,
        width: Optional[int] = None,
    ):
        self.ClickAction = click_action
        self.ContentUri = content_uri
        self.Description = description
        self.Height = height
        self.Href = href
        self.Length = length
        self.LinkType = link_type
        self.Name = name
        self.PreviewHeight = preview_height
        self.PreviewPictureUrl = preview_picture_url
        self.PreviewWidth = preview_width
        self.Status = status
        self.Width = width

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedLink"
