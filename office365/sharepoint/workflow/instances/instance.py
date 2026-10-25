from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class WorkflowInstance(Entity):
    """Represents a workflow instance."""

    @property
    def entity_type_name(self):
        return "SP.WorkflowServices.WorkflowInstance"

    @odata(name="FaultInfo")
    @property
    def fault_info(self) -> Optional[str]:
        """Gets the FaultInfo property"""
        return self.properties.get("FaultInfo", None)

    @odata(name="Id")
    @property
    def id(self) -> Optional[UUID]:
        """Gets the Id property"""
        return self.properties.get("Id", None)

    @odata(name="InstanceCreated")
    @property
    def instance_created(self) -> Optional[datetime]:
        """Gets the InstanceCreated property"""
        return self.properties.get("InstanceCreated", datetime.min)

    @odata(name="LastUpdated")
    @property
    def last_updated(self) -> Optional[datetime]:
        """Gets the LastUpdated property"""
        return self.properties.get("LastUpdated", datetime.min)

    @odata(name="Status")
    @property
    def status(self) -> Optional[int]:
        """Gets the Status property"""
        return self.properties.get("Status", None)

    @odata(name="UserStatus")
    @property
    def user_status(self) -> Optional[str]:
        """Gets the UserStatus property"""
        return self.properties.get("UserStatus", None)

    @odata(name="WorkflowSubscriptionId")
    @property
    def workflow_subscription_id(self) -> Optional[UUID]:
        """Gets the WorkflowSubscriptionId property"""
        return self.properties.get("WorkflowSubscriptionId", None)
