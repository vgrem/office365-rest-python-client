from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.policies.authentication_strength import AuthenticationStrengthPolicy
from office365.directory.policies.conditionalaccess.grantcontrol import ConditionalAccessGrantControl
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection


@dataclass
class ConditionalAccessGrantControls(ClientValue):
    builtInControls: ClientValueCollection[ConditionalAccessGrantControl] = field(
        default_factory=lambda: ClientValueCollection(ConditionalAccessGrantControl)
    )
    customAuthenticationFactors: StringCollection = field(default_factory=StringCollection)
    operator: str | None = None
    termsOfUse: StringCollection = field(default_factory=StringCollection)
    authenticationStrength: AuthenticationStrengthPolicy | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessGrantControls"
