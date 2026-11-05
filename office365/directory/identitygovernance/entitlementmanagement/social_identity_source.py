from __future__ import annotations

from office365.directory.identitygovernance.entitlementmanagement.socialidentitysourcetype import (
    SocialIdentitySourceType,
)
from office365.runtime.client_value import ClientValue


class SocialIdentitySource(ClientValue):
    displayName: str | None = None
    socialIdentitySourceType: SocialIdentitySourceType = SocialIdentitySourceType.facebook

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SocialIdentitySource"
