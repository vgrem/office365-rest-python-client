from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.timezones.base import TimeZoneBase
from office365.outlook.calendar.timezones.daylight_time_zone_offset import DaylightTimeZoneOffset
from office365.outlook.timezones.standard_time_zone_offset import StandardTimeZoneOffset


@dataclass
class CustomTimeZone(TimeZoneBase):
    """
    Represents a time zone where the transition from standard to daylight saving time, or vice versa is not standard.
    """

    bias: int | None = None
    daylightOffset: DaylightTimeZoneOffset = field(default_factory=DaylightTimeZoneOffset)
    standardOffset: StandardTimeZoneOffset = field(default_factory=StandardTimeZoneOffset)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomTimeZone"
