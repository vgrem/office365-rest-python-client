from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.delivery_action import DeliveryAction
from office365.security.delivery_location import DeliveryLocation


@value
class AnalyzedEmailDeliveryDetail(ClientValue):
    latestThreats: str | None = None
    originalThreats: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.AnalyzedEmailDeliveryDetail"

    action: DeliveryAction = DeliveryAction.unknown

    location: DeliveryLocation = DeliveryLocation.unknown
