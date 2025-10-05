from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class MicrofeedRetrievalOptions(ClientValue):

    def __init__(
        self,
        content_formatting_option: int = None,
        content_only: bool = None,
        drop_all_security_trimmable_posts: bool = None,
        gather_unread_mention_count_for_user: bool = None,
        included_types: int = None,
        newer_than: datetime = None,
        older_than: datetime = None,
        post_definition_filter: StringCollection = StringCollection(),
        result_sort_order: int = None,
        thread_count: int = None,
    ):
        self.ContentFormattingOption = content_formatting_option
        self.ContentOnly = content_only
        self.DropAllSecurityTrimmablePosts = drop_all_security_trimmable_posts
        self.GatherUnreadMentionCountForUser = gather_unread_mention_count_for_user
        self.IncludedTypes = included_types
        self.NewerThan = newer_than
        self.OlderThan = older_than
        self.PostDefinitionFilter = post_definition_filter
        self.ResultSortOrder = result_sort_order
        self.ThreadCount = thread_count

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedRetrievalOptions"
