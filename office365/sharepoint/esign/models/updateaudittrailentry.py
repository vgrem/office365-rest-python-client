from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class UpdateAuditTrailEntryModel(ClientValue):
    auditTrailEntryId: Optional[str] = None
    documentId: Optional[str] = None
    shouldRemoveEntry: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.UpdateAuditTrailEntryModel"
