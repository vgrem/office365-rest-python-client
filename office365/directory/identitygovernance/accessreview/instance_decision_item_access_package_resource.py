from __future__ import annotations

from office365.directory.identitygovernance.accessreview.instance_decision_item_resource import (
    AccessReviewInstanceDecisionItemResource,
)


class AccessReviewInstanceDecisionItemAccessPackageResource(AccessReviewInstanceDecisionItemResource):
    accessPackageAssignmentPolicyDisplayName: str | None = None
    accessPackageAssignmentPolicyId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewInstanceDecisionItemAccessPackageResource"
