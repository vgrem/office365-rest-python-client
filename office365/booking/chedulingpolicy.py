from datetime import timedelta
from typing import Optional

from office365.booking.availability import BookingsAvailability
from office365.booking.availabilitywindow import BookingsAvailabilityWindow
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class BookingSchedulingPolicy(ClientValue):
    def __init__(
        self,
        allow_staff_selection: Optional[bool] = None,
        custom_availabilities: Optional[ClientValueCollection[BookingsAvailabilityWindow]] = None,
        general_availability: Optional[BookingsAvailability] = None,
        is_meeting_invite_to_customers_enabled: Optional[bool] = None,
        maximum_advance: Optional[timedelta] = None,
        minimum_lead_time: Optional[timedelta] = None,
        send_confirmations_to_owner: Optional[bool] = None,
        time_slot_interval: Optional[timedelta] = None,
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
