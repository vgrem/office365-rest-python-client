from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.clientsidecomponent.card_element import CardElement
from office365.sharepoint.clientsidecomponent.padding import Padding
from office365.sharepoint.sitedesigns.autoinvokeaction import AutoInvokeAction
from office365.sharepoint.sitedesigns.autoinvokeoptions import AutoInvokeOptions


class AdaptiveCard(ClientValue):
    def __init__(
        self,
        body: ClientValueCollection[CardElement] = ClientValueCollection(CardElement),
        correlation_id: Optional[str] = None,
        hide_original_body: Optional[bool] = None,
        originator: Optional[str] = None,
        padding: Optional[Padding] = None,
        rtl: Optional[bool] = None,
        type_: Optional[str] = None,
        version: Optional[str] = None,
        auto_invoke_action: AutoInvokeAction = AutoInvokeAction(),
        auto_invoke_options: AutoInvokeOptions = AutoInvokeOptions(),
    ):
        self.body = body
        self.correlation_id = correlation_id
        self.hide_original_body = hide_original_body
        self.originator = originator
        self.padding = padding
        self.rtl = rtl
        self.type = type_
        self.version = version
        self.autoInvokeAction = auto_invoke_action
        self.autoInvokeOptions = auto_invoke_options
