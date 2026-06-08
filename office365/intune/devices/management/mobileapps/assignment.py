from __future__ import annotations

from office365.entity import Entity
from office365.intune.policies.installintent import InstallIntent


class MobileAppAssignment(Entity):
    @property
    def intent(self) -> InstallIntent:
        """Gets the intent property"""
        return self.properties.get("intent", InstallIntent.available)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MobileAppAssignment"
