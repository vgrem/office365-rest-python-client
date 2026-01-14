from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.location import DocumentLocation
from office365.sharepoint.documents.placeholderv2 import PlaceholderV2
from office365.sharepoint.documents.snippet import Snippet


class PublishModernTemplatePayload(ClientValue):
    def __init__(
        self,
        disable_search_and_approvals: bool = None,
        placeholders: ClientValueCollection[PlaceholderV2] = ClientValueCollection(PlaceholderV2),
        snippets: ClientValueCollection[Snippet] = ClientValueCollection(Snippet),
        url: str = None,
        document_location: DocumentLocation = DocumentLocation(),
    ):
        self.DisableSearchAndApprovals = disable_search_and_approvals
        self.Placeholders = placeholders
        self.Snippets = snippets
        self.Url = url
        self.DocumentLocation = document_location
