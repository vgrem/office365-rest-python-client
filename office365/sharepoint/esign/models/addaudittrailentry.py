from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class AddAuditTrailEntryModel(ClientValue):
    def __init__(
        self,
        action: Optional[str] = None,
        action_date_time: Optional[datetime] = None,
        document_id: Optional[str] = None,
        is_entry_visible: Optional[bool] = None,
        location: Optional[str] = None,
        name: Optional[str] = None,
    ):
        self.action = action
        self.actionDateTime = action_date_time
        self.documentId = document_id
        self.isEntryVisible = is_entry_visible
        self.location = location
        self.name = name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.AddAuditTrailEntryModel"
