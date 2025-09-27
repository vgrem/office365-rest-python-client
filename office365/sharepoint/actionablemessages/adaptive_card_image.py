from office365.sharepoint.actionablemessages.card_element import CardElement


class AdaptiveCardImage(CardElement):

    def __init__(
        self,
        alt_text: str = None,
        background_color: str = None,
        height: str = None,
        horizontal_alignment: str = None,
        size: str = None,
        style: str = None,
        url: str = None,
        width: str = None,
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
