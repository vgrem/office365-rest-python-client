from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.authentication.generic_error import GenericError
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AuthenticationConfigurationValidation(ClientValue):
    errors: ClientValueCollection[GenericError] = field(default_factory=lambda: ClientValueCollection(GenericError))
    warnings: ClientValueCollection[GenericError] = field(default_factory=lambda: ClientValueCollection(GenericError))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationConfigurationValidation"
