from office365.runtime.client_value import ClientValue
from typing import Optional


class GptEmbeddingsRequestOptions(ClientValue):
    def __init__(self, input_: Optional[str] = None):
        self.Input = input_

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptEmbeddingsRequestOptions"
