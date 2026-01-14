from office365.runtime.client_value import ClientValue
from office365.sharepoint.microfeed.linkaction import MicrofeedLinkAction


class MicrofeedLink(ClientValue):
    def __init__(
        self,
        click_action: MicrofeedLinkAction = MicrofeedLinkAction(),
        content_uri: str = None,
        description: str = None,
        height: int = None,
        href: str = None,
        length: int = None,
        link_type: int = None,
        name: str = None,
        preview_height: int = None,
        preview_picture_url: str = None,
        preview_width: int = None,
        status: int = None,
        width: int = None,
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
