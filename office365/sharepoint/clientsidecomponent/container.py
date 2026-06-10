from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.clientsidecomponent.card_element import CardElement
from office365.sharepoint.clientsidecomponent.padding import Padding
from office365.sharepoint.sitedesigns.adaptivecardaction import AdaptiveCardAction


class Container(CardElement):
    items: ClientValueCollection[CardElement] = field(default_factory=lambda: ClientValueCollection(CardElement))
    padding: Padding = field(default_factory=Padding)
    selectAction: AdaptiveCardAction = field(default_factory=AdaptiveCardAction)
    style: str | None = None
    verticalContentAlignment: str | None = None
    backgroundImage: str | None = None
