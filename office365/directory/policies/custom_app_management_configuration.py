from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.policies.custom_app_management_application_configuration import (
    CustomAppManagementApplicationConfiguration,
)
from office365.runtime.client_value import ClientValue


@dataclass
class CustomAppManagementConfiguration(ClientValue):
    applicationRestrictions: CustomAppManagementApplicationConfiguration = field(
        default_factory=CustomAppManagementApplicationConfiguration
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomAppManagementConfiguration"
