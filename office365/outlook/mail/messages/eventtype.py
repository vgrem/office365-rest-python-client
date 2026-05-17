from enum import Enum


class EventType(Enum):
    singleInstance = "0"
    occurrence = "1"
    exception = "2"
    seriesMaster = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EventType"
