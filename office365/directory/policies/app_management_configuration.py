from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.applications.key_credential_configuration import KeyCredentialConfiguration
from office365.directory.applications.password_credential_configuration import PasswordCredentialConfiguration
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AppManagementConfiguration(ClientValue):
    keyCredentials: ClientValueCollection[KeyCredentialConfiguration] = field(
        default_factory=lambda: ClientValueCollection(KeyCredentialConfiguration)
    )
    passwordCredentials: ClientValueCollection[PasswordCredentialConfiguration] = field(
        default_factory=lambda: ClientValueCollection(PasswordCredentialConfiguration)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AppManagementConfiguration"
