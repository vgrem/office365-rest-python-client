from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.teams.schedule.change_tracked_entity import ChangeTrackedEntity
from office365.teams.schedule.shifts.item import ShiftItem
from office365.teams.schedule.shifts.scheduling_group_info import SchedulingGroupInfo
from office365.teams.schedule.shifts.team_info import ShiftsTeamInfo
from office365.teams.schedule.shifts.user_info import ShiftsUserInfo


class Shift(ChangeTrackedEntity):
    """
    Represents a unit of scheduled work in a shifts.
    """

    @odata(name="draftShift")
    @property
    def draft_shift(self) -> ShiftItem:
        """
        The draft version of this shift that is viewable by managers.
        """
        return self.properties.get("draftShift", ShiftItem())

    @odata(name="sharedShift")
    @property
    def shared_shift(self) -> ShiftItem:
        """
        The shared version of this shift that is viewable by both employees and managers.
        """
        return self.properties.get("sharedShift", ShiftItem())

    @odata(name="isStagedForDeletion")
    @property
    def is_staged_for_deletion(self) -> Optional[bool]:
        """Gets the isStagedForDeletion property"""
        return self.properties.get("isStagedForDeletion", None)

    @odata(name="schedulingGroupId")
    @property
    def scheduling_group_id(self) -> Optional[str]:
        """Gets the schedulingGroupId property"""
        return self.properties.get("schedulingGroupId", None)

    @odata(name="userId")
    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Shift"

    @odata(name="schedulingGroupInfo", beta=True, readonly=True)
    @property
    def scheduling_group_info(self) -> Optional[SchedulingGroupInfo]:
        """Gets the schedulingGroupInfo property"""
        return self.properties.get("schedulingGroupInfo", None)

    @odata(name="teamInfo", beta=True, readonly=True)
    @property
    def team_info(self) -> Optional[ShiftsTeamInfo]:
        """Gets the teamInfo property"""
        return self.properties.get("teamInfo", None)

    @odata(name="userInfo", beta=True, readonly=True)
    @property
    def user_info(self) -> Optional[ShiftsUserInfo]:
        """Gets the userInfo property"""
        return self.properties.get("userInfo", None)
