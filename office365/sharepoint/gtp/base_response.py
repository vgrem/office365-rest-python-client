from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class BaseGptResponse(ClientValue):
    Created: Optional[int] = None
    Id: Optional[str] = None
    Model: Optional[str] = None
    ObjectType: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.BaseGptResponse"
