from office365.runtime.client_value import ClientValue


class TextBlock(ClientValue):

    def __init__(
        self,
        color: str = None,
        horizontal_alignment: str = None,
        size: str = None,
        text: str = None,
        weight: str = None,
        wrap: bool = None,
    ):
        self.color = color
        self.horizontal_alignment = horizontal_alignment
        self.size = size
        self.text = text
        self.weight = weight
        self.wrap = wrap
