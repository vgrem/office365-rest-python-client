from office365.runtime.client_value import ClientValue
from typing import Optional


class ListItemVersionCollectionPosition(ClientValue):
    def __init__(self, paging_info: Optional[str] = None):
        self.PagingInfo = paging_info

    ""
