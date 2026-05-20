from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class MicrofeedRetrievalOptions(ClientValue):
    ContentFormattingOption: Optional[int] = None
    ContentOnly: Optional[bool] = None
    DropAllSecurityTrimmablePosts: Optional[bool] = None
    GatherUnreadMentionCountForUser: Optional[bool] = None
    IncludedTypes: Optional[int] = None
    NewerThan: Optional[datetime] = None
    OlderThan: Optional[datetime] = None
    PostDefinitionFilter: StringCollection = field(default_factory=StringCollection)
    ResultSortOrder: Optional[int] = None
    ThreadCount: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedRetrievalOptions"
