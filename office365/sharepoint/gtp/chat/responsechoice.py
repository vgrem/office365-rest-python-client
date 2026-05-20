from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.gtp.message_entry import MessageEntry


@dataclass
class ChatGptResponseChoice(ClientValue):
    FinishReason: Optional[str] = None
    Index: Optional[int] = None
    Message: MessageEntry = field(default_factory=MessageEntry)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.ChatGptResponseChoice"
