from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class UpdateWriteBackFileModel(ClientValue):
    fileName: Optional[str] = None
    listItemId: Optional[str] = None
    url: Optional[str] = None
    workItemId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.UpdateWriteBackFileModel"
