from __future__ import annotations

from datetime import date

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class BookingsAvailabilityWindow(ClientValue):
    endDate: date = date.min
    startDate: date = date.min

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingsAvailabilityWindow"
