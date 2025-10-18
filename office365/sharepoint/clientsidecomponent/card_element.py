from office365.runtime.client_value import ClientValue


class CardElement(ClientValue):

    def __init__(
        self,
        id_: str = None,
        is_visible: bool = None,
        separator: bool = None,
        spacing: str = None,
        type_: str = None,
    ):
        self.id = id_
        self.isVisible = is_visible
        self.separator = separator
        self.spacing = spacing
        self.type = type_
