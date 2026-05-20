from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SPFolderInformation(ClientValue):
    Depth: Optional[int] = None
    IsSpecified: Optional[bool] = None
    Name: Optional[str] = None
    ServerRelativeUrl: Optional[str] = None
    WebRelativeUrl: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.SPFolderInformation"
