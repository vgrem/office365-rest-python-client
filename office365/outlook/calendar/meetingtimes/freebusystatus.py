from enum import Enum


class FreeBusyStatus(Enum):
    unknown = "-1"
    free = "0"
    tentative = "1"
    busy = "2"
    oof = "3"
    workingElsewhere = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.FreeBusyStatus"
