from __future__ import annotations
from dataclasses import dataclass, field
from office365.directory.authentication.conditions.applications import AuthenticationConditionsApplications
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field

@dataclass
class AuthenticationConditions(ClientValue):
    """The conditions on which an authenticationEventListener should trigger.

    :parm AuthenticationConditionsApplications applications: Applications which trigger a custom authentication
    extension.
    """
    applications: AuthenticationConditionsApplications = field(default_factory=AuthenticationConditionsApplications)

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.AuthenticationConditions'