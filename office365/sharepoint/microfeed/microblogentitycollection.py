from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.microfeed.entity import MicroBlogEntity


class MicroBlogEntityCollection(ClientValue):

    def __init__(
        self,
        items: ClientValueCollection[MicroBlogEntity] = ClientValueCollection(
            MicroBlogEntity
        ),
    ):
        self.Items = items
