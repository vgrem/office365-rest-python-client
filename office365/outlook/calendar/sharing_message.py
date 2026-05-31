from office365.outlook.calendar.sharing.message_action import (
    CalendarSharingMessageAction,
)
from office365.outlook.mail.messages.message import Message
from office365.runtime.types.odata_property import odata


class CalendarSharingMessage(Message):
    """"""

    @odata(name="sharingMessageAction")
    @property
    def sharing_message_action(self) -> CalendarSharingMessageAction:
        """"""
        return self.properties.setdefault("sharingMessageAction", CalendarSharingMessageAction())
