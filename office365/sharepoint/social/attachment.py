from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.social.attachment_action import SocialAttachmentAction


@dataclass
class SocialAttachment(ClientValue):
    """The SocialAttachment class represents an image, document preview, or video preview attachment."""

    AttachmentKind: Optional[int] = None
    ClickAction: SocialAttachmentAction = field(default_factory=SocialAttachmentAction)
    ContentUri: Optional[str] = None
    Description: Optional[str] = None
    Height: Optional[int] = None
    Length: Optional[int] = None
    Name: Optional[str] = None
    PreviewHeight: Optional[int] = None
    PreviewUri: Optional[str] = None
    PreviewWidth: Optional[int] = None
    Uri: Optional[str] = None
    Width: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialAttachment"
