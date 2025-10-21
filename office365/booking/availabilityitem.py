from office365.booking.savailabilitystatus import BookingsAvailabilityStatus
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.runtime.client_value import ClientValue


class AvailabilityItem(ClientValue):

    def __init__(
        self,
        end_date_time: DateTimeTimeZone = DateTimeTimeZone(),
        service_id: str = None,
        start_date_time: DateTimeTimeZone = DateTimeTimeZone(),
        status: BookingsAvailabilityStatus = BookingsAvailabilityStatus.none,
    ):
        self.endDateTime = end_date_time
        self.serviceId = service_id
        self.startDateTime = start_date_time
        self.status = status

    @property
    def entity_type_name(self):
        return "microsoft.graph.AvailabilityItem"
