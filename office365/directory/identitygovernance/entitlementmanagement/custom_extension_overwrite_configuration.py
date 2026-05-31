from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.extensions.customextensionclientconfiguration import CustomExtensionClientConfiguration
from office365.directory.identitygovernance.entitlementmanagement.custom_extension_behavior_on_error import (
    CustomExtensionBehaviorOnError,
)
from office365.runtime.client_value import ClientValue


@dataclass
class CustomExtensionOverwriteConfiguration(ClientValue):
    behaviorOnError: CustomExtensionBehaviorOnError = field(default_factory=CustomExtensionBehaviorOnError)
    clientConfiguration: CustomExtensionClientConfiguration = field(default_factory=CustomExtensionClientConfiguration)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomExtensionOverwriteConfiguration"
