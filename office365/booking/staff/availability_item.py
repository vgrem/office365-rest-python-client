from office365.booking.availabilityitem import AvailabilityItem
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class StaffAvailabilityItem(ClientValue):
    def __init__(
        self,
        availability_items: ClientValueCollection[AvailabilityItem] = ClientValueCollection(AvailabilityItem),
        staff_id: str = None,
    ):
        self.availabilityItems = availability_items
        self.staffId = staff_id

    "Represents the available and busy time slots of a Microsoft Bookings staff member."

    @property
    def entity_type_name(self):
        return "microsoft.graph.StaffAvailabilityItem"
