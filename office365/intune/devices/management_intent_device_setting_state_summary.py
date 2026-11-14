from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceManagementIntentDeviceSettingStateSummary(Entity):
    @odata(name="compliantCount")
    @property
    def compliant_count(self) -> Optional[int]:
        """Gets the compliantCount property"""
        return self.properties.get("compliantCount", None)

    @odata(name="conflictCount")
    @property
    def conflict_count(self) -> Optional[int]:
        """Gets the conflictCount property"""
        return self.properties.get("conflictCount", None)

    @odata(name="errorCount")
    @property
    def error_count(self) -> Optional[int]:
        """Gets the errorCount property"""
        return self.properties.get("errorCount", None)

    @odata(name="nonCompliantCount")
    @property
    def non_compliant_count(self) -> Optional[int]:
        """Gets the nonCompliantCount property"""
        return self.properties.get("nonCompliantCount", None)

    @odata(name="notApplicableCount")
    @property
    def not_applicable_count(self) -> Optional[int]:
        """Gets the notApplicableCount property"""
        return self.properties.get("notApplicableCount", None)

    @odata(name="remediatedCount")
    @property
    def remediated_count(self) -> Optional[int]:
        """Gets the remediatedCount property"""
        return self.properties.get("remediatedCount", None)

    @odata(name="settingName")
    @property
    def setting_name(self) -> Optional[str]:
        """Gets the settingName property"""
        return self.properties.get("settingName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementIntentDeviceSettingStateSummary"
