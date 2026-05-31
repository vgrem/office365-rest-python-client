from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identitygovernance.entitlementmanagement.custom_extension_overwrite_configuration import (
    CustomExtensionOverwriteConfiguration,
)
from office365.runtime.client_value import ClientValue


@dataclass
class OnVerifiedIdClaimValidationCustomExtensionHandler(ClientValue):
    configuration: CustomExtensionOverwriteConfiguration = field(default_factory=CustomExtensionOverwriteConfiguration)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnVerifiedIdClaimValidationCustomExtensionHandler"
