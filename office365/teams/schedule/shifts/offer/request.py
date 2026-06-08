from datetime import datetime
from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.teams.schedule.change_request import ScheduleChangeRequest


class OfferShiftRequest(ScheduleChangeRequest):
    """Represents a request to offer a shift to another user in the team."""

    @odata(name="recipientActionDateTime")
    @property
    def recipient_action_datetime(self):
        """
        The Timestamp type represents date and time information using ISO 8601 format and is always in UTC time.
        """
        return self.properties.get("recipientActionDateTime", datetime.min)

    @property
    def recipient_action_message(self) -> Optional[str]:
        """
        Custom message sent by recipient of the offer shift request.
        """
        return self.properties.get("recipientActionMessage", None)

    @property
    def recipient_user_id(self) -> Optional[str]:
        """
        User ID of the recipient of the offer shift request.
        """
        return self.properties.get("recipientUserId", None)

    @property
    def sender_shift_id(self) -> Optional[str]:
        """
        User ID of the sender of the offer shift request.
        """
        return self.properties.get("senderShiftId", None)
