from office365.runtime.client_value import ClientValue


class ItemOrderUpdateValue(ClientValue):

    def __init__(
        self,
        has_exception: bool = None,
        item_id: int = None,
        updated_order: float = None,
    ):
        self.has_exception = has_exception
        self.item_id = item_id
        self.updated_order = updated_order
