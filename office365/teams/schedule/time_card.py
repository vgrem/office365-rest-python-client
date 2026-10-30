from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.outlook.mail.item_body import ItemBody
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata
from office365.teams.schedule.confirmedby import ConfirmedBy
from office365.teams.schedule.time_card_break import TimeCardBreak
from office365.teams.schedule.time_card_entry import TimeCardEntry
from office365.teams.schedule.time_card_event import TimeCardEvent
from office365.teams.schedule.time_card_state import TimeCardState


class TimeCard(Entity):
    @odata(name="breaks")
    @property
    def breaks(self) -> ClientValueCollection[TimeCardBreak]:
        """Gets the breaks property"""
        return self.properties.get("breaks", ClientValueCollection[TimeCardBreak](TimeCardBreak))

    @odata(name="clockInEvent")
    @property
    def clock_in_event(self) -> TimeCardEvent:
        """Gets the clockInEvent property"""
        return self.properties.get("clockInEvent", TimeCardEvent())

    @odata(name="clockOutEvent")
    @property
    def clock_out_event(self) -> TimeCardEvent:
        """Gets the clockOutEvent property"""
        return self.properties.get("clockOutEvent", TimeCardEvent())

    @odata(name="confirmedBy")
    @property
    def confirmed_by(self) -> ConfirmedBy:
        """Gets the confirmedBy property"""
        return self.properties.get("confirmedBy", ConfirmedBy.none)

    @odata(name="notes")
    @property
    def notes(self) -> ItemBody:
        """Gets the notes property"""
        return self.properties.get("notes", ItemBody())

    @odata(name="originalEntry")
    @property
    def original_entry(self) -> TimeCardEntry:
        """Gets the originalEntry property"""
        return self.properties.get("originalEntry", TimeCardEntry())

    @odata(name="state")
    @property
    def state(self) -> TimeCardState:
        """Gets the state property"""
        return self.properties.get("state", TimeCardState.clockedIn)

    @odata(name="userId")
    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimeCard"
