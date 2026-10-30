from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.exportjoblocalizationtype import DeviceManagementExportJobLocalizationType
from office365.intune.devices.management.reports.fileformat import DeviceManagementReportFileFormat
from office365.intune.devices.management.reports.status import DeviceManagementReportStatus
from office365.runtime.types.odata_property import odata


class DeviceManagementExportJob(Entity):
    @odata(name="expirationDateTime")
    @property
    def expiration_date_time(self) -> Optional[datetime]:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @odata(name="filter")
    @property
    def filter(self) -> Optional[str]:
        """Gets the filter property"""
        return self.properties.get("filter", None)

    @odata(name="format")
    @property
    def format(self) -> DeviceManagementReportFileFormat:
        """Gets the format property"""
        return self.properties.get("format", DeviceManagementReportFileFormat.csv)

    @odata(name="localizationType")
    @property
    def localization_type(self) -> DeviceManagementExportJobLocalizationType:
        """Gets the localizationType property"""
        return self.properties.get(
            "localizationType", DeviceManagementExportJobLocalizationType.localizedValuesAsAdditionalColumn
        )

    @odata(name="reportName")
    @property
    def report_name(self) -> Optional[str]:
        """Gets the reportName property"""
        return self.properties.get("reportName", None)

    @odata(name="requestDateTime")
    @property
    def request_date_time(self) -> Optional[datetime]:
        """Gets the requestDateTime property"""
        return self.properties.get("requestDateTime", datetime.min)

    @odata(name="snapshotId")
    @property
    def snapshot_id(self) -> Optional[str]:
        """Gets the snapshotId property"""
        return self.properties.get("snapshotId", None)

    @odata(name="status")
    @property
    def status(self) -> DeviceManagementReportStatus:
        """Gets the status property"""
        return self.properties.get("status", DeviceManagementReportStatus.unknown)

    @odata(name="url")
    @property
    def url(self) -> Optional[str]:
        """Gets the url property"""
        return self.properties.get("url", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementExportJob"
