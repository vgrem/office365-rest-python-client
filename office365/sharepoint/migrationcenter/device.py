from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class Device(Entity):
    @odata(name="ActionId")
    @property
    def action_id(self) -> Optional[int]:
        """Gets the ActionId property"""
        return self.properties.get("ActionId", None)

    @odata(name="AssignedTimeUTC")
    @property
    def assigned_time_utc(self) -> datetime:
        """Gets the AssignedTimeUTC property"""
        return self.properties.get("AssignedTimeUTC", datetime.min)

    @odata(name="AssignmentId")
    @property
    def assignment_id(self) -> Optional[str]:
        """Gets the AssignmentId property"""
        return self.properties.get("AssignmentId", None)

    @odata(name="DebugCommand")
    @property
    def debug_command(self) -> Optional[str]:
        """Gets the DebugCommand property"""
        return self.properties.get("DebugCommand", None)

    @odata(name="DeviceAddedTimeUTC")
    @property
    def device_added_time_utc(self) -> datetime:
        """Gets the DeviceAddedTimeUTC property"""
        return self.properties.get("DeviceAddedTimeUTC", datetime.min)

    @odata(name="Disconnected")
    @property
    def disconnected(self) -> Optional[bool]:
        """Gets the Disconnected property"""
        return self.properties.get("Disconnected", None)

    @odata(name="ErrorCode")
    @property
    def error_code(self) -> Optional[str]:
        """Gets the ErrorCode property"""
        return self.properties.get("ErrorCode", None)

    @odata(name="ErrorMessage")
    @property
    def error_message(self) -> Optional[str]:
        """Gets the ErrorMessage property"""
        return self.properties.get("ErrorMessage", None)

    @odata(name="FromClient")
    @property
    def from_client(self) -> Optional[bool]:
        """Gets the FromClient property"""
        return self.properties.get("FromClient", None)

    @odata(name="LastActivityTimeUtc")
    @property
    def last_activity_time_utc(self) -> datetime:
        """Gets the LastActivityTimeUtc property"""
        return self.properties.get("LastActivityTimeUtc", datetime.min)

    @odata(name="LastHeartbeatTimeUtc")
    @property
    def last_heartbeat_time_utc(self) -> datetime:
        """Gets the LastHeartbeatTimeUtc property"""
        return self.properties.get("LastHeartbeatTimeUtc", datetime.min)

    @odata(name="LastModifiedTimeUtc")
    @property
    def last_modified_time_utc(self) -> datetime:
        """Gets the LastModifiedTimeUtc property"""
        return self.properties.get("LastModifiedTimeUtc", datetime.min)

    @odata(name="LinkedTaskId")
    @property
    def linked_task_id(self) -> Optional[UUID]:
        """Gets the LinkedTaskId property"""
        return self.properties.get("LinkedTaskId", None)

    @odata(name="Message")
    @property
    def message(self) -> Optional[str]:
        """Gets the Message property"""
        return self.properties.get("Message", None)

    @odata(name="RunningTaskCount")
    @property
    def running_task_count(self) -> Optional[int]:
        """Gets the RunningTaskCount property"""
        return self.properties.get("RunningTaskCount", None)

    @odata(name="Status")
    @property
    def status(self) -> Optional[int]:
        """Gets the Status property"""
        return self.properties.get("Status", None)

    @odata(name="UpdateTimestamp")
    @property
    def update_timestamp(self) -> Optional[str]:
        """Gets the UpdateTimestamp property"""
        return self.properties.get("UpdateTimestamp", None)

    @odata(name="WaitingTaskCount")
    @property
    def waiting_task_count(self) -> Optional[int]:
        """Gets the WaitingTaskCount property"""
        return self.properties.get("WaitingTaskCount", None)

    @odata(name="WorkflowJsonData")
    @property
    def workflow_json_data(self) -> Optional[str]:
        """Gets the WorkflowJsonData property"""
        return self.properties.get("WorkflowJsonData", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.Device"

    @odata(name="UpdateTimestamp")
    @property
    def up_datetimestamp(self) -> Optional[str]:
        """Gets the UpdateTimestamp property"""
        return self.properties.get("UpdateTimestamp", None)
