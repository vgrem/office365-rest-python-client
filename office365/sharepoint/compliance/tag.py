from office365.runtime.client_value import ClientValue


class ComplianceTag(ClientValue):
    """Represents a Compliance Tag"""

    def __init__(
        self,
        accept_messages_only_from_senders_or_members: bool = None,
        access_type: str = None,
        allow_access_from_unmanaged_device: bool = None,
        auto_delete: bool = None,
        block_delete: bool = None,
        block_edit: bool = None,
        compliance_flags: int = None,
        contains_site_label: bool = None,
        display_name: str = None,
        encryption_rms_template_id: str = None,
        has_retention_action: bool = None,
        is_event_tag: bool = None,
        multi_stage_reviewer_email: str = None,
        next_stage_compliance_tag: str = None,
        notes: str = None,
        require_sender_authentication_enabled: bool = None,
        reviewer_email: str = None,
        sharing_capabilities: str = None,
        super_lock: bool = None,
        tag_duration: int = None,
        tag_id: str = None,
        tag_name: str = None,
        tag_retention_based_on: str = None,
        unlocked_as_default: bool = None,
    ):
        """
        :param bool accept_messages_only_from_senders_or_members:
        :param str access_type:
        """
        self.AcceptMessagesOnlyFromSendersOrMembers = (
            accept_messages_only_from_senders_or_members
        )
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
