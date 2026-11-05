from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class IncompleteData(ClientValue):
    missingDataBeforeDateTime: datetime | None = None
    wasThrottled: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IncompleteData"
