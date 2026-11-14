from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceComplianceScriptRunSummary(Entity):
    @odata(name="detectionScriptErrorDeviceCount")
    @property
    def detection_script_error_device_count(self) -> Optional[int]:
        """Gets the detectionScriptErrorDeviceCount property"""
        return self.properties.get("detectionScriptErrorDeviceCount", None)

    @odata(name="detectionScriptPendingDeviceCount")
    @property
    def detection_script_pending_device_count(self) -> Optional[int]:
        """Gets the detectionScriptPendingDeviceCount property"""
        return self.properties.get("detectionScriptPendingDeviceCount", None)

    @odata(name="issueDetectedDeviceCount")
    @property
    def issue_detected_device_count(self) -> Optional[int]:
        """Gets the issueDetectedDeviceCount property"""
        return self.properties.get("issueDetectedDeviceCount", None)

    @odata(name="lastScriptRunDateTime")
    @property
    def last_script_run_date_time(self) -> Optional[datetime]:
        """Gets the lastScriptRunDateTime property"""
        return self.properties.get("lastScriptRunDateTime", None)

    @odata(name="noIssueDetectedDeviceCount")
    @property
    def no_issue_detected_device_count(self) -> Optional[int]:
        """Gets the noIssueDetectedDeviceCount property"""
        return self.properties.get("noIssueDetectedDeviceCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceComplianceScriptRunSummary"
