from office365.runtime.client_value import ClientValue
from typing import Optional


class CardElement(ClientValue):
    def __init__(
        self,
        id_: Optional[str] = None,
        is_visible: Optional[bool] = None,
        separator: Optional[bool] = None,
        spacing: Optional[str] = None,
        type_: Optional[str] = None,
    ):
        self.id = id_
        self.isVisible = is_visible
        self.separator = separator
        self.spacing = spacing
        self.type = type_
