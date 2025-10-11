from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.microfeed.post import MicrofeedPost


class MicrofeedPostCollection(ClientValue):

    def __init__(
        self,
        items: ClientValueCollection[MicrofeedPost] = ClientValueCollection(MicrofeedPost),
    ):
        self.Items = items

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedPostCollection"
