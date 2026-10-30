from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.identitygovernance.accessreview.instance_decision_item_permission import (  # noqa: E501
    AccessReviewInstanceDecisionItemPermission,
)
from office365.directory.identitygovernance.accessreview.instance_decision_item_resource import (  # noqa: E501
    AccessReviewInstanceDecisionItemResource,
)
from office365.directory.permissions.identity import Identity
from office365.directory.users.identity import UserIdentity
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.audit.signins.governance_insight import GovernanceInsight


class AccessReviewInstanceDecisionItem(Entity):
    @odata(name="accessReviewId")
    @property
    def access_review_id(self) -> Optional[str]:
        """Gets the accessReviewId property"""
        return self.properties.get("accessReviewId", None)

    @odata(name="appliedBy")
    @property
    def applied_by(self) -> UserIdentity:
        """Gets the appliedBy property"""
        return self.properties.get("appliedBy", UserIdentity())

    @odata(name="appliedDateTime")
    @property
    def applied_date_time(self) -> datetime:
        """Gets the appliedDateTime property"""
        return self.properties.get("appliedDateTime", datetime.min)

    @odata(name="applyResult")
    @property
    def apply_result(self) -> Optional[str]:
        """Gets the applyResult property"""
        return self.properties.get("applyResult", None)

    @odata(name="decision")
    @property
    def decision(self) -> Optional[str]:
        """Gets the decision property"""
        return self.properties.get("decision", None)

    @odata(name="justification")
    @property
    def justification(self) -> Optional[str]:
        """Gets the justification property"""
        return self.properties.get("justification", None)

    @odata(name="principal")
    @property
    def principal(self) -> Identity:
        """Gets the principal property"""
        return self.properties.get("principal", Identity())

    @odata(name="principalLink")
    @property
    def principal_link(self) -> Optional[str]:
        """Gets the principalLink property"""
        return self.properties.get("principalLink", None)

    @odata(name="recommendation")
    @property
    def recommendation(self) -> Optional[str]:
        """Gets the recommendation property"""
        return self.properties.get("recommendation", None)

    @odata(name="resourceLink")
    @property
    def resource_link(self) -> Optional[str]:
        """Gets the resourceLink property"""
        return self.properties.get("resourceLink", None)

    @odata(name="reviewedBy")
    @property
    def reviewed_by(self) -> UserIdentity:
        """Gets the reviewedBy property"""
        return self.properties.get("reviewedBy", UserIdentity())

    @odata(name="reviewedDateTime")
    @property
    def reviewed_date_time(self) -> datetime:
        """Gets the reviewedDateTime property"""
        return self.properties.get("reviewedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewInstanceDecisionItem"

    @odata(name="applyDescription")
    @property
    def apply_description(self) -> Optional[str]:
        """Gets the applyDescription property"""
        return self.properties.get("applyDescription", None)

    @odata(name="permission")
    @property
    def permission(self) -> AccessReviewInstanceDecisionItemPermission:
        """Gets the permission property"""
        return self.properties.get("permission", AccessReviewInstanceDecisionItemPermission())

    @odata(name="resource")
    @property
    def resource(self) -> AccessReviewInstanceDecisionItemResource:
        """Gets the resource property"""
        return self.properties.get("resource", AccessReviewInstanceDecisionItemResource())

    @odata(name="insights", navigation=True)
    @property
    def insights(self) -> EntityCollection[GovernanceInsight]:
        """Gets the insights property"""
        from office365.directory.audit.signins.governance_insight import (
            GovernanceInsight,
        )

        return self.properties.get(
            "insights",
            EntityCollection[GovernanceInsight](
                self.context, GovernanceInsight, ResourcePath("insights", self.resource_path)
            ),
        )
