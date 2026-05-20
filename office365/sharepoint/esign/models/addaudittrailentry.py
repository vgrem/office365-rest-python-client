from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AddAuditTrailEntryModel(ClientValue):
    action: Optional[str] = None
    actionDateTime: Optional[datetime] = None
    documentId: Optional[str] = None
    isEntryVisible: Optional[bool] = None
    location: Optional[str] = None
    name: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.AddAuditTrailEntryModel"
