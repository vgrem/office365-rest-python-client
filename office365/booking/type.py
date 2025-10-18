from enum import Enum


class BookingType(Enum):
    unknown = "0"
    standard = "1"
    reserved = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingType"
