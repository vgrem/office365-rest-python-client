from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class DashboardItemInfo(ClientValue):
    item_id: Optional[int] = None
    list_id: Optional[str] = None
    site_id: Optional[str] = None
    web_id: Optional[str] = None
