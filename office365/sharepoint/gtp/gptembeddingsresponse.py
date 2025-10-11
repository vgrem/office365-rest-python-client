from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.gtp.gptembeddingsresponsedata import GptEmbeddingsResponseData
from office365.sharepoint.gtp.gptresponseusage import GptResponseUsage


class GptEmbeddingsResponse(ClientValue):

    def __init__(
        self,
        data: ClientValueCollection[GptEmbeddingsResponseData] = ClientValueCollection(GptEmbeddingsResponseData),
        usage: GptResponseUsage = GptResponseUsage(),
    ):
        self.Data = data
        self.Usage = usage

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptEmbeddingsResponse"
