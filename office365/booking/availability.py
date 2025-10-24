from office365.booking.serviceavailabilitytype import BookingsServiceAvailabilityType
from office365.booking.work_hours import BookingWorkHours
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class BookingsAvailability(ClientValue):

    def __init__(
        self,
        availability_type: BookingsServiceAvailabilityType = BookingsServiceAvailabilityType.none,
        business_hours: ClientValueCollection[BookingWorkHours] = ClientValueCollection(BookingWorkHours),
    ):
        self.availabilityType = availability_type
        self.businessHours = business_hours

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingsAvailability"
