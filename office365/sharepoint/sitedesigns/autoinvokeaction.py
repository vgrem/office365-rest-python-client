from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.header import Header
from typing import Optional


class AutoInvokeAction(ClientValue):
    def __init__(
        self,
        body: Optional[str] = None,
        headers: ClientValueCollection[Header] = ClientValueCollection(Header),
        hide_card_on_invoke: Optional[str] = None,
        target: Optional[str] = None,
        type_: Optional[str] = None,
    ):
        self.body = body
        self.headers = headers
        self.hideCardOnInvoke = hide_card_on_invoke
        self.target = target
        self.type = type_

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.AutoInvokeAction"
