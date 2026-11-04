from __future__ import annotations

from office365.directory.users.user import User
from office365.entity_collection import EntityCollection
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ActivateUserScope(ClientValue):
    users: EntityCollection[User] | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.ActivateUserScope"
