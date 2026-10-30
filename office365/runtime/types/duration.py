from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta


@dataclass
class Duration:
    """Represents an Edm.Duration value (ISO 8601 duration format, e.g. PT1H)."""

    @staticmethod
    def parse(value: timedelta) -> str:
        """The ISO 8601 form ``Edm.Duration`` takes, to the microsecond.

        ``PT1H30M`` for a duration, ``PT0S`` for none. Every component the value
        actually holds is written: a duration of 90 seconds is ``PT1M30S``, not
        ``PT1M`` -- a round trip must not lose what the service sent.
        """
        microseconds = round(value / timedelta(microseconds=1))
        sign = "-" if microseconds < 0 else ""
        microseconds = abs(microseconds)
        days, rest = divmod(microseconds, 86_400_000_000)
        hours, rest = divmod(rest, 3_600_000_000)
        minutes, rest = divmod(rest, 60_000_000)
        seconds = rest / 1_000_000
        text = f"{sign}P" + (f"{days}D" if days else "") + "T"
        text += f"{hours}H" if hours else ""
        text += f"{minutes}M" if minutes else ""
        if seconds:
            text += f"{seconds:g}S"
        elif text.endswith("T"):
            text += "0S"
        return text
