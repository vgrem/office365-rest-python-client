from office365.runtime.client_value import ClientValue
from office365.sharepoint.gtp.chat.response import ChatGptResponse


class GptAsyncExecuteResponse(ClientValue):
    def __init__(
        self,
        request_metadata: str = None,
        response: ChatGptResponse = ChatGptResponse(),
        status: str = None,
    ):
        self.RequestMetadata = request_metadata
        self.Response = response
        self.Status = status

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptAsyncExecuteResponse"
