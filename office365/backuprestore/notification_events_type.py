from __future__ import annotations

from enum import Enum


class NotificationEventsType(Enum):
    none = "1"
    restoreAndPolicyUpdates = "2"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.NotificationEventsType"
