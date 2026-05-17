from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class MicrofeedRetrievalOptions(ClientValue):
    def __init__(
        self,
        content_formatting_option: Optional[int] = None,
        content_only: Optional[bool] = None,
        drop_all_security_trimmable_posts: Optional[bool] = None,
        gather_unread_mention_count_for_user: Optional[bool] = None,
        included_types: Optional[int] = None,
        newer_than: Optional[datetime] = None,
        older_than: Optional[datetime] = None,
        post_definition_filter: StringCollection = StringCollection(),
        result_sort_order: Optional[int] = None,
        thread_count: Optional[int] = None,
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
