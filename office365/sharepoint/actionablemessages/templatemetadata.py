from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.actionablemessages.placeholder import Placeholder


class TemplateMetaData(ClientValue):

    def __init__(
        self,
        placeholders: ClientValueCollection[Placeholder] = ClientValueCollection(
            Placeholder
        ),
        server_redirected_embed_url: str = None,
    ):
        self.placeholders = placeholders
        self.server_redirected_embed_url = server_redirected_embed_url
