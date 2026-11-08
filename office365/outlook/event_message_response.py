from __future__ import annotations

from office365.entity import Entity
from office365.outlook.calendar.meetingtimes.time_slot import TimeSlot
from office365.outlook.mail.messages.responsetype import ResponseType
from office365.runtime.types.odata_property import odata


class EventMessageResponse(Entity):
    @odata(name="proposedNewTime")
    @property
    def proposed_new_time(self) -> TimeSlot:
        """Gets the proposedNewTime property"""
        return self.properties.get("proposedNewTime", TimeSlot())

    @odata(name="responseType")
    @property
    def response_type(self) -> ResponseType:
        """Gets the responseType property"""
        return self.properties.get("responseType", ResponseType.none)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EventMessageResponse"
