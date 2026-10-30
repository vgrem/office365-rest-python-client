from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.teams.schedule.change_tracked_entity import ChangeTrackedEntity
from office365.teams.schedule.time_off_reason_icon_type import TimeOffReasonIconType


class TimeOffReason(ChangeTrackedEntity):
    """Represents a valid reason to take time off in a schedule."""

    @odata(name="code")
    @property
    def code(self) -> Optional[str]:
        """Gets the code property"""
        return self.properties.get("code", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="iconType")
    @property
    def icon_type(self) -> TimeOffReasonIconType:
        """Gets the iconType property"""
        return self.properties.get("iconType", TimeOffReasonIconType.none)

    @odata(name="isActive")
    @property
    def is_active(self) -> Optional[bool]:
        """Gets the isActive property"""
        return self.properties.get("isActive", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimeOffReason"
