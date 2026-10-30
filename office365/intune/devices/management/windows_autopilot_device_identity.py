from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.enrollment_state import EnrollmentState


class WindowsAutopilotDeviceIdentity(Entity):
    @odata(name="addressableUserName")
    @property
    def addressable_user_name(self) -> Optional[str]:
        """Gets the addressableUserName property"""
        return self.properties.get("addressableUserName", None)

    @odata(name="azureActiveDirectoryDeviceId")
    @property
    def azure_active_directory_device_id(self) -> Optional[str]:
        """Gets the azureActiveDirectoryDeviceId property"""
        return self.properties.get("azureActiveDirectoryDeviceId", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="enrollmentState")
    @property
    def enrollment_state(self) -> EnrollmentState:
        """Gets the enrollmentState property"""
        from office365.intune.devices.management.enrollment_state import EnrollmentState

        return self.properties.get("enrollmentState", EnrollmentState.unknown)

    @odata(name="groupTag")
    @property
    def group_tag(self) -> Optional[str]:
        """Gets the groupTag property"""
        return self.properties.get("groupTag", None)

    @odata(name="lastContactedDateTime")
    @property
    def last_contacted_date_time(self) -> Optional[datetime]:
        """Gets the lastContactedDateTime property"""
        return self.properties.get("lastContactedDateTime", datetime.min)

    @odata(name="managedDeviceId")
    @property
    def managed_device_id(self) -> Optional[str]:
        """Gets the managedDeviceId property"""
        return self.properties.get("managedDeviceId", None)

    @odata(name="manufacturer")
    @property
    def manufacturer(self) -> Optional[str]:
        """Gets the manufacturer property"""
        return self.properties.get("manufacturer", None)

    @odata(name="model")
    @property
    def model(self) -> Optional[str]:
        """Gets the model property"""
        return self.properties.get("model", None)

    @odata(name="productKey")
    @property
    def product_key(self) -> Optional[str]:
        """Gets the productKey property"""
        return self.properties.get("productKey", None)

    @odata(name="purchaseOrderIdentifier")
    @property
    def purchase_order_identifier(self) -> Optional[str]:
        """Gets the purchaseOrderIdentifier property"""
        return self.properties.get("purchaseOrderIdentifier", None)

    @odata(name="resourceName")
    @property
    def resource_name(self) -> Optional[str]:
        """Gets the resourceName property"""
        return self.properties.get("resourceName", None)

    @odata(name="serialNumber")
    @property
    def serial_number(self) -> Optional[str]:
        """Gets the serialNumber property"""
        return self.properties.get("serialNumber", None)

    @odata(name="skuNumber")
    @property
    def sku_number(self) -> Optional[str]:
        """Gets the skuNumber property"""
        return self.properties.get("skuNumber", None)

    @odata(name="systemFamily")
    @property
    def system_family(self) -> Optional[str]:
        """Gets the systemFamily property"""
        return self.properties.get("systemFamily", None)

    @odata(name="userPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsAutopilotDeviceIdentity"
