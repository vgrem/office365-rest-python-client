from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class OsVersionCount(ClientValue):
    deviceCount: int | None = None
    lastUpdateDateTime: datetime | None = None
    osVersion: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OsVersionCount"
