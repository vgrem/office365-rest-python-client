from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceConfigurationUserStateSummary(Entity):
    @odata(name="compliantUserCount")
    @property
    def compliant_user_count(self) -> Optional[int]:
        """Gets the compliantUserCount property"""
        return self.properties.get("compliantUserCount", None)

    @odata(name="conflictUserCount")
    @property
    def conflict_user_count(self) -> Optional[int]:
        """Gets the conflictUserCount property"""
        return self.properties.get("conflictUserCount", None)

    @odata(name="errorUserCount")
    @property
    def error_user_count(self) -> Optional[int]:
        """Gets the errorUserCount property"""
        return self.properties.get("errorUserCount", None)

    @odata(name="nonCompliantUserCount")
    @property
    def non_compliant_user_count(self) -> Optional[int]:
        """Gets the nonCompliantUserCount property"""
        return self.properties.get("nonCompliantUserCount", None)

    @odata(name="notApplicableUserCount")
    @property
    def not_applicable_user_count(self) -> Optional[int]:
        """Gets the notApplicableUserCount property"""
        return self.properties.get("notApplicableUserCount", None)

    @odata(name="remediatedUserCount")
    @property
    def remediated_user_count(self) -> Optional[int]:
        """Gets the remediatedUserCount property"""
        return self.properties.get("remediatedUserCount", None)

    @odata(name="unknownUserCount")
    @property
    def unknown_user_count(self) -> Optional[int]:
        """Gets the unknownUserCount property"""
        return self.properties.get("unknownUserCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceConfigurationUserStateSummary"
