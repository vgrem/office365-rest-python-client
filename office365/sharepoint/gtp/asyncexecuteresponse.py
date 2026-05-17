from office365.runtime.client_value import ClientValue
from office365.sharepoint.gtp.chat.response import ChatGptResponse
from typing import Optional


class GptAsyncExecuteResponse(ClientValue):
    def __init__(
        self,
        request_metadata: Optional[str] = None,
        response: ChatGptResponse = ChatGptResponse(),
        status: Optional[str] = None,
    ):
        self.RequestMetadata = request_metadata
        self.Response = response
        self.Status = status

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptAsyncExecuteResponse"
