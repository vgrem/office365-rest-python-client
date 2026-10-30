from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.communications.onlinemeetings.base import OnlineMeetingBase
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone


class VirtualEventSession(OnlineMeetingBase):
    """Represents a session in a virtualEvent."""

    @odata(name="capacity")
    @property
    def capacity(self) -> Optional[int]:
        """Gets the capacity property"""
        return self.properties.get("capacity", None)

    @odata(name="endDateTime")
    @property
    def end_date_time(self) -> DateTimeTimeZone:
        """Gets the endDateTime property"""
        from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone

        return self.properties.get("endDateTime", DateTimeTimeZone())

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> DateTimeTimeZone:
        """Gets the startDateTime property"""
        from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone

        return self.properties.get("startDateTime", DateTimeTimeZone())

    @odata(name="videoOnDemandWebUrl")
    @property
    def video_on_demand_web_url(self) -> Optional[str]:
        """Gets the videoOnDemandWebUrl property"""
        return self.properties.get("videoOnDemandWebUrl", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VirtualEventSession"
