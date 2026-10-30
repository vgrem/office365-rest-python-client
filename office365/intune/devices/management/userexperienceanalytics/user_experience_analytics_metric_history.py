from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class UserExperienceAnalyticsMetricHistory(Entity):
    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="metricDateTime")
    @property
    def metric_date_time(self) -> Optional[datetime]:
        """Gets the metricDateTime property"""
        return self.properties.get("metricDateTime", datetime.min)

    @odata(name="metricType")
    @property
    def metric_type(self) -> Optional[str]:
        """Gets the metricType property"""
        return self.properties.get("metricType", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsMetricHistory"
