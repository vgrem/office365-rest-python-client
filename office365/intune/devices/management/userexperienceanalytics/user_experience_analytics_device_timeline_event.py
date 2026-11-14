from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsDeviceTimelineEvent(Entity):
    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="eventDateTime")
    @property
    def event_date_time(self) -> Optional[datetime]:
        """Gets the eventDateTime property"""
        return self.properties.get("eventDateTime", None)

    @odata(name="eventDetails")
    @property
    def event_details(self) -> Optional[str]:
        """Gets the eventDetails property"""
        return self.properties.get("eventDetails", None)

    @odata(name="eventName")
    @property
    def event_name(self) -> Optional[str]:
        """Gets the eventName property"""
        return self.properties.get("eventName", None)

    @odata(name="eventSource")
    @property
    def event_source(self) -> Optional[str]:
        """Gets the eventSource property"""
        return self.properties.get("eventSource", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsDeviceTimelineEvent"
