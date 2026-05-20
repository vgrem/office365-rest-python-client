from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SocialAttachmentAction(ClientValue):
    """The SocialAttachmentAction class specifies the user actions that are allowed for the attachment object."""

    ActionKind: Optional[int] = None
    ActionUri: Optional[str] = None
    Height: Optional[int] = None
    Width: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialAttachmentAction"
