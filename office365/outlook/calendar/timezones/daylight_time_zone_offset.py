from __future__ import annotations

from office365.outlook.timezones.standard_time_zone_offset import StandardTimeZoneOffset


class DaylightTimeZoneOffset(StandardTimeZoneOffset):
    daylightBias: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DaylightTimeZoneOffset"
