from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class PlacesUserEntity(ClientValue):
    email: Optional[str] = None
    loginName: Optional[str] = None
    name: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.AddToOneDrive.PlacesUserEntity"
