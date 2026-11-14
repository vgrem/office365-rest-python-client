from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_status import (
    UserExperienceAnalyticsDeviceStatus,
)
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsAnomalyDevice(Entity):
    @odata(name="anomalyId")
    @property
    def anomaly_id(self) -> Optional[str]:
        """Gets the anomalyId property"""
        return self.properties.get("anomalyId", None)

    @odata(name="anomalyOnDeviceFirstOccurrenceDateTime")
    @property
    def anomaly_on_device_first_occurrence_date_time(self) -> Optional[datetime]:
        """Gets the anomalyOnDeviceFirstOccurrenceDateTime property"""
        return self.properties.get("anomalyOnDeviceFirstOccurrenceDateTime", None)

    @odata(name="anomalyOnDeviceLatestOccurrenceDateTime")
    @property
    def anomaly_on_device_latest_occurrence_date_time(self) -> Optional[datetime]:
        """Gets the anomalyOnDeviceLatestOccurrenceDateTime property"""
        return self.properties.get("anomalyOnDeviceLatestOccurrenceDateTime", None)

    @odata(name="correlationGroupId")
    @property
    def correlation_group_id(self) -> Optional[str]:
        """Gets the correlationGroupId property"""
        return self.properties.get("correlationGroupId", None)

    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="deviceManufacturer")
    @property
    def device_manufacturer(self) -> Optional[str]:
        """Gets the deviceManufacturer property"""
        return self.properties.get("deviceManufacturer", None)

    @odata(name="deviceModel")
    @property
    def device_model(self) -> Optional[str]:
        """Gets the deviceModel property"""
        return self.properties.get("deviceModel", None)

    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the deviceName property"""
        return self.properties.get("deviceName", None)

    @odata(name="deviceStatus")
    @property
    def device_status(self) -> Optional[UserExperienceAnalyticsDeviceStatus]:
        """Gets the deviceStatus property"""
        return self.properties.get("deviceStatus", None)

    @odata(name="osName")
    @property
    def os_name(self) -> Optional[str]:
        """Gets the osName property"""
        return self.properties.get("osName", None)

    @odata(name="osVersion")
    @property
    def os_version(self) -> Optional[str]:
        """Gets the osVersion property"""
        return self.properties.get("osVersion", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAnomalyDevice"
