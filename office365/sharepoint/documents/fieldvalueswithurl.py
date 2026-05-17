from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.documents.cafieldvalue import CAFieldValue
from typing import Optional


class FieldValuesWithUrl(ClientValue):
    def __init__(
        self,
        field_values: ClientValueCollection[CAFieldValue] = ClientValueCollection(CAFieldValue),
        server_redirected_embed_url: Optional[str] = None,
    ):
        self.field_values = field_values
        self.server_redirected_embed_url = server_redirected_embed_url
