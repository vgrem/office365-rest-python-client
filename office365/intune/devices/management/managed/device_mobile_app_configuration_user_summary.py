from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class ManagedDeviceMobileAppConfigurationUserSummary(Entity):
    @odata(name="configurationVersion")
    @property
    def configuration_version(self) -> Optional[int]:
        """Gets the configurationVersion property"""
        return self.properties.get("configurationVersion", None)

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

    @odata(name="lastUpdateDateTime")
    @property
    def last_update_date_time(self) -> Optional[datetime]:
        """Gets the lastUpdateDateTime property"""
        return self.properties.get("lastUpdateDateTime", datetime.min)

    @odata(name="notApplicableCount")
    @property
    def not_applicable_count(self) -> Optional[int]:
        """Gets the notApplicableCount property"""
        return self.properties.get("notApplicableCount", None)

    @odata(name="pendingCount")
    @property
    def pending_count(self) -> Optional[int]:
        """Gets the pendingCount property"""
        return self.properties.get("pendingCount", None)

    @odata(name="successCount")
    @property
    def success_count(self) -> Optional[int]:
        """Gets the successCount property"""
        return self.properties.get("successCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedDeviceMobileAppConfigurationUserSummary"
