from office365.runtime.client_value import ClientValue
from typing import Optional


class TextBlock(ClientValue):
    def __init__(
        self,
        color: Optional[str] = None,
        horizontal_alignment: Optional[str] = None,
        size: Optional[str] = None,
        text: Optional[str] = None,
        weight: Optional[str] = None,
        wrap: Optional[bool] = None,
    ):
        self.color = color
        self.horizontal_alignment = horizontal_alignment
        self.size = size
        self.text = text
        self.weight = weight
        self.wrap = wrap
