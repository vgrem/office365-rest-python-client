from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class GptEmbeddingsResponseData(ClientValue):

    def __init__(
        self,
        embedding: ClientValueCollection[float] = ClientValueCollection(float),
        index: int = None,
        object_: str = None,
    ):
        self.Embedding = embedding
        self.Index = index
        self.Object = object_

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptEmbeddingsResponseData"
