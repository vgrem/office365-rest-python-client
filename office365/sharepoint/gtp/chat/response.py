from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.gtp.chat.responsechoice import ChatGptResponseChoice
from office365.sharepoint.gtp.responseusage import GptResponseUsage


@dataclass
class ChatGptResponse(ClientValue):
    Choices: ClientValueCollection[ChatGptResponseChoice] = field(
        default_factory=lambda: ClientValueCollection(ChatGptResponseChoice)
    )
    Usage: GptResponseUsage = field(default_factory=GptResponseUsage)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.ChatGptResponse"
