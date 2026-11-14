from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceHealthScriptRunSummary(Entity):
    @odata(name="detectionScriptErrorDeviceCount")
    @property
    def detection_script_error_device_count(self) -> Optional[int]:
        """Gets the detectionScriptErrorDeviceCount property"""
        return self.properties.get("detectionScriptErrorDeviceCount", None)

    @odata(name="detectionScriptNotApplicableDeviceCount")
    @property
    def detection_script_not_applicable_device_count(self) -> Optional[int]:
        """Gets the detectionScriptNotApplicableDeviceCount property"""
        return self.properties.get("detectionScriptNotApplicableDeviceCount", None)

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

    @odata(name="issueRemediatedCumulativeDeviceCount")
    @property
    def issue_remediated_cumulative_device_count(self) -> Optional[int]:
        """Gets the issueRemediatedCumulativeDeviceCount property"""
        return self.properties.get("issueRemediatedCumulativeDeviceCount", None)

    @odata(name="issueRemediatedDeviceCount")
    @property
    def issue_remediated_device_count(self) -> Optional[int]:
        """Gets the issueRemediatedDeviceCount property"""
        return self.properties.get("issueRemediatedDeviceCount", None)

    @odata(name="issueReoccurredDeviceCount")
    @property
    def issue_reoccurred_device_count(self) -> Optional[int]:
        """Gets the issueReoccurredDeviceCount property"""
        return self.properties.get("issueReoccurredDeviceCount", None)

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

    @odata(name="remediationScriptErrorDeviceCount")
    @property
    def remediation_script_error_device_count(self) -> Optional[int]:
        """Gets the remediationScriptErrorDeviceCount property"""
        return self.properties.get("remediationScriptErrorDeviceCount", None)

    @odata(name="remediationSkippedDeviceCount")
    @property
    def remediation_skipped_device_count(self) -> Optional[int]:
        """Gets the remediationSkippedDeviceCount property"""
        return self.properties.get("remediationSkippedDeviceCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceHealthScriptRunSummary"
