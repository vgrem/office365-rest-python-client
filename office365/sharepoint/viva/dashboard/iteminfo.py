from office365.runtime.client_value import ClientValue


class DashboardItemInfo(ClientValue):
    def __init__(
        self,
        item_id: int = None,
        list_id: str = None,
        site_id: str = None,
        web_id: str = None,
    ):
        self.item_id = item_id
        self.list_id = list_id
        self.site_id = site_id
        self.web_id = web_id
