from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.clientsidecomponent.adaptivecard import AdaptiveCard


class ActionShowCard(ClientValue):
    card: AdaptiveCard = field(default_factory=AdaptiveCard)
