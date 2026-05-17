from enum import Enum


class RiskDetectionTimingType(Enum):
    notDefined = "0"
    realtime = "1"
    nearRealtime = "2"
    offline = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RiskDetectionTimingType"
