from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SocialPostDefinitionDataItem(ClientValue):
    """The SocialPostDefinitionDataItem class specifies an item to be inserted in a post by replacing a token in
    the post definition. This type can only be specified in a server-to-server call."""

    AccountName: Optional[str] = None
    ItemType: Optional[int] = None
    PlaceholderName: Optional[str] = None
    TagGuid: Optional[str] = None
    Text: Optional[str] = None
    Uri: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialPostDefinitionDataItem"
