from __future__ import annotations

from dataclasses import field

from office365.directory.policies.identifier_uri_configuration import IdentifierUriConfiguration
from office365.runtime.client_value import ClientValue


class CustomAppManagementApplicationConfiguration(ClientValue):
    identifierUris: IdentifierUriConfiguration = field(default_factory=IdentifierUriConfiguration)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomAppManagementApplicationConfiguration"
