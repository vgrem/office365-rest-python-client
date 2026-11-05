from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.clientsidecomponent.adaptivecardcolumn import AdaptiveCardColumn
from office365.sharepoint.clientsidecomponent.padding import Padding
from office365.sharepoint.sitedesigns.adaptivecardaction import AdaptiveCardAction


class ColumnSet(ClientValue):
    columns: ClientValueCollection[AdaptiveCardColumn] = field(
        default_factory=lambda: ClientValueCollection(AdaptiveCardColumn)
    )
    padding: Padding = field(default_factory=Padding)
    horizontalAlignment: str | None = None
    selectAction: AdaptiveCardAction = field(default_factory=AdaptiveCardAction)
