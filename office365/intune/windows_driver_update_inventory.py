from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.driver_approval_status import DriverApprovalStatus
from office365.intune.driver_category import DriverCategory
from office365.runtime.types.odata_property import odata, version


@version("beta")
class WindowsDriverUpdateInventory(Entity):
    @odata(name="applicableDeviceCount")
    @property
    def applicable_device_count(self) -> Optional[int]:
        """Gets the applicableDeviceCount property"""
        return self.properties.get("applicableDeviceCount", None)

    @odata(name="approvalStatus")
    @property
    def approval_status(self) -> Optional[DriverApprovalStatus]:
        """Gets the approvalStatus property"""
        return self.properties.get("approvalStatus", None)

    @odata(name="category")
    @property
    def category(self) -> Optional[DriverCategory]:
        """Gets the category property"""
        return self.properties.get("category", None)

    @odata(name="deployDateTime")
    @property
    def deploy_date_time(self) -> Optional[datetime]:
        """Gets the deployDateTime property"""
        return self.properties.get("deployDateTime", None)

    @odata(name="driverClass")
    @property
    def driver_class(self) -> Optional[str]:
        """Gets the driverClass property"""
        return self.properties.get("driverClass", None)

    @odata(name="manufacturer")
    @property
    def manufacturer(self) -> Optional[str]:
        """Gets the manufacturer property"""
        return self.properties.get("manufacturer", None)

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @odata(name="releaseDateTime")
    @property
    def release_date_time(self) -> Optional[datetime]:
        """Gets the releaseDateTime property"""
        return self.properties.get("releaseDateTime", None)

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsDriverUpdateInventory"
