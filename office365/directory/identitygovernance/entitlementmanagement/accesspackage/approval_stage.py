from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.approver_information_visibility import (
    ApproverInformationVisibility,
)
from office365.directory.subjectset import SubjectSet
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AccessPackageApprovalStage(ClientValue):
    approverInformationVisibility: ApproverInformationVisibility = ApproverInformationVisibility.default
    durationBeforeAutomaticDenial: timedelta | None = None
    durationBeforeEscalation: timedelta | None = None
    escalationApprovers: ClientValueCollection[SubjectSet] = field(
        default_factory=lambda: ClientValueCollection(SubjectSet)
    )
    fallbackEscalationApprovers: ClientValueCollection[SubjectSet] = field(
        default_factory=lambda: ClientValueCollection(SubjectSet)
    )
    fallbackPrimaryApprovers: ClientValueCollection[SubjectSet] = field(
        default_factory=lambda: ClientValueCollection(SubjectSet)
    )
    isApproverJustificationRequired: bool | None = None
    isEscalationEnabled: bool | None = None
    primaryApprovers: ClientValueCollection[SubjectSet] = field(
        default_factory=lambda: ClientValueCollection(SubjectSet)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageApprovalStage"
