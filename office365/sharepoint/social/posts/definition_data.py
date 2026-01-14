from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.social.posts.definition_data_item import (
    SocialPostDefinitionDataItem,
)


class SocialPostDefinitionData(ClientValue):
    def __init__(
        self,
        items: ClientValueCollection[SocialPostDefinitionDataItem] = ClientValueCollection(SocialPostDefinitionDataItem),
        name: str = None,
    ):
        """The SocialPostDefinitionData type provides additional information about server-generated posts.
        This type can only be specified in a server-to-server call."""
        self.Items = items
        self.Name = name

    @property
    def entity_type_name(self):
        return "SP.Social.SocialPostDefinitionData"
