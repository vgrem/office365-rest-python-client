from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.clientsidecomponent.card_element import CardElement
from office365.sharepoint.clientsidecomponent.padding import Padding


class AdaptiveCard(ClientValue):

    def __init__(
        self,
        body: ClientValueCollection[CardElement] = ClientValueCollection(CardElement),
        correlation_id: str = None,
        hide_original_body: bool = None,
        originator: str = None,
        padding: Padding = None,
        rtl: bool = None,
        type_: str = None,
        version: str = None,
    ):
        self.body = body
        self.correlation_id = correlation_id
        self.hide_original_body = hide_original_body
        self.originator = originator
        self.padding = padding
        self.rtl = rtl
        self.type = type_
        self.version = version
