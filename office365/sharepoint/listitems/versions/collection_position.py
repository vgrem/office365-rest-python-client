from typing import Optional

from office365.runtime.client_value import ClientValue


class ListItemVersionCollectionPosition(ClientValue):
    def __init__(self, paging_info: Optional[str] = None):
        self.PagingInfo = paging_info

    ""
