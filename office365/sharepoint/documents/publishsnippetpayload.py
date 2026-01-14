from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.placeholderv2 import PlaceholderV2


class PublishSnippetPayload(ClientValue):
    def __init__(
        self,
        placeholders: ClientValueCollection[PlaceholderV2] = ClientValueCollection(PlaceholderV2),
        url: str = None,
    ):
        self.placeholders = placeholders
        self.url = url
