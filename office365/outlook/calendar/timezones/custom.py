from __future__ import annotations

from dataclasses import dataclass

from office365.outlook.calendar.timezones.base import TimeZoneBase


@dataclass
class CustomTimeZone(TimeZoneBase):
    """
    Represents a time zone where the transition from standard to daylight saving time, or vice versa is not standard.
    """

    bias: int | None = None
