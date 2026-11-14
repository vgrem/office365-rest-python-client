from __future__ import annotations

from dataclasses import field

from office365.directory.policies.app_management_configuration import AppManagementConfiguration
from office365.directory.policies.identifier_uri_configuration import IdentifierUriConfiguration


class AppManagementApplicationConfiguration(AppManagementConfiguration):
    identifierUris: IdentifierUriConfiguration = field(default_factory=IdentifierUriConfiguration)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AppManagementApplicationConfiguration"
