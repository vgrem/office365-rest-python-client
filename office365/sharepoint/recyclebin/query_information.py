from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class RecycleBinQueryInformation(ClientValue):
    """Represents information for the recycle bin query.

    Args:
        show_only_my_items (bool): Gets or sets a Boolean value that specifies whether to get items deleted by other
            users.
        row_limit (int): Gets or sets a limit for the number of items returned in the query per page.
        paging_info (str): Gets or sets a string used to get the next set of rows in the page.
        order_by (int): Gets or sets the column by which to order the Recycle Bin query.
        item_state (int): Gets or sets the Recycle Bin state of items to return in the query.
        is_ascending (bool): Gets or sets a Boolean value that specifies whether to sort in ascending order.
    """

    IsAscending: Optional[bool] = None
    ItemState: Optional[int] = None
    OrderBy: Optional[int] = None
    PagingInfo: Optional[str] = None
    RowLimit: Optional[int] = None
    ShowOnlyMyItems: Optional[bool] = None
