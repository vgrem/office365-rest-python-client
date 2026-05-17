from enum import Enum


class TimeZoneStandard(Enum):
    windows = "0"
    iana = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TimeZoneStandard"
