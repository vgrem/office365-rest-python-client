from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.authentication.fraud_protection_configuration import FraudProtectionConfiguration
from office365.runtime.client_value import ClientValue


@dataclass
class OnFraudProtectionLoadStartExternalUsersAuthHandler(ClientValue):
    signUp: FraudProtectionConfiguration = field(default_factory=FraudProtectionConfiguration)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnFraudProtectionLoadStartExternalUsersAuthHandler"
