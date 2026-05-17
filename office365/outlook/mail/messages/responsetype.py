from enum import Enum


class ResponseType(Enum):
    none = "0"
    organizer = "1"
    tentativelyAccepted = "2"
    accepted = "3"
    declined = "4"
    notResponded = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ResponseType"
