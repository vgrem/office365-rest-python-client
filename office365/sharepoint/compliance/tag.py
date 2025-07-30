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

    @property
    def entity_type_name(self):
        return "SP.CompliancePolicy.ComplianceTag"
