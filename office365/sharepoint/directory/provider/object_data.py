from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.directory.provider.alternate_id_data import AlternateIdData
from office365.sharepoint.directory.provider.session_data import DirectorySessionData


@dataclass
class DirectoryObjectData(ClientValue):
    AlternateId: AlternateIdData = field(default_factory=AlternateIdData)
    AttributeExpirationTimes: Optional[str] = None
    ChangeMarker: Optional[str] = None
    DirectoryObjectSubType: Optional[int] = None
    DirectoryObjectType: Optional[int] = None
    DirectorySessionData: DirectorySessionData = field(default_factory=DirectorySessionData)
    Id: Optional[str] = None
    IsNew: Optional[bool] = None
    LastModifiedTime: Optional[str] = None
    TenantContextId: Optional[str] = None
    Version: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.DirectoryObjectData"
