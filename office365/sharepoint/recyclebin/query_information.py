from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class RecycleBinQueryInformation(ClientValue):

    """
    Represents information for the recycle bin query.

    :param bool show_only_my_items: Gets or sets a Boolean value that specifies whether to get items deleted by
    other users.
    :param int row_limit: Gets or sets a limit for the number of items returned in the query per page.
    :param str paging_info: Gets or sets a string used to get the next set of rows in the page.
    :param int order_by: Gets or sets the column by which to order the Recycle Bin query.
    :param int item_state: Gets or sets the Recycle Bin state of items to return in the query.
    :param bool is_ascending: Gets or sets a Boolean value that specifies whether to sort in ascending order.
    """

    IsAscending: Optional[bool] = None
    ItemState: Optional[int] = None
    OrderBy: Optional[int] = None
    PagingInfo: Optional[str] = None
    RowLimit: Optional[int] = None
    ShowOnlyMyItems: Optional[bool] = None