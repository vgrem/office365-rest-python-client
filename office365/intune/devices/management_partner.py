from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.intune.devices.management.partnerapptype import DeviceManagementPartnerAppType
from office365.intune.devices.management.partnertenantstate import DeviceManagementPartnerTenantState
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.partner_assignment import (
        DeviceManagementPartnerAssignment,
    )


class DeviceManagementPartner(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="groupsRequiringPartnerEnrollment")
    @property
    def groups_requiring_partner_enrollment(self) -> ClientValueCollection[DeviceManagementPartnerAssignment]:
        """Gets the groupsRequiringPartnerEnrollment property"""
        from office365.intune.devices.management.partner_assignment import (
            DeviceManagementPartnerAssignment,
        )

        return self.properties.get(
            "groupsRequiringPartnerEnrollment",
            ClientValueCollection[DeviceManagementPartnerAssignment](DeviceManagementPartnerAssignment),
        )

    @odata(name="isConfigured")
    @property
    def is_configured(self) -> Optional[bool]:
        """Gets the isConfigured property"""
        return self.properties.get("isConfigured", None)

    @odata(name="lastHeartbeatDateTime")
    @property
    def last_heartbeat_date_time(self) -> Optional[datetime]:
        """Gets the lastHeartbeatDateTime property"""
        return self.properties.get("lastHeartbeatDateTime", datetime.min)

    @odata(name="partnerAppType")
    @property
    def partner_app_type(self) -> DeviceManagementPartnerAppType:
        """Gets the partnerAppType property"""
        return self.properties.get("partnerAppType", DeviceManagementPartnerAppType.unknown)

    @odata(name="partnerState")
    @property
    def partner_state(self) -> DeviceManagementPartnerTenantState:
        """Gets the partnerState property"""
        return self.properties.get("partnerState", DeviceManagementPartnerTenantState.unknown)

    @odata(name="singleTenantAppId")
    @property
    def single_tenant_app_id(self) -> Optional[str]:
        """Gets the singleTenantAppId property"""
        return self.properties.get("singleTenantAppId", None)

    @odata(name="whenPartnerDevicesWillBeMarkedAsNonCompliantDateTime")
    @property
    def when_partner_devices_will_be_marked_as_non_compliant_date_time(self) -> Optional[datetime]:
        """Gets the whenPartnerDevicesWillBeMarkedAsNonCompliantDateTime property"""
        return self.properties.get("whenPartnerDevicesWillBeMarkedAsNonCompliantDateTime", datetime.min)

    @odata(name="whenPartnerDevicesWillBeRemovedDateTime")
    @property
    def when_partner_devices_will_be_removed_date_time(self) -> Optional[datetime]:
        """Gets the whenPartnerDevicesWillBeRemovedDateTime property"""
        return self.properties.get("whenPartnerDevicesWillBeRemovedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementPartner"
