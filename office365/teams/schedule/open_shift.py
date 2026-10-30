from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.outlook.calendar.schedule.open_shift_item import OpenShiftItem
from office365.runtime.types.odata_property import odata


class OpenShift(Entity):
    @odata(name="draftOpenShift")
    @property
    def draft_open_shift(self) -> OpenShiftItem:
        """Gets the draftOpenShift property"""
        return self.properties.get("draftOpenShift", OpenShiftItem())

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

    @odata(name="sharedOpenShift")
    @property
    def shared_open_shift(self) -> OpenShiftItem:
        """Gets the sharedOpenShift property"""
        return self.properties.get("sharedOpenShift", OpenShiftItem())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OpenShift"
