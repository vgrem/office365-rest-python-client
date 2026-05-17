from office365.runtime.client_value import ClientValue
from typing import Optional


class DashboardItemInfo(ClientValue):
    def __init__(
        self,
        item_id: Optional[int] = None,
        list_id: Optional[str] = None,
        site_id: Optional[str] = None,
        web_id: Optional[str] = None,
    ):
        self.item_id = item_id
        self.list_id = list_id
        self.site_id = site_id
        self.web_id = web_id
