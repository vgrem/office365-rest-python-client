from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.social.microfeed.thread import MicrofeedThread


class MicrofeedThreadCollection(ClientValue):
    def __init__(
        self,
        current_user_unread_mention_count: int = None,
        newest_processed: datetime = None,
        oldest_processed: datetime = None,
        items: ClientValueCollection[MicrofeedThread] = ClientValueCollection(MicrofeedThread),
    ):
        self.CurrentUserUnreadMentionCount = current_user_unread_mention_count
        self.NewestProcessed = newest_processed
        self.OldestProcessed = oldest_processed
        self.Items = items

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedThreadCollection"
