from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class PrinterShareViewpoint(ClientValue):
    lastUsedDateTime: datetime | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrinterShareViewpoint"
