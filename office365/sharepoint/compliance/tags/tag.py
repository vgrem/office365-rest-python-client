from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class ComplianceTag(ClientValue):
    """Represents a Compliance Tag"""

    def __init__(
        self,
        accept_messages_only_from_senders_or_members: Optional[bool] = None,
        access_type: Optional[str] = None,
        allow_access_from_unmanaged_device: Optional[bool] = None,
        auto_delete: Optional[bool] = None,
        block_delete: Optional[bool] = None,
        block_edit: Optional[bool] = None,
        compliance_flags: Optional[int] = None,
        contains_site_label: Optional[bool] = None,
        display_name: Optional[str] = None,
        encryption_rms_template_id: Optional[str] = None,
        has_retention_action: Optional[bool] = None,
        is_event_tag: Optional[bool] = None,
        multi_stage_reviewer_email: Optional[str] = None,
        next_stage_compliance_tag: Optional[str] = None,
        notes: Optional[str] = None,
        require_sender_authentication_enabled: Optional[bool] = None,
        reviewer_email: Optional[str] = None,
        sharing_capabilities: str | None = None,
        super_lock: Optional[bool] = None,
        tag_duration: Optional[int] = None,
        tag_id: Optional[str] = None,
        tag_name: Optional[str] = None,
        tag_retention_based_on: Optional[str] = None,
        unlocked_as_default: Optional[bool] = None,
    ):
        """ """
        self.AcceptMessagesOnlyFromSendersOrMembers = accept_messages_only_from_senders_or_members
        self.AccessType = access_type
        self.AllowAccessFromUnmanagedDevice = allow_access_from_unmanaged_device
        self.AutoDelete = auto_delete
        self.BlockDelete = block_delete
        self.BlockEdit = block_edit
        self.ComplianceFlags = compliance_flags
        self.ContainsSiteLabel = contains_site_label
        self.DisplayName = display_name
        self.EncryptionRMSTemplateId = encryption_rms_template_id
        self.HasRetentionAction = has_retention_action
        self.IsEventTag = is_event_tag
        self.MultiStageReviewerEmail = multi_stage_reviewer_email
        self.NextStageComplianceTag = next_stage_compliance_tag
        self.Notes = notes
        self.RequireSenderAuthenticationEnabled = require_sender_authentication_enabled
        self.ReviewerEmail = reviewer_email
        self.SharingCapabilities = sharing_capabilities
        self.SuperLock = super_lock
        self.TagDuration = tag_duration
        self.TagId = tag_id
        self.TagName = tag_name
        self.TagRetentionBasedOn = tag_retention_based_on
        self.UnlockedAsDefault = unlocked_as_default

    @property
    def entity_type_name(self):
        return "SP.CompliancePolicy.ComplianceTag"
