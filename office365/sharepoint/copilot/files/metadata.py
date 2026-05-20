from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.copilot.files.user_relationship import (
    CopilotFileUserRelationship,
)
from office365.sharepoint.copilot.useridentity import UserIdentity


@dataclass
class CopilotFileMetadata(ClientValue):
    ContainerUrl: Optional[str] = None
    CreatedBy: UserIdentity = field(default_factory=UserIdentity)
    FileName: Optional[str] = None
    FileUrl: Optional[str] = None
    LastModifiedBy: UserIdentity = field(default_factory=UserIdentity)
    ListId: Optional[str] = None
    ListItemId: Optional[str] = None
    SiteId: Optional[str] = None
    SitePath: Optional[str] = None
    UniqueId: Optional[str] = None
    UserRelationship: CopilotFileUserRelationship = field(default_factory=CopilotFileUserRelationship)
    WebId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Copilot.CopilotFileMetadata"
