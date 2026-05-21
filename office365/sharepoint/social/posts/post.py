from __future__ import annotations

from datetime import datetime
from typing import Optional

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.social.attachment import SocialAttachment
from office365.sharepoint.social.data_overlay import SocialDataOverlay
from office365.sharepoint.social.link import SocialLink
from office365.sharepoint.social.posts.actor_info import SocialPostActorInfo


@dataclass
class SocialPost(ClientValue):
    """The SocialPost specifies a post read from the server."""

    Attachment: SocialAttachment = field(default_factory=SocialAttachment)
    Overlays: ClientValueCollection[SocialDataOverlay] = field(default_factory=lambda: ClientValueCollection(SocialDataOverlay))
    Source: SocialLink = field(default_factory=SocialLink)
    LikerInfo: SocialPostActorInfo = field(default_factory=SocialPostActorInfo)
    Attributes: Optional[int] = None
    AuthorIndex: Optional[int] = None
    CreatedTime: Optional[datetime] = None
    Id: Optional[str] = None
    ModifiedTime: Optional[datetime] = None
    PostType: Optional[int] = None
    PreferredImageUri: Optional[str] = None
    Text: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialPost"
