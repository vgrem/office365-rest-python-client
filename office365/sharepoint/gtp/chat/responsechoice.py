from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.gtp.message_entry import MessageEntry


class ChatGptResponseChoice(ClientValue):
    def __init__(
        self,
        finish_reason: Optional[str] = None,
        index: Optional[int] = None,
        message: MessageEntry = MessageEntry(),
    ):
        self.FinishReason = finish_reason
        self.Index = index
        self.Message = message

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.ChatGptResponseChoice"
