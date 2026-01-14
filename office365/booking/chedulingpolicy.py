from datetime import timedelta

from office365.booking.availability import BookingsAvailability
from office365.booking.availabilitywindow import BookingsAvailabilityWindow
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class BookingSchedulingPolicy(ClientValue):
    def __init__(
        self,
        allow_staff_selection: bool = None,
        custom_availabilities: ClientValueCollection[BookingsAvailabilityWindow] = ClientValueCollection(
            BookingsAvailabilityWindow
        ),
        general_availability: BookingsAvailability = BookingsAvailability(),
        is_meeting_invite_to_customers_enabled: bool = None,
        maximum_advance: timedelta = None,
        minimum_lead_time: timedelta = None,
        send_confirmations_to_owner: bool = None,
        time_slot_interval: timedelta = None,
    ):
        self.allowStaffSelection = allow_staff_selection
        self.customAvailabilities = custom_availabilities
        self.generalAvailability = general_availability
        self.isMeetingInviteToCustomersEnabled = is_meeting_invite_to_customers_enabled
        self.maximumAdvance = maximum_advance
        self.minimumLeadTime = minimum_lead_time
        self.sendConfirmationsToOwner = send_confirmations_to_owner
        self.timeSlotInterval = time_slot_interval

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingSchedulingPolicy"
