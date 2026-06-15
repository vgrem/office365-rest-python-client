from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from office365.runtime.client_value import ClientValue


@dataclass
class Duration(ClientValue):
    """Represents an Edm.Duration value (ISO 8601 duration format, e.g. PT1H)."""

    value: str | None = None

    @staticmethod
    def parse(value: str | timedelta) -> Duration:
        if isinstance(value, timedelta):
            total_sec = int(value.total_seconds())
            h, r = divmod(total_sec, 3600)
            m = r // 60
            result = "PT"
            if h:
                result += f"{h}H"
            if m:
                result += f"{m}M"
            return Duration(value=result or "PT0M")
        return Duration(value=value)

    @property
    def entity_type_name(self):
        return None
