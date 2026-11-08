from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.management_compliance_action_item import DeviceManagementComplianceActionItem


@version("beta")
class DeviceManagementComplianceScheduledActionForRule(Entity):
    @odata(name="ruleName")
    @property
    def rule_name(self) -> Optional[str]:
        """Gets the ruleName property"""
        return self.properties.get("ruleName", None)

    @odata(name="scheduledActionConfigurations", navigation=True)
    @property
    def scheduled_action_configurations(self) -> EntityCollection[DeviceManagementComplianceActionItem]:
        """Gets the scheduledActionConfigurations property"""
        from office365.intune.devices.management_compliance_action_item import DeviceManagementComplianceActionItem

        return self.properties.get(
            "scheduledActionConfigurations",
            EntityCollection[DeviceManagementComplianceActionItem](
                self.context,
                DeviceManagementComplianceActionItem,
                ResourcePath("scheduledActionConfigurations", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementComplianceScheduledActionForRule"
