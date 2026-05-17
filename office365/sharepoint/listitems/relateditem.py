from typing import Optional

from office365.runtime.client_value import ClientValue


class RelatedItem(ClientValue):
    def __init__(
        self,
        icon_url: Optional[str] = None,
        item_id: Optional[int] = None,
        list_id: Optional[str] = None,
        title: Optional[str] = None,
        url: Optional[str] = None,
        web_id: Optional[str] = None,
    ):
        self.icon_url = icon_url
        self.item_id = item_id
        self.list_id = list_id
        self.title = title
        self.url = url
        self.web_id = web_id
