from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.actionablemessages.card_element import CardElement
from office365.sharepoint.actionablemessages.padding import Padding


class Container(CardElement):

    def __init__(
        self,
        background_image: str = None,
        items: ClientValueCollection[CardElement] = ClientValueCollection(CardElement),
        padding: Padding = Padding(),
        vertical_content_alignment: str = None,
    ):
        """Container object"""
        super().__init__()
        self.backgroundImage = background_image
        self.items = items
        self.padding = padding
        self.verticalContentAlignment = vertical_content_alignment
