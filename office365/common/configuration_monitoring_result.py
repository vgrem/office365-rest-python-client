from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.common.error_detail import ErrorDetail
    from office365.security.monitor_run_status import MonitorRunStatus


class ConfigurationMonitoringResult(Entity):
    @odata(name="driftsCount", readonly=True)
    @property
    def drifts_count(self) -> Optional[int]:
        """Gets the driftsCount property"""
        return self.properties.get("driftsCount", None)

    @odata(name="errorDetails", readonly=True)
    @property
    def error_details(self) -> ClientValueCollection[ErrorDetail]:
        """Gets the errorDetails property"""
        from office365.common.error_detail import ErrorDetail

        return self.properties.get("errorDetails", ClientValueCollection[ErrorDetail](ErrorDetail))

    @odata(name="monitorId", readonly=True)
    @property
    def monitor_id(self) -> Optional[str]:
        """Gets the monitorId property"""
        return self.properties.get("monitorId", None)

    @odata(name="runCompletionDateTime", readonly=True)
    @property
    def run_completion_date_time(self) -> Optional[datetime]:
        """Gets the runCompletionDateTime property"""
        return self.properties.get("runCompletionDateTime", datetime.min)

    @odata(name="runInitiationDateTime", readonly=True)
    @property
    def run_initiation_date_time(self) -> Optional[datetime]:
        """Gets the runInitiationDateTime property"""
        return self.properties.get("runInitiationDateTime", datetime.min)

    @odata(name="runStatus", readonly=True)
    @property
    def run_status(self) -> MonitorRunStatus:
        """Gets the runStatus property"""
        from office365.security.monitor_run_status import MonitorRunStatus

        return self.properties.get("runStatus", MonitorRunStatus.successful)

    @odata(name="tenantId", readonly=True)
    @property
    def tenant_id(self) -> Optional[str]:
        """Gets the tenantId property"""
        return self.properties.get("tenantId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConfigurationMonitoringResult"
