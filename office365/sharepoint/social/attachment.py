from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.social.attachment_action import SocialAttachmentAction


class SocialAttachment(ClientValue):
    def __init__(
        self,
        attachment_kind: Optional[int] = None,
        click_action: SocialAttachmentAction = SocialAttachmentAction(),
        content_uri: Optional[str] = None,
        description: Optional[str] = None,
        height: Optional[int] = None,
        length: Optional[int] = None,
        name: Optional[str] = None,
        preview_height: Optional[int] = None,
        preview_uri: Optional[str] = None,
        preview_width: Optional[int] = None,
        uri: Optional[str] = None,
        width: Optional[int] = None,
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
