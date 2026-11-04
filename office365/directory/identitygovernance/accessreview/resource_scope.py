from __future__ import annotations

from office365.directory.identitygovernance.accessreview.resource_scope_type import (
    AccessReviewResourceScopeType,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AccessReviewResourceScope(ClientValue):
    displayName: str | None = None
    resourceId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewResourceScope"

    scopeType: AccessReviewResourceScopeType = AccessReviewResourceScopeType.group
