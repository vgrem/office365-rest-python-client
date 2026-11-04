from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.sharepoint.social.posts.creation_data import SocialPostCreationData


@value
class SocialRestPostCreationData(ClientValue):
    ID: Optional[str] = None
    creationData: SocialPostCreationData = field(default_factory=SocialPostCreationData)

    @property
    def entity_type_name(self):
        return "SP.Social.SocialRestPostCreationData"
