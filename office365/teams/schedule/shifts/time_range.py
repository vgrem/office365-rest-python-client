from datetime import time

from office365.runtime.client_value import ClientValue


class TimeRange(ClientValue):
    endTime: time | None = None
    startTime: time | None = None
    "A time range resource with a start and end time."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimeRange"
