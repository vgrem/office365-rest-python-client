from office365.sharepoint.clientsidecomponent.card_element import CardElement
from typing import Optional


class AdaptiveCardImage(CardElement):
    def __init__(
        self,
        alt_text: Optional[str] = None,
        background_color: Optional[str] = None,
        height: Optional[str] = None,
        horizontal_alignment: Optional[str] = None,
        size: Optional[str] = None,
        style: Optional[str] = None,
        url: Optional[str] = None,
        width: Optional[str] = None,
    ):
        """"""
        super().__init__()
        self.altText = alt_text
        self.backgroundColor = background_color
        self.height = height
        self.horizontalAlignment = horizontal_alignment
        self.size = size
        self.style = style
        self.url = url
        self.width = width
