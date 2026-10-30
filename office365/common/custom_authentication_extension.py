from __future__ import annotations

from office365.directory.identitygovernance.entitlementmanagement.custom_extension_behavior_on_error import (  # noqa: E501
    CustomExtensionBehaviorOnError,
)
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class CustomAuthenticationExtension(Entity):
    @odata(name="behaviorOnError")
    @property
    def behavior_on_error(self) -> CustomExtensionBehaviorOnError:
        """Gets the behaviorOnError property"""
        return self.properties.get("behaviorOnError", CustomExtensionBehaviorOnError())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomAuthenticationExtension"
