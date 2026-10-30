from __future__ import annotations

from typing import Optional

from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.teams.schedule.change_tracked_entity import ChangeTrackedEntity


class SchedulingGroup(ChangeTrackedEntity):
    """A logical grouping of users in a shifts (usually by role)."""

    @odata(name="isActive", readonly=True)
    @property
    def is_active(self) -> Optional[bool]:
        """Indicates whether the schedulingGroup can be used when creating new entities or updating existing ones"""
        return self.properties.get("isActive", None)

    @odata(name="userIds")
    @property
    def user_ids(self) -> StringCollection:
        """The list of user IDs that are a member of the schedulingGroup."""
        return self.properties.get("userIds", StringCollection())

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

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SchedulingGroup"
