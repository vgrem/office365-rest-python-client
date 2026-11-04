from __future__ import annotations

from datetime import timedelta

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class RetentionSetting(ClientValue):
    interval: str | None = None
    period: timedelta | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RetentionSetting"
