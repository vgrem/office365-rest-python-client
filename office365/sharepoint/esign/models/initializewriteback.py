from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class InitializeWriteBackModel(ClientValue):
    documents: Optional[str] = None
    providerName: Optional[str] = None
    scheduledCleanUp: Optional[int] = None
    selectedLocation: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.InitializeWriteBackModel"
