from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class TenantAdminRecentAction(ClientValue):

    def __init__(
        self,
        admin_action_id: str = None,
        admin_action_source: int = None,
        admin_action_status: int = None,
        admin_action_type: int = None,
        correlation_id: UUID = None,
        created_time: datetime = None,
        is_part_of_bulk_update: bool = None,
        key: str = None,
        name: str = None,
        new_value: str = None,
        old_value: str = None,
        type_: str = None,
        url: str = None,
        user_email: str = None,
    ):
        self.adminActionId = admin_action_id
        self.adminActionSource = admin_action_source
        self.adminActionStatus = admin_action_status
        self.adminActionType = admin_action_type
        self.correlationId = correlation_id
        self.createdTime = created_time
        self.isPartOfBulkUpdate = is_part_of_bulk_update
        self.key = key
        self.name = name
        self.newValue = new_value
        self.oldValue = old_value
        self.type = type_
        self.url = url
        self.userEmail = user_email

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminRecentAction"
