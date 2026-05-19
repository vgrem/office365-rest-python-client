from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.clientsidecomponent.card_element import CardElement
from office365.sharepoint.clientsidecomponent.padding import Padding
from office365.sharepoint.sitedesigns.autoinvokeaction import AutoInvokeAction
from office365.sharepoint.sitedesigns.autoinvokeoptions import AutoInvokeOptions


@dataclass
class AdaptiveCard(ClientValue):
    """An adaptive card."""

    body: ClientValueCollection[CardElement] = field(default_factory=lambda: ClientValueCollection(CardElement))
    correlation_id: Optional[str] = None
    hide_original_body: Optional[bool] = None
    originator: Optional[str] = None
    padding: Optional[Padding] = None
    rtl: Optional[bool] = None
    type_: Optional[str] = None
    version: Optional[str] = None
    autoInvokeAction: AutoInvokeAction = field(default_factory=AutoInvokeAction)
    autoInvokeOptions: AutoInvokeOptions = field(default_factory=AutoInvokeOptions)
