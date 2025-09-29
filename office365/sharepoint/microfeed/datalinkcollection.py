from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.microfeed.datalink import MicrofeedDataLink


class MicrofeedDataLinkCollection(ClientValue):

    def __init__(
        self,
        items: ClientValueCollection[MicrofeedDataLink] = ClientValueCollection(
            MicrofeedDataLink
        ),
    ):
        self.Items = items
