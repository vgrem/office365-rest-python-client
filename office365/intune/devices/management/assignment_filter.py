from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.common.assignment_filter_evaluation_mode import AssignmentFilterEvaluationMode
from office365.common.assignment_filter_management_type import AssignmentFilterManagementType
from office365.common.payload_by_filter import PayloadByFilter
from office365.entity import Entity
from office365.intune.devices.platformtype import DevicePlatformType
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceAndAppManagementAssignmentFilter(Entity):
    @odata(name="assignmentFilterManagementType")
    @property
    def assignment_filter_management_type(self) -> Optional[AssignmentFilterManagementType]:
        """Gets the assignmentFilterManagementType property"""
        return self.properties.get("assignmentFilterManagementType", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="evaluationMode", readonly=True)
    @property
    def evaluation_mode(self) -> Optional[AssignmentFilterEvaluationMode]:
        """Gets the evaluationMode property"""
        return self.properties.get("evaluationMode", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="payloads")
    @property
    def payloads(self) -> ClientValueCollection[PayloadByFilter]:
        """Gets the payloads property"""
        return self.properties.get("payloads", ClientValueCollection[PayloadByFilter](PayloadByFilter))

    @odata(name="platform")
    @property
    def platform(self) -> DevicePlatformType:
        """Gets the platform property"""
        return self.properties.get("platform", DevicePlatformType.android)

    @odata(name="roleScopeTags")
    @property
    def role_scope_tags(self) -> StringCollection:
        """Gets the roleScopeTags property"""
        return self.properties.get("roleScopeTags", StringCollection())

    @odata(name="rule")
    @property
    def rule(self) -> Optional[str]:
        """Gets the rule property"""
        return self.properties.get("rule", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceAndAppManagementAssignmentFilter"
