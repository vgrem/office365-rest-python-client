from datetime import datetime

from office365.runtime.client_value import ClientValue


class AddAuditTrailEntryModel(ClientValue):

    def __init__(
        self,
        action: str = None,
        action_date_time: datetime = None,
        document_id: str = None,
        is_entry_visible: bool = None,
        location: str = None,
        name: str = None,
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
