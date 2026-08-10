from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from office365.runtime.client_value import ClientValue


@dataclass
class RetentionSetting(ClientValue):
    interval: str | None = None
    period: timedelta | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RetentionSetting"
