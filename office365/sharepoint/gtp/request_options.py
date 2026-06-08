from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.gtp.base_request_options import BaseGptRequestOptions
from office365.sharepoint.gtp.message_entry import MessageEntry


class ChatGptRequestOptions(BaseGptRequestOptions):
    """"""

    def __init__(self, messages=None):
        """Args:
            messages (list[MessageEntry]):
        """
        super().__init__()
        self.Messages = ClientValueCollection(MessageEntry, messages)

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Internal.ChatGptRequestOptions"
