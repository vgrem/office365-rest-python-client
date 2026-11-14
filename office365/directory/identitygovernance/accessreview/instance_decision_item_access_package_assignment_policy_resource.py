from __future__ import annotations

from office365.directory.identitygovernance.accessreview.instance_decision_item_resource import (
    AccessReviewInstanceDecisionItemResource,
)


class AccessReviewInstanceDecisionItemAccessPackageAssignmentPolicyResource(AccessReviewInstanceDecisionItemResource):
    accessPackageDisplayName: str | None = None
    accessPackageId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewInstanceDecisionItemAccessPackageAssignmentPolicyResource"
