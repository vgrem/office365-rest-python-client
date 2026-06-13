from dataclasses import field

from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.gtp.base_request_options import BaseGptRequestOptions
from office365.sharepoint.gtp.message_entry import MessageEntry


class ChatGptRequestOptions(BaseGptRequestOptions):
    """"""

    Messages: ClientValueCollection[MessageEntry] = field(default_factory=lambda: ClientValueCollection(MessageEntry))

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Internal.ChatGptRequestOptions"
