from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata
from office365.security.detection_action import DetectionAction
from office365.security.detection_rule_status import DetectionRuleStatus
from office365.security.query_condition import QueryCondition
from office365.security.rule_schedule import RuleSchedule


class DetectionRule(Entity):
    @odata(name="createdBy")
    @property
    def created_by(self) -> Optional[str]:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="detectionAction")
    @property
    def detection_action(self) -> Optional[DetectionAction]:
        """Gets the detectionAction property"""
        return self.properties.get("detectionAction", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> Optional[str]:
        """Gets the lastModifiedBy property"""
        return self.properties.get("lastModifiedBy", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="queryCondition")
    @property
    def query_condition(self) -> Optional[QueryCondition]:
        """Gets the queryCondition property"""
        return self.properties.get("queryCondition", None)

    @odata(name="schedule")
    @property
    def schedule(self) -> Optional[RuleSchedule]:
        """Gets the schedule property"""
        return self.properties.get("schedule", None)

    @odata(name="status")
    @property
    def status(self) -> Optional[DetectionRuleStatus]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.DetectionRule"
