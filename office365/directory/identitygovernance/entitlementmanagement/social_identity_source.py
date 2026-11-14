from __future__ import annotations

from office365.directory.identitygovernance.entitlementmanagement.identity_source import IdentitySource
from office365.directory.identitygovernance.entitlementmanagement.socialidentitysourcetype import (
    SocialIdentitySourceType,
)


class SocialIdentitySource(IdentitySource):
    displayName: str | None = None
    socialIdentitySourceType: SocialIdentitySourceType = SocialIdentitySourceType.facebook

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SocialIdentitySource"
