from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath

class AuthenticationConditionsApplications(ClientValue):
    includeApplications: EntityCollection[AuthenticationConditionApplication] | None = None
    'The applications on which an authenticationEventListener should trigger.'

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.AuthenticationConditionsApplications'