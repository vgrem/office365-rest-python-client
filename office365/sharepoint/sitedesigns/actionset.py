from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.sitedesigns.adaptivecardaction import AdaptiveCardAction


@value
class ActionSet(ClientValue):
    actions: ClientValueCollection[AdaptiveCardAction] = field(
        default_factory=lambda: ClientValueCollection(AdaptiveCardAction)
    )
    horizontalAlignment: str | None = None
