from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceManagementIntentDeviceStateSummary(Entity):
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

    @odata(name="failedCount")
    @property
    def failed_count(self) -> Optional[int]:
        """Gets the failedCount property"""
        return self.properties.get("failedCount", None)

    @odata(name="notApplicableCount")
    @property
    def not_applicable_count(self) -> Optional[int]:
        """Gets the notApplicableCount property"""
        return self.properties.get("notApplicableCount", None)

    @odata(name="notApplicablePlatformCount")
    @property
    def not_applicable_platform_count(self) -> Optional[int]:
        """Gets the notApplicablePlatformCount property"""
        return self.properties.get("notApplicablePlatformCount", None)

    @odata(name="successCount")
    @property
    def success_count(self) -> Optional[int]:
        """Gets the successCount property"""
        return self.properties.get("successCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementIntentDeviceStateSummary"
