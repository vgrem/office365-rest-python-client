from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class IncompleteData(ClientValue):
    missingDataBeforeDateTime: datetime | None = None
    wasThrottled: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IncompleteData"
