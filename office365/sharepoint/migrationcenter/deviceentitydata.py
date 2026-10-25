from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class DeviceEntityData(Entity):
    @odata(name="ClientUserName")
    @property
    def client_user_name(self) -> Optional[str]:
        """Gets the ClientUserName property"""
        return self.properties.get("ClientUserName", None)

    @odata(name="DeviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the DeviceName property"""
        return self.properties.get("DeviceName", None)

    @odata(name="DiskSpace")
    @property
    def disk_space(self) -> Optional[int]:
        """Gets the DiskSpace property"""
        return self.properties.get("DiskSpace", None)

    @odata(name="FreeQuota")
    @property
    def free_quota(self) -> Optional[int]:
        """Gets the FreeQuota property"""
        return self.properties.get("FreeQuota", None)

    @odata(name="FriendlyName")
    @property
    def friendly_name(self) -> Optional[str]:
        """Gets the FriendlyName property"""
        return self.properties.get("FriendlyName", None)

    @odata(name="GroupName")
    @property
    def group_name(self) -> Optional[str]:
        """Gets the GroupName property"""
        return self.properties.get("GroupName", None)

    @odata(name="StatusQueueExpiresOnTimeUtc")
    @property
    def status_queue_expires_on_time_utc(self) -> datetime:
        """Gets the StatusQueueExpiresOnTimeUtc property"""
        return self.properties.get("StatusQueueExpiresOnTimeUtc", datetime.min)

    @odata(name="StatusQueueUrl")
    @property
    def status_queue_url(self) -> Optional[str]:
        """Gets the StatusQueueUrl property"""
        return self.properties.get("StatusQueueUrl", None)

    @odata(name="TargetUserName")
    @property
    def target_user_name(self) -> Optional[str]:
        """Gets the TargetUserName property"""
        return self.properties.get("TargetUserName", None)

    @odata(name="TaskQueueExpiresOnTimeUtc")
    @property
    def task_queue_expires_on_time_utc(self) -> datetime:
        """Gets the TaskQueueExpiresOnTimeUtc property"""
        return self.properties.get("TaskQueueExpiresOnTimeUtc", datetime.min)

    @odata(name="TaskQueueUrl")
    @property
    def task_queue_url(self) -> Optional[str]:
        """Gets the TaskQueueUrl property"""
        return self.properties.get("TaskQueueUrl", None)

    @odata(name="Version")
    @property
    def version(self) -> Optional[str]:
        """Gets the Version property"""
        return self.properties.get("Version", None)

    @odata(name="WorkingFolder")
    @property
    def working_folder(self) -> Optional[str]:
        """Gets the WorkingFolder property"""
        return self.properties.get("WorkingFolder", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.DeviceEntityData"

    @odata(name="Id")
    @property
    def id(self) -> Optional[UUID]:
        """Gets the Id property"""
        return self.properties.get("Id", None)
