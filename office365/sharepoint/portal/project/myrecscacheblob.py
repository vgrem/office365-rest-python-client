from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.portal.project.myrecsqueryinfo import MyRecsQueryInfo


class MyRecsCacheBlob(ClientValue):
    def __init__(
        self,
        date_cached: Optional[datetime] = None,
        fill_in_query: Optional[str] = None,
        fill_in_sort_by: Optional[str] = None,
        query: Optional[str] = None,
        query_info: MyRecsQueryInfo = MyRecsQueryInfo(),
        result: Optional[str] = None,
        sort_by: Optional[str] = None,
    ):
        self.DateCached = date_cached
        self.FillInQuery = fill_in_query
        self.FillInSortBy = fill_in_sort_by
        self.Query = query
        self.QueryInfo = query_info
        self.Result = result
        self.SortBy = sort_by

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.Project.MyRecsCacheBlob"
