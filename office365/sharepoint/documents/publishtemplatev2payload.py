from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.placeholderv2 import PlaceholderV2
from office365.sharepoint.documents.publishmoderntemplatepayload import Snippet


class PublishTemplateV2Payload(ClientValue):

    def __init__(
        self,
        destination_list_content_type_id: str = None,
        destination_site_content_type_id: str = None,
        placeholders: ClientValueCollection[PlaceholderV2] = ClientValueCollection(
            PlaceholderV2
        ),
        snippets: ClientValueCollection[Snippet] = ClientValueCollection(Snippet),
        url: str = None,
    ):
        self.destination_list_content_type_id = destination_list_content_type_id
        self.destination_site_content_type_id = destination_site_content_type_id
        self.placeholders = placeholders
        self.snippets = snippets
        self.url = url
