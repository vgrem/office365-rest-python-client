from office365.runtime.client_value import ClientValue


class M365TabItem(ClientValue):

    def __init__(
        self,
        display_name: str = None,
        is_default: bool = None,
        item_type: int = None,
        url: str = None,
    ):
        self.displayName = display_name
        self.isDefault = is_default
        self.itemType = item_type
        self.url = url
