from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identitygovernance.accessreview.expirationbehavior import AccessReviewExpirationBehavior
from office365.directory.identitygovernance.entitlementmanagement.schedule import EntitlementManagementSchedule
from office365.directory.subjectset import SubjectSet
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AccessPackageAssignmentReviewSettings(ClientValue):
    expirationBehavior: AccessReviewExpirationBehavior = AccessReviewExpirationBehavior.keepAccess
    fallbackReviewers: ClientValueCollection[SubjectSet] = field(
        default_factory=lambda: ClientValueCollection(SubjectSet)
    )
    isEnabled: bool | None = None
    isRecommendationEnabled: bool | None = None
    isReviewerJustificationRequired: bool | None = None
    isSelfReview: bool | None = None
    primaryReviewers: ClientValueCollection[SubjectSet] = field(
        default_factory=lambda: ClientValueCollection(SubjectSet)
    )
    schedule: EntitlementManagementSchedule = field(default_factory=EntitlementManagementSchedule)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAssignmentReviewSettings"
