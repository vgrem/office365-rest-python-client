from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.compliance_action_item import (
        DeviceComplianceActionItem,
    )


class DeviceComplianceScheduledActionForRule(Entity):
    @odata(name="ruleName")
    @property
    def rule_name(self) -> Optional[str]:
        """Gets the ruleName property"""
        return self.properties.get("ruleName", None)

    @odata(name="scheduledActionConfigurations", navigation=True)
    @property
    def scheduled_action_configurations(self) -> EntityCollection[DeviceComplianceActionItem]:
        """Gets the scheduledActionConfigurations property"""
        from office365.intune.devices.compliance_action_item import (
            DeviceComplianceActionItem,
        )

        return self.properties.get(
            "scheduledActionConfigurations",
            EntityCollection[DeviceComplianceActionItem](
                self.context,
                DeviceComplianceActionItem,
                ResourcePath("scheduledActionConfigurations", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceComplianceScheduledActionForRule"
