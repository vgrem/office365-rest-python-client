from __future__ import annotations

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.teams.schedule.groups.group import SchedulingGroup
from office365.teams.schedule.shifts.open.change_request import OpenShiftChangeRequest
from office365.teams.schedule.shifts.shift import Shift
from office365.teams.schedule.time_off_reason import TimeOffReason


class Schedule(Entity):
    """A collection of schedulingGroup objects, shift objects, timeOffReason objects,
    and timeOff objects within a team."""

    @property
    def time_zone(self) -> str | None:
        """Indicates the time zone of the shifts team using tz database format. Required."""
        return self.properties.get("timeZone", None)

    @time_zone.setter
    def time_zone(self, value):
        self.set_property("timeZone", value)

    @odata(name="openShiftChangeRequests")
    @property
    def open_shift_change_requests(self) -> EntityCollection[OpenShiftChangeRequest]:
        """The shifts in the shifts."""
        return self.properties.get(
            "openShiftChangeRequests",
            EntityCollection(
                self.context,
                OpenShiftChangeRequest,
                ResourcePath("openShiftChangeRequests", self.resource_path),
            ),
        )

    @property
    def shifts(self) -> EntityCollection[Shift]:
        """The shifts in the shifts."""
        return self.properties.get(
            "shifts",
            EntityCollection(self.context, Shift, ResourcePath("shifts", self.resource_path)),
        )

    @odata(name="schedulingGroups")
    @property
    def scheduling_groups(self) -> EntityCollection[SchedulingGroup]:
        """The logical grouping of users in the shifts (usually by role)."""
        return self.properties.get(
            "schedulingGroups",
            EntityCollection(
                self.context,
                SchedulingGroup,
                ResourcePath("schedulingGroups", self.resource_path),
            ),
        )

    @odata(name="timeOffReasons")
    @property
    def time_off_reasons(self) -> EntityCollection[TimeOffReason]:
        """The set of reasons for a time off in the schedule."""
        return self.properties.get(
            "timeOffReasons",
            EntityCollection(
                self.context,
                TimeOffReason,
                ResourcePath("timeOffReasons", self.resource_path),
            ),
        )
