from __future__ import annotations

from dataclasses import dataclass

from office365.directory.policies.conditionalaccess.guestorexternalusertypes import (
    ConditionalAccessGuestOrExternalUserTypes,
)
from office365.runtime.client_value import ClientValue


@dataclass
class UserSignIn(ClientValue):
    externalTenantId: str | None = None
    externalUserType: ConditionalAccessGuestOrExternalUserTypes = ConditionalAccessGuestOrExternalUserTypes.none
    userId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserSignIn"
