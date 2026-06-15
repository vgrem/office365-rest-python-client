from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta


@dataclass
class Duration:
    """Represents an Edm.Duration value (ISO 8601 duration format, e.g. PT1H)."""

    @staticmethod
    def parse(value: timedelta) -> str:
        total_sec = int(value.total_seconds())
        h, r = divmod(total_sec, 3600)
        m = r // 60
        result = "PT"
        if h:
            result += f"{h}H"
        if m:
            result += f"{m}M"
        return result or "PT0M"
