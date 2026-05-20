from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.social.posts.definition_data_item import (
    SocialPostDefinitionDataItem,
)


@dataclass
class SocialPostDefinitionData(ClientValue):
    """The SocialPostDefinitionData type provides additional information about server-generated posts.
    This type can only be specified in a server-to-server call."""

    Items: ClientValueCollection[SocialPostDefinitionDataItem] = field(
        default_factory=lambda: ClientValueCollection(SocialPostDefinitionDataItem)
    )
    Name: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialPostDefinitionData"
