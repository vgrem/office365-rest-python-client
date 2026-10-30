from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.teams.schedule.time_off_item import TimeOffItem


class TimeOff(Entity):
    @odata(name="draftTimeOff")
    @property
    def draft_time_off(self) -> TimeOffItem:
        """Gets the draftTimeOff property"""
        from office365.teams.schedule.time_off_item import TimeOffItem

        return self.properties.get("draftTimeOff", TimeOffItem())

    @odata(name="isStagedForDeletion")
    @property
    def is_staged_for_deletion(self) -> Optional[bool]:
        """Gets the isStagedForDeletion property"""
        return self.properties.get("isStagedForDeletion", None)

    @odata(name="sharedTimeOff")
    @property
    def shared_time_off(self) -> TimeOffItem:
        """Gets the sharedTimeOff property"""
        from office365.teams.schedule.time_off_item import TimeOffItem

        return self.properties.get("sharedTimeOff", TimeOffItem())

    @odata(name="userId")
    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimeOff"
