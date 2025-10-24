from enum import Enum


class VirtualEventStatus(Enum):
    draft = "0"
    published = "1"
    canceled = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.VirtualEventStatus"
