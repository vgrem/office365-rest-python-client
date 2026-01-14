from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.portal.project.myrecsqueryinfo import MyRecsQueryInfo


class MyRecsCacheBlob(ClientValue):
    def __init__(
        self,
        date_cached: datetime = None,
        fill_in_query: str = None,
        fill_in_sort_by: str = None,
        query: str = None,
        query_info: MyRecsQueryInfo = MyRecsQueryInfo(),
        result: str = None,
        sort_by: str = None,
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
