from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.gtp.chat.responsechoice import ChatGptResponseChoice
from office365.sharepoint.gtp.responseusage import GptResponseUsage


class ChatGptResponse(ClientValue):
    def __init__(
        self,
        choices: ClientValueCollection[ChatGptResponseChoice] = ClientValueCollection(ChatGptResponseChoice),
        usage: GptResponseUsage = GptResponseUsage(),
    ):
        self.Choices = choices
        self.Usage = usage

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.ChatGptResponse"
