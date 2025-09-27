from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.placeholderv2 import PlaceholderV2


class Snippet(ClientValue):
    pass


class PublishModernTemplatePayload(ClientValue):

    def __init__(
        self,
        disable_search_and_approvals: bool = None,
        placeholders: ClientValueCollection[PlaceholderV2] = ClientValueCollection(
            PlaceholderV2
        ),
        snippets: ClientValueCollection[Snippet] = ClientValueCollection(Snippet),
        url: str = None,
    ):
        self.disable_search_and_approvals = disable_search_and_approvals
        self.placeholders = placeholders
        self.snippets = snippets
        self.url = url
