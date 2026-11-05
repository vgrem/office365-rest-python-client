from __future__ import annotations

from office365.directory.identitygovernance.accessreview.reviewer_scope_type import (
    AccessReviewReviewerScopeType,
)
from office365.runtime.client_value import ClientValue


class AccessReviewReviewerScope(ClientValue):
    query: str | None = None
    queryRoot: str | None = None
    queryType: str | None = None
    reviewerId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewReviewerScope"

    scopeType: AccessReviewReviewerScopeType = AccessReviewReviewerScopeType.user
