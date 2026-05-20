from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.migrationcenter.folderinformation import SPFolderInformation


@dataclass
class SPListInformation(ClientValue):
    AbsoluteUrl: Optional[str] = None
    BaseTemplate: Optional[int] = None
    DisplayTitle: Optional[str] = None
    FolderInfoList: ClientValueCollection[SPFolderInformation] = field(
        default_factory=lambda: ClientValueCollection(SPFolderInformation)
    )
    ID: Optional[UUID] = None
    IsListPathUsedAsTitle: Optional[bool] = None
    IsMySiteDocumentLibrary: Optional[bool] = None
    IsQueryFoldersThrottled: Optional[bool] = None
    IsSpecifiedOrDefault: Optional[bool] = None
    ServerRelativeUrl: Optional[str] = None
    ShowWarning: Optional[bool] = None
    Title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.SPListInformation"
