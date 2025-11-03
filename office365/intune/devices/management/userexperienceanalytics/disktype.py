from enum import Enum


class DiskType(Enum):
    unknown = "0"
    hdd = "1"
    ssd = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DiskType"
