from __future__ import annotations

from datetime import date
from typing import Optional

from office365.entity import Entity
from office365.outlook.mail.item_body import ItemBody
from office365.runtime.types.odata_property import odata


class DayNote(Entity):
    @odata(name="dayNoteDate")
    @property
    def day_note_date(self) -> Optional[date]:
        """Gets the dayNoteDate property"""
        return self.properties.get("dayNoteDate", None)

    @odata(name="draftDayNote")
    @property
    def draft_day_note(self) -> ItemBody:
        """Gets the draftDayNote property"""
        return self.properties.get("draftDayNote", ItemBody())

    @odata(name="sharedDayNote")
    @property
    def shared_day_note(self) -> ItemBody:
        """Gets the sharedDayNote property"""
        return self.properties.get("sharedDayNote", ItemBody())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DayNote"
