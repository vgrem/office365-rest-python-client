from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.identity.defaultdocumentlibrary import (
    SPDefaultDocumentLibrary,
)


@dataclass
class SPRubySite(ClientValue):
    channelGroupId: Optional[str] = None
    createdDateTime: Optional[datetime] = None
    defaultDocumentLibrary: SPDefaultDocumentLibrary = field(default_factory=SPDefaultDocumentLibrary)
    description: Optional[str] = None
    id: Optional[str] = None
    lastModifiedDateTime: Optional[datetime] = None
    name: Optional[str] = None
    webUrl: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.IdentityModel.SPRubySite"
