from office365.runtime.client_value import ClientValue
from typing import Optional


class ItemOrderUpdateValue(ClientValue):
    def __init__(
        self, has_exception: Optional[bool] = None, item_id: Optional[int] = None, updated_order: Optional[float] = None
    ):
        self.has_exception = has_exception
        self.item_id = item_id
        self.updated_order = updated_order
