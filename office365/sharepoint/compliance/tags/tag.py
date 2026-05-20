from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ComplianceTag(ClientValue):
    """Represents a Compliance Tag"""

    AcceptMessagesOnlyFromSendersOrMembers: Optional[bool] = None
    AccessType: Optional[str] = None
    AllowAccessFromUnmanagedDevice: Optional[bool] = None
    AutoDelete: Optional[bool] = None
    BlockDelete: Optional[bool] = None
    BlockEdit: Optional[bool] = None
    ComplianceFlags: Optional[int] = None
    ContainsSiteLabel: Optional[bool] = None
    DisplayName: Optional[str] = None
    EncryptionRMSTemplateId: Optional[str] = None
    HasRetentionAction: Optional[bool] = None
    IsEventTag: Optional[bool] = None
    MultiStageReviewerEmail: Optional[str] = None
    NextStageComplianceTag: Optional[str] = None
    Notes: Optional[str] = None
    RequireSenderAuthenticationEnabled: Optional[bool] = None
    ReviewerEmail: Optional[str] = None
    SharingCapabilities: Optional[str] = None
    SuperLock: Optional[bool] = None
    TagDuration: Optional[int] = None
    TagId: Optional[str] = None
    TagName: Optional[str] = None
    TagRetentionBasedOn: Optional[str] = None
    UnlockedAsDefault: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.CompliancePolicy.ComplianceTag"
