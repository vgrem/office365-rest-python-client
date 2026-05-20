from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class PacInfo(ClientValue):
    Endpoint: Optional[str] = None
    IsAppOnly: Optional[bool] = None
    Scenario: Optional[str] = None
    Token: Optional[str] = None
    Version: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.MicroService.Internal.PacInfo"
