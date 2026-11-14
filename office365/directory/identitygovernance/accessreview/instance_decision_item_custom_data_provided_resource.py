from __future__ import annotations

from office365.directory.identitygovernance.accessreview.instance_decision_item_resource import (
    AccessReviewInstanceDecisionItemResource,
)


class AccessReviewInstanceDecisionItemCustomDataProvidedResource(AccessReviewInstanceDecisionItemResource):
    customData: str | None = None
    scopeDisplayName: str | None = None
    scopeId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewInstanceDecisionItemCustomDataProvidedResource"
