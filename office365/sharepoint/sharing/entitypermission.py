from office365.runtime.client_value import ClientValue


class EntityPermission(ClientValue):
    def __init__(
        self,
        can_have_access: bool = None,
        existing_access_type: int = None,
        has_access: bool = None,
        input_entity: str = None,
        is_pending: bool = None,
        recipient_denied_reason: int = None,
        resolved_entity: str = None,
        role: int = None,
    ):
        self.canHaveAccess = can_have_access
        self.existingAccessType = existing_access_type
        self.hasAccess = has_access
        self.inputEntity = input_entity
        self.isPending = is_pending
        self.recipientDeniedReason = recipient_denied_reason
        self.resolvedEntity = resolved_entity
        self.role = role

    @property
    def entity_type_name(self):
        return "SP.Sharing.EntityPermission"
