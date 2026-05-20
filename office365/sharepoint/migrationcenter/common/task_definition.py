from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class MigrationTaskDefinition(ClientValue):
    Name: Optional[str] = None
    SourceListName: Optional[str] = None
    SourceListRelativePath: Optional[str] = None
    SourceUri: Optional[str] = None
    SourceUserName: Optional[str] = None
    TargetListName: Optional[str] = None
    TargetListRelativePath: Optional[str] = None
    TargetSiteUrl: Optional[str] = None
    TargetUserName: Optional[str] = None
    Type: Optional[int] = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.MigrationTaskDefinition"
