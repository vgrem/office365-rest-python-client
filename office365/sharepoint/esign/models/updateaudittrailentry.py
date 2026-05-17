from typing import Optional

from office365.runtime.client_value import ClientValue


class UpdateAuditTrailEntryModel(ClientValue):
    def __init__(
        self,
        audit_trail_entry_id: Optional[str] = None,
        document_id: Optional[str] = None,
        should_remove_entry: Optional[bool] = None,
    ):
        self.auditTrailEntryId = audit_trail_entry_id
        self.documentId = document_id
        self.shouldRemoveEntry = should_remove_entry

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.UpdateAuditTrailEntryModel"
