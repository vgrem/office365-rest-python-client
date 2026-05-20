from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.social.posts.creation_data import SocialPostCreationData


@dataclass
class SocialRestPostCreationData(ClientValue):
    ID: Optional[str] = None
    creationData: SocialPostCreationData = field(default_factory=SocialPostCreationData)

    @property
    def entity_type_name(self):
        return "SP.Social.SocialRestPostCreationData"
