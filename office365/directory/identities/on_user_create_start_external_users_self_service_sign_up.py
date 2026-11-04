from __future__ import annotations

from office365.directory.identities.userflows.usertype import UserType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class OnUserCreateStartExternalUsersSelfServiceSignUp(ClientValue):
    userTypeToCreate: UserType = UserType.member

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnUserCreateStartExternalUsersSelfServiceSignUp"
