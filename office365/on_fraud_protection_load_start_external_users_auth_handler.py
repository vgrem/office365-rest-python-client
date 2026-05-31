from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field

@dataclass
class OnFraudProtectionLoadStartExternalUsersAuthHandler(ClientValue):
    signUp: FraudProtectionConfiguration = field(default_factory=FraudProtectionConfiguration)

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.OnFraudProtectionLoadStartExternalUsersAuthHandler'