from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.outlook.mail.messages.responsetype import ResponseType
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.outlook.calendar.meetingtimes.time_slot import TimeSlot


class EventMessageResponse(Entity):
    @odata(name="proposedNewTime")
    @property
    def proposed_new_time(self) -> TimeSlot:
        """Gets the proposedNewTime property"""
        from office365.outlook.calendar.meetingtimes.time_slot import TimeSlot

        return self.properties.get("proposedNewTime", TimeSlot())

    @odata(name="responseType")
    @property
    def response_type(self) -> ResponseType:
        """Gets the responseType property"""
        return self.properties.get("responseType", ResponseType.none)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EventMessageResponse"
