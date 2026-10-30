from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.virtualendpoint.cloudpcs.deviceimageerrorcode import CloudPcDeviceImageErrorCode
from office365.intune.devices.management.virtualendpoint.cloudpcs.deviceimageosstatus import CloudPcDeviceImageOsStatus
from office365.intune.devices.management.virtualendpoint.cloudpcs.deviceimagestatus import CloudPcDeviceImageStatus
from office365.runtime.types.odata_property import odata


class CloudPcDeviceImage(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="errorCode")
    @property
    def error_code(self) -> CloudPcDeviceImageErrorCode:
        """Gets the errorCode property"""
        return self.properties.get("errorCode", CloudPcDeviceImageErrorCode.internalServerError)

    @odata(name="expirationDate")
    @property
    def expiration_date(self) -> Optional[date]:
        """Gets the expirationDate property"""
        return self.properties.get("expirationDate", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="operatingSystem")
    @property
    def operating_system(self) -> Optional[str]:
        """Gets the operatingSystem property"""
        return self.properties.get("operatingSystem", None)

    @odata(name="osBuildNumber")
    @property
    def os_build_number(self) -> Optional[str]:
        """Gets the osBuildNumber property"""
        return self.properties.get("osBuildNumber", None)

    @odata(name="osStatus")
    @property
    def os_status(self) -> CloudPcDeviceImageOsStatus:
        """Gets the osStatus property"""
        return self.properties.get("osStatus", CloudPcDeviceImageOsStatus.supported)

    @odata(name="osVersionNumber")
    @property
    def os_version_number(self) -> Optional[str]:
        """Gets the osVersionNumber property"""
        return self.properties.get("osVersionNumber", None)

    @odata(name="sizeInGB")
    @property
    def size_in_gb(self) -> Optional[int]:
        """Gets the sizeInGB property"""
        return self.properties.get("sizeInGB", None)

    @odata(name="sourceImageResourceId")
    @property
    def source_image_resource_id(self) -> Optional[str]:
        """Gets the sourceImageResourceId property"""
        return self.properties.get("sourceImageResourceId", None)

    @odata(name="status")
    @property
    def status(self) -> CloudPcDeviceImageStatus:
        """Gets the status property"""
        return self.properties.get("status", CloudPcDeviceImageStatus.pending)

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudPcDeviceImage"
