from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class MyRecsQueryInfo(ClientValue):
    Category: Optional[int] = None
    ExpertiseTags: StringCollection = field(default_factory=StringCollection)
    FollowedUrls: StringCollection = field(default_factory=StringCollection)
    InterestTags: StringCollection = field(default_factory=StringCollection)
    QueryInfoExists: Optional[bool] = None
    SuggestedTags: Optional[StringCollection] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.Project.MyRecsQueryInfo"
