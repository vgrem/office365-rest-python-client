from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.compliance.setting_state_device_summary import (
        SettingStateDeviceSummary,
    )
    from office365.intune.devices.compliance_device_overview import (
        DeviceComplianceDeviceOverview,
    )
    from office365.intune.devices.compliance_device_status import (
        DeviceComplianceDeviceStatus,
    )
    from office365.intune.devices.compliance_policy_assignment import (
        DeviceCompliancePolicyAssignment,
    )
    from office365.intune.devices.compliance_scheduled_action_for_rule import (
        DeviceComplianceScheduledActionForRule,
    )
    from office365.intune.devices.compliance_user_overview import (
        DeviceComplianceUserOverview,
    )
    from office365.intune.devices.compliance_user_status import (
        DeviceComplianceUserStatus,
    )


class DeviceCompliancePolicy(Entity):
    """This is the base class for Compliance policy. Compliance policies are platform specific and individual
    per-platform compliance policies inherit from here"""

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="version")
    @property
    def version(self) -> Optional[int]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[DeviceCompliancePolicyAssignment]:
        """Gets the assignments property"""
        from office365.intune.devices.compliance_policy_assignment import (
            DeviceCompliancePolicyAssignment,
        )

        return self.properties.get(
            "assignments",
            EntityCollection[DeviceCompliancePolicyAssignment](
                self.context, DeviceCompliancePolicyAssignment, ResourcePath("assignments", self.resource_path)
            ),
        )

    @odata(name="deviceSettingStateSummaries", navigation=True)
    @property
    def device_setting_state_summaries(self) -> EntityCollection[SettingStateDeviceSummary]:
        """Gets the deviceSettingStateSummaries property"""
        from office365.intune.devices.compliance.setting_state_device_summary import (
            SettingStateDeviceSummary,
        )

        return self.properties.get(
            "deviceSettingStateSummaries",
            EntityCollection[SettingStateDeviceSummary](
                self.context, SettingStateDeviceSummary, ResourcePath("deviceSettingStateSummaries", self.resource_path)
            ),
        )

    @odata(name="deviceStatuses", navigation=True)
    @property
    def device_statuses(self) -> EntityCollection[DeviceComplianceDeviceStatus]:
        """Gets the deviceStatuses property"""
        from office365.intune.devices.compliance_device_status import (
            DeviceComplianceDeviceStatus,
        )

        return self.properties.get(
            "deviceStatuses",
            EntityCollection[DeviceComplianceDeviceStatus](
                self.context, DeviceComplianceDeviceStatus, ResourcePath("deviceStatuses", self.resource_path)
            ),
        )

    @odata(name="deviceStatusOverview", navigation=True)
    @property
    def device_status_overview(self) -> DeviceComplianceDeviceOverview:
        """Gets the deviceStatusOverview property"""
        from office365.intune.devices.compliance_device_overview import (
            DeviceComplianceDeviceOverview,
        )

        return self.properties.get(
            "deviceStatusOverview",
            DeviceComplianceDeviceOverview(self.context, ResourcePath("deviceStatusOverview", self.resource_path)),
        )

    @odata(name="scheduledActionsForRule", navigation=True)
    @property
    def scheduled_actions_for_rule(self) -> EntityCollection[DeviceComplianceScheduledActionForRule]:
        """Gets the scheduledActionsForRule property"""
        from office365.intune.devices.compliance_scheduled_action_for_rule import (
            DeviceComplianceScheduledActionForRule,
        )

        return self.properties.get(
            "scheduledActionsForRule",
            EntityCollection[DeviceComplianceScheduledActionForRule](
                self.context,
                DeviceComplianceScheduledActionForRule,
                ResourcePath("scheduledActionsForRule", self.resource_path),
            ),
        )

    @odata(name="userStatuses", navigation=True)
    @property
    def user_statuses(self) -> EntityCollection[DeviceComplianceUserStatus]:
        """Gets the userStatuses property"""
        from office365.intune.devices.compliance_user_status import (
            DeviceComplianceUserStatus,
        )

        return self.properties.get(
            "userStatuses",
            EntityCollection[DeviceComplianceUserStatus](
                self.context, DeviceComplianceUserStatus, ResourcePath("userStatuses", self.resource_path)
            ),
        )

    @odata(name="userStatusOverview", navigation=True)
    @property
    def user_status_overview(self) -> DeviceComplianceUserOverview:
        """Gets the userStatusOverview property"""
        from office365.intune.devices.compliance_user_overview import (
            DeviceComplianceUserOverview,
        )

        return self.properties.get(
            "userStatusOverview",
            DeviceComplianceUserOverview(self.context, ResourcePath("userStatusOverview", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceCompliancePolicy"

    @odata(name="osMaximumVersion", system=True)
    @property
    def os_maximum_version(self) -> Optional[str]:
        """Gets the osMaximumVersion property"""
        return self.properties.get("osMaximumVersion", None)

    @odata(name="osMinimumVersion", system=True)
    @property
    def os_minimum_version(self) -> Optional[str]:
        """Gets the osMinimumVersion property"""
        return self.properties.get("osMinimumVersion", None)
