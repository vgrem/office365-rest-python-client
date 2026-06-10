from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.adaptivecardaction import AdaptiveCardAction


@dataclass
class ActionSet(ClientValue):
    actions: ClientValueCollection[AdaptiveCardAction] = field(
        default_factory=lambda: ClientValueCollection(AdaptiveCardAction)
    )
    horizontalAlignment: str | None = None
