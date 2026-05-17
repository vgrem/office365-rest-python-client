from enum import Enum


class BookingPageAccessControl(Enum):
    unrestricted = "0"
    restrictedToOrganization = "1"
    unknownFutureValue = "2"

    none = "-1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingPageAccessControl"
