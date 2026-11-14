from __future__ import annotations

from office365.directory.identitygovernance.accessreview.instance_decision_item_resource import (
    AccessReviewInstanceDecisionItemResource,
)


class AccessReviewInstanceDecisionItemServicePrincipalResource(AccessReviewInstanceDecisionItemResource):
    appId: str | None = None
    appRoleDisplayName: str | None = None
    appRoleId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewInstanceDecisionItemServicePrincipalResource"
