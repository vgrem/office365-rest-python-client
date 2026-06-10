from office365.runtime.types.odata_property import odata
from office365.teams.schedule.change_tracked_entity import ChangeTrackedEntity
from office365.teams.schedule.shifts.item import ShiftItem


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
