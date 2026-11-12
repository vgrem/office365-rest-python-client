from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.directory.identitygovernance.accessreview.error import AccessReviewError
from office365.directory.identitygovernance.accessreview.instance_decision_item import (
    AccessReviewInstanceDecisionItem,
)
from office365.directory.identitygovernance.accessreview.reviewer import (
    AccessReviewReviewer,
)
from office365.directory.identitygovernance.accessreview.reviewer_scope import AccessReviewReviewerScope
from office365.directory.identitygovernance.accessreview.scope import AccessReviewScope
from office365.directory.identitygovernance.accessreview.stages import (
    AccessReviewStageCollection,
)
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.directory.identitygovernance.accessreview.instance_decision_item_apply_result import (
        AccessReviewInstanceDecisionItemApplyResult,
    )


class AccessReviewInstance(Entity):
    """
    Represents a Microsoft Entra access review recurrence. If the parent accessReviewScheduleDefinition is a
    recurring access review, instances represent each recurrence. A review that does not recur will have exactly
    one instance. Instances also represent each unique group being reviewed in the schedule definition.
    If a schedule definition reviews multiple groups, each group will have a unique instance for each recurrence.

    Every accessReviewInstance contains a list of decisions that reviewers can take action on.
    There is one decision per identity being reviewed.
    """

    @odata(name="stages", navigation=True)
    @property
    def stages(self) -> AccessReviewStageCollection:
        """If the instance has multiple stages, this returns the collection of stages.
        A new stage will only be created when the previous stage ends"""
        return self.properties.get(
            "stages", AccessReviewStageCollection(self.context, ResourcePath("stages", self.resource_path))
        )

    @odata(name="endDateTime")
    @property
    def end_date_time(self) -> datetime:
        """Gets the endDateTime property"""
        return self.properties.get("endDateTime", datetime.min)

    @odata(name="scope")
    @property
    def scope(self) -> AccessReviewScope:
        """Gets the scope property"""
        return self.properties.get("scope", AccessReviewScope())

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> datetime:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> Optional[str]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @odata(name="contactedReviewers", navigation=True)
    @property
    def contacted_reviewers(self) -> EntityCollection[AccessReviewReviewer]:
        """Gets the contactedReviewers property"""
        return self.properties.get(
            "contactedReviewers",
            EntityCollection[AccessReviewReviewer](
                self.context, AccessReviewReviewer, ResourcePath("contactedReviewers", self.resource_path)
            ),
        )

    @odata(name="decisions", navigation=True)
    @property
    def decisions(self) -> EntityCollection[AccessReviewInstanceDecisionItem]:
        """Gets the decisions property"""
        return self.properties.get(
            "decisions",
            EntityCollection[AccessReviewInstanceDecisionItem](
                self.context, AccessReviewInstanceDecisionItem, ResourcePath("decisions", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewInstance"

    @odata(name="errors")
    @property
    def errors(self) -> ClientValueCollection[AccessReviewError]:
        """Gets the errors property"""
        return self.properties.get("errors", ClientValueCollection[AccessReviewError](AccessReviewError))

    @odata(name="fallbackReviewers")
    @property
    def fallback_reviewers(self) -> ClientValueCollection[AccessReviewReviewerScope]:
        """Gets the fallbackReviewers property"""
        return self.properties.get(
            "fallbackReviewers", ClientValueCollection[AccessReviewReviewerScope](AccessReviewReviewerScope)
        )

    @odata(name="reviewers")
    @property
    def reviewers(self) -> ClientValueCollection[AccessReviewReviewerScope]:
        """Gets the reviewers property"""
        return self.properties.get(
            "reviewers", ClientValueCollection[AccessReviewReviewerScope](AccessReviewReviewerScope)
        )

    @verb(role="action", effect="write")
    @require_permission(delegated=["AccessReview.ReadWrite.All"])
    def accept_recommendations(self) -> Self:
        """acceptRecommendations operation."""
        qry = ServiceOperationQuery(self, "acceptRecommendations", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(delegated=["AccessReview.ReadWrite.All"], application=["AccessReview.ReadWrite.All"])
    def apply_decisions(self) -> Self:
        """applyDecisions operation."""
        qry = ServiceOperationQuery(self, "applyDecisions", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(delegated=["AccessReview.ReadWrite.All"], application=["AccessReview.ReadWrite.All"])
    def batch_apply_custom_data_provided_resource_decisions(
        self,
        apply_result: AccessReviewInstanceDecisionItemApplyResult,
        apply_description: str,
        custom_data_provided_resource_id: str,
    ) -> Self:
        """batchApplyCustomDataProvidedResourceDecisions operation.

        Args:
            apply_result (AccessReviewInstanceDecisionItemApplyResult):
                applyResult parameter
            apply_description (str):
                applyDescription parameter
            custom_data_provided_resource_id (str):
                customDataProvidedResourceId parameter
        """
        qry = ServiceOperationQuery(
            self,
            "batchApplyCustomDataProvidedResourceDecisions",
            None,
            {
                "applyResult": apply_result,
                "applyDescription": apply_description,
                "customDataProvidedResourceId": custom_data_provided_resource_id,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(delegated=["AccessReview.ReadWrite.All"], application=["AccessReview.ReadWrite.All"])
    def batch_record_decisions(self, decision: str, justification: str, principal_id: str, resource_id: str) -> Self:
        """batchRecordDecisions operation.

        Args:
            decision (str):
                decision parameter
            justification (str):
                justification parameter
            principal_id (str):
                principalId parameter
            resource_id (str):
                resourceId parameter
        """
        qry = ServiceOperationQuery(
            self,
            "batchRecordDecisions",
            None,
            {
                "decision": decision,
                "justification": justification,
                "principalId": principal_id,
                "resourceId": resource_id,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(delegated=["AccessReview.ReadWrite.All"], application=["AccessReview.ReadWrite.All"])
    def reset_decisions(self) -> Self:
        """resetDecisions operation."""
        qry = ServiceOperationQuery(self, "resetDecisions", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(delegated=["AccessReview.ReadWrite.All"], application=["AccessReview.ReadWrite.All"])
    def send_reminder(self) -> Self:
        """sendReminder operation."""
        qry = ServiceOperationQuery(self, "sendReminder", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(delegated=["AccessReview.ReadWrite.All"], application=["AccessReview.ReadWrite.All"])
    def stop(self) -> Self:
        """stop operation."""
        qry = ServiceOperationQuery(self, "stop", None, {}, None, None)
        self.context.add_query(qry)
        return self
