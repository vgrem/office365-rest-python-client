from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.gtp.chat.response import ChatGptResponse


@dataclass
class GptAsyncExecuteResponse(ClientValue):
    RequestMetadata: Optional[str] = None
    Response: ChatGptResponse = field(default_factory=ChatGptResponse)
    Status: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptAsyncExecuteResponse"
