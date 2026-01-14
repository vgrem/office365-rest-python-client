from office365.runtime.client_value import ClientValue
from office365.sharepoint.social.attachment_action import SocialAttachmentAction


class SocialAttachment(ClientValue):
    def __init__(
        self,
        attachment_kind: int = None,
        click_action: SocialAttachmentAction = SocialAttachmentAction(),
        content_uri: str = None,
        description: str = None,
        height: int = None,
        length: int = None,
        name: str = None,
        preview_height: int = None,
        preview_uri: str = None,
        preview_width: int = None,
        uri: str = None,
        width: int = None,
    ):
        """The SocialAttachment class represents an image, document preview, or video preview attachment."""
        self.AttachmentKind = attachment_kind
        self.ClickAction = click_action
        self.ContentUri = content_uri
        self.Description = description
        self.Height = height
        self.Length = length
        self.Name = name
        self.PreviewHeight = preview_height
        self.PreviewUri = preview_uri
        self.PreviewWidth = preview_width
        self.Uri = uri
        self.Width = width

    @property
    def entity_type_name(self):
        return "SP.Social.SocialAttachment"
