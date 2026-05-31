from __future__ import annotations

from office365.directory.authentication.conditions.application import AuthenticationConditionApplication
from office365.entity_collection import EntityCollection
from office365.runtime.client_value import ClientValue


class AuthenticationConditionsApplications(ClientValue):
    includeApplications: EntityCollection[AuthenticationConditionApplication] | None = None
    "The applications on which an authenticationEventListener should trigger."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationConditionsApplications"
