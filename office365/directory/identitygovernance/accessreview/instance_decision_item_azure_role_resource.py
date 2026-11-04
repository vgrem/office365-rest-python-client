from __future__ import annotations

from dataclasses import field

from office365.directory.identitygovernance.accessreview.instance_decision_item_resource import (
    AccessReviewInstanceDecisionItemResource,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AccessReviewInstanceDecisionItemAzureRoleResource(ClientValue):
    scope: AccessReviewInstanceDecisionItemResource = field(default_factory=AccessReviewInstanceDecisionItemResource)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewInstanceDecisionItemAzureRoleResource"
