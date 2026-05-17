from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue
from typing import Optional


class TenantAdminRecentAction(ClientValue):
    def __init__(
        self,
        admin_action_id: Optional[str] = None,
        admin_action_source: Optional[int] = None,
        admin_action_status: Optional[int] = None,
        admin_action_type: Optional[int] = None,
        correlation_id: Optional[UUID] = None,
        created_time: Optional[datetime] = None,
        is_part_of_bulk_update: Optional[bool] = None,
        key: Optional[str] = None,
        name: Optional[str] = None,
        new_value: Optional[str] = None,
        old_value: Optional[str] = None,
        type_: Optional[str] = None,
        url: Optional[str] = None,
        user_email: Optional[str] = None,
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
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminRecentAction"
