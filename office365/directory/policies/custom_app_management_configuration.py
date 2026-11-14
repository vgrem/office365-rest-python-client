from __future__ import annotations

from dataclasses import field

from office365.directory.policies.app_management_configuration import AppManagementConfiguration
from office365.directory.policies.custom_app_management_application_configuration import (
    CustomAppManagementApplicationConfiguration,
)


class CustomAppManagementConfiguration(AppManagementConfiguration):
    applicationRestrictions: CustomAppManagementApplicationConfiguration = field(
        default_factory=CustomAppManagementApplicationConfiguration
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomAppManagementConfiguration"
