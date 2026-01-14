from office365.runtime.client_value import ClientValue


class RelatedItem(ClientValue):
    def __init__(
        self,
        icon_url: str = None,
        item_id: int = None,
        list_id: str = None,
        title: str = None,
        url: str = None,
        web_id: str = None,
    ):
        self.icon_url = icon_url
        self.item_id = item_id
        self.list_id = list_id
        self.title = title
        self.url = url
        self.web_id = web_id
