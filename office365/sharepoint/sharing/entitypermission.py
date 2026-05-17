from typing import Optional

from office365.runtime.client_value import ClientValue


class EntityPermission(ClientValue):
    def __init__(
        self,
        can_have_access: Optional[bool] = None,
        existing_access_type: Optional[int] = None,
        has_access: Optional[bool] = None,
        input_entity: Optional[str] = None,
        is_pending: Optional[bool] = None,
        recipient_denied_reason: Optional[int] = None,
        resolved_entity: Optional[str] = None,
        role: Optional[int] = None,
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
