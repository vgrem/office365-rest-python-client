from datetime import date

from office365.runtime.client_value import ClientValue


class BookingsAvailabilityWindow(ClientValue):
    def __init__(self, end_date: date = date.min, start_date: date = date.min):
        self.endDate = end_date
        self.startDate = start_date

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingsAvailabilityWindow"
