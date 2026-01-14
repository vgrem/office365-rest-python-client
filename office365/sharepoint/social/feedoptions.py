from datetime import datetime

from office365.runtime.client_value import ClientValue


class SocialFeedOptions(ClientValue):
    def __init__(
        self,
        max_thread_count: int = None,
        newer_than: datetime = None,
        older_than: datetime = None,
        sort_order: int = None,
    ):
        self.MaxThreadCount = max_thread_count
        self.NewerThan = newer_than
        self.OlderThan = older_than
        self.SortOrder = sort_order

    @property
    def entity_type_name(self):
        return "SP.Social.SocialFeedOptions"
