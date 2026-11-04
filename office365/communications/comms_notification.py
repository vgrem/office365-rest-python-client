from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.subscriptions.changetype import ChangeType


@value
class CommsNotification(ClientValue):
    changeType: ChangeType = ChangeType.created

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CommsNotification"
