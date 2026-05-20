from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.portal.project.myrecsqueryinfo import MyRecsQueryInfo


@dataclass
class MyRecsCacheBlob(ClientValue):
    DateCached: Optional[datetime] = None
    FillInQuery: Optional[str] = None
    FillInSortBy: Optional[str] = None
    Query: Optional[str] = None
    QueryInfo: MyRecsQueryInfo = field(default_factory=MyRecsQueryInfo)
    Result: Optional[str] = None
    SortBy: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.Project.MyRecsCacheBlob"
